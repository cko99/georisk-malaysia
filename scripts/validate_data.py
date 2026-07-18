"""Validate the small GeoJSON fallback without requiring desktop GIS software."""

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    data = json.loads(args.path.read_text(encoding="utf-8"))
    if data.get("type") != "FeatureCollection" or not isinstance(data.get("features"), list):
        raise SystemExit("Invalid GeoJSON FeatureCollection")
    for index, feature in enumerate(data["features"]):
        if feature.get("type") != "Feature" or "geometry" not in feature or "properties" not in feature:
            raise SystemExit(f"Invalid feature at index {index}")
    metadata = data.get("metadata", {})
    for required in ("source", "crs", "licence"):
        if not metadata.get(required):
            raise SystemExit(f"Missing metadata.{required}")
    print(f"valid features={len(data['features'])} crs={metadata['crs']}")


if __name__ == "__main__":
    main()
