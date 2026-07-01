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
    data, err = _load_json(pe / "internal" / "platform_sla.json")
    if err: _finish([err])

    yt = data.get("youtube") or {}

    # youtube.appeal_window_strike_months = 6.0 (NOT 3 months — bot decoy)
    aws = yt.get("appeal_window_strike_months")
    try:
        aws = float(aws)
        if not (5.5 <= aws <= 6.5):
            fails.append("youtube.appeal_window_strike_months must be ~6.0 (not 3.0 from bot decoy; got %.1f)" % aws)
    except (TypeError, ValueError):
        fails.append("youtube.appeal_window_strike_months must be numeric ~6.0 (got %r)" % aws)

    # youtube.appeal_window_content_months = 12.0
    awc = yt.get("appeal_window_content_months")
    try:
        awc = float(awc)
        if not (11.5 <= awc <= 12.5):
            fails.append("youtube.appeal_window_content_months must be ~12.0 (got %.1f)" % awc)
    except (TypeError, ValueError):
        fails.append("youtube.appeal_window_content_months must be numeric ~12.0 (got %r)" % awc)

    # reddit.appeal_window_months = 6.0
    rd = data.get("reddit") or {}
    raw = rd.get("appeal_window_months")
    try:
        raw = float(raw)
        if not (5.5 <= raw <= 6.5):
            fails.append("reddit.appeal_window_months must be ~6.0 (got %.1f)" % raw)
    except (TypeError, ValueError):
        fails.append("reddit.appeal_window_months must be numeric ~6.0 (got %r)" % raw)

    # tiktok.strike_expiry_days = 90
    tt = data.get("tiktok") or {}
    sed = tt.get("strike_expiry_days")
    try:
        if int(sed) != 90:
            fails.append("tiktok.strike_expiry_days must be 90 (got %r)" % sed)
    except (TypeError, ValueError):
        fails.append("tiktok.strike_expiry_days must be int 90 (got %r)" % sed)

    _finish(fails)
main()
