"""
api/warning.py

HTTP layer for the Weather Warning module.
"""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from core.exceptions import ExternalAPIError
from core.response import error_response, success_response
from schemas.warning import WeatherWarningQuery
from services.warning import MODULE_NAME, get_weather_warning

router = APIRouter(prefix="/api", tags=["Weather Warning"])


@router.get(
    "/weather/warning",
    summary="Get active weather warnings",
    description=(
        "Retrieves active weather warning notices sourced from "
        "data.gov.my. Supports optional filtering by state and "
        "result limit."
    ),
    response_description="Standardized envelope containing warning records.",
)
def read_weather_warning(
    query: WeatherWarningQuery = Depends(),
) -> JSONResponse:
    try:
        data = get_weather_warning(query)
        return success_response(module=MODULE_NAME, data=data)
    except ExternalAPIError as exc:
        return error_response(
            module=exc.module,
            message=exc.message,
            status_code=exc.status_code,
        )


router.add_api_route(
    path="/v1/weather/warning",
    endpoint=read_weather_warning,
    methods=["GET"],
    include_in_schema=False,
)
