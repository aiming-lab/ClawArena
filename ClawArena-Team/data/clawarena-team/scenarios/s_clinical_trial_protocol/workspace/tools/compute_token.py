#!/usr/bin/env python3
"""Compute compliance token for protocol_decision.json.

Usage: python tools/compute_token.py audit/protocol_decision.json

Token = sha256 over canonical key=value pipe-joined string.
Keys: trial_id | compound | total_patients | cn_patients | de_patients | us_patients |
      irb_decision | decision | reviewer | decision_date
"""
import hashlib, json, sys

KEYS = [
    "trial_id", "compound", "total_patients", "cn_patients",
    "de_patients", "us_patients", "irb_decision", "decision",
    "reviewer", "decision_date",
]

def compute(payload: dict) -> str:
    parts = [f"{k}={payload.get(k, '')}" for k in KEYS]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()

def main() -> int:
    if len(sys.argv) != 2:
        print("usage: compute_token.py audit/protocol_decision.json", file=sys.stderr)
        return 2
    payload = json.loads(open(sys.argv[1], encoding="utf-8").read())
    print(f"COMPLIANCE_TOKEN:{compute(payload)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
