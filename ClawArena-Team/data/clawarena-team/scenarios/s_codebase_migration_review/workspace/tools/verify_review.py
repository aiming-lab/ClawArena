#!/usr/bin/env python3
"""Compute COMPLIANCE_TOKEN for a final_review.json file.

Usage: python tools/verify_review.py audit/final_review.json

Token is sha256 over the canonical key=value lines of:
  decision | services | risks | coverage_gap | rpc_diff_count
Token is printed as COMPLIANCE_TOKEN:<hex>.
"""
import hashlib
import json
import sys

KEYS = ["decision", "services", "risks", "coverage_gap", "rpc_diff_count"]


def compute(payload: dict) -> str:
    parts = []
    for k in KEYS:
        v = payload.get(k, "")
        if isinstance(v, (list, dict)):
            v = json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        parts.append(f"{k}={v}")
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_review.py audit/final_review.json", file=sys.stderr)
        return 2
    payload = json.loads(open(sys.argv[1], encoding="utf-8").read())
    print(f"COMPLIANCE_TOKEN:{compute(payload)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
