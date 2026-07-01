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
    data, err = _load_json(ws / "reports" / "review_violations_q6.json")
    if err: _finish([err])
    # total_reviews_monitored must be ~850
    trm = data.get("total_reviews_monitored")
    try:
        trm = int(trm)
        if not (750 <= trm <= 950):
            fails.append("total_reviews_monitored == %d (expected ~850)" % trm)
    except (TypeError, ValueError):
        fails.append("total_reviews_monitored not numeric: %r" % trm)
    # violation_breakdown must exist as a dict
    vb = data.get("violation_breakdown")
    if not isinstance(vb, dict):
        fails.append("violation_breakdown must be a JSON object")
        _finish(fails)
    # fake_reviews_465_2 = 47
    fr = vb.get("fake_reviews_465_2")
    try:
        fr = int(fr)
        if not (40 <= fr <= 55):
            fails.append("fake_reviews_465_2 == %d (expected ~47)" % fr)
    except (TypeError, ValueError):
        fails.append("fake_reviews_465_2 not numeric: %r" % fr)
    # insider_reviews_465_3 = 41
    ir = vb.get("insider_reviews_465_3")
    try:
        ir = int(ir)
        if not (35 <= ir <= 50):
            fails.append("insider_reviews_465_3 == %d (expected ~41)" % ir)
    except (TypeError, ValueError):
        fails.append("insider_reviews_465_3 not numeric: %r" % ir)
    # no_violation = 715
    nv = vb.get("no_violation")
    try:
        nv = int(nv)
        if not (650 <= nv <= 780):
            fails.append("no_violation == %d (expected ~715)" % nv)
    except (TypeError, ValueError):
        fails.append("no_violation not numeric: %r" % nv)
    _finish(fails)
main()
