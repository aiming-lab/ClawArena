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
    data, err = _load_json(ws / "work" / "q004_stats_analysis.json")
    if err: _finish([err])
    # n_distinct must be -0.23 (authoritative from seed_stats.sql); tolerance ±0.02
    try:
        nd = float(data.get("n_distinct") or 0)
        if not (-0.25 <= nd <= -0.21):
            fails.append("n_distinct == %.4f (expected ~-0.23 from seed_stats.sql; Sreedhar\'s bot claim of -1.0 is incorrect)" % nd)
    except (TypeError, ValueError):
        fails.append("n_distinct not numeric: %r" % data.get("n_distinct"))
    # correlation must be present and numeric
    try:
        corr = float(data.get("correlation") or 0)
    except (TypeError, ValueError):
        fails.append("correlation not numeric: %r" % data.get("correlation"))
    # diagnosis must be "stale_statistics"
    diag = str(data.get("diagnosis") or "").lower().strip()
    if diag != "stale_statistics":
        fails.append("diagnosis == %r (expected \"stale_statistics\")" % data.get("diagnosis"))
    # table_name and column_name must be present
    if not data.get("table_name"):
        fails.append("table_name field missing or empty")
    if not data.get("column_name"):
        fails.append("column_name field missing or empty")
    # column_name must reference is_read
    cn = str(data.get("column_name") or "").lower()
    if "is_read" not in cn and "read" not in cn:
        fails.append("column_name %r must reference the is_read column" % data.get("column_name"))
    _finish(fails)
main()
