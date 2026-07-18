# Existing Project Audit

Audit date: 18 July 2026  
Primary project: `D:\geo_dashboard\GeoRisk-Malaysia`  
Untouched backup: `D:\geo_dashboard\GeoRisk-Malaysia_backup_before_georich`

## Executive summary

The selected project is the closest existing foundation for GeoRich AI because it already contains a working FastAPI service layer, public Malaysian weather integrations, tests, Docker configuration, and a single-file GIS dashboard. The backend baseline is healthy (12 tests pass), but the frontend is a monolithic Leaflet prototype with mostly hard-coded indicators, placeholder navigation, and no spatial datasets or analysis. PostgreSQL/PostGIS and deployment orchestration are absent.

The conservative reconstruction path is to keep the tested Python service architecture, split the dashboard into a small static frontend, migrate the sole map engine to MapLibre GL JS, and add bounded spatial/demo fallbacks around the existing API.

## Project discovery

### Selected root

`GeoRisk-Malaysia` contains `app.py`, `dashboard.html`, `requirements.txt`, `Dockerfile`, API routers, services, schemas, and tests. It is therefore a stronger base than the other Desktop candidates.

### Reference folders

| Folder | Useful reference | Decision |
|---|---|---|
| `geo dashboard -green\Gis_into_Ai` | Responsive React/Vite dashboard components, error boundaries, layer toggle patterns | Reference only. It uses Leaflet and a heavier React stack that conflicts with the requested no-framework frontend. |
| `GEO-DASHBOARD_blue_streamlit\geospatial-industry-dashboard` | Small Streamlit GIS portfolio | Reference only; not compatible with the target frontend/runtime. |
| `PROFILE GIT` | Portfolio copy and visual assets | Reference only; not part of the operational GIS app. |

## File inventory

### Active root

| Path | Role | Language/type | Status |
|---|---|---|---|
| `app.py` | FastAPI entry point, middleware, health and static HTML routes | Python | Working; needs GeoRich naming and API health alias |
| `config.py` | Pydantic settings | Python | Working; insecure development defaults |
| `api/` | Weather, warning, earthquake routers | Python | Working and tested |
| `services/` | External API client and normalization | Python | Working; synchronous HTTP |
| `schemas/` | Query validation | Python | Working |
| `core/` | Logging, response envelopes, exceptions | Python | Working |
| `utils/` | Filtering and pagination | Python | Working |
| `tests/` | API/service unit tests | Python | 12 tests pass |
| `dashboard.html` | Entire existing UI, CSS, map and charts | HTML/CSS/JS | Runs, but monolithic and placeholder-heavy |
| `requirements.txt` | Python dependencies | Text | Complete for current Sprint 2 only |
| `Dockerfile` | Non-root container build | Dockerfile | Sound baseline; Python 3.12 rather than target 3.11 |
| `.env.example` | Runtime settings example | Env | No secrets; CORS wildcard default |
| `.gitignore` | Exclusions | Git config | Covers secrets, venv, logs and caches |

### Duplicate/archive content

- `sprint-01-dashboard/backend/` duplicates most active backend files byte-for-byte and should be retained only as an archive until stabilization.
- `gemini-code-*.html` are superseded prototype variants.
- `georisk-malaysia-backend-sprint2.zip` is an archive of the backend.
- `Codex Installer.exe` and `Microsoft.Services.Store.winmd` are unrelated binary artefacts.
- `GeoRisk-Malaysia/{ai,dashboard,data,database,docs,images,sql}` exists as an empty nested scaffold.
- `venv/`, `__pycache__/`, `.pytest_cache/`, and `logs/` are local runtime artefacts, correctly ignored but physically present.

No files are deleted during reconstruction; archive candidates are listed in `reuse-plan.md`.

## Frontend audit

- One 49 KB `dashboard.html` contains all markup, approximately 550 lines of CSS, and all JavaScript. This makes testing and safe iteration difficult.
- The visual structure is desktop-first: fixed sidebar/header, six KPI cards, three bottom panels, and no functional mobile drawer or bottom sheet.
- Leaflet 1.9.4, Chart.js, Font Awesome, and Google Fonts are loaded from CDNs without integrity pinning.
- Navigation, report generation, notification, AI chat, settings, and multiple `Coming Soon` modules are non-functional or explicitly prohibited by the MVP brief.
- Search is present visually but is not a place/coordinate search workflow.
- Six KPI values and chart series begin as hard-coded portfolio data. Live feed code updates only part of the UI.
- Multiple `innerHTML` writes are used. Several are static, but upstream values are interpolated into generated markup and should be replaced with DOM/text APIs.
- There are no automated frontend tests, build/lint check, accessible mobile navigation, skip link, live-region strategy, or robust focus management.
- External API errors are partially rendered as feed cards; the primary dashboard lacks coherent loading, empty, and offline states.

## Map audit

