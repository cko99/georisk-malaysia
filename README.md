# GeoRich AI

**Open-Source Geospatial Risk Intelligence for Malaysia**

[Live portfolio demo](https://georich-ai.onrender.com) · [Interactive API documentation](https://georich-ai.onrender.com/docs)

GeoRich AI is a working portfolio MVP reconstructed from the existing GeoRisk Malaysia project. It combines a MapLibre GL JS dashboard, official Malaysian weather warnings, keyless coordinate weather, Malaysian place search, proximity analysis, deterministic spatial insight and a PostGIS-ready data path.

The default application costs RM0 to run locally and uses no paid AI, map token or API key.

## Public demo

Open **<https://georich-ai.onrender.com>** to explore the deployed v1 dashboard. Search for a Malaysian place or enter coordinates such as `3.139, 101.687`, compare Satellite, Hybrid and OpenStreetMap, then run a radius-based proximity analysis.

The demo runs on Render's free service. After a period without traffic, the first request can take about a minute while the service wakes up.

## What works

- MapLibre GL JS map centered on Malaysia
- Navigation, scale, fullscreen, coordinates, popup and selected marker
- Five operational overlays: administrative, roads, rivers, weather and hazards
- Three requested basemap choices: Satellite, Hybrid and OpenStreetMap. Satellite/Hybrid use Esri World Imagery services because Google imagery requires an authenticated, billing-enabled Google Maps Platform account.
- Place search through a policy-conscious Nominatim proxy
- Latitude/longitude search and fly-to
- Open-Meteo temperature, rainfall, wind, code and timestamp
- data.gov.my weather warning KPI
- 500 m, 1 km, 3 km and 5 km proximity analysis
- Feature count, nearest feature, result GeoJSON and map highlight
- Rule-based insight with no paid AI service
- Four KPI cards, one source-labelled chart and a traceable data-source panel
- Mobile drawer, analysis bottom sheet and no horizontal scroll
- FastAPI validation, error envelopes, logs, security headers and restricted local CORS defaults
- PostgreSQL/PostGIS schema, GiST index, seed and parameterized loader
- Docker Compose, Render blueprint and GitHub Actions test workflow

## Quick start

Use the existing environment:

```powershell
.\venv\Scripts\python.exe -m uvicorn app:app --reload
```

Open <http://localhost:8000>. API documentation is at <http://localhost:8000/docs>.

Or use containers:

```powershell
docker compose up --build
```

## API

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/health` | Liveness and version |
| GET | `/api/weather` | data.gov.my forecast |
| GET | `/api/weather/warning` | Official warnings |
| GET | `/api/weather/earthquake` | Earthquake warning feed |
| GET | `/api/weather/current` | Coordinate weather from Open-Meteo |
| GET | `/api/locations/search` | Malaysia place search |
| GET | `/api/layers/{name}` | Small attributed GeoJSON layer |
| POST | `/api/analysis/proximity` | Preset-radius spatial analysis |

Example proximity request:

```json
{
  "latitude": 3.139,
  "longitude": 101.6869,
  "radius_m": 3000,
  "layer": "rivers"
}
```

## Tests and data validation

```powershell
.\venv\Scripts\python.exe -m pytest -q
.\venv\Scripts\python.exe scripts\validate_data.py data\sample\hazards.geojson
```

## Project structure

```text
frontend/       MapLibre dashboard and assets
api/            FastAPI route layer
services/       External clients and spatial rules
schemas/        Validated request models
data/sample/    Small WGS84 demo fallback
database/       PostGIS schema, indexes and seed
scripts/        Fetch, validate, transform and load ETL
tests/          Backend and MVP regression tests
docs/           Audit, architecture, sources, security and deployment
```

## Important data notice

Official live feeds are labelled separately from demo data. The fallback boundaries, roads and rivers are generalised; all hazard points and chart values are synthetic. GeoRich AI is a portfolio decision-support demonstration, not an emergency warning, navigation, engineering or insurance system.

Start with [the audit](docs/existing-project-audit.md), [architecture](docs/architecture.md), [data sources](docs/data-sources.md), [security](docs/security.md), [deployment](docs/deployment.md) and [limitations](docs/limitations.md).

## Licence

Application code is released under the MIT License. Third-party data remains under its documented provider licence and attribution requirements; see `docs/data-sources.md`.
