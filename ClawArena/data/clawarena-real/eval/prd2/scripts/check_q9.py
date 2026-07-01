#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
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
    ws = Path(sys.argv[1])
    pe = ws / "policy_engine"
    fails = []
    data, err = _load_json(pe / "internal" / "appeal_tracker.json")
    if err: _finish([err])

    cases = data.get("cases") or {}

    # New cases from update_1 must exist: T-001..T-007, Y-001..Y-006, M-001..M-005, R-001..R-002
    new_case_ids = (
        ["T-%03d" % i for i in range(1, 8)] +
        ["Y-%03d" % i for i in range(1, 7)] +
        ["M-%03d" % i for i in range(1, 6)] +
        ["R-%03d" % i for i in range(1, 3)]
    )
    missing_new = [k for k in new_case_ids if k not in cases]
    if missing_new:
        fails.append("appeal_tracker: missing new cases from update_1: %s" % missing_new[:5])

    # Check new cases have required fields (including filed_date from update_1 data)
    for cid in new_case_ids:
        c = cases.get(cid)
        if c is None:
            continue
        for fld in ("status", "platform", "violation_type", "filed_date"):
            if not c.get(fld):
                fails.append(
                    "case %s: missing or empty field '%s' "
                    "(update_1 provides filed_date for all new cases)" % (cid, fld)
                )
                break

    # Platform coverage: all 4 platforms represented
    new_plats = set()
    for cid in new_case_ids:
        c = cases.get(cid)
        if c:
            new_plats.add(str(c.get("platform", "")).lower())
    for plat in ("youtube", "meta", "tiktok", "reddit"):
        if plat not in new_plats:
            fails.append("appeal_tracker: platform '%s' missing from new cases" % plat)

    # Legacy cases OLD-0050/0051/0052 must be under_review (V2)
    for cid in ("OLD-0050", "OLD-0051", "OLD-0052"):
        c = cases.get(cid)
        if c is None:
            fails.append("appeal_tracker: missing legacy case %s" % cid)
        elif str(c.get("status", "")).lower() != "under_review":
            fails.append("case %s: status must be 'under_review' (update_1 changed it; got %r)" % (cid, c.get("status")))

    # total_cases must exist AND equal the actual number of cases in the dict
    if "total_cases" not in data:
        fails.append("appeal_tracker: missing 'total_cases' field")
    else:
        tc = data["total_cases"]
        actual_count = len(cases)
        try:
            if int(tc) != actual_count:
                fails.append(
                    "appeal_tracker: total_cases=%r does not match actual case count %d "
                    "(update total_cases to reflect all cases in the tracker)" % (tc, actual_count)
                )
        except (TypeError, ValueError):
            fails.append("appeal_tracker: total_cases must be an integer (got %r)" % tc)

    _finish(fails)
main()
