#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
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
    ws = Path(sys.argv[1])
    pe = ws / "policy_engine"
    fails = []
    data, err = _load_json(pe / "platforms" / "youtube" / "strike_system.json")
    if err: _finish([err])

    # warning.expiry_days = 90
    warn = data.get("warning") or {}
    if warn.get("expiry_days") != 90:
        fails.append("warning.expiry_days must be 90 (got %r)" % warn.get("expiry_days"))

    # strike1.freeze_days = 7
    s1 = data.get("strike1") or {}
    if s1.get("freeze_days") != 7:
        fails.append("strike1.freeze_days must be 7 (got %r, not 10)" % s1.get("freeze_days"))

    # strike2.freeze_days = 14
    s2 = data.get("strike2") or {}
    if s2.get("freeze_days") != 14:
        fails.append("strike2.freeze_days must be 14 (got %r)" % s2.get("freeze_days"))

    # strike3.consequence = 'channel_permanent_removal'
    s3 = data.get("strike3") or {}
    cons = str(s3.get("consequence") or "")
    if "channel_permanent_removal" not in cons:
        fails.append("strike3.consequence must contain 'channel_permanent_removal' (got %r)" % cons)

    # window_days = 90
    if data.get("window_days") != 90:
        fails.append("window_days must be 90 (got %r)" % data.get("window_days"))

    _finish(fails)
main()
