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

    # appeal_tracker: T-001..T-007 must be pending (superseded)
    at, err = _load_json(pe / "internal" / "appeal_tracker.json")
    if err: _finish([err])
    cases = at.get("cases") or {}

    for cid in ("T-001", "T-002", "T-003", "T-004", "T-005", "T-006", "T-007"):
        c = cases.get(cid)
        if c is None:
            fails.append("appeal_tracker: TikTok case %s missing (must exist and be pending)" % cid)
        elif str(c.get("status", "")).lower() != "pending":
            fails.append("case %s: status must be 'pending' (superseded by Discord notice; got %r)" % (cid, c.get("status")))

    # YouTube cases Y-001..Y-006 must NOT be pending (V10: only TikTok subset superseded)
    for cid in ("Y-001", "Y-002", "Y-003", "Y-004", "Y-005", "Y-006"):
        c = cases.get(cid)
        if c is not None and str(c.get("status", "")).lower() == "pending":
            fails.append("case %s: YouTube case should NOT be reset to pending (only TikTok T-001..T-007 were superseded)" % cid)

    # q3_2025_report.json must exist with quarter field containing 'Q3_2025'
    q3, err2 = _load_json(pe / "platforms" / "tiktok" / "q3_2025_report.json")
    if err2: _finish([err2])
    q3_quarter = str(q3.get("quarter") or "")
    if "Q3_2025" not in q3_quarter and "Q3" not in q3_quarter:
        fails.append("q3_2025_report.json: quarter field must contain 'Q3_2025' (got %r)" % q3_quarter)

    _finish(fails)
main()
