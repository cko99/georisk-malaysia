"""Coordinate-based current weather from the keyless Open-Meteo API."""

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from config import settings
from core.exceptions import ExternalAPIError
from core.response import error_response, success_response
from services.external import get_external_json

router = APIRouter(prefix="/api", tags=["Current Weather"])


@router.get("/weather/current")
def current_weather(
    latitude: float = Query(ge=-90, le=90),
    longitude: float = Query(ge=-180, le=180),
) -> JSONResponse:
    try:
        payload = get_external_json(
            f"{settings.OPEN_METEO_BASE_URL}/v1/forecast",
            module="open_meteo",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,precipitation,rain,weather_code,wind_speed_10m",
                "timezone": "Asia/Kuala_Lumpur",
            },
        )
        return success_response(module="current_weather", source="Open-Meteo", data=payload)
    except ExternalAPIError as exc:
        return error_response(module=exc.module, message=exc.message, status_code=exc.status_code)
