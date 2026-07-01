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

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "ropa" / "ropa_controller_v2.json")
    if err: _finish([err])
    activities = data.get("activities") if isinstance(data, dict) else None
    if not isinstance(activities, list):
        _finish(["ropa_controller_v2.json must have an 'activities' list"])
    if len(activities) != 31:
        fails.append("total activities == %d (expected 31: 30 original + ACT-021 from addendum)" % len(activities))
    # There must be an activity with purposes containing 'personalisation' and
    # legal_ground/art6_basis referencing 'legitimate_interests' (the AI addendum activity)
    ai_act = None
    for a in activities:
        if not isinstance(a, dict):
            continue
        purposes_str = str(a.get("purposes", "")).lower()
        if "personalisation" in purposes_str or "personalization" in purposes_str:
            lg = str(a.get("legal_ground", "")).lower()
            a6 = str(a.get("art6_basis", "")).lower()
            if "legitimate_interests" in lg or "legitimate interests" in lg or                "legitimate_interests" in a6 or "legitimate interests" in a6:
                ai_act = a
                break
    if ai_act is None:
        fails.append("No AI recommendation engine activity found with purposes containing "
                     "'personalisation' AND legal_ground/art6_basis referencing 'legitimate_interests'")
    _finish(fails)
main()
