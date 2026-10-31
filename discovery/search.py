"""Offline search adapter with an injectable transport.

The adapter owns response parsing and failure mapping.  The fixture transport
below is only a stand-in for a future HTTP client; this module imports no HTTP
library and never opens a socket.
"""

from __future__ import annotations

from collections.abc import Mapping
import json
from pathlib import Path
from typing import Protocol

from .models import (
    SearchError,
    SearchHit,
    SearchResult,
    SearchStatus,
)
from .util import clean, is_calendar_date


class SearchTransportError(Exception):
    """A provider-level failure that must become an explicit search status."""

    def __init__(self, code: str, message: str, *, retryable: bool = False) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable


class SearchTransport(Protocol):
    provider: str

    def request(self, query: str, limit: int) -> Mapping[str, object]:
        """Return one decoded provider response or raise SearchTransportError."""


class FixtureSearchTransport:
    """Replay synthetic provider responses from a local JSON fixture."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("fixture_version") != 1:
            raise ValueError(f"{self.path}: fixture_version 1 is required")
        queries = data.get("queries")
        if not isinstance(queries, dict):
            raise ValueError(f"{self.path}: 'queries' must be an object")
        self.provider = clean(data.get("provider")) or "synthetic-search"
        self._queries = queries

    def request(self, query: str, limit: int) -> Mapping[str, object]:
        del limit  # the fixture already contains the final synthetic page
        entry = self._queries.get(query)
        if not isinstance(entry, dict):
            raise SearchTransportError(
                "fixture-not-found",
                f"no synthetic response for query {query!r}",
            )
        error = entry.get("error")
        if isinstance(error, dict):
            raise SearchTransportError(
                clean(error.get("code")) or "transport-error",
                clean(error.get("message")) or "synthetic transport failure",
                retryable=bool(error.get("retryable")),
            )
        payload = dict(entry)
        payload.setdefault("provider", self.provider)
        payload.setdefault("results", [])
        return payload


class SearchAdapter:
    """Parse provider payloads into normalized hits without touching the web."""

    def __init__(self, transport: SearchTransport) -> None:
        self.transport = transport
        self.provider = getattr(transport, "provider", "unknown")

    def search(self, query: object, *, limit: int = 20) -> SearchResult:
        query_text = clean(query)
        if not query_text:
            return self._error("", "invalid-query", "query must be a non-empty string")
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
            return self._error(query_text, "invalid-limit", "limit must be a positive integer")
        try:
            payload = self.transport.request(query_text, limit)
        except SearchTransportError as exc:
            return self._error(query_text, exc.code, exc.message, retryable=exc.retryable)
        except OSError as exc:
            return self._error(query_text, "transport-error", str(exc), retryable=True)
        return self._parse(query_text, payload, limit)

    def _error(
        self,
        query: str,
        code: str,
        message: str,
        *,
        retryable: bool = False,
    ) -> SearchResult:
        return SearchResult(
            query=query,
            provider=self.provider,
            status=SearchStatus.ERROR,
            error=SearchError(code=code, message=message, retryable=retryable),
        )

    def _parse(self, query: str, payload: object, limit: int) -> SearchResult:
        if not isinstance(payload, Mapping):
            return self._error(query, "invalid-response", "provider response must be an object")
        results = payload.get("results")
        if not isinstance(results, list):
            return self._error(query, "invalid-response", "'results' must be an array")
        retrieved_at = payload.get("retrieved_at")
        if not is_calendar_date(retrieved_at):
            return self._error(
                query,
                "invalid-response",
                "'retrieved_at' must be a valid YYYY-MM-DD date",
            )
        provider = clean(payload.get("provider")) or self.provider
        hits: list[SearchHit] = []
        warnings: list[str] = []
        skipped = 0
        for position, item in enumerate(results[:limit]):
            if not isinstance(item, Mapping):
                skipped += 1
                warnings.append(f"result {position} is not an object; skipped")
                continue
            hit_date = item.get("retrieved_at")
            if not is_calendar_date(hit_date):
                hit_date = retrieved_at
            source_id = clean(item.get("source_id")) or clean(item.get("id"))
            title = clean(item.get("title"))
            url = clean(item.get("url"))
            snippet = clean(item.get("snippet"))
            revision = clean(item.get("revision")) or None
            categories = item.get("business_categories")
            if isinstance(categories, list):
                category_tuple = tuple(
                    clean(category) for category in categories if clean(category)
                )
            else:
                category_tuple = ()
            rank = item.get("rank")
            if isinstance(rank, bool) or not isinstance(rank, int) or rank < 1:
                rank = position + 1
            hits.append(SearchHit(
                hit_id=clean(item.get("id")) or source_id or f"hit-{position + 1}",
                source_id=source_id,
                title=title,
                url=url,
                snippet=snippet,
                retrieved_at=hit_date,
                provider=provider,
                rank=rank,
                revision=revision,
                business_categories=category_tuple,
                runtime=clean(item.get("runtime")) or None,
                runtime_evidence=clean(item.get("runtime_evidence")) or None,
                maintainer=clean(item.get("maintainer")) or None,
            ))
        if not hits and results and skipped == min(len(results), limit):
            return self._error(query, "invalid-response", "every result entry was invalid")
        return SearchResult(
            query=query,
            provider=provider,
            status=SearchStatus.OK if hits else SearchStatus.EMPTY,
            hits=tuple(hits),
            warnings=tuple(warnings),
        )
