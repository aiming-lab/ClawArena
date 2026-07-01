#!/usr/bin/env python3
"""Compute COMPLIANCE_TOKEN for audit/postmortem.json.

Usage: python tools/verify_postmortem.py audit/postmortem.json

The token is sha256 over canonical key=value lines for:
  decision | root_cause | service | spike_time | action_items | reviewer | postmortem_date
printed as: COMPLIANCE_TOKEN:<hex>
"""
import hashlib
import json
import sys

KEYS = [
    "decision", "root_cause", "service",
    "spike_time", "action_items", "reviewer", "postmortem_date",
]


def compute(payload: dict) -> str:
    parts = []
    for k in KEYS:
        v = payload.get(k, "")
        if isinstance(v, list):
            v = ",".join(str(x) for x in v)
        parts.append(f"{k}={v}")
    canonical = "|".join(parts)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_postmortem.py audit/postmortem.json", file=sys.stderr)
        return 2
    payload = json.loads(open(sys.argv[1], encoding="utf-8").read())
    print(f"COMPLIANCE_TOKEN:{compute(payload)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
