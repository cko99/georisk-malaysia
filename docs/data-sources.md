# Data Sources

Reviewed 18 July 2026. PasarAPI was not required because original provider documentation was available.

| Provider | Dataset / endpoint | Format | Key / cost | Update / reliability | Licence and attribution |
|---|---|---|---|---|---|
| Government of Malaysia, data.gov.my | `GET https://api.data.gov.my/weather/forecast` | JSON list | No key; RM0 | Official high-use endpoint; returned HTTP 200 in audit | Public-sector open data; display `data.gov.my` |
| Government of Malaysia, data.gov.my | `GET https://api.data.gov.my/weather/warning` | JSON list | No key; RM0 | Active warning records; returned HTTP 200 | Display `data.gov.my` and Government of Malaysia |
| Government of Malaysia, data.gov.my | `GET https://api.data.gov.my/weather/warning/earthquake` | JSON list | No key; RM0 | Can be slow; one audit request timed out | Display `data.gov.my` and Government of Malaysia |
| Open-Meteo | `GET https://api.open-meteo.com/v1/forecast` | JSON | No key on public endpoint; RM0 for evaluation/prototyping | Model-dependent, continuously updated forecast | Weather data CC BY 4.0; link to Open-Meteo beside displayed data |
| OpenStreetMap Nominatim | `GET https://nominatim.openstreetmap.org/search` | GeoJSON | No key | Maximum 1 request/second on public service; valid User-Agent and attribution required | OSM data ODbL 1.0; credit OpenStreetMap contributors |
| OpenStreetMap standard raster tiles | `https://tile.openstreetmap.org/{z}/{x}/{y}.png`, relayed by `/api/basemaps/osm/{z}/{x}/{y}` | PNG tiles | No key; best effort | Street basemap; browser/server caching and tile policy apply | ODbL attribution in the map control |
| Esri ArcGIS Online | World Imagery + reference transportation/boundary tiles, relayed by the allowlisted `/api/basemaps/*` routes | JPEG/PNG tiles | No key in current public services | Satellite and Hybrid basemaps; service availability is external | Display `Tiles © Esri` and imagery contributor attribution |
| GeoRich AI sample | `/api/layers/{name}` | GeoJSON, EPSG:4326 | Local | Always available | Administrative/road/river geometry is generalised demo material; hazards are synthetic CC0 records |

## Public service safeguards

- Place search only occurs on form submission, is limited to five Malaysian results, and is proxied with an identifying User-Agent.
- No autocomplete request loop is used, respecting the Nominatim policy.
- External calls have bounded timeouts and report degraded states.
- OSM tiles are never bulk-downloaded or used for offline prefetch.
- The basemap relay accepts only four fixed providers and valid slippy-map coordinates; callers cannot supply an arbitrary upstream URL.
- All operational cards distinguish official live feeds from generalised/synthetic samples.

## References

- data.gov.my weather documentation: <https://developer.data.gov.my/realtime-api/weather>
- Open-Meteo forecast documentation: <https://open-meteo.com/en/docs>
- Open-Meteo licence: <https://open-meteo.com/en/license>
- Nominatim usage policy: <https://operations.osmfoundation.org/policies/nominatim/>
- OpenStreetMap copyright: <https://www.openstreetmap.org/copyright>
- OSM tile usage policy: <https://operations.osmfoundation.org/policies/tiles/>
- ArcGIS basemap layers: <https://developers.arcgis.com/documentation/mapping-and-location-services/mapping/basemap-layers/>
- MapLibre GL JS: <https://maplibre.org/maplibre-gl-js/docs/>
