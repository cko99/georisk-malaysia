"""Serve the small, attributed GeoJSON fallback layers used by the MVP."""

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api", tags=["Spatial Layers"])
_data_dir = Path(__file__).resolve().parents[1] / "data" / "sample"
_allowed = {"administrative", "roads", "rivers", "hazards"}


@router.get("/layers/{layer_name}")
def read_layer(layer_name: str) -> JSONResponse:
    if layer_name not in _allowed:
        raise HTTPException(status_code=404, detail="Unknown layer")
    path = _data_dir / f"{layer_name}.geojson"
    return JSONResponse(json.loads(path.read_text(encoding="utf-8")))
