# Security

## Implemented controls

- No API key or database credential is embedded in frontend code.
- `.env`, venvs, caches and logs are ignored.
- Production origins are configured through `CORS_ORIGINS`; the default permits only the two local development origins.
- Request inputs have Pydantic bounds. Proximity radius and layer are allowlisted.
- Layer paths are allowlisted and cannot traverse the filesystem.
- External calls use fixed provider base URLs, bounded timeouts and an identifying User-Agent.
- The same-origin tile relay is provider-allowlisted, validates zoom/x/y bounds and never accepts a caller-controlled upstream URL.
- Frontend result rendering uses text nodes/`textContent`; popup values are built with DOM nodes rather than HTML interpolation.
- PostGIS loading uses SQLAlchemy bind parameters; geometry is parsed by PostGIS from a parameter.
- Responses set `nosniff`, frame denial, referrer policy and a restrictive geolocation permissions policy.
- The container runs as a non-root system user.

## Deployment requirements

- Set `ENVIRONMENT=production`, `DEBUG=false`, and an exact HTTPS `CORS_ORIGINS` value.
- Store `DATABASE_URL` only in the host's secret/environment manager.
- Terminate HTTPS at the hosting provider and never claim end-to-end encryption that is not verified.
- Review dependency/CDN versions regularly. A strict CSP should be added after either self-hosting the frontend libraries or calculating/maintaining valid integrity metadata.
- Rate-limit public proxy routes at the platform or reverse proxy for a higher-traffic deployment.
- Do not use sample layers for emergency response, navigation, engineering or insurance decisions.

## Secret audit

No committed `.env`, password, API key, private database URL or token was found. Example development credentials in Compose are local-only and must not be reused on a public database.
