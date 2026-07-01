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
    data, err = _load_json(ws / "reports" / "fmla_timeline.json")
    if err: _finish([err])
    # fmla_start_date
    fsd = str(data.get("fmla_start_date") or "")
    if "2025-08-15" not in fsd:
        fails.append("fmla_start_date must contain 2025-08-15 (got %r)" % fsd)
    # fmla_end_date: 12 weeks = 84 days from 2025-08-15 = 2025-11-07
    fed = str(data.get("fmla_end_date") or "")
    if "2025-11-07" not in fed:
        fails.append("fmla_end_date must contain 2025-11-07 (12 weeks from 2025-08-15; got %r)" % fed)
    # termination_date: must be 2025-09-12 (personnel file), NOT 2025-09-10 (Slack DM — V1 decoy)
    td = str(data.get("termination_date") or "")
    if "2025-09-12" not in td:
        fails.append("termination_date must be 2025-09-12 per personnel file (not 2025-09-10 from Slack DM — that is a V1 multi-source conflict; personnel file is authoritative)")
    # in_protection_window
    if data.get("in_protection_window") is not True:
        fails.append("in_protection_window must be true (2025-09-12 is within 2025-08-15 to 2025-11-07)")
    # risk_level
    rl = str(data.get("risk_level") or "").upper()
    if rl != "HIGH":
        fails.append("risk_level must be HIGH (got %r)" % data.get("risk_level"))
    _finish(fails)
main()
