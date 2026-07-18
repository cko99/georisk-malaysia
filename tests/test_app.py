"""
tests/test_app.py

System-level endpoint coverage for the GeoRisk Malaysia backend.
"""


class TestApplicationRoutes:
    def test_root_serves_dashboard_html(self, client):
        response = client.get("/")

        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/html")

    def test_health_endpoint_returns_ok(self, client):
        response = client.get("/health")
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert body["module"] == "system"
        assert body["data"]["status"] == "ok"
