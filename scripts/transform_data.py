"""Normalize GeoJSON properties and preserve source metadata."""

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("--layer", required=True, choices=["administrative", "roads", "rivers", "hazards"])
    args = parser.parse_args()
    data = json.loads(args.source.read_text(encoding="utf-8"))
    for index, feature in enumerate(data.get("features", []), start=1):
        properties = feature.setdefault("properties", {})
        properties.setdefault("id", f"{args.layer.upper()}-{index:04d}")
        properties["layer_name"] = args.layer
    args.target.parent.mkdir(parents=True, exist_ok=True)
    args.target.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(args.target)


if __name__ == "__main__":
    main()
