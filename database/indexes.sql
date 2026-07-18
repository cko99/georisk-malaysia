CREATE INDEX IF NOT EXISTS spatial_features_geom_gix ON spatial_features USING GIST (geom);
CREATE INDEX IF NOT EXISTS spatial_features_layer_idx ON spatial_features (layer_name);
CREATE INDEX IF NOT EXISTS spatial_features_observed_idx ON spatial_features (observed_at DESC);
