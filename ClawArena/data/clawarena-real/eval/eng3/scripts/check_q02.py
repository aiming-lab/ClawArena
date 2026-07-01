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
    data, err = _load_json(ws / "output" / "q02_backbone_window.json")
    if err: _finish([err])
    for k in ("start_utc", "end_utc", "duration_seconds"):
        if k not in data:
            fails.append("missing key: " + k)
    if fails: _finish(fails)
    # start ≈ 17:33 ±60s
    s = data.get("start_utc", "")
    if not re.match(r"2024-06-20T17:3[23]:[0-5]\dZ", s):
        fails.append("start_utc == %r (expected 2024-06-20T17:3[23]:xxZ, ±60s of 17:33)" % s)
    # end ≈ 17:50 ±60s
    e = data.get("end_utc", "")
    if not re.match(r"2024-06-20T17:[45][0-9]:[0-5]\dZ", e):
        fails.append("end_utc == %r (expected 2024-06-20T17:4[89]:xxZ or 17:5[01]:xxZ, ±60s of 17:50)" % e)
    # duration_seconds ∈ [900, 1100]
    try:
        ds = int(data.get("duration_seconds"))
        if not (900 <= ds <= 1100):
            fails.append("duration_seconds == %d (expected in [900, 1100], i.e. ~17 min)" % ds)
    except (TypeError, ValueError):
        fails.append("duration_seconds not numeric: %r" % data.get("duration_seconds"))
    _finish(fails)
main()
