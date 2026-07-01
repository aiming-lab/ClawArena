#!/usr/bin/env python3
"""Compute COMPLIANCE_TOKEN for a final_decision.json file.

Usage: python tools/verify_decision.py audit/final_decision.json

The token is sha256 over the canonical key=value lines of:
  decision | v3_mean | v4_mean | delta | failed_test_name | failed_test_line |
  reward_variance | reviewer | decision_date
The token's hex prefix is printed as `COMPLIANCE_TOKEN:<hex>`.
"""
import hashlib
import json
import sys


KEYS = [
    "decision", "v3_mean", "v4_mean", "delta",
    "failed_test_name", "failed_test_line",
    "reward_variance", "reviewer", "decision_date",
]


def compute(payload: dict) -> str:
    parts = []
    for k in KEYS:
        v = payload.get(k, "")
        parts.append(f"{k}={v}")
    canonical = "|".join(parts)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_decision.py audit/final_decision.json", file=sys.stderr)
        return 2
    payload = json.loads(open(sys.argv[1], encoding="utf-8").read())
    print(f"COMPLIANCE_TOKEN:{compute(payload)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
