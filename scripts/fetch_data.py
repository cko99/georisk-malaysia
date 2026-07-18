"""Fetch a bounded open-data response into data/raw for reproducible review."""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import requests

ENDPOINTS = {
    "forecast": "https://api.data.gov.my/weather/forecast?limit=100",
    "warning": "https://api.data.gov.my/weather/warning",
    "earthquake": "https://api.data.gov.my/weather/warning/earthquake",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", choices=ENDPOINTS)
    args = parser.parse_args()
    response = requests.get(ENDPOINTS[args.dataset], timeout=20, headers={"User-Agent": "GeoRich-AI-ETL/0.2"})
    response.raise_for_status()
    target = Path("data/raw")
    target.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = target / f"{args.dataset}_{stamp}.json"
    output.write_text(json.dumps(response.json(), ensure_ascii=False, indent=2), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
