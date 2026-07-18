"""Small, policy-conscious Malaysia place search proxy for Nominatim."""

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from config import settings
from core.exceptions import ExternalAPIError
from core.response import error_response, success_response
from services.external import get_external_json

router = APIRouter(prefix="/api", tags=["Location Search"])


@router.get("/locations/search")
def search_locations(
    q: str = Query(min_length=2, max_length=120),
    limit: int = Query(default=5, ge=1, le=5),
) -> JSONResponse:
    try:
        payload = get_external_json(
            f"{settings.NOMINATIM_BASE_URL}/search",
            module="location_search",
            params={
                "q": q,
                "format": "geojson",
                "limit": limit,
                "countrycodes": "my",
                "addressdetails": 1,
            },
        )
        return success_response(module="location_search", source="OpenStreetMap Nominatim", data=payload)
    except ExternalAPIError as exc:
        return error_response(module=exc.module, message=exc.message, status_code=exc.status_code)
