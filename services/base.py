"""
services/base.py

Shared, isolated HTTP client used by every Service that talks to
data.gov.my. Routers never call `requests.get()` directly — all
outbound traffic is centralized here so that timeout handling, retry
policy, logging, and error translation are consistent across modules.
"""

import time
from typing import Any, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import settings
from core.exceptions import (
    ExternalAPIError,
    ExternalAPIInvalidResponseError,
    ExternalAPITimeoutError,
)
from core.logging import get_module_logger

_logger = get_module_logger("external_api_client")


def _build_session() -> requests.Session:
    """
    Builds a `requests.Session` with a bounded retry policy for
    transient failures (connection errors, 502/503/504) while
    intentionally NOT retrying on 4xx client errors.
    """
    session = requests.Session()
    retry_strategy = Retry(
        total=settings.HTTP_MAX_RETRIES,
        backoff_factor=0.5,
        status_forcelist=[502, 503, 504],
        allowed_methods=frozenset({"GET"}),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update(
        {
            "Accept": "application/json",
            "User-Agent": settings.EXTERNAL_USER_AGENT,
        }
    )
    return session


_session = _build_session()


def fetch_json(
    path: str,
    module: str,
    params: Optional[dict] = None,
) -> Any:
    """
    Performs a GET request against `DATA_GOV_MY_BASE_URL + path` and
    returns the parsed JSON payload.

    Raises:
        ExternalAPITimeoutError: on connection/read timeout.
        ExternalAPIInvalidResponseError: on malformed JSON payloads.
        ExternalAPIError: on any other network or HTTP-level failure.
    """
    url = f"{settings.DATA_GOV_MY_BASE_URL}{path}"
    start_time = time.perf_counter()

    try:
        response = _session.get(
            url,
            params=params,
            timeout=settings.HTTP_TIMEOUT_SECONDS,
        )
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

        if response.status_code >= 400:
            _logger.error(
                f"UPSTREAM_ERROR | module={module} | url={url} "
                f"| status={response.status_code} | execution_time_ms={elapsed_ms}"
            )
            raise ExternalAPIError(
                module=module,
                message="External API unavailable",
                status_code=503,
            )

        try:
            payload = response.json()
        except ValueError as exc:
            _logger.error(
                f"INVALID_JSON | module={module} | url={url} | error={exc}"
            )
            raise ExternalAPIInvalidResponseError(module=module) from exc

        _logger.info(
            f"UPSTREAM_OK | module={module} | url={url} "
            f"| status={response.status_code} | execution_time_ms={elapsed_ms}"
        )
        return payload

    except requests.exceptions.Timeout as exc:
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        _logger.error(
            f"TIMEOUT | module={module} | url={url} | execution_time_ms={elapsed_ms} | error={exc}"
        )
        raise ExternalAPITimeoutError(module=module) from exc

    except requests.exceptions.RequestException as exc:
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        _logger.error(
            f"CONNECTION_ERROR | module={module} | url={url} | execution_time_ms={elapsed_ms} | error={exc}"
        )
        raise ExternalAPIError(
            module=module,
            message="External API unavailable",
            status_code=503,
        ) from exc
