# GeoRich AI MVP Gap Analysis

Priority: P0 = required to run, P1 = required for MVP, P2 = strong portfolio value, P3 = later.

| Requirement | Existing Status | Gap | Action | Priority |
|---|---|---|---|---|
| MapLibre GL JS map | Leaflet basemap only | Wrong engine | Replace isolated map implementation | P0 |
| Malaysia initial extent | Approximate Leaflet center | No documented bounds | Configure Malaysia center, bounds and sensible zoom | P0 |
| Layer control | None | No operational toggles | Add five-layer maximum control | P1 |
| Administrative boundary | None | No boundary source | Add attributed WGS84 boundary/source | P1 |
| Roads | Basemap pixels only | Not independently controllable | Expose/map a roads layer | P1 |
| Rivers | Basemap pixels only | Not independently controllable | Expose/map a rivers layer | P1 |
| Weather API | data.gov.my forecast exists | No coordinate current weather | Add keyless Open-Meteo proxy and retain official forecast | P1 |
| Warning API | Working data.gov.my route | UI is incomplete | Normalize status, timestamps and degraded state | P1 |
| Location search | Decorative field | No geocoder or results | Add rate-limited Nominatim proxy/search UI | P1 |
| Coordinate search | None | Missing validation/fly-to | Add lat/lon parser and marker | P1 |
| Popup | None | Missing feature details | Add safe popup content | P1 |
| Legend | None | Missing symbology explanation | Add dynamic legend from active layers | P1 |
| Proximity analysis | None | No radius/layer query | Add 500 m/1/3/5 km endpoint with demo/PostGIS path | P1 |
| Automated insight | Static fake AI chat | No real rules | Add deterministic rule-based summary | P1 |
| Dashboard KPI | Six mostly hard-coded KPIs | Wrong count/meaning | Reduce to active layers, warnings, nearby hazards, rainfall | P1 |
| Charts | Two hard-coded charts | Not source-backed | Add at most three small source-labelled charts; MVP can start with two | P2 |
| Responsive mobile | Desktop-only | No drawer/bottom sheet | Implement drawer, backdrop and analysis sheet | P1 |
| FastAPI backend | Working | Needs new endpoints and names | Extend, do not rewrite | P0 |
| PostgreSQL/PostGIS | Absent | No persistence/spatial index | Add Compose/schema/index and optional runtime adapter | P2 |
| Demo fallback | Absent | App fails without DB/spatial API | Add labelled local GeoJSON fallback | P1 |
| ETL | Absent | No reproducible data process | Add fetch/validate/transform/load scripts | P2 |
| Error handling | Backend good, frontend partial | No unified loading/offline states | Add safe frontend state model | P1 |
| Security | CORS `*`, `innerHTML`, false claims | Production risk | Restrict config, security headers, safe DOM and documentation | P1 |
| Testing | 12 backend tests | No spatial/weather-current/search/frontend smoke tests | Add route/unit/static smoke tests | P1 |
| Docker | Backend Dockerfile only | No PostGIS/local orchestration | Add Compose and health checks | P2 |
| Deployment | Documentation only | No deploy skeleton/live URL | Add zero-cost manifests/workflow guidance; live publish needs provider access | P2 |
| Documentation | Sprint 2 README only | Missing GeoRich docs | Add architecture, data sources, security, deployment and limitations | P1 |

## MVP implementation boundary

The first stable release will expose no more than five overlays: administrative boundaries, major roads, rivers, weather/warnings, and hazard/incidents. It will show at most two basemaps, four KPIs, and three charts. Any fallback data will be visibly labelled as demo data.

