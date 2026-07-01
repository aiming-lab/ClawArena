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
    p = ws / "output" / "q13_actions_tracker_v2.csv"
    if not p.exists():
        _finish(["file not found: output/q13_actions_tracker_v2.csv"])
    rows = list(csv.DictReader(p.open(encoding="utf-8")))
    # total rows 应为 9（7 original + CA-003-revised - CA-003 exists but stays）
    # Actually: original 7 items remain, CA-003-revised added = 8 items, but CA-003 stays as superseded
    # So total = 8 rows (CA-001,CA-002,CA-003,CA-003-revised,CA-004,CA-005,CA-006,CA-007)
    # But wait - BRIEF says 7 items in v1, v2 supersedes CA-003 and adds CA-003-revised = 8 items
    # Adjusted: accept 8 or 9
    if len(rows) < 8:
        fails.append("q13_actions_tracker_v2.csv has %d rows (expected >= 8: 7 original + CA-003-revised)" % len(rows))
    # CA-003 must have superseded_by = CA-003-revised
    headers = set(rows[0].keys()) if rows else set()
    if "superseded_by" not in headers:
        fails.append("q13_actions_tracker_v2.csv missing 'superseded_by' column")
    else:
        ca3_rows = [r for r in rows if r.get("id", "").strip() == "CA-003"]
        if not ca3_rows:
            fails.append("CA-003 row missing from q13_actions_tracker_v2.csv")
        else:
            sup = ca3_rows[0].get("superseded_by", "").strip()
            if "CA-003-revised" not in sup and "ca-003-revised" not in sup.lower():
                fails.append("CA-003.superseded_by == %r (expected 'CA-003-revised')" % sup)
    # CA-003-revised must exist
    ca3r = [r for r in rows if "CA-003-revised" in r.get("id", "") or
            "automated" in r.get("title", "").lower() or "watchdog" in r.get("title", "").lower()]
    if not ca3r:
        fails.append("CA-003-revised (automated-restart-watchdog) row missing from tracker v2")
    _finish(fails)
main()
