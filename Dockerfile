# ==============================================================
# GeoRich AI — Production Dockerfile
# Multi-stage build: slim runtime image, non-root user, no dev deps.
# ==============================================================

FROM python:3.11-slim AS builder

WORKDIR /build

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.11-slim AS runtime

LABEL maintainer="GeoRich AI" \
      org.opencontainers.image.title="GeoRich AI" \
      org.opencontainers.image.description="Open-source geospatial risk intelligence for Malaysia" \
      org.opencontainers.image.version="0.2.0"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

COPY --from=builder /install /usr/local

COPY . .

RUN groupadd --system georich && \
    useradd --system --gid georich --no-create-home georich && \
    mkdir -p /app/logs && \
    chown -R georich:georich /app

USER georich

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
