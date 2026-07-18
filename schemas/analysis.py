"""Validated proximity analysis request."""

from typing import Literal

from pydantic import BaseModel, Field


class ProximityRequest(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    radius_m: Literal[500, 1000, 3000, 5000]
    layer: Literal["hazards", "roads", "rivers"]
