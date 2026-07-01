#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv
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

def _read_csv(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        with p.open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        return rows, None
    except Exception as e:
        return None, "CSV error in " + p.name + ": " + str(e)

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    rows, err = _read_csv(ws / "output" / "charge_nurse_violations.csv")
    if err: _finish([err])
    if not rows:
        _finish(["charge_nurse_violations.csv is empty"])
    # 结构层：必要字段
    req_fields = {"shift_id", "unit", "date"}
    for rf in req_fields:
        if rf not in rows[0]:
            fails.append("missing column %r" % rf)
    if fails: _finish(fails)
    # 字段层：ICU 班次存在
    icu_rows = [r for r in rows if "ICU" in str(r.get("unit", "")).upper()]
    if len(icu_rows) < 3:
        fails.append("fewer than 3 ICU rows with charge nurse error (got %d)" % len(icu_rows))
    # 真值层：ratio_excluding_charge > 2.0 for ICU rows
    icu_violation_count = 0
    for r in icu_rows:
        ratio_field = None
        for k in ("ratio_excluding_charge", "ratio_excl_charge", "actual_ratio", "ratio"):
            if k in r and r[k] not in ("", None):
                ratio_field = k
                break
        if ratio_field:
            try:
                ratio = float(r[ratio_field])
                if ratio > 2.0:
                    icu_violation_count += 1
            except (ValueError, TypeError):
                pass
    if icu_violation_count < 3:
        fails.append("fewer than 3 ICU charge-nurse-corrected shifts with ratio > 2.0 (got %d)" % icu_violation_count)
    # is_violation must be truthy for violation rows
    viol_col = None
    for k in ("is_violation", "violation", "is_shift_violation"):
        if k in rows[0]:
            viol_col = k
            break
    if viol_col:
        icu_true = [r for r in icu_rows if str(r.get(viol_col, "")).lower() in ("true", "1", "yes")]
        if len(icu_true) < 3:
            fails.append("fewer than 3 ICU rows with %s=True (got %d)" % (viol_col, len(icu_true)))
    # 真值层 (A加难)：shift_id 必须来自 SVMC_staffing_log_oct2024.csv 的真实记录
    # 源数据中 charge_nurse_included_error=True 的班次 ID 为 SH-2159, SH-2171, SH-2183
    EXPECTED_SHIFT_IDS = {"SH-2159", "SH-2171", "SH-2183"}
    found_ids = {str(r.get("shift_id", "")).strip() for r in icu_rows}
    missing_ids = EXPECTED_SHIFT_IDS - found_ids
    if missing_ids:
        fails.append(
            "shift_id mismatch: expected shift_ids %s from SVMC_staffing_log_oct2024.csv "
            "(charge_nurse_included_error=True rows), but not found. Got: %s" % (
                sorted(missing_ids), sorted(found_ids)[:5]))
    # 真值层 (A加难)：date 必须精确匹配 2024-10-05, 2024-10-06, 2024-10-07
    EXPECTED_DATES = {"2024-10-05", "2024-10-06", "2024-10-07"}
    found_dates = {str(r.get("date", "")).strip() for r in icu_rows}
    missing_dates = EXPECTED_DATES - found_dates
    if missing_dates:
        fails.append("missing expected violation dates %s (ICU charge nurse error dates from staffing log)" % sorted(missing_dates))
    _finish(fails)
main()
main()
