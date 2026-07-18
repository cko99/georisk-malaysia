CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS spatial_features (
    id BIGSERIAL PRIMARY KEY,
    external_id TEXT,
    layer_name TEXT NOT NULL CHECK (layer_name IN ('administrative', 'roads', 'rivers', 'hazards')),
    feature_name TEXT,
    properties JSONB NOT NULL DEFAULT '{}'::jsonb,
    source_name TEXT NOT NULL,
    source_licence TEXT,
    observed_at TIMESTAMPTZ,
    geom geometry(Geometry, 4326) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (layer_name, external_id)
);
