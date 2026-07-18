"""
app.py

Application entrypoint for the GeoRich AI backend.

Responsibilities:
    - Instantiate the FastAPI application with Swagger metadata.
    - Register CORS middleware for the existing HTML dashboard.
    - Register routers (weather, warning, earthquake).
    - Register global exception handlers so unhandled errors still
      conform to the standardized response envelope.
    - Expose a lightweight `/health` endpoint for uptime checks and
      container orchestration probes.
"""

import time
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api.earthquake import router as earthquake_router
from api.warning import router as warning_router
from api.weather import router as weather_router
from api.analysis import router as analysis_router
from api.basemaps import router as basemaps_router
from api.layers import router as layers_router
from api.location import router as location_router
from api.open_meteo import router as open_meteo_router
from config import settings
from core.exceptions import ExternalAPIError
from core.logging import get_module_logger
from core.response import error_response, success_response

_logger = get_module_logger("app")
_base_dir = Path(__file__).resolve().parent
_dashboard_file = _base_dir / "frontend" / "index.html"
_legacy_dashboard_file = _base_dir / "dashboard.html"

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    contact={
        "name": settings.CONTACT_NAME,
        "email": settings.CONTACT_EMAIL,
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.mount("/assets", StaticFiles(directory=_base_dir / "frontend" / "assets"), name="assets")


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    """
    Logs every inbound HTTP request with timestamp, path, execution
    time, and resulting status code — satisfying the project's
    logging requirement at the transport layer in addition to the
    per-service logging already performed in `services/base.py`.
    """
    start_time = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception as exc:
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        _logger.error(
            f"HTTP {request.method} {request.url.path} "
            f"| status=500 | execution_time_ms={elapsed_ms} | error={exc}"
        )
        raise

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
    _logger.info(
        f"HTTP {request.method} {request.url.path} "
        f"| status={response.status_code} | execution_time_ms={elapsed_ms}"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(self)"
    return response


@app.exception_handler(ExternalAPIError)
async def external_api_error_handler(request: Request, exc: ExternalAPIError):
    """Global safety net: converts any un-caught ExternalAPIError into the standard envelope."""
    return error_response(
        module=exc.module,
        message=exc.message,
        status_code=exc.status_code,
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Global safety net for truly unexpected errors — never leak stack traces to clients."""
    _logger.error(f"UNHANDLED_EXCEPTION | path={request.url.path} | error={exc}")
    return error_response(
        module="app",
        message="Internal server error",
        source="georich-ai",
        status_code=500,
    )


# ----------------------------------------------------------------------
# Routers
# ----------------------------------------------------------------------
app.include_router(weather_router)
app.include_router(warning_router)
app.include_router(earthquake_router)
app.include_router(open_meteo_router)
app.include_router(location_router)
app.include_router(layers_router)
app.include_router(analysis_router)
app.include_router(basemaps_router)


# ----------------------------------------------------------------------
# Health check
# ----------------------------------------------------------------------
@app.get(
    "/health",
    tags=["System"],
    summary="Service health check",
    description="Lightweight liveness probe for container orchestration and uptime monitoring.",
)
def health_check():
    return success_response(
        module="system",
        source="georich-ai",
        data={
            "status": "ok",
            "environment": settings.ENVIRONMENT,
            "version": settings.APP_VERSION,
        },
    )


app.add_api_route("/api/health", health_check, methods=["GET"], tags=["System"])


@app.get("/", include_in_schema=False)
def read_root() -> FileResponse:
    return FileResponse(_dashboard_file, media_type="text/html")


@app.get("/dashboard.html", include_in_schema=False)
def read_dashboard() -> FileResponse:
    return FileResponse(_dashboard_file, media_type="text/html")


@app.get("/legacy", include_in_schema=False)
def read_legacy_dashboard() -> FileResponse:
    return FileResponse(_legacy_dashboard_file, media_type="text/html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
