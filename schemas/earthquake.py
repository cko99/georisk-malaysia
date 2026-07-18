"""
schemas/earthquake.py

Request/response schemas for the Earthquake Warning module.
"""

from typing import Any, Optional

from pydantic import BaseModel, Field


class EarthquakeWarningQuery(BaseModel):
    """Optional filters forwarded to the upstream earthquake warning endpoint."""

    contains: Optional[str] = Field(
        default=None, description="Filter earthquake events where location contains this value."
    )
    min_magnitude: Optional[float] = Field(
        default=None, ge=0, le=10, description="Minimum earthquake magnitude filter."
    )
    limit: Optional[int] = Field(
        default=None, ge=1, le=1000, description="Maximum number of records to return."
    )


EarthquakeWarningRecord = dict[str, Any]
