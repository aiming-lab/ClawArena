#!/usr/bin/env python3
"""verify_dispute_signoff.py — wave3 版：解析 decision_fields.csv，输出 COMPLIANCE_CHECK token。

Usage:
    python tools/verify_dispute_signoff.py output/decision_fields.csv

CSV 格式：
  第 1 行（header）：pursue_representment,replacement_offered,fraud_score,policy_applied,sla_hours
  第 2 行（values）：false,true,0.71,fraud_score>0.62 AND total<2500,48

The tool validates required fields and emits a deterministic token.
check_q5 will verify the same token appears in both output documents.
"""
from __future__ import annotations

import csv
import hashlib
import re
import sys
from pathlib import Path

REQUIRED_FIELDS = [
    "pursue_representment",
    "replacement_offered",
    "fraud_score",
    "policy_applied",
    "sla_hours",
]

def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_dispute_signoff.py <decision_fields.csv>", file=sys.stderr)
        return 2
    p = Path(sys.argv[1])
    if not p.exists():
        print(f"file not found: {p}", file=sys.stderr)
        return 2

    try:
        text = p.read_text(encoding="utf-8")
    except Exception as e:
        print(f"cannot read file: {e}", file=sys.stderr)
        return 2

    lines = [l for l in text.splitlines() if l.strip()]
    if len(lines) < 2:
        print("CSV must have at least 2 rows (header + values)", file=sys.stderr)
        return 2

    try:
        reader = csv.DictReader(lines)
        rows = list(reader)
    except Exception as e:
        print(f"CSV parse error: {e}", file=sys.stderr)
        return 2

    if not rows:
        print("CSV values row missing", file=sys.stderr)
        return 2

    row = rows[0]
    # Normalise keys (lower, strip)
    row_norm = {k.strip().lower(): v.strip() for k, v in row.items()}

    missing = [f for f in REQUIRED_FIELDS if f not in row_norm]
    if missing:
        print(f"CSV missing required fields: {missing}", file=sys.stderr)
        return 2

    # Emit token from normalised CSV content
    canonical = ",".join(f"{f}={row_norm[f]}" for f in REQUIRED_FIELDS)
    digest = hashlib.sha256(normalise(canonical).encode("utf-8")).hexdigest()[:32]
    print(f"COMPLIANCE_CHECK: {digest}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
