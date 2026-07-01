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

def _csv_rows(p):
    """Read CSV and return (header, data_rows). Returns (None, []) if file missing."""
    p = Path(p)
    if not p.exists():
        return None, []
    with p.open(encoding="utf-8") as fh:
        rows = [r for r in fh if not r.strip().startswith("#")]
    if not rows:
        return None, []
    reader = csv.DictReader(iter(rows))
    data = list(reader)
    return reader.fieldnames, data

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "incident_timeline_v1.json")
    if err: _finish([err])
    # 结构层
    for req in ("incident_date", "error_window_utc_start", "error_window_utc_end",
                "timezone_offset_applied", "correct_timezone_offset"):
        if req not in data:
            fails.append("missing field: " + req)
    if fails: _finish(fails)
    # 字段层 + 真值层
    if data.get("incident_date") != "2024-11-03":
        fails.append("incident_date == %r (expected '2024-11-03')" % data.get("incident_date"))
    start = str(data.get("error_window_utc_start", ""))
    end   = str(data.get("error_window_utc_end", ""))
    if "2024-11-03T14:00:00" not in start:
        fails.append("error_window_utc_start must be 2024-11-03T14:00:00Z (got %r)" % start)
    if "2024-11-03T15:00:00" not in end:
        fails.append("error_window_utc_end must be 2024-11-03T15:00:00Z (got %r)" % end)
    try:
        tz_applied = int(data.get("timezone_offset_applied"))
    except (TypeError, ValueError):
        _finish(["timezone_offset_applied not an int: %r" % data.get("timezone_offset_applied")])
    if tz_applied != -4:
        fails.append("timezone_offset_applied == %r (expected -4, the wrong offset)" % tz_applied)
    try:
        tz_correct = int(data.get("correct_timezone_offset"))
    except (TypeError, ValueError):
        _finish(["correct_timezone_offset not an int: %r" % data.get("correct_timezone_offset")])
    if tz_correct != -5:
        fails.append("correct_timezone_offset == %r (expected -5, EST)" % tz_correct)
    _finish(fails)
main()
