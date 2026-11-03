"""Facade wiring the three independently testable Discovery interfaces."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from .dedupe import dedupe_hits
from .fetch import FetchAdapter, FixtureSourceStore, SourceStore
from .models import (
    DiscoveryFailure,
    DiscoveryRun,
    FetchStatus,
    PinnedRef,
    SearchHit,
    SearchStatus,
    SourceSnapshot,
)
from .normalize import NormalizationError, normalize
from .search import FixtureSearchTransport, SearchAdapter, SearchTransport


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(moment: datetime) -> str:
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


class DiscoveryAdapter:
    """Offline-first facade; no method contacts a network or writes a file."""

    def __init__(
        self,
        search_transport: SearchTransport,
        source_store: SourceStore,
        *,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        self._search = SearchAdapter(search_transport)
        self._fetch = FetchAdapter(source_store)
        self._now = now or _utc_now

    @classmethod
    def from_fixtures(
        cls,
        search_fixture: str | Path,
        source_fixture: str | Path,
        *,
        now: Callable[[], datetime] | None = None,
    ) -> "DiscoveryAdapter":
        return cls(
            FixtureSearchTransport(search_fixture),
            FixtureSourceStore(source_fixture),
            now=now,
        )

    @property
    def provider(self) -> str:
        return self._search.provider

    def search(self, query: object, *, limit: int = 20):
        """Interface 1: return a standardized SearchResult (hits + status)."""
        return self._search.search(query, limit=limit)

    def fetch_pinned(self, ref: PinnedRef) -> SourceSnapshot:
        """Interface 2: read one exact pinned source, preserving failure state."""
        return self._fetch.fetch_pinned(ref)

    def normalize(
        self,
        hit: SearchHit,
        snapshot: SourceSnapshot | None = None,
    ) -> dict[str, object]:
        """Interface 3: map one hit into the existing candidate contract."""
        return normalize(hit, snapshot)

    def collect(self, query: object, *, limit: int = 20) -> DiscoveryRun:
        """Run search -> dedupe -> fetch -> normalize and retain an audit trail."""
        started_at = _iso(self._now())
        search_result = self.search(query, limit=limit)
        unique_hits, duplicates = dedupe_hits(search_result.hits)
        candidates: list[dict[str, object]] = []
        failures: list[DiscoveryFailure] = []
        content_withheld = 0

        if search_result.status is SearchStatus.ERROR and search_result.error is not None:
            failures.append(DiscoveryFailure(
                stage="search",
                source_id="",
                url="",
                status=search_result.error.code,
                message=search_result.error.message,
            ))

        for hit in unique_hits:
            ref = PinnedRef.from_hit(hit)
            snapshot = self.fetch_pinned(ref)
            if snapshot.status is FetchStatus.METADATA_ONLY:
                content_withheld += 1
            if snapshot.status not in {FetchStatus.OK, FetchStatus.METADATA_ONLY}:
                failures.append(DiscoveryFailure(
                    stage="fetch",
                    source_id=hit.source_id,
                    url=hit.url,
                    status=snapshot.status.value,
                    message=snapshot.notes or "pinned source read failed",
                ))
            try:
                candidate = self.normalize(hit, snapshot)
            except NormalizationError as exc:
                failures.append(DiscoveryFailure(
                    stage="normalize",
                    source_id=hit.source_id,
                    url=hit.url,
                    status="normalization-error",
                    message=exc.message,
                    field=exc.field,
                ))
                continue
            candidates.append(candidate)

        return DiscoveryRun(
            query=search_result.query,
            search=search_result,
            candidates=tuple(candidates),
            duplicates=duplicates,
            failures=tuple(failures),
            started_at=started_at,
            finished_at=_iso(self._now()),
            content_withheld=content_withheld,
        )
