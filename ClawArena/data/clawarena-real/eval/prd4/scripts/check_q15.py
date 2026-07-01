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
    data, err = _load_json(ws / "output" / "aws_credit_calc.json")
    if err: _finish([err])
    # service
    svc = str(data.get("service") or "").lower()
    if "ec2" not in svc:
        fails.append("service == %r (expected 'ec2')" % data.get("service"))
    # actual_uptime_pct = 98.5
    upt = data.get("actual_uptime_pct")
    try:
        upt_f = float(upt)
        if abs(upt_f - 98.5) > 0.01:
            fails.append("actual_uptime_pct == %r (expected 98.5)" % upt)
    except (TypeError, ValueError):
        fails.append("actual_uptime_pct not numeric: %r" % upt)
    # credit_pct must be 30 (95.0-99.0% tier)
    pct = data.get("credit_pct")
    try:
        pct_i = int(pct)
        if pct_i != 30:
            fails.append("credit_pct == %d (expected 30 for 95.0-99.0%% tier; 10%% is for 99.0-99.99%%)" % pct_i)
    except (TypeError, ValueError):
        fails.append("credit_pct not numeric: %r" % pct)
    # claim_deadline must be 2025-01-31
    deadline = str(data.get("claim_deadline") or "")
    if "2025-01-31" not in deadline and "2025-01" not in deadline:
        fails.append("claim_deadline == %r (expected 2025-01-31 for Nov 2024 incident)" % deadline)
    # source_url must reference aws.amazon.com/ec2/sla/
    src = str(data.get("source_url") or "")
    if "aws.amazon.com/ec2/sla" not in src:
        fails.append("source_url == %r (expected https://aws.amazon.com/ec2/sla/)" % src)
    # reviewer_signature must exist (P5)
    if "reviewer_signature" not in data:
        fails.append("reviewer_signature field missing (P5)")
    _finish(fails)
main()
