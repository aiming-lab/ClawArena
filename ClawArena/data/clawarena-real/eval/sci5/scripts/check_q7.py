#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv
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
    data, err = _load_json(ws / "reports" / "warn_nys_v1.json")
    if err: _finish([err])
    nd = data.get("notice_days")
    try:
        if int(nd) != 90:
            fails.append("notice_days == %r (expected 90 per NY Labor Law § 860-b 2023 amendment)" % nd)
    except (TypeError, ValueError):
        fails.append("notice_days not an int: %r" % nd)
    th = data.get("threshold")
    try:
        if int(th) != 25:
            fails.append("threshold == %r (expected 25 — NYS WARN plant closing trigger, lower than federal 50)" % th)
    except (TypeError, ValueError):
        fails.append("threshold not an int: %r" % th)
    # F: ny_employees_affected must be exactly 11 (from restructuring_plan_v1.md NY office)
    ny_ea = data.get("ny_employees_affected")
    try:
        if int(ny_ea) != 11:
            fails.append("ny_employees_affected == %r (expected 11 — restructuring_plan_v1.md NY office headcount)" % ny_ea)
    except (TypeError, ValueError):
        fails.append("ny_employees_affected not an int: %r" % ny_ea)
    # F: triggered must be false (11 < 25)
    if data.get("triggered") is not False:
        fails.append("triggered must be false (11 NY employees < 25 plant closing threshold under Plan v1)")
    _finish(fails)
main()
