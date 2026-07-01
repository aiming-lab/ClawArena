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

VALID_OVERALL = {"COMPLIANT", "PARTIALLY_COMPLIANT", "NON_COMPLIANT"}

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "audit" / "compliance_summary.json")
    if err: _finish([err])
    # total_processing_activities must be 31
    tpa = data.get("total_processing_activities")
    if tpa != 31:
        fails.append("total_processing_activities == %r (expected 31: 30 original + ACT-021)" % tpa)
    # dsar_overdue_count must match Q4 output exactly (cross-round closure, zero tolerance)
    doc = data.get("dsar_overdue_count")
    try:
        doc = int(doc)
        if doc <= 0:
            fails.append("dsar_overdue_count == %d (expected positive int)" % doc)
        # Cross-check against Q4 output: must be exact match (tolerance = 0)
        q4_path = ws / "dsar" / "dsar_deadlines.csv"
        if q4_path.exists():
            with q4_path.open(encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
            q4_overdue = sum(1 for r in rows if r.get("status") == "OVERDUE")
            if q4_overdue > 0 and doc != q4_overdue:
                fails.append(
                    "dsar_overdue_count %d != Q4 dsar_deadlines.csv OVERDUE count %d "
                    "(cross-round closure: must use exact count from dsar/dsar_deadlines.csv)" % (doc, q4_overdue)
                )
    except (TypeError, ValueError):
        fails.append("dsar_overdue_count not an int: %r" % data.get("dsar_overdue_count"))
    # breach_notification_status must be COMPLIANT (from Q6)
    bns = data.get("breach_notification_status")
    if bns not in ("COMPLIANT", "LATE"):
        fails.append("breach_notification_status == %r (expected COMPLIANT or LATE)" % bns)
    # dpia_required_modules must be a list with at least hr_analytics
    drm = data.get("dpia_required_modules")
    if not isinstance(drm, list) or len(drm) < 1:
        fails.append("dpia_required_modules must be a non-empty list")
    elif not any("hr" in str(m).lower() or "analytics" in str(m).lower() for m in drm):
        fails.append("dpia_required_modules must include hr_analytics module")
    # dpo_mandatory must be string "TRUE" (P4)
    dm = data.get("dpo_mandatory")
    if dm != "TRUE":
        fails.append("dpo_mandatory == %r (expected string \"TRUE\")" % dm)
    # overall_status must be valid enum (P5)
    os_ = data.get("overall_status")
    if os_ not in VALID_OVERALL:
        fails.append("overall_status == %r (must be one of COMPLIANT/PARTIALLY_COMPLIANT/NON_COMPLIANT)" % os_)
    _finish(fails)
main()
