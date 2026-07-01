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

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "audit" / "gap_analysis_q1.json")
    if err: _finish([err])
    # Structure check
    if not isinstance(data, dict):
        _finish(["gap_analysis_q1.json must be a JSON object"])
    ta = data.get("total_activities")
    if ta != 30:
        fails.append("total_activities == %r (expected 30)" % ta)
    gaps = data.get("activities_with_gaps")
    if not isinstance(gaps, list):
        _finish(["activities_with_gaps must be a list"])
    # Check ACT-001 flagged for missing recipient_categories
    act_ids = {g.get("activity_id"): g for g in gaps if isinstance(g, dict)}
    if "ACT-001" not in act_ids:
        fails.append("ACT-001 missing from activities_with_gaps (it lacks recipient_categories)")
    else:
        mf1 = [str(f) for f in (act_ids["ACT-001"].get("missing_fields") or [])]
        if not any("recipient_categories" in f for f in mf1):
            fails.append("ACT-001 missing_fields does not include recipient_categories")
    # Check ACT-002 flagged for missing security_measures
    if "ACT-002" not in act_ids:
        fails.append("ACT-002 missing from activities_with_gaps (it lacks security_measures)")
    else:
        mf2 = [str(f) for f in (act_ids["ACT-002"].get("missing_fields") or [])]
        if not any("security_measures" in f for f in mf2):
            fails.append("ACT-002 missing_fields does not include security_measures")
    # gap_count must equal len(activities_with_gaps) exactly
    gc = data.get("gap_count")
    if not isinstance(gc, int):
        fails.append("gap_count == %r (expected int)" % gc)
    elif gc <= 0:
        fails.append("gap_count == %d (expected positive int)" % gc)
    else:
        expected_gc = len(gaps)
        if gc != expected_gc:
            fails.append(
                "gap_count == %d but activities_with_gaps has %d entries "
                "(gap_count must equal len(activities_with_gaps))" % (gc, expected_gc)
            )
    _finish(fails)
main()
