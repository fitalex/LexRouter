"""Pinned-source reading with an injectable local store.

The fixture store is intentionally dumb: it returns records from a local JSON
file.  The adapter enforces the pin, source identity and content-copy policy so
that a caller cannot silently read a moving URL or copy unlicensed full text.
"""

from __future__ import annotations

from collections.abc import Mapping
import json
import re
from pathlib import Path
from typing import Protocol
from urllib.parse import unquote, urlsplit

from .models import FetchStatus, PinnedRef, SourceSnapshot
from .util import (
    append_note,
    clean,
    is_full_sha,
    is_https_url,
    unique_https_urls,
)


class SourceStore(Protocol):
    def get(self, source_id: str) -> Mapping[str, object] | None:
        """Return one raw source record or None when the ID is unknown."""


class FixtureSourceStore:
    """Index synthetic source records by stable source ID."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("fixture_version") != 1:
            raise ValueError(f"{self.path}: fixture_version 1 is required")
        sources = data.get("sources")
        if not isinstance(sources, list):
            raise ValueError(f"{self.path}: 'sources' must be an array")
        indexed: dict[str, Mapping[str, object]] = {}
        for index, record in enumerate(sources):
            if not isinstance(record, Mapping):
                raise ValueError(f"{self.path}: sources/{index} must be an object")
            source_id = clean(record.get("source_id"))
            if not source_id:
                raise ValueError(f"{self.path}: sources/{index}/source_id is required")
            if source_id in indexed:
                raise ValueError(f"{self.path}: duplicate source_id {source_id!r}")
            indexed[source_id] = record
        self._sources = indexed

    def get(self, source_id: str) -> Mapping[str, object] | None:
        return self._sources.get(source_id)

    def __len__(self) -> int:
        return len(self._sources)


PERCENT_ESCAPE = re.compile(r"%[0-9A-Fa-f]{2}")
DECODE_ROUNDS = 6


def _canonical_segment(segment: str) -> str | None:
    """Decode one path segment and reject path-reinterpreting forms.

    Literal or encoded dot segments, encoded separators, control characters,
    repeated slashes and unstable multi-encoded paths are rejected.  Valid
    encoded filenames (spaces, Unicode and percent-encoded ASCII) remain valid.
    """
    if "%" in segment:
        for index, character in enumerate(segment):
            if character == "%" and not PERCENT_ESCAPE.match(segment, index):
                return None
    decoded = segment
    for _ in range(DECODE_ROUNDS):
        following = unquote(decoded)
        if following == decoded:
            break
        decoded = following
    else:
        return None
    if not decoded or decoded in {".", ".."}:
        return None
    if "/" in decoded or "\\" in decoded:
        return None
    if any(ord(character) < 0x20 or ord(character) == 0x7F for character in decoded):
        return None
    return decoded


def _github_pinned_parts(url: str) -> tuple[str, str, str, str, tuple[str, ...]] | None:
    """Return strict (owner, repo, kind, revision, decoded file path) or None.

    The supported canonical forms are GitHub ``blob``/``raw`` URLs and
    ``raw.githubusercontent.com`` URLs.  Owner, repository and revision must
    be literal (not percent-encoded); file path segments may be valid encoded
    names.  Any dot segment or separator encoded inside a segment is rejected.
    """
    if not is_https_url(url):
        return None
    parsed = urlsplit(url)
    host = (parsed.hostname or "").lower()
    if not parsed.path.startswith("/") or parsed.path == "/":
        return None
    raw_segments = parsed.path.split("/")[1:]
    if not raw_segments or any(segment == "" for segment in raw_segments):
        return None
    decoded = [_canonical_segment(segment) for segment in raw_segments]
    if any(segment is None for segment in decoded):
        return None
    values = [segment for segment in decoded if segment is not None]

    if host in {"github.com", "www.github.com"}:
        if len(values) < 5:
            return None
        owner, repo, kind, revision = values[:4]
        if raw_segments[0] != owner or raw_segments[1] != repo:
            return None
        if kind not in {"blob", "raw"} or raw_segments[2] != kind:
            return None
        if raw_segments[3] != revision or not is_full_sha(revision):
            return None
        return owner, repo, kind, revision, tuple(values[4:])
    if host == "raw.githubusercontent.com":
        if len(values) < 4:
            return None
        owner, repo, revision = values[:3]
        if raw_segments[0] != owner or raw_segments[1] != repo:
            return None
        if raw_segments[2] != revision or not is_full_sha(revision):
            return None
        return owner, repo, "raw", revision, tuple(values[3:])
    return None


def _url_is_pinned_to_revision(url: str, revision: str) -> bool:
    """Accept only strict canonical GitHub pinned shapes."""
    parts = _github_pinned_parts(url)
    return parts is not None and parts[3] == revision


class FetchAdapter:
    """Read one exact source entry, preserving every failure state."""

    def __init__(self, store: SourceStore) -> None:
        self.store = store

    def fetch_pinned(self, ref: PinnedRef | object) -> SourceSnapshot:
        if not isinstance(ref, PinnedRef):
            raise TypeError("fetch_pinned expects a PinnedRef")
        problem = self._ref_problem(ref)
        if problem:
            return SourceSnapshot(
                ref=ref,
                status=FetchStatus.INVALID_REF,
                notes=problem,
            )
        try:
            record = self.store.get(ref.source_id)
        except OSError as exc:
            return SourceSnapshot(
                ref=ref,
                status=FetchStatus.TRANSPORT_ERROR,
                notes=f"source store read failed: {exc}",
            )
        if record is None:
            return SourceSnapshot(
                ref=ref,
                status=FetchStatus.NOT_FOUND,
                notes=f"no pinned source is recorded for source_id {ref.source_id!r}",
            )

        source_url = clean(record.get("url"))
        revision = clean(record.get("revision"))
        if not is_https_url(source_url) or not is_full_sha(revision):
            return SourceSnapshot(
                ref=ref,
                status=FetchStatus.INVALID_SOURCE,
                notes="stored source requires an HTTPS URL and a full 40-character commit SHA",
            )
        if not _url_is_pinned_to_revision(source_url, revision):
            return SourceSnapshot(
                ref=ref,
                status=FetchStatus.INVALID_SOURCE,
                notes=(
                    "stored source URL is not a GitHub blob/raw URL pinned to "
                    "its recorded revision"
                ),
            )
        stored_parts = _github_pinned_parts(source_url)
        requested_parts = _github_pinned_parts(ref.url)
        if stored_parts is None or requested_parts is None:
            return SourceSnapshot(
                ref=ref,
                status=FetchStatus.INVALID_SOURCE,
                notes="stored or requested source is not a canonical GitHub pinned URL",
            )
        stored_identity = (stored_parts[0].lower(), stored_parts[1].lower(), stored_parts[4])
        requested_identity = (
            requested_parts[0].lower(),
            requested_parts[1].lower(),
            requested_parts[4],
        )
        if stored_identity != requested_identity:
            return SourceSnapshot(
                ref=ref,
                status=FetchStatus.SOURCE_MISMATCH,
                notes="stored source identity does not match the requested pinned file path",
            )
        if revision != ref.revision:
            return SourceSnapshot(
                ref=ref,
                status=FetchStatus.REVISION_MISMATCH,
                notes=f"requested revision {ref.revision} but the store holds {revision}",
            )

        retrieved_at = clean(record.get("retrieved_at")) or None
        evidence_urls = unique_https_urls(record.get("evidence_urls"))
        if source_url not in evidence_urls:
            evidence_urls = (source_url, *evidence_urls)
        authorization_urls = unique_https_urls(record.get("authorization_evidence_urls"))
        categories = record.get("business_categories")
        if not isinstance(categories, list):
            categories = []
        jurisdiction = record.get("jurisdiction")
        if not isinstance(jurisdiction, dict):
            jurisdiction = None

        policy = clean(record.get("content_policy")) or "reference-only"
        raw_content = record.get("content")
        content = None
        status = FetchStatus.METADATA_ONLY
        notes = clean(record.get("notes"))
        if policy == "synthetic-own" and isinstance(raw_content, str) and raw_content.strip():
            content = raw_content
            status = FetchStatus.OK
        elif policy == "synthetic-own":
            notes = append_note(notes, "Synthetic content was missing; metadata retained only.")
        elif isinstance(raw_content, str) and raw_content.strip():
            notes = append_note(
                notes,
                f"Full text withheld because content_policy is {policy!r}; metadata and links retained.",
            )
        else:
            notes = append_note(
                notes,
                f"Full text not copied because content_policy is {policy!r}.",
            )

        return SourceSnapshot(
            ref=ref,
            status=status,
            revision=revision,
            retrieved_at=retrieved_at,
            title=clean(record.get("title")),
            maintainer=clean(record.get("maintainer")),
            license=clean(record.get("license")) or "not-identified",
            authorization_status=clean(record.get("authorization_status")) or "pending-verification",
            authorization_evidence_urls=authorization_urls,
            authorization_notes=clean(record.get("authorization_notes")),
            jurisdiction=jurisdiction,
            business_categories=tuple(clean(category) for category in categories if clean(category)),
            runtime=clean(record.get("runtime")) or "other",
            runtime_evidence=clean(record.get("runtime_evidence")),
            content=content,
            content_policy=policy,
            evidence_urls=evidence_urls,
            notes=notes,
        )

    @staticmethod
    def _ref_problem(ref: PinnedRef) -> str:
        if not clean(ref.source_id):
            return "source_id is required"
        if not is_https_url(ref.url):
            return "pinned URL must be an absolute HTTPS URL"
        if not is_full_sha(ref.revision):
            return "revision must be a full 40-character lowercase commit SHA"
        if not _url_is_pinned_to_revision(ref.url, ref.revision):
            return "URL is not a supported GitHub blob/raw URL pinned to the requested revision"
        return ""
