#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, subprocess
from pathlib import Path
from datetime import date, timedelta

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
    data, err = _load_json(ws / "output" / "q6_risk_scores.json")
    if err: _finish([err])

    alerts = data.get("alerts") or data.get("scores") or []
    if isinstance(data, list):
        alerts = data

    if len(alerts) < 3:
        fails.append(f"expected 3 scored alerts, got {len(alerts)}")

    lookup = {}
    for a in alerts:
        lookup[str(a.get("alert_id", ""))] = a

    thresholds = set()
    for a in alerts:
        t = a.get("threshold_used")
        if t is not None:
            thresholds.add(float(t))
    if thresholds and thresholds != {0.5}:
        fails.append(f"threshold_used must be 0.5 (got {thresholds}); do not use the bot summary's 0.3")

    expected = {
        "ALRT-20260301-0001": ("FRAUD", 0.72),
        "ALRT-20260301-0005": ("LEGITIMATE", 0.43),
        "ALRT-20260301-0009": ("FRAUD", 0.88),
    }
    for alrt_id, (exp_decision, exp_score) in expected.items():
        entry = lookup.get(alrt_id)
        if entry is None:
            fails.append(f"missing alert {alrt_id}")
            continue
        dec = str(entry.get("decision", "")).upper()
        if dec != exp_decision:
            fails.append(f"{alrt_id}: decision={dec!r} (expected {exp_decision!r})")

    _finish(fails)
main()
