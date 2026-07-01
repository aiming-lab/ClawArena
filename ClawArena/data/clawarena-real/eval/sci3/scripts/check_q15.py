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

LEGAL_MAX = {"ICU": 2.0, "Med/Surg": 5.0, "Step-Down": 3.0, "Telemetry": 4.0,
             "ED": 4.0, "Psychiatric": 6.0}

def _get_legal_max(unit_str):
    u = str(unit_str).strip()
    for k, v in LEGAL_MAX.items():
        if k.lower() in u.lower() or u.lower() in k.lower():
            return v
    return None

def main():
    ws = Path(sys.argv[1]); fails = []
    rows, err = _read_csv(ws / "output" / "cdph_staffing_log_week2.csv")
    if err: _finish([err])
    if not rows:
        _finish(["cdph_staffing_log_week2.csv is empty"])
    req = {"date", "unit", "nurse_id", "license_type", "patient_count", "ratio"}
    missing = req - set(rows[0].keys())
    if missing:
        fails.append("missing columns: %s" % sorted(missing))
    if fails: _finish(fails)
    valid_lic = {"RN", "LVN", "PT"}
    for i, r in enumerate(rows):
        lic = str(r.get("license_type", "")).strip().upper()
        if lic not in valid_lic:
            fails.append("row %d: license_type %r not valid" % (i+1, lic))
            continue
        unit = str(r.get("unit", ""))
        try:
            pc = int(r.get("patient_count", 0))
        except (ValueError, TypeError):
            pc = 0
        if pc == 0:
            continue
        lm = _get_legal_max(unit)
        if lm is None:
            continue
        ratio_str = str(r.get("ratio", "")).strip()
        try:
            ratio = float(ratio_str)
            if ratio > lm + 1e-9:
                fails.append("row %d: ratio %.2f > legal max %.1f for unit %r" % (i+1, ratio, lm, unit))
        except (ValueError, TypeError):
            fails.append("row %d: ratio %r not numeric" % (i+1, ratio_str))
    # Update 2 requirement: ICU must have >= 3 float pool nurses per shift
    # Check: count distinct nurse_ids in ICU with patient_count > 0
    from collections import defaultdict
    icu_shift_nurses = defaultdict(set)
    for r in rows:
        if "icu" not in str(r.get("unit", "")).lower():
            continue
        try:
            pc = int(r.get("patient_count", 0))
        except (ValueError, TypeError):
            pc = 0
        if pc > 0:
            shift_key = (str(r.get("date", "")), str(r.get("shift_start", "")))
            icu_shift_nurses[shift_key].add(str(r.get("nurse_id", "")))
    if icu_shift_nurses:
        max_icu_nurses = max(len(v) for v in icu_shift_nurses.values())
        if max_icu_nurses < 3:
            fails.append("ICU must have >= 3 nurses per shift (Update 2 float pool requirement); max found: %d" % max_icu_nurses)
    else:
        fails.append("no ICU rows found in week2 log")
    _finish(fails)
main()
main()
