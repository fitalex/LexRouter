"""Canonical source-entry identity and first-seen duplicate detection.

The key deliberately mirrors ``scripts/validate_discovery_batches.py`` so the
adapter and the repository validator classify the same GitHub revision/host
presentations as the same entry.  ``tests/test_discovery_adapter.py`` asserts
parity; changing one implementation without the other breaks that test.
"""

from __future__ import annotations

from urllib.parse import unquote, urlsplit

from .models import DuplicateHit, SearchHit


def source_identity(url: str) -> tuple[str, ...]:
    """Ignore GitHub revision, URL presentation and host/repository casing.

    File paths remain case sensitive.  Forks, mirrors, copied prompts and
    semantic capability duplicates still require manual comparison; this key
    only prevents the same entry from being counted twice.
    """
    try:
        parsed = urlsplit(url)
    except (TypeError, ValueError):
        # Normalization will reject the malformed hit; deduplication must not
        # crash before that failure can be recorded.
        return ("", url if isinstance(url, str) else "", "")
    host = (parsed.hostname or "").lower()
    parts = unquote(parsed.path).strip("/").split("/")
    if host in {"github.com", "www.github.com"} and len(parts) >= 5:
        if parts[2] in {"blob", "raw"}:
            return ("github", parts[0].lower(), parts[1].lower(), "/".join(parts[4:]))
    if host == "raw.githubusercontent.com" and len(parts) >= 4:
        return ("github", parts[0].lower(), parts[1].lower(), "/".join(parts[3:]))
    return (host, parsed.path, parsed.query)


def dedupe_hits(
    hits: tuple[SearchHit, ...] | list[SearchHit],
) -> tuple[tuple[SearchHit, ...], tuple[DuplicateHit, ...]]:
    """Keep the first hit per canonical source entry and retain duplicates."""
    seen: dict[tuple[str, ...], SearchHit] = {}
    unique: list[SearchHit] = []
    duplicates: list[DuplicateHit] = []
    for hit in hits:
        key = source_identity(hit.url)
        first = seen.get(key)
        if first is None:
            seen[key] = hit
            unique.append(hit)
        else:
            duplicates.append(DuplicateHit(hit=hit, first_hit=first))
    return tuple(unique), tuple(duplicates)