- Primary engine: Leaflet 1.9.4. No MapLibre, Mapbox, OpenLayers, Google Maps, or ArcGIS JS runtime is active.
- Basemap: CARTO dark raster tiles; no API token is required, but provider usage/attribution is not documented in the repo.
- Initial view is Malaysia-like but the current configuration is not expressed as a documented national extent.
- The map has zoom interaction and a basemap only. There are no operational sources, GeoJSON layers, markers, popups, legend, layer toggles, scale, fullscreen, current-coordinate display, or selected-location marker.
- Roads and rivers are visible only as part of the raster basemap, not addressable analytical layers.
- No geospatial dependencies or client-side geometry library are present.

Migration is justified: the existing map is isolated to one HTML file, contains no reusable Leaflet analytical logic, and MapLibre GL JS is a core requirement.

## Backend audit

- FastAPI application with thin routers, validated queries, a shared service layer, standardized JSON envelopes, exception handlers, request timing logs, Swagger/ReDoc, and a non-root container.
- Routes: `/health`, `/api/weather`, `/api/weather/warning`, `/api/weather/earthquake`, plus hidden `/api/v1/...` aliases.
- `data.gov.my` weather forecast and warning endpoints returned HTTP 200 during the audit. The earthquake endpoint timed out once, confirming the need for clear degraded-state handling.
- External calls use a bounded timeout and retries. The synchronous `requests` client is acceptable for a small MVP but can block FastAPI workers under concurrency.
- CORS permits all origins by default. Production defaults need restriction and environment validation.
- No rate limiting, response caching, security headers, readiness check, database connection, spatial endpoint, or ETL layer exists.
- The required `/api/health` route does not exist yet.

## Data audit

No GeoJSON, JSON, CSV, Shapefile, GeoPackage, KML, or raster dataset exists in the active project. Consequently CRS, geometry, feature count, attribute completeness, duplicates, and validity cannot be measured for project data.

The only operational data are live JSON responses:

| Provider/dataset | Format | Coverage | Key fields | Licence/attribution | Audit status |
|---|---|---|---|---|---|
| data.gov.my weather forecast | JSON list | Malaysia locations | location, date, morning/afternoon/night forecast, min/max temperature | Malaysia public-sector open data; show provider attribution | Live HTTP 200 |
| data.gov.my weather warning | JSON list | Malaysia | issue/validity, English and Malay heading/text/instructions | Malaysia public-sector open data; show provider attribution | Live HTTP 200 |
| data.gov.my earthquake warning | JSON list | Malaysia/region | event data including location and magnitude where supplied | Malaysia public-sector open data; show provider attribution | Timed out once during audit |

Any added sample GeoJSON must declare WGS84 (`EPSG:4326`), provenance, licence, timestamp, and its demo/non-authoritative nature.

## Deployment audit

- A production-style Dockerfile exists, but there is no `docker-compose.yml`, database service, deployment manifest, GitHub Actions workflow, or frontend hosting split.
- The app serves the HTML dashboard from FastAPI, which is convenient for local/demo deployment.
- Documentation assumes `localhost:8000`; no production URL is hard-coded in application JavaScript.
- Git CLI is unavailable in the current environment, so a verified filesystem backup was used instead of a baseline commit.
- No `.openai/hosting.json` exists; the Sites-specific runtime is therefore not imposed on this FastAPI project.

## Security audit

- No committed `.env` file or obvious API key/password/database connection string was found. Values in `.env.example` are non-secret examples.
- CORS wildcard is the most immediate configuration risk. `allow_credentials=False` reduces impact but production origins should be explicit.
- Several `innerHTML` paths can combine UI markup with external values, presenting an avoidable XSS risk.
- Error handlers return generic client messages, but full exception text is written to local logs. Logs must never contain credentials or full sensitive URLs.
- SQL injection is not currently applicable because no SQL/database layer exists. Future spatial queries must use SQLAlchemy parameters.
- Docker runs as a non-root user, a positive control.
- CDN dependencies lack Subresource Integrity; self-hosting or strict version pinning plus CSP should be considered.
- The UI makes unverified security claims (for example TLS and end-to-end encryption) and must remove them.

## Baseline verification

| Check | Result |
|---|---|
| Backup file count/bytes | 2,555 files and 39,777,776 bytes match source |
| Python test suite | 12 passed |
| data.gov.my forecast | HTTP 200 |
| data.gov.my warning | HTTP 200 |
| data.gov.my earthquake | One read timeout; degraded handling required |
| Open-Meteo coordinate weather | HTTP 200, keyless JSON response |
| Nominatim Malaysia place search | HTTP 200 with identifying User-Agent |

## Missing files/capabilities

Missing: separated frontend assets, MapLibre map, GeoJSON/data metadata, location search, coordinate search, selected marker, operational layer control/legend, proximity endpoint, automated insight, four-MVP KPI logic, responsive drawer/bottom sheet, PostGIS schema/index/seed, ETL scripts, Compose, CI, deployment/security/data-source/architecture documentation, and minimum tests for the new spatial flows.

