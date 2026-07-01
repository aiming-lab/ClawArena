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
    data, err = _load_json(ws / "reports" / "warn_california.json")
    if err: _finish([err])
    if data.get("applies") is not True:
        fails.append("applies must be true (320 employees > 75 Cal-WARN threshold)")
    et = data.get("employer_threshold")
    try:
        if int(et) != 75:
            fails.append("employer_threshold == %r (expected 75 per California Labor Code § 1400)" % et)
    except (TypeError, ValueError):
        fails.append("employer_threshold not an int: %r" % et)
    tt = data.get("trigger_threshold")
    try:
        if int(tt) != 50:
            fails.append("trigger_threshold == %r (expected 50 — Cal-WARN has no 33%% ratio requirement, unlike federal)" % tt)
    except (TypeError, ValueError):
        fails.append("trigger_threshold not an int: %r" % tt)
    nd = data.get("notice_days")
    try:
        if int(nd) != 60:
            fails.append("notice_days == %r (expected 60)" % nd)
    except (TypeError, ValueError):
        fails.append("notice_days not an int: %r" % nd)
    # additional_obligations must mention California EDD
    ao = data.get("additional_obligations") or []
    ao_text = " ".join(str(x) for x in ao).lower()
    if not re.search(r"(edd|employment development|california employment)", ao_text):
        fails.append("additional_obligations must mention California Employment Development Department (EDD)")
    _finish(fails)
main()
