# Limitations

- Administrative, road and river fallback geometries are deliberately generalised portfolio samples, not authoritative cartography.
- Hazard points are synthetic. They demonstrate workflows and are not current incidents.
- Proximity uses a local equirectangular approximation suitable for the small preset radii and demo scale. Operational use should query PostGIS geography with `ST_DWithin`/`ST_Distance`.
- The PostGIS schema, spatial index and loader are available, but the default API truthfully reports `demo-fallback` until a database query adapter is implemented and enabled.
- data.gov.my and public OSM/Open-Meteo services can throttle, time out or change. The dashboard reports degraded states but does not persist a cache across restarts.
- Esri Satellite/Hybrid and the standard OSM raster basemap are external best-effort services subject to their provider terms and attribution. Google Earth imagery is not scraped or embedded because Google requires authorized API access and billing for production.
- Nominatim public search is submission-based, not autocomplete, and should remain low volume.
- Chart data are synthetic and visibly labelled DEMO.
- No public URL was created because deployment needs a user-owned repository and hosting account.
