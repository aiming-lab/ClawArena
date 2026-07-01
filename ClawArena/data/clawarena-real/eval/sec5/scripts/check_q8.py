#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, subprocess
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
    data, err = _load_json(ws / "output" / "q8_vamp_calc.json")
    if err: _finish([err])

    for k in ("tc40_count", "tc15_count", "tc05_count", "vamp_ratio_bps",
               "threshold_bps", "is_excessive", "source_url"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    if int(data.get("tc40_count", -1)) != 42:
        fails.append(f"tc40_count={data.get('tc40_count')} (expected 42)")
    if int(data.get("tc15_count", -1)) != 18:
        fails.append(f"tc15_count={data.get('tc15_count')} (expected 18)")
    if int(data.get("tc05_count", -1)) != 3800:
        fails.append(f"tc05_count={data.get('tc05_count')} (expected 3800)")

    ratio = float(data.get("vamp_ratio_bps", 0))
    expected_ratio = (42 + 18) / 3800 * 10000  # = 157.8947...
    if abs(ratio - expected_ratio) > 0.1:
        fails.append(f"vamp_ratio_bps={ratio:.4f} (expected {expected_ratio:.4f}, tolerance ±0.1 bps)")

    # Must use 150 bps, NOT the DRAFT 220 bps
    thr = int(data.get("threshold_bps", 0))
    if thr == 220:
        fails.append("threshold_bps=220 — this is from the DRAFT (red herring); must use 150 from visa_vamp_thresholds_2026.json")
    elif thr != 150:
        fails.append(f"threshold_bps={thr} (expected 150 from authoritative file)")

    # is_excessive must be True (157.89 > 150)
    if data.get("is_excessive") is not True:
        fails.append(f"is_excessive={data.get('is_excessive')} (expected True — 157.89 > 150 bps)")

    if not str(data.get("source_url", "")).strip():
        fails.append("source_url is empty — P5 requires regulatory citations include source_url")

    _finish(fails)
main()
