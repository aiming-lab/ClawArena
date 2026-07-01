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
    data, err = _load_json(ws / "output" / "q3_paysim_meta.json")
    if err: _finish([err])

    for k in ("transaction_types", "isFlaggedFraud_threshold", "simulation_steps",
               "fraud_rate", "sample_case_id"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    ttypes = [str(t) for t in (data.get("transaction_types") or [])]
    REQUIRED_TYPES = ["CASH-IN", "CASH-OUT", "DEBIT", "PAYMENT", "TRANSFER"]
    for need in REQUIRED_TYPES:
        if need not in ttypes:
            fails.append(f"transaction_types missing verbatim value {need!r}")
    if len(ttypes) != 5:
        fails.append(f"transaction_types must have exactly 5 entries (got {len(ttypes)}): {REQUIRED_TYPES}")

    if int(data.get("isFlaggedFraud_threshold", 0)) != 200000:
        fails.append(f"isFlaggedFraud_threshold={data.get('isFlaggedFraud_threshold')} (expected 200000)")

    if int(data.get("simulation_steps", 0)) != 744:
        fails.append(f"simulation_steps={data.get('simulation_steps')} (expected 744)")

    fr = float(data.get("fraud_rate", 0))
    if abs(fr - 0.00129) > 0.00001:
        fails.append(f"fraud_rate={fr:.6f} (expected exactly 0.00129 per README, tolerance ±0.00001)")

    cid = str(data.get("sample_case_id", ""))
    if cid != "CASE-20260310-001":
        fails.append(f"sample_case_id must be exactly 'CASE-20260310-001' (got {cid!r})")

    _finish(fails)
main()
