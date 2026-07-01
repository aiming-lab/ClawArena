#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv
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
    txt = _read(ws / "output" / "corrective_action_plan.md")
    if txt is None:
        _finish(["file not found: output/corrective_action_plan.md"])
    low = txt.lower()
    # Must cite Rule 15c3-5(b) (with sub-clause per P3)
    if "15c3-5" not in txt:
        fails.append("CAP does not reference Rule 15c3-5")
    if not re.search(r"15c3-5\(b\)|15c3-5\s*\(b\)", txt, re.IGNORECASE):
        fails.append("CAP must cite Rule 15c3-5(b) with sub-clause (P3)")
    # Must cite Rule 15c6-1
    if "15c6-1" not in txt:
        fails.append("CAP does not reference Rule 15c6-1 (T+1 settlement)")
    # Must mention timezone automation/DST-aware library
    if not re.search(r"dst|daylight|timezone.*auto|pytz|zoneinfo|dateutil", low):
        fails.append("CAP does not include DST-aware timezone automation action")
    # Must have >= 4 remediation items with owner field
    # Look for owner: or owner field occurrences
    owner_count = len(re.findall(r"owner", low))
    if owner_count < 4:
        fails.append("CAP has fewer than 4 owner fields (%d found); each remediation item needs 'owner' (P4)" % owner_count)
    # Must have deadline_days or deadline field
    if not re.search(r"deadline|days", low):
        fails.append("CAP does not include deadline_days for remediation items")
    _finish(fails)
main()
