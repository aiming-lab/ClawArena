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
    data, err = _load_json(ws / "reports" / "fmla_eligibility_check.json")
    if err: _finish([err])
    # 结构层
    for key in ("employer_covered", "employee_eligible", "weeks_entitled"):
        if key not in data:
            fails.append("missing key: " + key)
    if fails: _finish(fails)
    # 字段层
    if data.get("employer_covered") is not True:
        fails.append("employer_covered must be true (320 employees > 50 threshold)")
    if data.get("employee_eligible") is not True:
        fails.append("employee_eligible must be true (tenure 4.5 yrs, hours 1310 > 1250)")
    we = data.get("weeks_entitled")
    try:
        if int(we) != 12:
            fails.append("weeks_entitled == %r (expected 12)" % we)
    except (TypeError, ValueError):
        fails.append("weeks_entitled not an int: %r" % we)
    _finish(fails)
main()
