"""
api/weather.py

HTTP layer for the Weather Forecast module.
Routers are intentionally thin: they validate input via Pydantic,
delegate to the Service layer, and format the standardized response.
Routers never call `requests.get()` directly.
"""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from core.exceptions import ExternalAPIError
from core.response import error_response, success_response
from schemas.weather import WeatherForecastQuery
from services.weather import MODULE_NAME, get_weather_forecast

router = APIRouter(prefix="/api", tags=["Weather Forecast"])


@router.get(
    "/weather",
    summary="Get weather forecast",
    description=(
        "Retrieves the latest weather forecast data sourced from "
        "data.gov.my. Supports optional filtering by location, date, "
        "and result limit."
    ),
    response_description="Standardized envelope containing forecast records.",
)
def read_weather_forecast(
    query: WeatherForecastQuery = Depends(),
) -> JSONResponse:
    try:
        data = get_weather_forecast(query)
        return success_response(module=MODULE_NAME, data=data)
    except ExternalAPIError as exc:
        return error_response(
            module=exc.module,
            message=exc.message,
            status_code=exc.status_code,
        )


router.add_api_route(
    path="/v1/weather/forecast",
    endpoint=read_weather_forecast,
    methods=["GET"],
    include_in_schema=False,
)
