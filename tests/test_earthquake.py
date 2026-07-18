"""
tests/test_earthquake.py

Unit and integration-style tests for the Earthquake Warning module,
including the client-side `min_magnitude` post-filter.
"""

from unittest.mock import patch

from core.exceptions import ExternalAPIError


SAMPLE_EARTHQUAKES_RAW = [
    {
        "utcdatetime": "2026-07-06T00:00:00",
        "localdatetime": "2026-07-06T08:00:00",
        "lat": 5.9804,
        "lon": 116.0735,
        "depth": 10,
        "location": "Ranau, Sabah",
        "location_original": "Ranau, Sabah",
        "n_distancemas": "20km E Ranau, Sabah",
        "n_distancerest": "20km E Ranau, Sabah",
        "nbm_distancemas": "20km T Ranau, Sabah",
        "nbm_distancerest": "20km T Ranau, Sabah",
        "magdefault": 5.2,
        "magtypedefault": "Mw",
        "status": "ADVISORY",
        "visible": True,
    },
    {
        "utcdatetime": "2026-07-05T23:00:00",
        "localdatetime": "2026-07-06T07:00:00",
        "lat": 6.8837,
        "lon": 116.8477,
        "depth": 5,
        "location": "Kudat, Sabah",
        "location_original": "Kudat, Sabah",
        "n_distancemas": "12km N Kudat, Sabah",
        "n_distancerest": "12km N Kudat, Sabah",
        "nbm_distancemas": "12km U Kudat, Sabah",
        "nbm_distancerest": "12km U Kudat, Sabah",
        "magdefault": 2.1,
        "magtypedefault": "mb",
        "status": "NORMAL",
        "visible": True,
    },
]

EXPECTED_EARTHQUAKES = [
    {
        "utc_datetime": "2026-07-06T00:00:00",
        "local_datetime": "2026-07-06T08:00:00",
        "latitude": 5.9804,
        "longitude": 116.0735,
        "depth_km": 10,
        "location": "Ranau, Sabah",
        "location_original": "Ranau, Sabah",
        "distance_malaysia": "20km E Ranau, Sabah",
        "distance_reference": "20km E Ranau, Sabah",
        "magnitude": 5.2,
        "magnitude_type": "Mw",
        "status": "ADVISORY",
        "visible": True,
    },
    {
        "utc_datetime": "2026-07-05T23:00:00",
        "local_datetime": "2026-07-06T07:00:00",
        "latitude": 6.8837,
        "longitude": 116.8477,
        "depth_km": 5,
        "location": "Kudat, Sabah",
        "location_original": "Kudat, Sabah",
        "distance_malaysia": "12km N Kudat, Sabah",
        "distance_reference": "12km N Kudat, Sabah",
        "magnitude": 2.1,
        "magnitude_type": "mb",
        "status": "NORMAL",
        "visible": True,
    },
]


class TestEarthquakeWarningEndpoint:
    @patch("services.earthquake.fetch_json", return_value=SAMPLE_EARTHQUAKES_RAW)
    def test_returns_standard_envelope_on_success(self, mock_fetch, client):
        response = client.get("/api/weather/earthquake")
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert body["module"] == "earthquake_warning"
        assert body["data"] == EXPECTED_EARTHQUAKES

    @patch("services.earthquake.fetch_json", return_value=SAMPLE_EARTHQUAKES_RAW)
    def test_min_magnitude_filters_results(self, mock_fetch, client):
        response = client.get(
            "/api/weather/earthquake",
            params={"min_magnitude": 5.0},
        )
        body = response.json()

        assert response.status_code == 200
        assert len(body["data"]) == 1
        assert body["data"][0]["location"] == "Ranau, Sabah"

    @patch(
        "services.earthquake.fetch_json",
        side_effect=ExternalAPIError(module="earthquake_warning", message="External API unavailable"),
    )
    def test_returns_503_when_upstream_unavailable(self, mock_fetch, client):
        response = client.get("/api/weather/earthquake")
        body = response.json()

        assert response.status_code == 503
        assert body["success"] is False
        assert body["module"] == "earthquake_warning"
