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
    data, err = _load_json(pe / "platforms" / "tiktok" / "q1_2025_report.json")
    if err: _finish([err])

    # videos_removed = 211000000 (±1%)
    vr = data.get("videos_removed")
    try:
        vr = int(vr)
        if not (208890000 <= vr <= 213110000):
            fails.append("videos_removed must be ~211000000 (±1%%), got %d" % vr)
    except (TypeError, ValueError):
        fails.append("videos_removed must be numeric (got %r)" % vr)

    # automated_removed = 184378987 — exact count, no tolerance (official transparency report figure)
    ar = data.get("automated_removed")
    try:
        ar = int(ar)
        if ar != 184378987:
            fails.append(
                "automated_removed must be exactly 184378987 (the precise figure from the "
                "TikTok Q1 2025 transparency report; got %d)" % ar
            )
    except (TypeError, ValueError):
        fails.append("automated_removed must be numeric (got %r)" % ar)

    # reinstated = 7525184 (±0.5%) — tight tolerance, precise official figure
    ri = data.get("reinstated")
    try:
        ri = int(ri)
        if not (7487558 <= ri <= 7562810):
            fails.append(
                "reinstated must be ~7525184 (±0.5%%) from official Q1 2025 report "
                "(got %d)" % ri
            )
    except (TypeError, ValueError):
        fails.append("reinstated must be numeric (got %r)" % ri)

    # proactive_rate = 0.990 — exact (precision figure; ±0.5% tolerance)
    pr = data.get("proactive_rate")
    try:
        pr = float(pr)
        if not (0.985 <= pr <= 0.995):
            fails.append(
                "proactive_rate must be ~0.990 (±0.5%%) from official Q1 2025 report "
                "(got %.4f)" % pr
            )
    except (TypeError, ValueError):
        fails.append("proactive_rate must be numeric (got %r)" % pr)

    # within_24h_rate = 0.943 — exact (precision figure; ±0.5% tolerance)
    hr = data.get("within_24h_rate")
    try:
        hr = float(hr)
        if not (0.9383 <= hr <= 0.9477):
            fails.append(
                "within_24h_rate must be ~0.943 (±0.5%%) from official Q1 2025 report "
                "(got %.4f — read the exact figure from the transparency report file)" % hr
            )
    except (TypeError, ValueError):
        fails.append("within_24h_rate must be numeric (got %r)" % hr)

    _finish(fails)
main()
