INSERT INTO spatial_features (external_id, layer_name, feature_name, properties, source_name, source_licence, observed_at, geom)
VALUES (
    'HZ-SEED-KL',
    'hazards',
    'Synthetic Kuala Lumpur flood record',
    '{"hazard":"Flood","severity":"moderate","synthetic":true}'::jsonb,
    'GeoRich AI synthetic seed',
    'CC0',
    '2026-07-16T00:00:00Z',
    ST_SetSRID(ST_MakePoint(101.61, 3.06), 4326)
)
ON CONFLICT (layer_name, external_id) DO NOTHING;
