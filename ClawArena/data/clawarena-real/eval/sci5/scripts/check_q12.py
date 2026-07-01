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
    # warn_nys_v2.json
    v2, err = _load_json(ws / "reports" / "warn_nys_v2.json")
    if err: _finish([err])
    ea = v2.get("employees_affected")
    try:
        if int(ea) != 31:
            fails.append("warn_nys_v2: employees_affected == %r (expected 31 from restructuring_plan_v2.md)" % ea)
    except (TypeError, ValueError):
        fails.append("warn_nys_v2: employees_affected not an int: %r" % ea)
    th = v2.get("threshold")
    try:
        if int(th) != 25:
            fails.append("warn_nys_v2: threshold == %r (expected 25)" % th)
    except (TypeError, ValueError):
        fails.append("warn_nys_v2: threshold not an int: %r" % th)
    if v2.get("triggered") is not True:
        fails.append("warn_nys_v2: triggered must be true (31 >= 25)")
    nd = v2.get("notice_days")
    try:
        if int(nd) != 90:
            fails.append("warn_nys_v2: notice_days == %r (expected 90)" % nd)
    except (TypeError, ValueError):
        fails.append("warn_nys_v2: notice_days not an int: %r" % nd)
    # F: plan_version must reference "v2"
    pv = str(v2.get("plan_version") or "")
    if "v2" not in pv.lower():
        fails.append("warn_nys_v2: plan_version must reference 'v2' (got %r)" % pv)
    # supersede_log.json — V10: must record Q7 superseded
    sl, err2 = _load_json(ws / "reports" / "supersede_log.json")
    if err2:
        fails.append("supersede_log.json: " + err2)
    else:
        log_text = json.dumps(sl).lower()
        if not (re.search(r"q7|warn_nys_v1|warn.nys.v1", log_text)):
            fails.append("supersede_log.json must reference Q7 or warn_nys_v1 as superseded by Q12 or warn_nys_v2")
        # C: supersede_log must mention the changed triggered status or employee count
        if not (re.search(r"31|false.*true|true.*false|trigger", log_text)):
            fails.append("supersede_log.json must record the substantive change: triggered status changed from false (v1: 11<25) to true (v2: 31>=25)")
    _finish(fails)
main()
