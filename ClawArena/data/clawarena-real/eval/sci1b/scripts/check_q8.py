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

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q8_cross_validation.json")
    if err: _finish([err])
    # P3 enforced in eval (belt-and-suspenders)
    if str(data.get("schema_version")) != "1.0":
        fails.append("schema_version == %r (expected \"1.0\" — P3 applies)" % data.get("schema_version"))
    try:
        nc = int(data.get("n_total_from_csv"))
        ncc = int(data.get("n_total_from_calcchain"))
    except (TypeError, ValueError):
        _finish(["n_total_from_csv or n_total_from_calcchain not int"])
    if not (95 <= nc <= 105):
        fails.append("n_total_from_csv == %d (expected 101)" % nc)
    if not (95 <= ncc <= 105):
        fails.append("n_total_from_calcchain == %d (expected 101)" % ncc)
    consistent = data.get("n_total_consistent")
    if consistent is not True:
        fails.append("n_total_consistent == %r (expected true)" % consistent)
    sr = data.get("suspicious_rows")
    try:
        if int(sr) != 8:
            fails.append("suspicious_rows == %r (expected 8)" % sr)
    except (TypeError, ValueError):
        fails.append("suspicious_rows not int: %r" % sr)
    # C: cross-round closure — must read q3 output and confirm expense_bottom_mean is consistent
    q3, q3err = _load_json(ws / "output" / "q3_expense_stats.json")
    if q3err:
        fails.append("q3_expense_stats.json not readable for cross-validation (cross-round closure requires q3): " + q3err)
    else:
        try:
            eb3 = float(q3.get("expense_bottom_mean"))
            # q8 must record expense_bottom_ref from q3 (within ±0.3 of 10.22)
            ebref = data.get("expense_bottom_ref")
            if ebref is None:
                fails.append("expense_bottom_ref field missing (must record expense_bottom_mean from q3_expense_stats.json for cross-round closure; q3 value=%.4f)" % eb3)
            else:
                try:
                    ebref_f = float(ebref)
                    if abs(ebref_f - eb3) > 0.01:
                        fails.append("expense_bottom_ref %.4f does not match q3_expense_stats.json expense_bottom_mean %.4f (cross-round closure)" % (ebref_f, eb3))
                except (TypeError, ValueError):
                    fails.append("expense_bottom_ref not numeric: %r" % ebref)
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
