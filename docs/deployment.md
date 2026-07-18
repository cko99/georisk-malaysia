# Zero-Cost Deployment

## Local Docker deployment

```powershell
docker compose up --build
```

Open `http://localhost:8000`. PostGIS starts alongside the API, but the UI remains usable through the demo fallback if the database is unavailable.

## Render free web service

`render.yaml` defines one Docker web service with `/api/health`. As of 18 July 2026, Render documents free web services for hobby/testing use, with important limits: idle spin-down after 15 minutes, roughly one-minute cold start, monthly usage limits and ephemeral local files. No payment method is required for the documented free path; exceeded allowance suspends service when no payment method is attached.

Deployment requires a GitHub/GitLab/Bitbucket repository and the user's Render account:

1. Push this folder to a repository.
2. In Render, create a Blueprint or Docker Web Service from the repo.
3. Select the Free instance.
4. Set `CORS_ORIGINS=https://<service>.onrender.com`.
5. Verify `/api/health`, `/`, location search and a proximity request.

Do not add a Render free Postgres database for durable portfolio data: current free databases expire after 30 days. Use the app's demo fallback, local PostGIS, or a separately managed free PostGIS service with explicit lifecycle monitoring.

## Optional Supabase PostGIS

Supabase can provide hosted PostgreSQL/PostGIS. Use a backend-only pooler connection string in `DATABASE_URL`; never expose it to the browser. Confirm current free-plan limits before creating a project.

## CI

`.github/workflows/test.yml` installs Python 3.11 dependencies, runs all tests and validates every sample GeoJSON file. It does not deploy automatically, preventing accidental external changes.

## Public deployment status

Version 1 is deployed from the public `cko99/georisk-malaysia` repository through the `georich-ai-v1` Render Blueprint:

- Application: <https://georich-ai.onrender.com>
- API documentation: <https://georich-ai.onrender.com/docs>
- Health check: <https://georich-ai.onrender.com/api/health>

The production root page, health endpoint, GeoJSON layer, weather endpoint, proximity analysis, Satellite tiles and OpenStreetMap tiles were verified after the first deployment.
