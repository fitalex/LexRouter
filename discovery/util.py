"""Small standard-library helpers for the offline Discovery adapter."""

from __future__ import annotations

from datetime import date
import re
from urllib.parse import urlsplit


BUSINESS_CATEGORIES = frozenset({
    "contract-review",
    "civil-commercial-litigation",
    "corporate-ma",
    "corporate-compliance",
    "criminal-administrative",
    "legal-research",
})

RUNTIMES = frozenset({
    "claude-skill",
    "codex-skill",
    "cursor-rule",
    "dify-workflow",
    "prompt",
    "other",
})

AUTHORIZATION_STATUSES = frozenset({
    "verified",
    "pending-verification",
    "restricted",
    "not-permitted",
})

JURISDICTION_VALUES = frozenset({"CN-Mainland", "unknown", "other"})
JURISDICTION_STATUSES = frozenset({
    "source-declared",
    "pending-verification",
    "verified",
})

SOURCE_FAILURE_STATUSES = frozenset({
    "not-found",
    "revision-mismatch",
    "source-mismatch",
    "invalid-ref",
    "transport-error",
    "invalid-source",
})

FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
CALENDAR_DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")


def clean(value: object) -> str:
    """Return stripped text for strings and an empty string for everything else."""
    return value.strip() if isinstance(value, str) else ""


def is_full_sha(value: object) -> bool:
    return isinstance(value, str) and bool(FULL_SHA.fullmatch(value))


def is_calendar_date(value: object) -> bool:
    """Require exactly YYYY-MM-DD and a real calendar day."""
    if not isinstance(value, str) or not CALENDAR_DATE.fullmatch(value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def is_https_url(value: object) -> bool:
    """Check syntax only; this never resolves or contacts the URL."""
    if not isinstance(value, str) or not value or value != value.strip():
        return False
    if any(character.isspace() for character in value):
        return False
    try:
        parsed = urlsplit(value)
    except ValueError:
        return False
    return parsed.scheme == "https" and bool(parsed.hostname)


def clip(value: object, limit: int) -> str:
    """Trim to a contract length without leaving trailing whitespace."""
    text = clean(value)
    if len(text) <= limit:
        return text
    return text[: max(limit - 1, 0)].rstrip() + "…"


def slugify(value: object, limit: int = 60) -> str:
    text = clean(value).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    text = re.sub(r"-{2,}", "-", text)
    return text[:limit].strip("-") or "source"


def unique_https_urls(values: object) -> tuple[str, ...]:
    """Keep valid absolute HTTPS URLs in order, dropping duplicates."""
    if not isinstance(values, (list, tuple)):
        return ()
    seen: set[str] = set()
    kept: list[str] = []
    for value in values:
        if is_https_url(value) and value not in seen:
            seen.add(value)
            kept.append(value)
    return tuple(kept)


def append_note(existing: str, addition: str) -> str:
    """Append a short diagnostic sentence without duplicating it."""
    addition = clean(addition)
    if not addition:
        return clean(existing)
    if not existing:
        return addition
    if addition in existing:
        return existing
    return f"{existing} {addition}"
