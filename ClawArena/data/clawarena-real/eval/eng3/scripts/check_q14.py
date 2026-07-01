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
    txt = _read(ws / "postmortem" / "DRAFT_v2.md")
    if txt is None:
        _finish(["file not found: postmortem/DRAFT_v2.md"])
    # 六个关键时间点
    for ts in ("17:47", "17:33", "17:50", "18:04", "19:27", "19:34"):
        if ts not in txt:
            fails.append("DRAFT_v2.md missing timestamp %r in Timeline section" % ts)
    # V4 cross-round: 17:47 must align with q01, 19:27 must align with q06
    q01, e1 = _load_json(ws / "output" / "q01_incident_start.json")
    if not e1 and q01:
        start = q01.get("incident_start_utc", "")
        # extract HH:MM from start
        m1 = re.search(r"T(\d{2}:\d{2})", start)
        if m1 and m1.group(1) not in txt:
            fails.append("DRAFT_v2.md timeline does not contain the Q1 start time %s" % m1.group(1))
    q06, e6 = _load_json(ws / "output" / "q06_duration.json")
    if not e6 and q06:
        end = q06.get("end_utc", "")
        m6 = re.search(r"T(\d{2}:\d{2})", end)
        if m6 and m6.group(1) not in txt:
            fails.append("DRAFT_v2.md timeline does not contain Q6 end time %s" % m6.group(1))
    _finish(fails)
main()
