"""Load validated GeoJSON into PostGIS using parameterized SQL."""

import argparse
import json
import os
from pathlib import Path

from sqlalchemy import create_engine, text

SQL = text("""
INSERT INTO spatial_features
    (external_id, layer_name, feature_name, properties, source_name, source_licence, observed_at, geom)
VALUES
    (:external_id, :layer_name, :feature_name, CAST(:properties AS jsonb), :source_name, :source_licence,
     :observed_at, ST_SetSRID(ST_GeomFromGeoJSON(:geometry), 4326))
ON CONFLICT (layer_name, external_id) DO UPDATE SET
    feature_name = EXCLUDED.feature_name,
    properties = EXCLUDED.properties,
    observed_at = EXCLUDED.observed_at,
    geom = EXCLUDED.geom;
""")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--layer", required=True, choices=["administrative", "roads", "rivers", "hazards"])
    args = parser.parse_args()
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise SystemExit("DATABASE_URL is required")
    collection = json.loads(args.path.read_text(encoding="utf-8"))
    metadata = collection.get("metadata", {})
    engine = create_engine(database_url)
    with engine.begin() as connection:
        for index, feature in enumerate(collection["features"], start=1):
            props = feature.get("properties", {})
            connection.execute(SQL, {
                "external_id": str(props.get("id", f"{args.layer}-{index}")),
                "layer_name": args.layer,
                "feature_name": props.get("name") or props.get("hazard"),
                "properties": json.dumps(props),
                "source_name": metadata.get("source", "unknown"),
                "source_licence": metadata.get("licence"),
                "observed_at": props.get("observed"),
                "geometry": json.dumps(feature["geometry"]),
            })
    print(f"loaded {len(collection['features'])} features")


if __name__ == "__main__":
    main()
