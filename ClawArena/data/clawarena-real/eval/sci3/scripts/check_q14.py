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
    data, err = _load_json(ws / "output" / "ca_vs_or_comparison.json")
    if err: _finish([err])
    # top-level penalty fields
    or_pen = data.get("or_penalty_max_usd")
    ca_pen = data.get("ca_first_violation_usd")
    try:
        if int(or_pen) != 5000:
            fails.append("or_penalty_max_usd == %r (expected 5000 per OR HB 2697)" % or_pen)
    except (TypeError, ValueError):
        fails.append("or_penalty_max_usd not an int: %r" % or_pen)
    try:
        if int(ca_pen) != 15000:
            fails.append("ca_first_violation_usd == %r (expected 15000 per H&SC § 1280.3)" % ca_pen)
    except (TypeError, ValueError):
        fails.append("ca_first_violation_usd not an int: %r" % ca_pen)
    # units array
    units = data.get("units") or []
    if not isinstance(units, list) or len(units) < 2:
        fails.append("units array must have at least 2 entries")
        _finish(fails)
    def norm(s): return str(s).lower().replace("-", "").replace("/", "").replace(" ", "")
    by_unit = {norm(e.get("unit", "")): e for e in units if isinstance(e, dict)}
    # ICU: ca=2, or2024=2, or2026=2
    icu = None
    for k in ("icu", "intensivecareunit", "criticalcare"):
        if k in by_unit:
            icu = by_unit[k]; break
    if icu:
        for field, expected in [("ca_ratio", 2), ("or_ratio_2024", 2), ("or_ratio_2026", 2)]:
            try:
                if int(icu.get(field, -1)) != expected:
                    fails.append("ICU %s == %r (expected %d)" % (field, icu.get(field), expected))
            except (TypeError, ValueError):
                fails.append("ICU %s not an int: %r" % (field, icu.get(field)))
    else:
        fails.append("no ICU entry in units array")
    # Med/Surg: ca=5, or2024=5, or2026=4, or_stricter_by_2026=true
    ms = None
    for k in ("medsurg", "medicalsurgical", "medicalsurg"):
        if k in by_unit:
            ms = by_unit[k]; break
    if ms:
        for field, expected in [("ca_ratio", 5), ("or_ratio_2024", 5), ("or_ratio_2026", 4)]:
            try:
                if int(ms.get(field, -1)) != expected:
                    fails.append("Med/Surg %s == %r (expected %d)" % (field, ms.get(field), expected))
            except (TypeError, ValueError):
                fails.append("Med/Surg %s not an int: %r" % (field, ms.get(field)))
        if ms.get("or_stricter_by_2026") is not True:
            fails.append("Med/Surg or_stricter_by_2026 must be true (OR goes to 1:4 in 2026, CA stays 1:5)")
    else:
        fails.append("no Med/Surg entry in units array")
    _finish(fails)
main()
main()
