#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, math
from pathlib import Path

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON: " + str(e)

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
    data, err = _load_json(ws / "output" / "q12_cuped_eligibility.json")
    if err: _finish([err])
    for key in ("eligible", "pct_coverage", "reason", "units_with_pre_data"):
        if key not in data:
            fails.append("missing key: %s" % key)
    if fails: _finish(fails)
    # eligible must be True (640 > 100 AND 8% > 5%)
    if data.get("eligible") is not True:
        fails.append("eligible == %r (expected true: 640 units > 100, coverage=8%% > 5%%)" % data.get("eligible"))
    try:
        units = int(data["units_with_pre_data"])
        pct = float(data["pct_coverage"])
    except (TypeError, ValueError) as e:
        _finish(["non-numeric field: %s" % e])
    if not (580 <= units <= 700):
        fails.append("units_with_pre_data == %d (expected ~640 for exp005 from pre_experiment_metrics.csv)" % units)
    if not (6.0 <= pct <= 10.0):
        fails.append("pct_coverage == %.2f%% (expected ~8%% = 640/8000)" % pct)
    # reason must mention 7-day pre-experiment window (V9 verbatim)
    reason = str(data.get("reason", "")).lower()
    if "7" not in reason and "seven" not in reason:
        fails.append("reason must reference the 7-day pre-experiment window (Statsig Cloud default)")
    _finish(fails)
main()
