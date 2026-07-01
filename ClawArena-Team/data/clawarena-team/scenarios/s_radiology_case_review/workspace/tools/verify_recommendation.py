#!/usr/bin/env python3
"""Compute COMPLIANCE_TOKEN for audit/recommendation.json.

Usage: python tools/verify_recommendation.py audit/recommendation.json

The token is sha256 over canonical key=value lines for the fields:
  decision | lesion_size_mm | lobe | urgency | roi_x | roi_y |
  reviewer | decision_date
Output: COMPLIANCE_TOKEN:<hex>
"""
import hashlib
import json
import sys

KEYS = [
    "decision", "lesion_size_mm", "lobe", "urgency",
    "roi_x", "roi_y", "reviewer", "decision_date",
]


def compute(payload: dict) -> str:
    parts = [f"{k}={payload.get(k, '')}" for k in KEYS]
    canonical = "|".join(parts)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_recommendation.py audit/recommendation.json", file=sys.stderr)
        return 2
    payload = json.loads(open(sys.argv[1], encoding="utf-8").read())
    print(f"COMPLIANCE_TOKEN:{compute(payload)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
