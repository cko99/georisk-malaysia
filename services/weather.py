"""
services/weather.py

Service layer for the Weather Forecast module.
Normalizes forecast records from the `/weather/forecast` upstream
endpoint and applies lightweight server-side filtering for a stable
localhost contract.
"""

from typing import Any

from config import settings
from core.exceptions import ExternalAPIInvalidResponseError
from core.logging import log_execution
from schemas.weather import WeatherForecastQuery
from services.base import fetch_json
from utils.filters import any_field_contains, matches_text
from utils.pagination import cap_results, is_list_payload

MODULE_NAME = "weather"


def get_weather_forecast(query: WeatherForecastQuery) -> list[dict[str, Any]]:
    """
    Retrieves and normalizes weather forecast records from data.gov.my.
    Filtering is performed locally because unsupported query parameters
    can cause unstable upstream behavior.
    """
    with log_execution(MODULE_NAME, "fetch_weather_forecast"):
        payload = fetch_json(
            path=settings.WEATHER_FORECAST_PATH,
            module=MODULE_NAME,
        )

    if not is_list_payload(payload):
        raise ExternalAPIInvalidResponseError(module=MODULE_NAME)

    records = [_normalize_weather_record(record) for record in payload]
    filtered_records = [
        record for record in records if _matches_weather_query(record, query)
    ]
    return cap_results(filtered_records, query.limit)


def _normalize_weather_record(record: dict[str, Any]) -> dict[str, Any]:
    location = record.get("location") or {}
    return {
        "location_id": location.get("location_id"),
        "location_name": location.get("location_name"),
        "date": record.get("date"),
        "morning_forecast": record.get("morning_forecast"),
        "afternoon_forecast": record.get("afternoon_forecast"),
        "night_forecast": record.get("night_forecast"),
        "summary_forecast": record.get("summary_forecast"),
        "summary_when": record.get("summary_when"),
        "min_temp": record.get("min_temp"),
        "max_temp": record.get("max_temp"),
    }


def _matches_weather_query(
    record: dict[str, Any],
    query: WeatherForecastQuery,
) -> bool:
    if query.location and not matches_text(
        record.get("location_name"),
        query.location,
        exact=True,
    ):
        return False

    if query.date and record.get("date") != query.date:
        return False

    if query.contains and not any_field_contains(record, query.contains):
        return False

    return True
