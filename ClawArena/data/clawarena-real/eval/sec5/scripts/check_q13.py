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
    data, err = _load_json(ws / "output" / "q13_vamp_revised.json")
    if err: _finish([err])

    for k in ("old_threshold_bps", "new_threshold_bps", "vamp_ratio_bps",
               "revised_is_excessive", "update_source", "source_url", "enforcement_date"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    old_t = int(data.get("old_threshold_bps", 0))
    if old_t != 220:
        fails.append(f"old_threshold_bps={old_t} (expected 220 — the superseded DRAFT value)")

    new_t = int(data.get("new_threshold_bps", 0))
    if new_t != 150:
        fails.append(f"new_threshold_bps={new_t} (expected 150 — authoritative after Update-2)")

    # C★ cross-round closure: vamp_ratio_bps must precisely match Q8 output (tolerance ±0.01)
    q8_data, q8_err = _load_json(ws / "output" / "q8_vamp_calc.json")
    if q8_err:
        # Fall back to direct calculation check
        ratio = float(data.get("vamp_ratio_bps", 0))
        expected = (42 + 18) / 3800 * 10000
        if abs(ratio - expected) > 0.01:
            fails.append(f"vamp_ratio_bps={ratio:.4f} (expected {expected:.4f}, tolerance ±0.01 bps)")
    else:
        q8_ratio = float(q8_data.get("vamp_ratio_bps", 0)) if q8_data else 0
        q13_ratio = float(data.get("vamp_ratio_bps", 0))
        if abs(q13_ratio - q8_ratio) > 0.01:
            fails.append(
                f"vamp_ratio_bps={q13_ratio:.4f} does not match Q8.vamp_ratio_bps={q8_ratio:.4f} "
                f"(cross-round closure requires exact match, tolerance ±0.01 bps)"
            )

    if data.get("revised_is_excessive") is not True:
        fails.append(f"revised_is_excessive={data.get('revised_is_excessive')} (expected True)")

    if not str(data.get("update_source", "")).strip():
        fails.append("update_source is empty — must reference Update-2 or the supersede email")

    if not str(data.get("source_url", "")).strip():
        fails.append("source_url is empty (P5)")

    # F-rule: enforcement_date must be exactly "2026-04-01" from the authoritative threshold file
    ed = str(data.get("enforcement_date", "")).strip()
    if ed != "2026-04-01":
        fails.append(f"enforcement_date={ed!r} must be exactly '2026-04-01' (from visa_vamp_thresholds_2026.json)")

    _finish(fails)
main()
