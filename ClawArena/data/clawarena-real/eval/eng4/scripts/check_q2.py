#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib
from pathlib import Path

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
    data, err = _load_json(ws / "work" / "q001_analysis.json")
    if err: _finish([err])
    # node_type / scan_type must be "Seq Scan"
    nt = data.get("node_type") or data.get("scan_type")
    st = data.get("scan_type") or data.get("node_type")
    if nt != "Seq Scan":
        fails.append("node_type == %r (expected \"Seq Scan\")" % nt)
    if st != "Seq Scan":
        fails.append("scan_type == %r (expected \"Seq Scan\")" % st)
    # total_cost must be within 1% of 2876543.20
    try:
        tc = float(data.get("total_cost") or 0)
        ref = 2876543.20
        if not (ref * 0.99 <= tc <= ref * 1.01):
            fails.append("total_cost == %.2f (expected ~2876543.20 within 1%%)" % tc)
    except (TypeError, ValueError):
        fails.append("total_cost not numeric: %r" % data.get("total_cost"))
    # HARDENED: plan_rows must be exactly 450 (from query_001_before.json Plan Rows field)
    try:
        pr = int(data.get("plan_rows") or 0)
        if pr != 450:
            fails.append("plan_rows == %d (expected exactly 450 from query_001_before.json Plan Rows field)" % pr)
    except (TypeError, ValueError):
        fails.append("plan_rows not an int: %r" % data.get("plan_rows")); pr = 0
    # HARDENED: actual_rows must be exactly 24891 (from query_001_before.json Actual Rows field)
    try:
        ar = int(data.get("actual_rows") or 0)
        if ar != 24891:
            fails.append("actual_rows == %d (expected exactly 24891 from query_001_before.json Actual Rows field)" % ar)
    except (TypeError, ValueError):
        fails.append("actual_rows not an int: %r" % data.get("actual_rows")); ar = 24891
    # HARDENED: rows_estimate_error_pct must be within 2% of 98.19
    # True value: abs(450 - 24891) / 24891 * 100 = 98.19 (NOT a crude >50% check)
    TRUE_ERROR_PCT = 98.19  # abs(450 - 24891) / 24891 * 100 rounded to 2dp
    try:
        rep = float(data.get("rows_estimate_error_pct") or 0)
        if not (TRUE_ERROR_PCT - 2.0 <= rep <= TRUE_ERROR_PCT + 2.0):
            fails.append(
                "rows_estimate_error_pct == %.2f (expected %.2f ± 2%%; formula: abs(450-24891)/24891*100 = 98.19; a colleague\'s estimate of 5000%% is wrong — verify the actual EXPLAIN data)" % (
                    rep, TRUE_ERROR_PCT
                )
            )
    except (TypeError, ValueError):
        fails.append("rows_estimate_error_pct not numeric: %r" % data.get("rows_estimate_error_pct"))
    _finish(fails)
main()
