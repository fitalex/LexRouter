"""Pinned-source reading with an injectable local store.

The fixture store is intentionally dumb: it returns records from a local JSON
file.  The adapter enforces the pin, source identity and content-copy policy so
that a caller cannot silently read a moving URL or copy unlicensed full text.
"""

from __future__ import annotations

from collections.abc import Mapping
import json
from pathlib import Path
from typing import Protocol
from urllib.parse import unquote, urlsplit

from .dedupe import source_identity
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


def _url_is_pinned_to_revision(url: str, revision: str) -> bool:
    """Accept the same GitHub pinned shapes as the repository batch validator."""
    parsed = urlsplit(url)
    host = (parsed.hostname or "").lower()
    parts = unquote(parsed.path).strip("/").split("/")
    if host in {"github.com", "www.github.com"} and len(parts) >= 5:
        return parts[2] in {"blob", "raw"} and parts[3] == revision
    if host == "raw.githubusercontent.com" and len(parts) >= 4:
        return parts[2] == revision
    return False


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
        if source_identity(source_url) != source_identity(ref.url):
            return SourceSnapshot(
                ref=ref,
                status=FetchStatus.SOURCE_MISMATCH,
                notes="stored source identity does not match the requested pinned entry",
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
