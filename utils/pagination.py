"""
utils/pagination.py

Small, reusable helper for client-side capping of upstream result sets
when the upstream API does not natively support a `limit` parameter or
returns more records than requested.
"""

from typing import Any, TypeVar

T = TypeVar("T")


def cap_results(records: list[T], limit: int | None) -> list[T]:
    """Returns at most `limit` records, preserving original order."""
    if limit is None or limit <= 0:
        return records
    return records[:limit]


def is_list_payload(payload: Any) -> bool:
    """Type guard used by services before applying list-only post-processing."""
    return isinstance(payload, list)
