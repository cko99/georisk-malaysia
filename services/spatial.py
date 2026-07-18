"""Dependency-free WGS84 proximity fallback for the small demo GeoJSON layers."""

import json
import math
from pathlib import Path
from typing import Any

_data_dir = Path(__file__).resolve().parents[1] / "data" / "sample"
_earth_radius_m = 6_371_008.8


def _xy(coord: list[float], latitude: float, longitude: float) -> tuple[float, float]:
    x = math.radians(coord[0] - longitude) * _earth_radius_m * math.cos(math.radians(latitude))
    y = math.radians(coord[1] - latitude) * _earth_radius_m
    return x, y


def _point_distance(coord: list[float], latitude: float, longitude: float) -> float:
    x, y = _xy(coord, latitude, longitude)
    return math.hypot(x, y)


def _segment_distance(a: list[float], b: list[float], latitude: float, longitude: float) -> float:
    ax, ay = _xy(a, latitude, longitude)
    bx, by = _xy(b, latitude, longitude)
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.hypot(ax, ay)
    t = max(0.0, min(1.0, -(ax * dx + ay * dy) / (dx * dx + dy * dy)))
    return math.hypot(ax + t * dx, ay + t * dy)


def _geometry_distance(geometry: dict[str, Any], latitude: float, longitude: float) -> float:
    if geometry["type"] == "Point":
        return _point_distance(geometry["coordinates"], latitude, longitude)
    coords = geometry["coordinates"]
    return min(_segment_distance(coords[i], coords[i + 1], latitude, longitude) for i in range(len(coords) - 1))


def analyze_proximity(latitude: float, longitude: float, radius_m: int, layer: str) -> dict[str, Any]:
    collection = json.loads((_data_dir / f"{layer}.geojson").read_text(encoding="utf-8"))
    ranked = []
    for feature in collection["features"]:
        distance = round(_geometry_distance(feature["geometry"], latitude, longitude), 1)
        result = {**feature, "properties": {**feature["properties"], "distance_m": distance}}
        ranked.append((distance, result))
    ranked.sort(key=lambda item: item[0])
    within = [feature for distance, feature in ranked if distance <= radius_m]
    nearest = ranked[0][1] if ranked else None
    count = len(within)
    label = {"hazards": "hazard record", "roads": "mapped road", "rivers": "mapped river"}[layer]
    if nearest:
        distance_text = f"{nearest['properties']['distance_m'] / 1000:.1f} km" if nearest["properties"]["distance_m"] >= 1000 else f"{nearest['properties']['distance_m']:.0f} m"
        insight = f"The nearest {label} in the demo fallback is {distance_text} away. {count} feature(s) fall within the selected radius."
    else:
        insight = f"No {label} is available in the demo fallback."
    return {
        "count": count,
        "nearest": nearest,
        "result_geojson": {"type": "FeatureCollection", "features": within},
        "insight": insight,
        "mode": "demo-fallback",
        "disclaimer": "Generalised portfolio sample; not suitable for operational decisions.",
    }
