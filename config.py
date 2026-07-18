"""
config.py

Centralized application configuration.
Loads environment variables via python-dotenv and exposes a single
immutable Settings object consumed across the application.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    """
    Application-wide configuration.

    All values can be overridden via environment variables or a `.env`
    file placed at the project root (see `.env.example`).
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # Application metadata
    # ------------------------------------------------------------------
    APP_NAME: str = "GeoRich AI API"
    APP_VERSION: str = "0.2.0"
    APP_DESCRIPTION: str = (
        "Open-source geospatial risk intelligence for Malaysia."
    )
    CONTACT_NAME: str = "GeoRich AI"
    CONTACT_EMAIL: str = "maintainer@georich-ai.local"

    # ------------------------------------------------------------------
    # Server
    # ------------------------------------------------------------------
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # ------------------------------------------------------------------
    # CORS
    # ------------------------------------------------------------------
    CORS_ORIGINS: str = "http://localhost:8000,http://127.0.0.1:8000"

    # ------------------------------------------------------------------
    # External data source: data.gov.my
    # ------------------------------------------------------------------
    DATA_GOV_MY_BASE_URL: str = "https://api.data.gov.my"
    WEATHER_FORECAST_PATH: str = "/weather/forecast"
    WEATHER_WARNING_PATH: str = "/weather/warning"
    EARTHQUAKE_WARNING_PATH: str = "/weather/warning/earthquake"

    OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com"
    NOMINATIM_BASE_URL: str = "https://nominatim.openstreetmap.org"
    EXTERNAL_USER_AGENT: str = "GeoRich-AI/0.2 (open-source portfolio MVP)"

    DATABASE_URL: str = "postgresql+psycopg://georich:georich@db:5432/georich"

    HTTP_TIMEOUT_SECONDS: float = Field(default=10.0, ge=1.0, le=60.0)
    HTTP_MAX_RETRIES: int = Field(default=2, ge=0, le=5)

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "logs"
    LOG_ROTATION: str = "10 MB"
    LOG_RETENTION: str = "14 days"

    @property
    def cors_origin_list(self) -> list[str]:
        if self.CORS_ORIGINS.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Returns a cached Settings singleton.

    Using `lru_cache` avoids re-parsing environment variables on every
    request while still allowing dependency injection via FastAPI's
    `Depends(get_settings)`.
    """
    return Settings()


settings = get_settings()
