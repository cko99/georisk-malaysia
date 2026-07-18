"""
schemas/common.py

Shared Pydantic models used across every module's response schema.
These describe the standardized envelope for OpenAPI/Swagger docs.
"""

from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class StandardResponse(BaseModel, Generic[DataT]):
    """Standardized successful response envelope."""

    success: bool = Field(default=True, examples=[True])
    timestamp: str = Field(..., examples=["2026-07-06T09:15:00.000+00:00"])
    source: str = Field(default="data.gov.my", examples=["data.gov.my"])
    module: str = Field(..., examples=["weather_forecast"])
    data: DataT


class ErrorResponse(BaseModel):
    """Standardized error response envelope."""

    success: bool = Field(default=False, examples=[False])
    timestamp: str = Field(..., examples=["2026-07-06T09:15:00.000+00:00"])
    source: str = Field(default="data.gov.my", examples=["data.gov.my"])
    module: str = Field(..., examples=["weather_forecast"])
    message: str = Field(..., examples=["External API unavailable"])
    details: Optional[Any] = None
