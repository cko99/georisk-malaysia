"""Rule-based proximity analysis API."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from core.response import success_response
from schemas.analysis import ProximityRequest
from services.spatial import analyze_proximity

router = APIRouter(prefix="/api", tags=["Spatial Analysis"])


@router.post("/analysis/proximity")
def proximity(request: ProximityRequest) -> JSONResponse:
    data = analyze_proximity(
        latitude=request.latitude,
        longitude=request.longitude,
        radius_m=request.radius_m,
        layer=request.layer,
    )
    return success_response(module="proximity", source="GeoRich AI demo fallback", data=data)
