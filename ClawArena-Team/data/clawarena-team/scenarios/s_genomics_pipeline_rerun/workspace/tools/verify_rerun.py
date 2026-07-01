#!/usr/bin/env python3
"""Compute COMPLIANCE_TOKEN for audit/rerun_plan.json.

Usage: python tools/verify_rerun.py audit/rerun_plan.json

The token is sha256 over canonical key=value pipe-joined string:
  pipeline | ref_genome | decision | samples_to_rerun |
  failed_samples_excluded | analyst | plan_date
Printed as: COMPLIANCE_TOKEN:<hex>
"""
import hashlib
import json
import sys

KEYS = [
    "pipeline",
    "ref_genome",
    "decision",
    "samples_to_rerun",
    "failed_samples_excluded",
    "analyst",
    "plan_date",
]


def compute(payload: dict) -> str:
    parts = [f"{k}={payload.get(k, '')}" for k in KEYS]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_rerun.py audit/rerun_plan.json", file=sys.stderr)
        return 2
    payload = json.loads(open(sys.argv[1], encoding="utf-8").read())
    print(f"COMPLIANCE_TOKEN:{compute(payload)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
