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
    data, err = _load_json(pe / "reports" / "cross_validation.json")
    if err: _finish([err])

    yt = data.get("youtube") or {}
    meta = data.get("meta") or {}
    tt = data.get("tiktok") or {}

    # youtube.strike1_freeze_days must be 7 (from Q2 file)
    s1d = yt.get("strike1_freeze_days")
    try:
        if int(s1d) != 7:
            fails.append("cross_validation: youtube.strike1_freeze_days must be 7 (got %r)" % s1d)
    except (TypeError, ValueError):
        fails.append("cross_validation: youtube.strike1_freeze_days must be int 7 (got %r)" % s1d)

    # meta.strike9_ban_days must be 7 (from Q3 file)
    s9d = meta.get("strike9_ban_days")
    try:
        if int(s9d) != 7:
            fails.append("cross_validation: meta.strike9_ban_days must be 7 (got %r)" % s9d)
    except (TypeError, ValueError):
        fails.append("cross_validation: meta.strike9_ban_days must be int 7 (got %r)" % s9d)

    # tiktok.videos_removed_q1_2025 must be 211000000 (±1%)
    tvr = tt.get("videos_removed_q1_2025")
    try:
        tvr = int(tvr)
        if not (208890000 <= tvr <= 213110000):
            fails.append("cross_validation: tiktok.videos_removed_q1_2025 must be ~211000000 (±1%%), got %d" % tvr)
    except (TypeError, ValueError):
        fails.append("cross_validation: tiktok.videos_removed_q1_2025 must be numeric (got %r)" % tvr)

    # Cross-verify against actual source files (V4 closure)
    yt_src, yt_err = _load_json(pe / "platforms" / "youtube" / "strike_system.json")
    if not yt_err and yt_src:
        actual_s1 = (yt_src.get("strike1") or {}).get("freeze_days")
        try:
            if int(actual_s1) != int(s1d):
                fails.append("cross_validation drift: youtube.strike1_freeze_days %r != actual %r in strike_system.json" % (s1d, actual_s1))
        except (TypeError, ValueError):
            pass

    tt_src, tt_err = _load_json(pe / "platforms" / "tiktok" / "q1_2025_report.json")
    if not tt_err and tt_src:
        actual_vr = tt_src.get("videos_removed")
        try:
            if int(actual_vr) != int(tvr):
                fails.append("cross_validation drift: tiktok.videos_removed_q1_2025 %r != actual %r in q1_2025_report.json" % (tvr, actual_vr))
        except (TypeError, ValueError):
            pass

    _finish(fails)
main()
