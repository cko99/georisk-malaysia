"""
core/logging.py

Centralized Loguru configuration for the entire application.
Provides a single `logger` instance and a `log_execution` context
manager/decorator used by services and routers to log:

    - timestamp
    - module
    - execution time
    - status
"""

import sys
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from loguru import logger

from config import settings

_LOGGER_CONFIGURED = False


def configure_logging() -> None:
    """
    Configures Loguru sinks exactly once.

    - Console sink: human-readable, colorized, level from settings.
    - File sink: rotating JSON-friendly file for persistence / shipping
      to external log aggregators (ELK, CloudWatch, etc.).
    """
    global _LOGGER_CONFIGURED
    if _LOGGER_CONFIGURED:
        return

    logger.remove()

    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        colorize=True,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{extra[module]}</cyan> | "
            "<level>{message}</level>"
        ),
        filter=_ensure_module_field,
        backtrace=False,
        diagnose=False,
    )

    log_dir = Path(settings.LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)

    logger.add(
        log_dir / "georich_backend.log",
        level=settings.LOG_LEVEL,
        rotation=settings.LOG_ROTATION,
        retention=settings.LOG_RETENTION,
        serialize=True,
        filter=_ensure_module_field,
        backtrace=False,
        diagnose=False,
    )

    _LOGGER_CONFIGURED = True


def _ensure_module_field(record: dict) -> bool:
    """Guarantees `extra['module']` always exists to avoid KeyError in format strings."""
    record["extra"].setdefault("module", "app")
    return True


def get_module_logger(module_name: str):
    """Returns a logger bound with a fixed `module` field for structured logs."""
    return logger.bind(module=module_name)


@contextmanager
def log_execution(module_name: str, action: str) -> Generator[None, None, None]:
    """
    Context manager that logs the start, completion (with execution time),
    and failure of an operation in a standardized format.

    Usage:
        with log_execution("weather_service", "fetch_forecast"):
            ...
    """
    bound_logger = get_module_logger(module_name)
    start_time = time.perf_counter()
    bound_logger.info(f"START | action={action}")

    try:
        yield
    except Exception as exc:
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        bound_logger.error(
            f"FAILED | action={action} | execution_time_ms={elapsed_ms} | error={exc}"
        )
        raise
    else:
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        bound_logger.info(
            f"SUCCESS | action={action} | execution_time_ms={elapsed_ms}"
        )


configure_logging()
