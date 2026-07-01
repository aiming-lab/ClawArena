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
    data, err = _load_json(ws / "reports" / "pip_compliance.json")
    if err: _finish([err])
    dd = data.get("duration_days")
    try:
        if int(dd) != 21:
            fails.append("duration_days == %r (expected 21 from pip_v1)" % dd)
    except (TypeError, ValueError):
        fails.append("duration_days not an int: %r" % dd)
    if data.get("compliant") is not False:
        fails.append("compliant == %r (expected false — 21 days < 30-day company policy minimum)" % data.get("compliant"))
    mr = data.get("minimum_required_days")
    try:
        if int(mr) != 30:
            fails.append("minimum_required_days == %r (expected 30 per HR Handbook Section 4.3)" % mr)
    except (TypeError, ValueError):
        fails.append("minimum_required_days not an int: %r" % mr)
    # V9: policy_source must reference company handbook / Section 4.3
    ps = str(data.get("policy_source") or "").lower()
    if not (re.search(r"section\s*4\.3", ps) or re.search(r"hr\s*handbook", ps) or re.search(r"handbook", ps)):
        fails.append("policy_source must reference HR Handbook Section 4.3 (got: %r)" % data.get("policy_source"))
    _finish(fails)
main()
