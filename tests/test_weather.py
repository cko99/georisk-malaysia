"""
tests/test_weather.py

Unit and integration-style tests for the Weather Forecast module.
External calls are mocked at the `services.base.fetch_json` boundary
so tests remain fast, deterministic, and independent of data.gov.my
availability.
"""

from unittest.mock import patch

from core.exceptions import ExternalAPIError


SAMPLE_FORECAST_RAW = [
    {
        "location": {
            "location_id": "W001",
            "location_name": "Kuala Lumpur",
        },
        "date": "2026-07-06",
        "morning_forecast": "Thunderstorms",
        "afternoon_forecast": "Cloudy",
        "night_forecast": "Rain",
        "summary_forecast": "Thunderstorms",
        "summary_when": "Morning",
        "min_temp": 24,
        "max_temp": 33,
    },
    {
        "location": {
            "location_id": "W002",
            "location_name": "Johor Bahru",
        },
        "date": "2026-07-07",
        "morning_forecast": "Sunny",
        "afternoon_forecast": "Hot",
        "night_forecast": "Clear",
        "summary_forecast": "Sunny",
        "summary_when": "All day",
        "min_temp": 25,
        "max_temp": 34,
    },
]

EXPECTED_FORECAST = [
    {
        "location_id": "W001",
        "location_name": "Kuala Lumpur",
        "date": "2026-07-06",
        "morning_forecast": "Thunderstorms",
        "afternoon_forecast": "Cloudy",
        "night_forecast": "Rain",
        "summary_forecast": "Thunderstorms",
        "summary_when": "Morning",
        "min_temp": 24,
        "max_temp": 33,
    },
    {
        "location_id": "W002",
        "location_name": "Johor Bahru",
        "date": "2026-07-07",
        "morning_forecast": "Sunny",
        "afternoon_forecast": "Hot",
        "night_forecast": "Clear",
        "summary_forecast": "Sunny",
        "summary_when": "All day",
        "min_temp": 25,
        "max_temp": 34,
    },
]


class TestWeatherForecastEndpoint:
    @patch("services.weather.fetch_json", return_value=SAMPLE_FORECAST_RAW)
    def test_returns_standard_envelope_on_success(self, mock_fetch, client):
        response = client.get("/api/weather")
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert body["module"] == "weather"
        assert body["source"] == "data.gov.my"
        assert body["data"] == EXPECTED_FORECAST
        assert "timestamp" in body

    @patch("services.weather.fetch_json", return_value=SAMPLE_FORECAST_RAW)
    def test_applies_query_filters_locally(self, mock_fetch, client):
        response = client.get(
            "/api/weather",
            params={"contains": "Kuala Lumpur", "limit": 1},
        )
        body = response.json()

        assert response.status_code == 200
        assert len(body["data"]) == 1
        assert body["data"][0]["location_name"] == "Kuala Lumpur"
        _, kwargs = mock_fetch.call_args
        assert kwargs.get("params") is None

    @patch(
        "services.weather.fetch_json",
        side_effect=ExternalAPIError(module="weather", message="External API unavailable"),
    )
    def test_returns_503_when_upstream_unavailable(self, mock_fetch, client):
        response = client.get("/api/weather")
        body = response.json()

        assert response.status_code == 503
        assert body["success"] is False
        assert body["module"] == "weather"
        assert "message" in body

    def test_rejects_invalid_limit(self, client):
        response = client.get("/api/weather", params={"limit": 0})
        assert response.status_code == 422
