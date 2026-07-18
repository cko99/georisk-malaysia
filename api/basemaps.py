"""Same-origin relay for the explicitly approved public basemap services."""

from fastapi import APIRouter, HTTPException, Path
from fastapi.responses import Response
import requests

from config import settings

router = APIRouter(prefix="/api/basemaps", tags=["Basemaps"])

SOURCES = {
    "imagery": (
        "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        86_400,
    ),
    "transport": (
        "https://services.arcgisonline.com/ArcGIS/rest/services/Reference/World_Transportation/MapServer/tile/{z}/{y}/{x}",
        86_400,
    ),
    "places": (
        "https://services.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",
        86_400,
    ),
    "osm": ("https://tile.openstreetmap.org/{z}/{x}/{y}.png", 604_800),
}


@router.get("/{provider}/{z}/{x}/{y}", include_in_schema=False)
def basemap_tile(
    provider: str,
    z: int = Path(ge=0, le=19),
    x: int = Path(ge=0),
    y: int = Path(ge=0),
) -> Response:
    if provider not in SOURCES:
        raise HTTPException(status_code=404, detail="Unknown basemap provider")
    limit = (1 << z) - 1
    if x > limit or y > limit:
        raise HTTPException(status_code=422, detail="Tile coordinate outside zoom grid")
    template, max_age = SOURCES[provider]
    try:
        upstream = requests.get(
            template.format(z=z, x=x, y=y),
            timeout=settings.HTTP_TIMEOUT_SECONDS,
            headers={"User-Agent": settings.EXTERNAL_USER_AGENT},
        )
        upstream.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=503, detail="Basemap tile unavailable") from exc
    content_type = upstream.headers.get("content-type", "image/png")
    return Response(
        content=upstream.content,
        media_type=content_type,
        headers={"Cache-Control": f"public, max-age={max_age}"},
    )
