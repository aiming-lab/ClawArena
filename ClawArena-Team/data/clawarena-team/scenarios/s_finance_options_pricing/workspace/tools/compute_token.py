#!/usr/bin/env python3
"""compute_token.py — produce a compliance sha256 for the final decision JSON.

Usage:
    python tools/compute_token.py audit/model_decision.json

Prints: COMPLIANCE_TOKEN:<hex>

Token is sha256 over canonical "key=value|key=value|..." string of the
following fields (in order):
  decision | mc_estimate | bs_reference | model_name |
  var_95 | reviewer | decision_date
"""
import hashlib
import json
import sys

KEYS = [
    "decision", "mc_estimate", "bs_reference", "model_name",
    "var_95", "reviewer", "decision_date",
]


def compute(payload: dict) -> str:
    parts = [f"{k}={payload.get(k, '')}" for k in KEYS]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: compute_token.py audit/model_decision.json", file=sys.stderr)
        return 2
    payload = json.loads(open(sys.argv[1], encoding="utf-8").read())
    print(f"COMPLIANCE_TOKEN:{compute(payload)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
