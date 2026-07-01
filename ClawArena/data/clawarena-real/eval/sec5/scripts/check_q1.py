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
    data, err = _load_json(ws / "output" / "q1_fields.json")
    if err: _finish([err])

    # Layer 1: structure — schema_version silently checked (E-rule: no reminder in question)
    if data.get("schema_version") != "1.0":
        fails.append(f"schema_version={data.get('schema_version')!r} must be '1.0' (session-wide requirement)")

    for k in ("total_transactions", "fraud_count", "fraud_rate", "features", "class_values", "doi"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    # Layer 2: field types
    if not isinstance(data.get("features"), list):
        fails.append("features must be a list")
    if not isinstance(data.get("class_values"), list):
        fails.append("class_values must be a list")

    # Layer 3: true values
    if data.get("total_transactions") != 284807:
        fails.append(f"total_transactions={data.get('total_transactions')} (expected 284807)")
    if data.get("fraud_count") != 492:
        fails.append(f"fraud_count={data.get('fraud_count')} (expected 492)")
    rate = float(data.get("fraud_rate", 0))
    if abs(rate - 0.00172) > 0.00001:
        fails.append(f"fraud_rate={rate:.6f} (expected exactly 0.00172, tolerance ±0.00001)")

    # Verbatim V1-V28 features present
    feats = [str(f) for f in (data.get("features") or [])]
    for vi in range(1, 29):
        fname = f"V{vi}"
        if fname not in feats:
            fails.append(f"features missing verbatim field {fname!r}")
    for must in ("Time", "Amount", "Class"):
        if must not in feats:
            fails.append(f"features missing {must!r}")

    # Exact feature count: V1-V28 (28) + Time + Amount + Class = 31
    if len(feats) != 31:
        fails.append(f"features list must have exactly 31 elements (V1-V28 + Time + Amount + Class), got {len(feats)}")

    # class_values must contain exactly [0, 1] (integers, not strings)
    cv = data.get("class_values") or []
    if set(cv) != {0, 1} or len(cv) != 2:
        fails.append(f"class_values must be exactly [0, 1] (two integer values), got {cv!r}")

    # DOI must be exactly "10.1016/j.eswa.2014.02.026" (exact match, not substring)
    doi = str(data.get("doi", ""))
    if doi != "10.1016/j.eswa.2014.02.026":
        fails.append(f"doi must be exactly '10.1016/j.eswa.2014.02.026', got {doi!r}")

    # source_url must reference the Kaggle dataset (F-rule: verbatim source citation)
    su = str(data.get("source_url", "")).strip()
    if not su:
        fails.append("source_url is missing — must cite the Kaggle dataset URL from README")
    elif "kaggle" not in su.lower():
        fails.append(f"source_url={su!r} must reference the Kaggle dataset (from README_datasets.md)")

    _finish(fails)
main()
