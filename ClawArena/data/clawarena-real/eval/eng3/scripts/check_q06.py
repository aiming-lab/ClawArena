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
    data, err = _load_json(ws / "output" / "q06_duration.json")
    if err: _finish([err])
    for k in ("start_utc", "end_utc", "duration_minutes"):
        if k not in data:
            fails.append("missing key: " + k)
    if fails: _finish(fails)
    # duration_minutes ∈ [98, 102]
    try:
        dm = int(data.get("duration_minutes"))
        if not (98 <= dm <= 102):
            fails.append("duration_minutes == %d (expected [98, 102])" % dm)
    except (TypeError, ValueError):
        fails.append("duration_minutes not int: %r" % data.get("duration_minutes"))
    # end_utc ≈ 2024-06-20T19:27:00Z ±60s
    end = data.get("end_utc", "")
    if not re.match(r"2024-06-20T19:2[678]:[0-5]\dZ", end):
        fails.append("end_utc == %r (expected ~2024-06-20T19:27:00Z ±60s)" % end)
    # V4 cross-round: start_utc must match q01_incident_start.json exactly
    q01, e1 = _load_json(ws / "output" / "q01_incident_start.json")
    if not e1 and q01 is not None:
        expected_start = q01.get("incident_start_utc")
        if expected_start and data.get("start_utc") != expected_start:
            fails.append("start_utc %r != q01 incident_start_utc %r (cross-round drift not allowed)" % (
                data.get("start_utc"), expected_start))
    _finish(fails)
main()
