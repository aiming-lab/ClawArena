#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, subprocess
from pathlib import Path
from datetime import date, timedelta

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON in " + p.name + ": " + str(e)

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q2_stats.json")
    if err: _finish([err])

    # E-rule: schema_version silently checked
    if data.get("schema_version") != "1.0":
        fails.append(f"schema_version={data.get('schema_version')!r} must be '1.0'")

    for k in ("total_transactions", "fraud_count", "fraud_rate", "non_fraud_count"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    if data.get("total_transactions") != 284807:
        fails.append(f"total_transactions={data.get('total_transactions')} (expected 284807)")
    if data.get("fraud_count") != 492:
        fails.append(f"fraud_count={data.get('fraud_count')} (expected 492)")

    rate = float(data.get("fraud_rate", 0))
    if abs(rate - 0.00172) > 0.00001:
        fails.append(f"fraud_rate={rate:.6f} (expected exactly 0.00172, tolerance ±0.00001)")

    non_fraud = data.get("non_fraud_count", 0)
    if non_fraud != 284315:
        fails.append(f"non_fraud_count={non_fraud} (expected exactly 284315 = 284807 - 492)")

    total = data.get("total_transactions", 0)
    fraud = data.get("fraud_count", 0)
    if isinstance(total, int) and isinstance(fraud, int) and isinstance(non_fraud, int):
        if fraud + non_fraud != total:
            fails.append(f"closure failed: fraud({fraud}) + non_fraud({non_fraud}) != total({total})")
    else:
        fails.append("total_transactions/fraud_count/non_fraud_count must be integers")

    _finish(fails)
main()
