#!/usr/bin/env python3
"""Compute COMPLIANCE_TOKEN for a maintenance_ticket.json file.

Usage: python tools/verify_decision.py audit/maintenance_ticket.json

The token is sha256 over canonical key=value lines of:
  decision | alarm_code | robot_id | root_cause | dispatcher | ticket_date
"""
import hashlib
import json
import sys

KEYS = ["decision", "alarm_code", "robot_id", "root_cause", "dispatcher", "ticket_date"]


def compute(payload: dict) -> str:
    parts = [f"{k}={payload.get(k, '')}" for k in KEYS]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_decision.py audit/maintenance_ticket.json", file=sys.stderr)
        return 2
    payload = json.loads(open(sys.argv[1], encoding="utf-8").read())
    print(f"COMPLIANCE_TOKEN:{compute(payload)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
