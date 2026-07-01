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
    data, err = _load_json(ws / "output" / "q15_weekly_report.json")
    if err: _finish([err])

    for k in ("total_alerts_batch001", "total_alerts_batch002", "vamp_ratio_bps",
               "vamp_threshold_bps", "vamp_status", "mc_program_tier",
               "sar_to_file_count", "source_url", "report_period",
               "investigation_period_days"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    rp = str(data.get("report_period", "")).strip()
    if rp != "2026-03-01 to 2026-03-17":
        fails.append(f"report_period={rp!r} (expected exactly '2026-03-01 to 2026-03-17')")

    if int(data.get("total_alerts_batch001", -1)) != 200:
        fails.append(f"total_alerts_batch001={data.get('total_alerts_batch001')} (expected 200)")
    if int(data.get("total_alerts_batch002", -1)) != 350:
        fails.append(f"total_alerts_batch002={data.get('total_alerts_batch002')} (expected 350)")

    # F-rule: investigation_period_days must be exactly 17 (2026-03-01 to 2026-03-17 inclusive)
    ipd = data.get("investigation_period_days")
    try:
        ipd_int = int(ipd)
    except (TypeError, ValueError):
        ipd_int = -1
    if ipd_int != 17:
        fails.append(f"investigation_period_days={ipd} (expected 17 — calendar days from 2026-03-01 to 2026-03-17 inclusive)")

    # C★ cross-round closure: vamp_ratio_bps must precisely match Q8 (tolerance ±0.01)
    q8_data, q8_err = _load_json(ws / "output" / "q8_vamp_calc.json")
    if q8_err:
        ratio = float(data.get("vamp_ratio_bps", 0))
        expected = (42 + 18) / 3800 * 10000
        if abs(ratio - expected) > 0.01:
            fails.append(f"vamp_ratio_bps={ratio:.4f} (expected {expected:.4f}, tolerance ±0.01 bps)")
    else:
        q8_ratio = float(q8_data.get("vamp_ratio_bps", 0)) if q8_data else 0
        q15_ratio = float(data.get("vamp_ratio_bps", 0))
        if abs(q15_ratio - q8_ratio) > 0.01:
            fails.append(
                f"vamp_ratio_bps={q15_ratio:.4f} does not match Q8.vamp_ratio_bps={q8_ratio:.4f} "
                f"(cross-round closure, tolerance ±0.01 bps)"
            )

    # vamp_ratio_bps must be exactly 2dp
    ratio_val = data.get("vamp_ratio_bps", 0)
    ratio_str = str(ratio_val)
    if "." in ratio_str:
        dp = len(ratio_str.split(".")[1])
        if dp > 2:
            fails.append(f"vamp_ratio_bps={ratio_str} has >2 decimal places (P4)")

    thr = int(data.get("vamp_threshold_bps", 0))
    if thr == 220:
        fails.append("vamp_threshold_bps=220 — Update-2 superseded this; must use 150")
    elif thr != 150:
        fails.append(f"vamp_threshold_bps={thr} (expected 150)")

    status = str(data.get("vamp_status", "")).upper()
    if status not in ("EXCESSIVE", "COMPLIANT"):
        fails.append(f"vamp_status={status!r} must be 'EXCESSIVE' or 'COMPLIANT'")
    if status != "EXCESSIVE":
        fails.append(f"vamp_status={status!r} — 157.89 bps > 150 bps threshold → should be EXCESSIVE")

    # C★ cross-round closure: mc_program_tier must exactly match Q11.program_tier
    q11_data, q11_err = _load_json(ws / "output" / "q11_mc_compliance.json")
    if q11_err:
        tier = str(data.get("mc_program_tier", "")).strip()
        if tier.upper() != "ECM":
            fails.append(f"mc_program_tier={tier!r} (expected 'ECM' per Q11)")
    else:
        q11_tier = str(q11_data.get("program_tier", "")).strip() if q11_data else ""
        q15_tier = str(data.get("mc_program_tier", "")).strip()
        if q11_tier and q15_tier.upper() != q11_tier.upper():
            fails.append(
                f"mc_program_tier={q15_tier!r} must exactly match Q11.program_tier={q11_tier!r} (cross-round consistency)"
            )
        if q15_tier.upper() != "ECM":
            fails.append(f"mc_program_tier={q15_tier!r} (expected 'ECM' per Q11)")

    sar_count = data.get("sar_to_file_count")
    try:
        sar_count_int = int(sar_count)
    except (TypeError, ValueError):
        sar_count_int = -1
    ocu_path = ws / "cases" / "open_cases_updated.json"
    if ocu_path.exists():
        import json as _json
        ocu = _json.loads(ocu_path.read_text(encoding="utf-8"))
        true_count = sum(1 for c in ocu.get("cases", []) if c.get("sar_required", False))
        if sar_count_int != true_count:
            fails.append(
                f"sar_to_file_count={sar_count_int} but open_cases_updated.json has {true_count} "
                f"sar_required=true cases — must match exactly"
            )
    else:
        if sar_count_int <= 0:
            fails.append(f"sar_to_file_count={sar_count_int} (expected a positive integer)")

    if not str(data.get("source_url", "")).strip():
        fails.append("source_url is empty (P5)")

    _finish(fails)
main()
