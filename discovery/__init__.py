"""Offline prototype for repeatable Chinese legal-Skills discovery.

Public surfaces:

``DiscoveryAdapter.search(query)``
    Return ``SearchResult`` (normalized hits, empty state or explicit error).
``DiscoveryAdapter.fetch_pinned(ref)``
    Read one exact source entry and retain version, evidence and failure state.
``normalize(hit, snapshot=None)``
    Convert one hit into the existing candidate contract.

The package uses only the Python standard library.  It does not call a real
search or fetch API, does not schedule runs, does not execute third-party
Skills and does not perform legal, license or regulatory-currency review.
"""

from .adapter import DiscoveryAdapter
from .dedupe import dedupe_hits, source_identity
from .fetch import FetchAdapter, FixtureSourceStore
from .models import (
    DiscoveryFailure,
    DiscoveryRun,
    DuplicateHit,
    FetchStatus,
    PinnedRef,
    SearchError,
    SearchHit,
    SearchResult,
    SearchStatus,
    SourceSnapshot,
)
from .normalize import NormalizationError, normalize
from .search import (
    FixtureSearchTransport,
    SearchAdapter,
    SearchTransport,
    SearchTransportError,
)

__all__ = [
    "DiscoveryAdapter",
    "DiscoveryFailure",
    "DiscoveryRun",
    "DuplicateHit",
    "FetchAdapter",
    "FetchStatus",
    "FixtureSearchTransport",
    "FixtureSourceStore",
    "NormalizationError",
    "PinnedRef",
    "SearchAdapter",
    "SearchError",
    "SearchHit",
    "SearchResult",
    "SearchStatus",
    "SearchTransport",
    "SearchTransportError",
    "SourceSnapshot",
    "dedupe_hits",
    "normalize",
    "source_identity",
]
