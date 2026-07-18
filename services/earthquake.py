"""
services/earthquake.py

Service layer for the Earthquake Warning module.
Normalizes earthquake records from the `/weather/warning/earthquake`
upstream endpoint and applies stable localhost filtering.
"""

from typing import Any

from config import settings
from core.exceptions import ExternalAPIInvalidResponseError
from core.logging import log_execution
from schemas.earthquake import EarthquakeWarningQuery
from services.base import fetch_json
from utils.filters import any_field_contains
from utils.pagination import cap_results, is_list_payload

MODULE_NAME = "earthquake_warning"


def get_earthquake_warning(query: EarthquakeWarningQuery) -> list[dict[str, Any]]:
    """
    Retrieves and normalizes earthquake warning records from
    data.gov.my. Filtering is performed locally for stability.
    """
    with log_execution(MODULE_NAME, "fetch_earthquake_warning"):
        payload = fetch_json(
            path=settings.EARTHQUAKE_WARNING_PATH,
            module=MODULE_NAME,
        )

    if not is_list_payload(payload):
        raise ExternalAPIInvalidResponseError(module=MODULE_NAME)

    records = [_normalize_earthquake_record(record) for record in payload]
    filtered_records = [
        record for record in records if _matches_earthquake_query(record, query)
    ]
    return cap_results(filtered_records, query.limit)


def _normalize_earthquake_record(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "utc_datetime": record.get("utcdatetime"),
        "local_datetime": record.get("localdatetime"),
        "latitude": record.get("lat"),
        "longitude": record.get("lon"),
        "depth_km": record.get("depth"),
        "location": record.get("location"),
        "location_original": record.get("location_original"),
        "distance_malaysia": record.get("n_distancemas")
        or record.get("nbm_distancemas"),
        "distance_reference": record.get("n_distancerest")
        or record.get("nbm_distancerest"),
        "magnitude": record.get("magdefault"),
        "magnitude_type": record.get("magtypedefault"),
        "status": record.get("status"),
        "visible": record.get("visible"),
    }


def _matches_earthquake_query(
    record: dict[str, Any],
    query: EarthquakeWarningQuery,
) -> bool:
    if query.contains and not any_field_contains(record, query.contains):
        return False

    if query.min_magnitude is not None and _safe_magnitude(record) < query.min_magnitude:
        return False

    return True


def _safe_magnitude(record: dict[str, Any]) -> float:
    """Defensively extracts a numeric magnitude from a record, defaulting to 0.0."""
    value = record.get("magnitude", 0.0)
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0
