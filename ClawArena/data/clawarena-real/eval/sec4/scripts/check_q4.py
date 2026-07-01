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

from datetime import date, timedelta

def main():
    ws = Path(sys.argv[1]); fails = []
    fp = ws / "dsar" / "dsar_deadlines.csv"
    if not fp.exists():
        _finish(["file not found: dsar/dsar_deadlines.csv"])
    with fp.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if len(rows) < 390 or len(rows) > 410:
        fails.append("dsar_deadlines.csv has %d rows (expected ~400)" % len(rows))
    # Required columns
    if rows:
        for col in ("case_id", "request_date", "response_deadline", "status"):
            if col not in rows[0]:
                fails.append("missing column: %s" % col)
    # Spot-check: REQ-042 deadline must be 2025-02-10 + 30 days = 2025-03-12
    r42 = next((r for r in rows if r.get("case_id") == "REQ-042"), None)
    if r42 is None:
        fails.append("REQ-042 not found in dsar_deadlines.csv")
    else:
        expected = (date(2025, 2, 10) + timedelta(days=30)).isoformat()
        if r42.get("response_deadline") != expected:
            fails.append("REQ-042 response_deadline == %r (expected %s = 2025-02-10 + 30d)" % (
                r42.get("response_deadline"), expected))
        # Should be OVERDUE (deadline 2025-03-12 < ref 2025-03-20, not COMPLETED)
        if r42.get("status") != "OVERDUE":
            fails.append("REQ-042 status == %r (expected OVERDUE; deadline 2025-03-12 < 2025-03-20)" % r42.get("status"))
    # Verify REQ-001 deadline: 2025-02-18 + 30d = 2025-03-20 — on the boundary
    r01 = next((r for r in rows if r.get("case_id") == "REQ-001"), None)
    if r01:
        expected01 = (date(2025, 2, 18) + timedelta(days=30)).isoformat()
        if r01.get("response_deadline") != expected01:
            fails.append("REQ-001 response_deadline == %r (expected %s)" % (r01.get("response_deadline"), expected01))
    _finish(fails)
main()
