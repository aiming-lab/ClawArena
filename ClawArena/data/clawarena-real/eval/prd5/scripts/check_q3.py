#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, math
from pathlib import Path

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON: " + str(e)

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
    data, err = _load_json(ws / "output" / "q3_cuped_audit.json")
    if err: _finish([err])
    for key in ("reported_theta", "correct_theta", "error_pct", "formula_source"):
        if key not in data:
            fails.append("missing key: %s" % key)
    if fails: _finish(fails)
    try:
        rt = float(data["reported_theta"])
        ct = float(data["correct_theta"])
        ep = float(data["error_pct"])
    except (TypeError, ValueError) as e:
        _finish(["non-numeric field: %s" % e])
    # reported_theta must be 0.31
    if not (0.29 <= rt <= 0.33):
        fails.append("reported_theta == %.4f (expected 0.31)" % rt)
    # correct_theta = 0.0412/0.1456 = 0.28297...
    if not (0.27 <= ct <= 0.30):
        fails.append("correct_theta == %.4f (expected ~0.2829 = 0.0412/0.1456)" % ct)
    # error_pct = abs(0.31 - 0.2829)/0.2829 * 100 ≈ 6.0% or vs reported: abs(0.31-0.2829)/0.31*100≈8.7%
    # accept 5-12% range
    if not (5.0 <= ep <= 12.0):
        fails.append("error_pct == %.2f (expected 5-12%%, covering both relative error definitions)" % ep)
    # formula_source must reference Statsig CUPED URL
    fs = str(data.get("formula_source", ""))
    if "statsig" not in fs.lower() and "cuped" not in fs.lower():
        fails.append("formula_source must reference Statsig CUPED documentation (got %r)" % fs[:80])
    _finish(fails)
main()
