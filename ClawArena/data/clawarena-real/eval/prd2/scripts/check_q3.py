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
    data, err = _load_json(pe / "platforms" / "meta" / "strike_system.json")
    if err: _finish([err])

    strikes = data.get("strikes") or {}

    # strike_7.content_ban_days = 1 (NOT 3 — email/bot error)
    s7 = strikes.get("strike_7") or {}
    s7_days = s7.get("content_ban_days")
    try:
        if int(s7_days) != 1:
            fails.append("strike_7.content_ban_days must be 1 (the email claiming 3 days is WRONG; official value is 1 day; got %r)" % s7_days)
    except (TypeError, ValueError):
        fails.append("strike_7.content_ban_days must be int 1 (got %r)" % s7_days)

    # strike_8.content_ban_days = 3
    s8 = strikes.get("strike_8") or {}
    s8_days = s8.get("content_ban_days")
    try:
        if int(s8_days) != 3:
            fails.append("strike_8.content_ban_days must be 3 (got %r)" % s8_days)
    except (TypeError, ValueError):
        fails.append("strike_8.content_ban_days must be int 3 (got %r)" % s8_days)

    # strike_9.content_ban_days = 7
    s9 = strikes.get("strike_9") or {}
    s9_days = s9.get("content_ban_days")
    try:
        if int(s9_days) != 7:
            fails.append("strike_9.content_ban_days must be 7 (got %r)" % s9_days)
    except (TypeError, ValueError):
        fails.append("strike_9.content_ban_days must be int 7 (got %r)" % s9_days)

    # strike_10plus.content_ban_days = 30
    s10 = strikes.get("strike_10plus") or {}
    s10_days = s10.get("content_ban_days")
    try:
        if int(s10_days) != 30:
            fails.append("strike_10plus.content_ban_days must be 30 (got %r)" % s10_days)
    except (TypeError, ValueError):
        fails.append("strike_10plus.content_ban_days must be int 30 (got %r)" % s10_days)

    _finish(fails)
main()
