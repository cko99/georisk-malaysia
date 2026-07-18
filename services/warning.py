"""
services/warning.py

Service layer for the Weather Warning module.
Normalizes warning records from the `/weather/warning` upstream
endpoint and applies stable localhost filtering.
"""

from typing import Any

from config import settings
from core.exceptions import ExternalAPIInvalidResponseError
from core.logging import log_execution
from schemas.warning import WeatherWarningQuery
from services.base import fetch_json
from utils.filters import any_field_contains
from utils.pagination import cap_results, is_list_payload

MODULE_NAME = "weather_warning"


def get_weather_warning(query: WeatherWarningQuery) -> list[dict[str, Any]]:
    """
    Retrieves and normalizes active weather warning records from
    data.gov.my. Filtering is performed locally because upstream query
    syntax is not consistent for this feed.
    """
    with log_execution(MODULE_NAME, "fetch_weather_warning"):
        payload = fetch_json(
            path=settings.WEATHER_WARNING_PATH,
            module=MODULE_NAME,
        )

    if not is_list_payload(payload):
        raise ExternalAPIInvalidResponseError(module=MODULE_NAME)

    records = [_normalize_warning_record(record) for record in payload]
    filtered_records = [
        record for record in records if _matches_warning_query(record, query)
    ]
    return cap_results(filtered_records, query.limit)


def _normalize_warning_record(record: dict[str, Any]) -> dict[str, Any]:
    warning_issue = record.get("warning_issue") or {}
    return {
        "issued_at": warning_issue.get("issued"),
        "valid_from": record.get("valid_from"),
        "valid_to": record.get("valid_to"),
        "title": warning_issue.get("title_en")
        or warning_issue.get("title_bm")
        or record.get("heading_en")
        or record.get("heading_bm"),
        "title_en": warning_issue.get("title_en"),
        "title_bm": warning_issue.get("title_bm"),
        "heading": record.get("heading_en") or record.get("heading_bm"),
        "heading_en": record.get("heading_en"),
        "heading_bm": record.get("heading_bm"),
        "description": record.get("text_en") or record.get("text_bm"),
        "description_en": record.get("text_en"),
        "description_bm": record.get("text_bm"),
        "instruction": record.get("instruction_en") or record.get("instruction_bm"),
        "instruction_en": record.get("instruction_en"),
        "instruction_bm": record.get("instruction_bm"),
    }


def _matches_warning_query(
    record: dict[str, Any],
    query: WeatherWarningQuery,
) -> bool:
    if query.state and not any_field_contains(record, query.state):
        return False

    if query.contains and not any_field_contains(record, query.contains):
        return False

    return True
