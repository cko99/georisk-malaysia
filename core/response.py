"""
core/response.py

Standardized response envelope used by every endpoint in the API.

Success:
    {
        "success": true,
        "timestamp": "...",
        "source": "data.gov.my",
        "module": "...",
        "data": ...
    }

Failure:
    {
        "success": false,
        "timestamp": "...",
        "source": "data.gov.my",
        "module": "...",
        "message": "..."
    }
"""

from datetime import datetime, timezone
from typing import Any, Optional

from fastapi.responses import JSONResponse


DEFAULT_SOURCE = "data.gov.my"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def success_response(
    module: str,
    data: Any,
    source: str = DEFAULT_SOURCE,
    status_code: int = 200,
) -> JSONResponse:
    """Builds a standardized successful JSON response."""
    payload = {
        "success": True,
        "timestamp": _utc_now_iso(),
        "source": source,
        "module": module,
        "data": data,
    }
    return JSONResponse(status_code=status_code, content=payload)


def error_response(
    module: str,
    message: str,
    source: str = DEFAULT_SOURCE,
    status_code: int = 503,
    details: Optional[Any] = None,
) -> JSONResponse:
    """Builds a standardized error JSON response."""
    payload = {
        "success": False,
        "timestamp": _utc_now_iso(),
        "source": source,
        "module": module,
        "message": message,
    }
    if details is not None:
        payload["details"] = details
    return JSONResponse(status_code=status_code, content=payload)
