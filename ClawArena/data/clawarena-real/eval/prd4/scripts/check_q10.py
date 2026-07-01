#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib
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
    data, err = _load_json(ws / "output" / "combined_breach_summary.json")
    if err: _finish([err])
    total = data.get("total_tickets")
    breaches = data.get("total_breaches")
    pct = data.get("breach_pct")
    try:
        total_i = int(total)
        breach_i = int(breaches)
        pct_f = float(pct)
    except (TypeError, ValueError):
        _finish(["total_tickets/total_breaches/breach_pct not numeric"])
    if total_i != 350:
        fails.append("total_tickets == %d (expected 350 = 200+150)" % total_i)
    # cross-round closure: Q7(31) + Q9(19) = 50
    q7, e7 = _load_json(ws / "output" / "breach_tickets_Q4_v2.json")
    q9, e9 = _load_json(ws / "output" / "breach_tickets_Q1.json")
    if not e7 and not e9 and q7 is not None and q9 is not None:
        q7t = q7 if isinstance(q7, list) else q7.get("tickets", [])
        q9t = q9 if isinstance(q9, list) else q9.get("tickets", [])
        expected_b = len(q7t) + len(q9t)
        if breach_i != expected_b:
            fails.append("total_breaches %d != Q7(%d) + Q9(%d) = %d (cross-round closure fail)" % (
                breach_i, len(q7t), len(q9t), expected_b))
    # breach_pct closure
    expected_pct = round(breach_i / total_i * 100, 2) if total_i > 0 else 0
    if abs(pct_f - expected_pct) > 0.1:
        fails.append("breach_pct %.2f != expected %.2f (= %d/%d*100)" % (pct_f, expected_pct, breach_i, total_i))
    _finish(fails)
main()
