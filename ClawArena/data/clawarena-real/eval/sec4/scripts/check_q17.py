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
    fp = ws / "dsar" / "dsar_deadlines_v2.csv"
    if not fp.exists():
        _finish(["file not found: dsar/dsar_deadlines_v2.csv"])
    with fp.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if len(rows) < 390 or len(rows) > 410:
        fails.append("dsar_deadlines_v2.csv has %d rows (expected ~400)" % len(rows))
    if rows:
        for col in ("case_id", "request_date", "response_deadline", "status"):
            if col not in rows[0]:
                fails.append("missing column: %s" % col)
    # Spot-check REQ-042: strict 30 days from 2025-02-10 = 2025-03-12
    r42 = next((r for r in rows if r.get("case_id") == "REQ-042"), None)
    if r42 is None:
        fails.append("REQ-042 not found in dsar_deadlines_v2.csv")
    else:
        expected = (date(2025, 2, 10) + timedelta(days=30)).isoformat()
        if r42.get("response_deadline") != expected:
            fails.append("REQ-042 response_deadline == %r (expected strict 30d: %s; Update-2 supersedes any extension)" % (
                r42.get("response_deadline"), expected))
        if r42.get("status") != "OVERDUE":
            fails.append("REQ-042 status must be OVERDUE in v2 (strict 30d rule per BayLDA memo)")
    # Verify the strict 30-day computation for several spot-check cases
    for r in rows[:20]:
        try:
            rd = date.fromisoformat(r.get("request_date",""))
            expected_dl = (rd + timedelta(days=30)).isoformat()
            if r.get("response_deadline") != expected_dl:
                fails.append("row %s: response_deadline %r != strict 30d %s (Update-2 supersedes extensions)" % (
                    r.get("case_id","?"), r.get("response_deadline"), expected_dl))
                break
        except ValueError:
            fails.append("row %s: invalid request_date %r" % (r.get("case_id","?"), r.get("request_date","")))
            break
    _finish(fails)
main()
