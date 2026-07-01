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
    rows, err = _read_csv(ws / "output" / "schedule_icu_stepdown.csv")
    if err: _finish([err])
    if not rows:
        _finish(["schedule_icu_stepdown.csv is empty"])
    req = {"date", "shift", "unit", "nurse_id", "patient_count", "ratio_computed"}
    missing = req - set(rows[0].keys())
    if missing:
        fails.append("missing columns: %s" % sorted(missing))
    if fails: _finish(fails)
    # 真值层：ratio limits
    for r in rows:
        unit = str(r.get("unit", "")).upper()
        ratio_str = str(r.get("ratio_computed", "")).strip()
        try:
            ratio = float(ratio_str)
        except (ValueError, TypeError):
            continues = True  # skip non-numeric
            continue
        if "ICU" in unit and ratio > 2.00 + 1e-9:
            fails.append("ICU shift ratio_computed == %.2f > 2.00 (date=%s)" % (ratio, r.get("date", "")))
        if "STEP" in unit and ratio > 3.00 + 1e-9:
            fails.append("Step-Down shift ratio_computed == %.2f > 3.00 (date=%s)" % (ratio, r.get("date", "")))
    # must have both units
    units_seen = {str(r.get("unit", "")).upper() for r in rows}
    if not any("ICU" in u for u in units_seen):
        fails.append("no ICU rows found in schedule")
    if not any("STEP" in u or "DOWN" in u for u in units_seen):
        fails.append("no Step-Down rows found in schedule")
    # 真值层 (A加难)：日期范围必须覆盖 2024-11-01 到 2024-11-14 全部 14 天
    import datetime
    expected_dates = set()
    d = datetime.date(2024, 11, 1)
    for _ in range(14):
        expected_dates.add(d.strftime("%Y-%m-%d"))
        d += datetime.timedelta(days=1)
    found_dates = {str(r.get("date", "")).strip() for r in rows}
    missing_dates = expected_dates - found_dates
    if missing_dates:
        fails.append(
            "schedule must cover all 14 days Nov 1-14 2024; missing dates: %s" % sorted(missing_dates)[:5])
    # 真值层 (A加难)：ICU 和 Step-Down 各有 ≥ 14 个不同日期
    icu_dates = {str(r.get("date","")) for r in rows if "ICU" in str(r.get("unit","")).upper()}
    sd_dates = {str(r.get("date","")) for r in rows if "STEP" in str(r.get("unit","")).upper() or "DOWN" in str(r.get("unit","")).upper()}
    if len(icu_dates) < 14:
        fails.append("ICU schedule covers only %d distinct dates (must cover all 14 days Nov 1-14)" % len(icu_dates))
    if len(sd_dates) < 14:
        fails.append("Step-Down schedule covers only %d distinct dates (must cover all 14 days Nov 1-14)" % len(sd_dates))
    _finish(fails)
main()
main()
