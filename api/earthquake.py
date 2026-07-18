"""
api/earthquake.py

HTTP layer for the Earthquake Warning module.
"""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from core.exceptions import ExternalAPIError
from core.response import error_response, success_response
from schemas.earthquake import EarthquakeWarningQuery
from services.earthquake import MODULE_NAME, get_earthquake_warning

router = APIRouter(prefix="/api", tags=["Earthquake Warning"])


@router.get(
    "/weather/earthquake",
    summary="Get earthquake warnings",
    description=(
        "Retrieves earthquake warning/event data sourced from "
        "data.gov.my. Supports optional filtering by minimum "
        "magnitude and result limit."
    ),
    response_description="Standardized envelope containing earthquake event records.",
)
def read_earthquake_warning(
    query: EarthquakeWarningQuery = Depends(),
) -> JSONResponse:
    try:
        data = get_earthquake_warning(query)
        return success_response(module=MODULE_NAME, data=data)
    except ExternalAPIError as exc:
        return error_response(
            module=exc.module,
            message=exc.message,
            status_code=exc.status_code,
        )


router.add_api_route(
    path="/v1/weather/warning/earthquake",
    endpoint=read_earthquake_warning,
    methods=["GET"],
    include_in_schema=False,
)
