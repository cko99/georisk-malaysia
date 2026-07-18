"""Bounded JSON client for keyless providers other than data.gov.my."""

from typing import Any

import requests

from config import settings
from core.exceptions import ExternalAPIError, ExternalAPIInvalidResponseError, ExternalAPITimeoutError


def get_external_json(url: str, module: str, params: dict[str, Any]) -> Any:
    try:
        response = requests.get(
            url,
            params=params,
            headers={"Accept": "application/json", "User-Agent": settings.EXTERNAL_USER_AGENT},
            timeout=settings.HTTP_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        try:
            return response.json()
        except ValueError as exc:
            raise ExternalAPIInvalidResponseError(module=module) from exc
    except requests.exceptions.Timeout as exc:
        raise ExternalAPITimeoutError(module=module) from exc
    except requests.exceptions.RequestException as exc:
        raise ExternalAPIError(module=module, message="External API unavailable", status_code=503) from exc
