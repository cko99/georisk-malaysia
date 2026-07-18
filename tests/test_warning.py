"""
tests/test_warning.py

Unit and integration-style tests for the Weather Warning module.
"""

from unittest.mock import patch

from core.exceptions import ExternalAPIError


SAMPLE_WARNING_RAW = [
    {
        "warning_issue": {
            "issued": "2026-07-06T06:00:00+08:00",
            "title_en": "Heavy Rain Warning",
            "title_bm": "Amaran Hujan Lebat",
        },
        "valid_from": "2026-07-06T06:00:00+08:00",
        "valid_to": "2026-07-06T12:00:00+08:00",
        "heading_en": "Heavy Rain",
        "heading_bm": "Hujan Lebat",
        "text_en": "Heavy rain expected over Selangor.",
        "text_bm": "Hujan lebat dijangka di Selangor.",
        "instruction_en": "Stay alert.",
        "instruction_bm": "Sentiasa berwaspada.",
    },
    {
        "warning_issue": {
            "issued": "2026-07-06T07:00:00+08:00",
            "title_en": "Strong Wind Warning",
            "title_bm": "Amaran Angin Kencang",
        },
        "valid_from": "2026-07-06T07:00:00+08:00",
        "valid_to": "2026-07-06T18:00:00+08:00",
        "heading_en": "Strong Wind",
        "heading_bm": "Angin Kencang",
        "text_en": "Strong winds expected over Sabah.",
        "text_bm": "Angin kencang dijangka di Sabah.",
        "instruction_en": None,
        "instruction_bm": None,
    }
]

EXPECTED_WARNING = [
    {
        "issued_at": "2026-07-06T06:00:00+08:00",
        "valid_from": "2026-07-06T06:00:00+08:00",
        "valid_to": "2026-07-06T12:00:00+08:00",
        "title": "Heavy Rain Warning",
        "title_en": "Heavy Rain Warning",
        "title_bm": "Amaran Hujan Lebat",
        "heading": "Heavy Rain",
        "heading_en": "Heavy Rain",
        "heading_bm": "Hujan Lebat",
        "description": "Heavy rain expected over Selangor.",
        "description_en": "Heavy rain expected over Selangor.",
        "description_bm": "Hujan lebat dijangka di Selangor.",
        "instruction": "Stay alert.",
        "instruction_en": "Stay alert.",
        "instruction_bm": "Sentiasa berwaspada.",
    },
    {
        "issued_at": "2026-07-06T07:00:00+08:00",
        "valid_from": "2026-07-06T07:00:00+08:00",
        "valid_to": "2026-07-06T18:00:00+08:00",
        "title": "Strong Wind Warning",
        "title_en": "Strong Wind Warning",
        "title_bm": "Amaran Angin Kencang",
        "heading": "Strong Wind",
        "heading_en": "Strong Wind",
        "heading_bm": "Angin Kencang",
        "description": "Strong winds expected over Sabah.",
        "description_en": "Strong winds expected over Sabah.",
        "description_bm": "Angin kencang dijangka di Sabah.",
        "instruction": None,
        "instruction_en": None,
        "instruction_bm": None,
    },
]


class TestWeatherWarningEndpoint:
    @patch("services.warning.fetch_json", return_value=SAMPLE_WARNING_RAW)
    def test_returns_standard_envelope_on_success(self, mock_fetch, client):
        response = client.get("/api/weather/warning")
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert body["module"] == "weather_warning"
        assert body["data"] == EXPECTED_WARNING

    @patch("services.warning.fetch_json", return_value=SAMPLE_WARNING_RAW)
    def test_applies_state_filter_locally(self, mock_fetch, client):
        response = client.get("/api/weather/warning", params={"state": "Selangor"})
        body = response.json()

        assert response.status_code == 200
        assert len(body["data"]) == 1
        assert body["data"][0]["title"] == "Heavy Rain Warning"
        _, kwargs = mock_fetch.call_args
        assert kwargs.get("params") is None

    @patch(
        "services.warning.fetch_json",
        side_effect=ExternalAPIError(module="weather_warning", message="External API unavailable"),
    )
    def test_returns_503_when_upstream_unavailable(self, mock_fetch, client):
        response = client.get("/api/weather/warning")
        body = response.json()

        assert response.status_code == 503
        assert body["success"] is False
        assert body["module"] == "weather_warning"
