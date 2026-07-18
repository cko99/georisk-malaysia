"""
schemas/weather.py

Request/response schemas for the Weather Forecast module.

The upstream payload shape from data.gov.my is passed through largely
as-is (list of forecast records), so `data` is typed as a generic list
of dictionaries rather than a rigid model — this avoids silently
dropping fields the frontend dashboard may already rely on while still
documenting the expected query parameters clearly in Swagger.
"""

from typing import Any, Optional

from pydantic import BaseModel, Field


class WeatherForecastQuery(BaseModel):
    """Optional filters forwarded to the upstream weather forecast endpoint."""

    contains: Optional[str] = Field(
        default=None, description="Filter forecasts where location contains this value."
    )
    location: Optional[str] = Field(
        default=None, description="Exact location / district name filter."
    )
    date: Optional[str] = Field(
        default=None, description="Filter by forecast date (YYYY-MM-DD)."
    )
    limit: Optional[int] = Field(
        default=None, ge=1, le=1000, description="Maximum number of records to return."
    )


WeatherForecastRecord = dict[str, Any]
