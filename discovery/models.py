"""Typed values exchanged by the offline Discovery adapter.

Nothing in this module performs I/O, legal review, license review or network
access.  The dataclasses keep provenance and failure states explicit so that a
caller cannot turn a failed read into a successful search result by accident.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import Enum
import hashlib
import re


class SearchStatus(str, Enum):
    OK = "ok"
    EMPTY = "empty"
    ERROR = "error"


class FetchStatus(str, Enum):
    OK = "ok"
    METADATA_ONLY = "metadata-only"
    NOT_FOUND = "not-found"
    REVISION_MISMATCH = "revision-mismatch"
    SOURCE_MISMATCH = "source-mismatch"
    INVALID_REF = "invalid-ref"
    TRANSPORT_ERROR = "transport-error"
    INVALID_SOURCE = "invalid-source"


@dataclass(frozen=True)
class SearchError:
    code: str
    message: str
    retryable: bool = False


@dataclass(frozen=True)
class SearchHit:
    """One standardized hit.

    ``business_categories`` and the runtime hints are discovery-stage inputs,
    not a legal classification.  A missing value stays missing; normalization
    decides whether that is an error or an explicit unknown state.
    """

    hit_id: str
    source_id: str
    title: str
    url: str
    snippet: str
    retrieved_at: str
    provider: str
    rank: int
    revision: str | None = None
    business_categories: tuple[str, ...] = ()
    runtime: str | None = None
    runtime_evidence: str | None = None
    maintainer: str | None = None


@dataclass(frozen=True)
class SearchResult:
    query: str
    provider: str
    status: SearchStatus
    hits: tuple[SearchHit, ...] = ()
    error: SearchError | None = None
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class PinnedRef:
    """A request for one exact pinned source entry."""

    source_id: str
    url: str
    revision: str

    @classmethod
    def from_hit(cls, hit: SearchHit) -> "PinnedRef":
        return cls(source_id=hit.source_id, url=hit.url, revision=hit.revision or "")


@dataclass(frozen=True)
class SourceSnapshot:
    """Metadata read from one pinned source.

    ``content`` is populated only when the source policy permits copying.  A
    reference-only source still yields metadata and evidence links, but never
    the full text.
    """

    ref: PinnedRef
    status: FetchStatus
    revision: str | None = None
    retrieved_at: str | None = None
    title: str = ""
    maintainer: str = ""
    license: str = "not-identified"
    authorization_status: str = "pending-verification"
    authorization_evidence_urls: tuple[str, ...] = ()
    authorization_notes: str = ""
    jurisdiction: dict[str, object] | None = None
    business_categories: tuple[str, ...] = ()
    runtime: str = "other"
    runtime_evidence: str = ""
    content: str | None = None
    content_policy: str = "reference-only"
    evidence_urls: tuple[str, ...] = ()
    notes: str = ""


@dataclass(frozen=True)
class DiscoveryFailure:
    """A non-fatal stage failure retained in the run audit."""

    stage: str
    source_id: str
    url: str
    status: str
    message: str
    field: str | None = None


@dataclass(frozen=True)
class DuplicateHit:
    hit: SearchHit
    first_hit: SearchHit


@dataclass(frozen=True)
class DiscoveryRun:
    query: str
    search: SearchResult
    candidates: tuple[dict[str, object], ...]
    duplicates: tuple[DuplicateHit, ...]
    failures: tuple[DiscoveryFailure, ...]
    started_at: str
    finished_at: str
    content_withheld: int = 0

    @property
    def run_id(self) -> str:
        stamp = re.sub(r"[^0-9]", "", self.started_at)[:14] or "run"
        digest = hashlib.sha256(f"{self.query}\0{self.started_at}".encode("utf-8")).hexdigest()[:8]
        return f"disc-{stamp}-{digest}"

    def manifest(self) -> dict[str, object]:
        """Candidate data only; passes the existing candidate validator."""
        return {
            "format_version": 1,
            "candidates": [dict(candidate) for candidate in self.candidates],
        }

    def audit(self) -> dict[str, object]:
        """Machine-readable batch record; separate from candidate data."""
        error = None
        if self.search.error is not None:
            error = {
                "code": self.search.error.code,
                "message": self.search.error.message,
                "retryable": self.search.error.retryable,
            }
        return {
            "format_version": 1,
            "run_id": self.run_id,
            "query": self.query,
            "provider": self.search.provider,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "search": {
                "status": self.search.status.value,
                "hits": len(self.search.hits),
                "error": error,
                "warnings": list(self.search.warnings),
            },
            "duplicates": [
                {
                    "source_id": duplicate.hit.source_id,
                    "url": duplicate.hit.url,
                    "first_url": duplicate.first_hit.url,
                    "reason": "same canonical source entry",
                }
                for duplicate in self.duplicates
            ],
            "failures": [
                {
                    "stage": failure.stage,
                    "source_id": failure.source_id,
                    "url": failure.url,
                    "status": failure.status,
                    "field": failure.field,
                    "message": failure.message,
                }
                for failure in self.failures
            ],
            "candidates": len(self.candidates),
            "candidate_status": dict(sorted(Counter(
                candidate["candidate_status"] for candidate in self.candidates
            ).items())),
            "regulatory_currency": dict(sorted(Counter(
                candidate["regulatory_currency"]["status"]
                for candidate in self.candidates
            ).items())),
            "content_withheld": self.content_withheld,
            "notes": [
                "Offline fixtures only; no external search, fetch, scheduler or API key was used.",
                "A candidate/needs-evidence result is not a legal, license or currency conclusion.",
                "Semantic duplicate review remains manual.",
            ],
        }
