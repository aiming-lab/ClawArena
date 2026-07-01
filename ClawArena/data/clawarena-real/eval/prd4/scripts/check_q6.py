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
    data, err = _load_json(ws / "output" / "credit_calc_atlassian.json")
    if err: _finish([err])
    # actual_uptime must be 99.92
    upt = data.get("actual_uptime_pct")
    try:
        upt_f = float(upt)
        if abs(upt_f - 99.92) > 0.01:
            fails.append("actual_uptime_pct == %r (expected 99.92)" % upt)
    except (TypeError, ValueError):
        fails.append("actual_uptime_pct not numeric: %r" % upt)
    # credit_pct must be 5 (Enterprise tier0 for 99.90-99.95%)
    pct = data.get("credit_pct")
    try:
        pct_i = int(pct)
        if pct_i != 5:
            fails.append("credit_pct == %d (expected 5 for Enterprise 99.90-99.95%% tier; 10 is wrong)" % pct_i)
    except (TypeError, ValueError):
        fails.append("credit_pct not numeric: %r" % pct)
    # source_url must reference atlassian.com/legal/sla
    src = str(data.get("source_url") or "")
    if "atlassian.com/legal/sla" not in src:
        fails.append("source_url == %r (expected https://www.atlassian.com/legal/sla)" % src)
    # reviewer_signature field must exist (P5)
    if "reviewer_signature" not in data:
        fails.append("reviewer_signature field missing (P5 requires this field)")
    _finish(fails)
main()
