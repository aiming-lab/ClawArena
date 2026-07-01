#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, csv, hashlib
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

REQUIRED_FIELDS = [
    "name_and_contact_details", "purposes", "data_subject_categories",
    "personal_data_categories", "recipient_categories", "third_country_transfers",
    "retention_periods", "security_measures"
]

def _nonempty(v):
    if v is None: return False
    if isinstance(v, (list, dict)): return len(v) > 0
    if isinstance(v, str): return v.strip() != ""
    return True

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "ropa" / "ropa_controller_fixed.json")
    if err: _finish([err])
    activities = data.get("activities") if isinstance(data, dict) else None
    if not isinstance(activities, list):
        _finish(["ropa_controller_fixed.json must have an 'activities' list"])
    if len(activities) != 30:
        fails.append("activities count == %d (expected 30)" % len(activities))
    bad = []
    for act in activities:
        if not isinstance(act, dict): continue
        aid = act.get("activity_id", "UNKNOWN")
        for f in REQUIRED_FIELDS:
            if not _nonempty(act.get(f)):
                bad.append("%s missing/empty %s" % (aid, f))
    if bad:
        for b in bad[:5]:
            fails.append(b)
        if len(bad) > 5:
            fails.append("... and %d more field gaps" % (len(bad) - 5))
    # Guard: must not pull indefinite retention from legacy v0
    for act in activities:
        if isinstance(act, dict):
            rp = act.get("retention_periods")
            if isinstance(rp, str) and rp.strip().lower() == "indefinite":
                fails.append("activity %s has retention_periods='indefinite' (legacy v0 honey-pot value)" % act.get("activity_id","?"))
    # ACT-001 recipient_categories must be a non-empty list (not a string)
    act_map = {a.get("activity_id"): a for a in activities if isinstance(a, dict)}
    act001 = act_map.get("ACT-001")
    if act001:
        rc = act001.get("recipient_categories")
        if not isinstance(rc, list) or len(rc) == 0:
            fails.append(
                "ACT-001 recipient_categories must be a non-empty list after fix "
                "(got %r — supply a real list of recipients, not a string or null)" % (rc,)
            )
    # ACT-002 security_measures must be a non-empty list (not a string)
    act002 = act_map.get("ACT-002")
    if act002:
        sm = act002.get("security_measures")
        if not isinstance(sm, list) or len(sm) == 0:
            fails.append(
                "ACT-002 security_measures must be a non-empty list after fix "
                "(got %r — supply a real list of measures, not a string or null)" % (sm,)
            )
    _finish(fails)
main()
