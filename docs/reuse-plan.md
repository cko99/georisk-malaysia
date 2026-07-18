# Reuse Plan

This plan preserves all original files until the reconstructed MVP is verified.

## KEEP

| Item | Technical reason |
|---|---|
| FastAPI router/service/schema separation | Clear responsibilities, tested behavior, and a stable response envelope |
| `core/exceptions.py`, `core/response.py`, `core/logging.py` | Consistent errors and logging already covered by tests |
| data.gov.my services | Live, keyless official Malaysian data integration is directly relevant |
| Pydantic query models | Provide bounded validation and OpenAPI documentation |
| Existing tests | 12-test regression baseline protects current integrations |
| Non-root Docker pattern | Good production security baseline |
| `.env.example` / `.gitignore` approach | Secrets are externalized and ignored |

## IMPROVE

| Item | Required improvement |
|---|---|
| `app.py` | GeoRich naming, static frontend directory, `/api/health`, security headers, new routers |
| `config.py` | Safe production CORS defaults, Open-Meteo/Nominatim/database settings, environment validation |
| `requirements.txt` | Add only used SQLAlchemy/GeoAlchemy/PostGIS-related and geometry dependencies |
| Dockerfile | Align with Python 3.11 target and copy a cleaner project surface |
| Dashboard visual language | Retain the professional dark risk-intelligence character, but reduce density to four KPIs and real controls |
| Live feed/error handling | Turn feed failures into explicit stale/degraded states with timestamps |
| data.gov.my client | Add cache/fallback boundaries and do not make the whole dashboard depend on a single upstream request |

## REPLACE

| Item | Technical reason |
|---|---|
| Leaflet map block | No analytical Leaflet work exists; MapLibre GL JS is required and migration is isolated |
| Single-file `dashboard.html` | Mixed presentation/data/network code is hard to maintain and test |
| Hard-coded KPI/chart content | Misrepresents demo data as live intelligence |
| Placeholder navigation, report, AI chat and security panels | Non-functional controls and unverified claims violate MVP rules |
| `innerHTML`-driven live rendering | Avoidable XSS surface; use safe DOM/text APIs |
| CARTO-only raster basemap | Use a documented, token-free MapLibre style with at most two basemaps |

## REMOVE LATER

These items are quarantined by documentation only; do not delete them until the new app is stable:

- `sprint-01-dashboard/` duplicated backend snapshot
- `gemini-code-1783280882863.html`
- `gemini-code-1783282168985.html`
- `georisk-malaysia-backend-sprint2.zip`
- `Codex Installer.exe`
- `Microsoft.Services.Store.winmd`
- empty nested `GeoRisk-Malaysia/` scaffold
- root `venv/`, caches and logs from any future distributable artefact

## Reference reuse decision

The green React/Vite dashboard is not copied because it introduces React and retains Leaflet. Only its conceptual patterns—error boundaries, explicit layer configuration, and responsive panel behavior—inform the new vanilla JavaScript implementation.

