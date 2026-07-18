"""MVP route, validation, security-header and fallback spatial tests."""


def test_api_health_alias_and_security_headers(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "ok"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"


def test_layer_endpoint_returns_valid_feature_collection(client):
    response = client.get("/api/layers/hazards")
    body = response.json()
    assert response.status_code == 200
    assert body["type"] == "FeatureCollection"
    assert len(body["features"]) == 8
    assert body["metadata"]["mode"] == "demo-fallback"


def test_unknown_layer_is_rejected(client):
    assert client.get("/api/layers/private").status_code == 404


def test_proximity_returns_geojson_and_rule_based_insight(client):
    response = client.post("/api/analysis/proximity", json={
        "latitude": 3.139,
        "longitude": 101.6869,
        "radius_m": 3000,
        "layer": "rivers",
    })
    body = response.json()["data"]
    assert response.status_code == 200
    assert body["nearest"]["properties"]["name"] == "Klang River (demo)"
    assert body["result_geojson"]["type"] == "FeatureCollection"
    assert body["mode"] == "demo-fallback"
    assert "nearest mapped river" in body["insight"]


def test_proximity_validation_rejects_arbitrary_radius(client):
    response = client.post("/api/analysis/proximity", json={
        "latitude": 3.139,
        "longitude": 101.6869,
        "radius_m": 2500,
        "layer": "hazards",
    })
    assert response.status_code == 422


def test_frontend_assets_are_served(client):
    response = client.get("/assets/js/app.js")
    assert response.status_code == 200
    assert "maplibregl.Map" in response.text


def test_basemap_provider_is_allowlisted(client):
    assert client.get("/api/basemaps/google/4/12/7").status_code == 404
    assert client.get("/api/basemaps/osm/4/99/7").status_code == 422
