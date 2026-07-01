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
    data, err = _load_json(ws / "output" / "incident_timeline_v1.json")
    if err: _finish([err])
    # incident_date
    idate = str(data.get("incident_date") or "")
    if "2024-11-03" not in idate:
        fails.append("incident_date == %r (expected '2024-11-03')" % idate)
    # event_time_utc — first mis-timed T+1 order at 14:30:00Z
    etutc = str(data.get("event_time_utc") or "")
    if "2024-11-03T14:30:00" not in etutc:
        fails.append("event_time_utc == %r (expected '2024-11-03T14:30:00Z' per incident timeline)" % etutc)
    # timezone_offset — the BUG value = -4
    tz_off = data.get("timezone_offset")
    try:
        tz_off = int(tz_off)
    except (TypeError, ValueError):
        _finish(["timezone_offset not an int: %r" % tz_off])
    if tz_off != -4:
        fails.append("timezone_offset == %d (expected -4, the bug value)" % tz_off)
    # correct_timezone_offset — should be -5 (EST)
    corr = data.get("correct_timezone_offset")
    try:
        corr = int(corr)
    except (TypeError, ValueError):
        _finish(["correct_timezone_offset not an int: %r" % corr])
    if corr != -5:
        fails.append("correct_timezone_offset == %d (expected -5 for EST after DST switch)" % corr)
    _finish(fails)
main()
