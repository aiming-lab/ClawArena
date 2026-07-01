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
    data, err = _load_json(ws / "reports" / "adea_compliance.json")
    if err: _finish([err])
    age = data.get("employee_age")
    try:
        if int(age) != 42:
            fails.append("employee_age == %r (expected 42 from employee_roster.csv EMP-0042)" % age)
    except (TypeError, ValueError):
        fails.append("employee_age not an int: %r" % age)
    if data.get("adea_protected") is not True:
        fails.append("adea_protected must be true (age 42 >= 40)")
    cd = data.get("consideration_days")
    try:
        if int(cd) != 21:
            fails.append("consideration_days == %r (expected 21 for INDIVIDUAL termination; 45 days is for GROUP terminations — Marcus\'s Slack DM claim of 45 days is incorrect)" % cd)
    except (TypeError, ValueError):
        fails.append("consideration_days not an int: %r" % cd)
    rd = data.get("revocation_days")
    try:
        if int(rd) != 7:
            fails.append("revocation_days == %r (expected 7 — irrevocable)" % rd)
    except (TypeError, ValueError):
        fails.append("revocation_days not an int: %r" % rd)
    _finish(fails)
main()
