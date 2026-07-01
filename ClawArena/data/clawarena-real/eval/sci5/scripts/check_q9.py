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
    data, err = _load_json(ws / "reports" / "eeoc_deadline.json")
    if err: _finish([err])
    if data.get("state_agency_exists") is not True:
        fails.append("state_agency_exists must be true (California CRD exists)")
    fdd = data.get("filing_deadline_days")
    try:
        if int(fdd) != 300:
            fails.append("filing_deadline_days == %r (expected 300 — California is a deferral state)" % fdd)
    except (TypeError, ValueError):
        fails.append("filing_deadline_days not an int: %r" % fdd)
    # deadline_date must be 2026-07-08 (300 days from 2025-09-12)
    dd = str(data.get("deadline_date") or "")
    if "2026-07-08" not in dd:
        fails.append("deadline_date must contain 2026-07-08 (300 days from 2025-09-12; got %r)" % dd)
    # statute_basis must reference Title VII and ADEA
    sb = str(data.get("statute_basis") or "").lower()
    if "title vii" not in sb and "42 u.s.c" not in sb and "2000e" not in sb:
        fails.append("statute_basis must reference Title VII / 42 U.S.C. § 2000e (got %r)" % data.get("statute_basis"))
    if "adea" not in sb and "age discrimination" not in sb:
        fails.append("statute_basis must reference ADEA (got %r)" % data.get("statute_basis"))
    _finish(fails)
main()
