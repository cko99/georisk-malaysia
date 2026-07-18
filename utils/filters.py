"""
utils/filters.py

Reusable helpers for lightweight client-side filtering of upstream
records when data.gov.my query semantics are unavailable or unstable.
"""

from typing import Any


def normalize_text(value: Any) -> str:
    """Normalizes any scalar value for case-insensitive text matching."""
    if value is None:
        return ""
    return str(value).strip().casefold()


def matches_text(value: Any, query: str | None, *, exact: bool = False) -> bool:
    """Returns whether a scalar value matches the supplied query."""
    if not query:
        return True

    normalized_query = normalize_text(query)
    normalized_value = normalize_text(value)

    if exact:
        return normalized_value == normalized_query
    return normalized_query in normalized_value


def any_field_contains(value: Any, query: str | None) -> bool:
    """Recursively searches nested values for a case-insensitive match."""
    if not query:
        return True

    if isinstance(value, dict):
        return any(any_field_contains(item, query) for item in value.values())

    if isinstance(value, list):
        return any(any_field_contains(item, query) for item in value)

    return matches_text(value, query)
