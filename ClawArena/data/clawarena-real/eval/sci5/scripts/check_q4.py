#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv
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
    data, err = _load_json(ws / "reports" / "pretext_risk_assessment.json")
    if err: _finish([err])
    cod = data.get("contractor_overlap_days")
    try:
        cod = int(cod)
        # CTR-2025-041 started 2025-09-02; termination 2025-09-12; gap = 10 days
        # allow 8-12 to accommodate ±2 day parsing variance
        if not (8 <= cod <= 12):
            fails.append("contractor_overlap_days == %d (expected ~10; CTR-2025-041 started 2025-09-02, termination 2025-09-12)" % cod)
    except (TypeError, ValueError):
        fails.append("contractor_overlap_days not an int: %r" % cod)
    pr = data.get("performance_rating_2024_q3")
    try:
        prf = float(pr)
        # Q3 rating 2.1, allow ±0.2
        if not (1.9 <= prf <= 2.3):
            fails.append("performance_rating_2024_q3 == %s (expected ~2.1)" % pr)
    except (TypeError, ValueError):
        fails.append("performance_rating_2024_q3 not numeric: %r" % pr)
    pi = data.get("pretext_indicators")
    if not isinstance(pi, list) or len(pi) < 2:
        fails.append("pretext_indicators must be a list with >= 2 items (got %r)" % pi)
    rs = data.get("risk_score")
    try:
        if int(rs) < 70:
            fails.append("risk_score == %d (expected >= 70)" % int(rs))
    except (TypeError, ValueError):
        fails.append("risk_score not an int: %r" % rs)
    _finish(fails)
main()
