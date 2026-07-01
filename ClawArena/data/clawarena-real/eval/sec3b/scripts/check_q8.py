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
    data, err = _load_json(ws / "output" / "t1_settlement_impact.json")
    if err: _finish([err])
    # rule_effective_date: 2024-05-28
    red = str(data.get("rule_effective_date") or "")
    if "2024-05-28" not in red:
        fails.append("rule_effective_date == %r (expected '2024-05-28')" % red)
    # offset_minutes: exactly 60
    om = data.get("offset_minutes")
    try:
        om = int(om)
    except (TypeError, ValueError):
        _finish(["offset_minutes not an int: %r" % om])
    if om != 60:
        fails.append("offset_minutes == %d (expected 60, the 1-hour DST offset)" % om)
    # Validate the exact UTC cutoff values (not just the diff)
    # T+1 cutoff is 21:00 ET per Rule 15c6-1
    # incorrect_cutoff_utc: 21:00 ET with UTC-4 = 2024-11-04T01:00:00Z
    # correct_cutoff_utc: 21:00 ET with UTC-5 = 2024-11-04T02:00:00Z
    import datetime
    ic = str(data.get("incorrect_cutoff_utc") or "")
    cc = str(data.get("correct_cutoff_utc") or "")
    if not ic or not cc:
        fails.append("incorrect_cutoff_utc and/or correct_cutoff_utc missing")
    else:
        # Check exact expected values
        if "2024-11-04T01:00:00" not in ic:
            fails.append(
                "incorrect_cutoff_utc == %r (expected '2024-11-04T01:00:00Z'; "
                "T+1 cutoff 21:00 ET with wrong UTC-4 offset = 21+4 = 01:00 UTC next day)" % ic
            )
        if "2024-11-04T02:00:00" not in cc:
            fails.append(
                "correct_cutoff_utc == %r (expected '2024-11-04T02:00:00Z'; "
                "T+1 cutoff 21:00 ET with correct UTC-5 offset = 21+5 = 02:00 UTC next day)" % cc
            )
        # Also verify the difference
        try:
            def _parse(s):
                return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
            ic_dt = _parse(ic); cc_dt = _parse(cc)
            delta = (cc_dt - ic_dt).total_seconds()
            if abs(delta - 3600) > 1:
                fails.append("correct_cutoff_utc - incorrect_cutoff_utc == %.0fs (expected 3600s = 60min)" % delta)
        except Exception as exc:
            fails.append("cannot parse cutoff times: %s" % exc)
    _finish(fails)
main()
