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
    data, err = _load_json(ws / "reports" / "warn_federal.json")
    if err: _finish([err])
    if data.get("employer_qualifies") is not True:
        fails.append("employer_qualifies must be true (320 employees > 100 threshold per 29 U.S.C. § 2101(a)(1); NOT 500 — the GC v1 memo error)")
    ea = data.get("employees_affected")
    try:
        if int(ea) != 58:
            fails.append("employees_affected == %r (expected 58 from restructuring_plan_v1.md)" % ea)
    except (TypeError, ValueError):
        fails.append("employees_affected not an int: %r" % ea)
    nd = data.get("notice_days_required")
    try:
        if int(nd) != 60:
            fails.append("notice_days_required == %r (expected 60 per 29 U.S.C. § 2102)" % nd)
    except (TypeError, ValueError):
        fails.append("notice_days_required not an int: %r" % nd)
    # applicable_rule must reference plant closing or mass layoff (not just "warn act")
    ar = str(data.get("applicable_rule") or "").lower()
    if not (re.search(r"plant.clos", ar) or re.search(r"mass.layoff", ar)):
        fails.append("applicable_rule must reference 'plant closing' or 'mass layoff' (got %r)" % data.get("applicable_rule"))
    # must NOT just reference the 500-person threshold
    if re.search(r"500.*(threshold|employer)", ar):
        fails.append("applicable_rule appears to use the GC v1 erroneous 500-person threshold")
    _finish(fails)
main()
