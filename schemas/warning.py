"""
schemas/warning.py

Request/response schemas for the Weather Warning module.
"""

from typing import Any, Optional

from pydantic import BaseModel, Field


class WeatherWarningQuery(BaseModel):
    """Optional filters forwarded to the upstream weather warning endpoint."""

    contains: Optional[str] = Field(
        default=None, description="Filter warnings where location/title contains this value."
    )
    state: Optional[str] = Field(
        default=None, description="Filter warnings by Malaysian state."
    )
    limit: Optional[int] = Field(
        default=None, ge=1, le=1000, description="Maximum number of records to return."
    )


WeatherWarningRecord = dict[str, Any]
