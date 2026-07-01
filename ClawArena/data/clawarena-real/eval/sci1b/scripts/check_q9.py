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
    data, err = _load_json(ws / "output" / "q9_comprehensive_stats.json")
    if err: _finish([err])
    pnas = data.get("pnas_study1") or {}
    wc   = data.get("why_connect") or {}
    try:
        n = int(pnas.get("n_total"))
        if n != 101:
            fails.append("pnas_study1.n_total == %d (expected exactly 101)" % n)
    except (TypeError, ValueError):
        fails.append("pnas_study1.n_total not int: %r" % pnas.get("n_total"))
    # expense anchors tightened to ±0.3 (true values: bottom=10.2226, top=5.7998)
    try:
        eb = float(pnas.get("expense_bottom"))
        if not (9.92 <= eb <= 10.52):
            fails.append("pnas_study1.expense_bottom == %.4f (expected near 10.22, within 9.92-10.52)" % eb)
    except (TypeError, ValueError):
        fails.append("pnas_study1.expense_bottom not numeric")
    try:
        et = float(pnas.get("expense_top"))
        if not (5.50 <= et <= 6.10):
            fails.append("pnas_study1.expense_top == %.4f (expected near 5.80, within 5.50-6.10)" % et)
    except (TypeError, ValueError):
        fails.append("pnas_study1.expense_top not numeric")
    # puzzle overreport percentages (true: bottom=82, top=43); tightened ±1
    try:
        pb9 = int(pnas.get("puzzle_bottom_pct"))
        if not (81 <= pb9 <= 83):
            fails.append("pnas_study1.puzzle_bottom_pct == %d (expected 82 ±1)" % pb9)
    except (TypeError, ValueError):
        fails.append("pnas_study1.puzzle_bottom_pct missing or not int")
    try:
        pt9 = int(pnas.get("puzzle_top_pct"))
        if not (42 <= pt9 <= 44):
            fails.append("pnas_study1.puzzle_top_pct == %d (expected 43 ±1)" % pt9)
    except (TypeError, ValueError):
        fails.append("pnas_study1.puzzle_top_pct missing or not int")
    # p_puzzle must be exactly 0.0013
    try:
        pp9 = float(pnas.get("p_puzzle"))
        if abs(pp9 - 0.0013) > 1e-9:
            fails.append("pnas_study1.p_puzzle == %r (expected exactly 0.0013)" % pnas.get("p_puzzle"))
    except (TypeError, ValueError):
        fails.append("pnas_study1.p_puzzle missing or not numeric")
    # suspicious_rows
    try:
        if int(pnas.get("suspicious_rows")) != 8:
            fails.append("pnas_study1.suspicious_rows == %r (expected 8)" % pnas.get("suspicious_rows"))
    except (TypeError, ValueError):
        fails.append("pnas_study1.suspicious_rows not int")
    # C+F: p_expense must be exactly 0.0014 (from statistical_reference.json)
    pe9 = pnas.get("p_expense")
    try:
        pe9f = float(pe9)
        if abs(pe9f - 0.0014) > 1e-9:
            fails.append("pnas_study1.p_expense == %r (expected exactly 0.0014; read from cases/gino/raw_data_analysis/statistical_reference.json)" % pe9)
    except (TypeError, ValueError):
        fails.append("pnas_study1.p_expense missing or not numeric (expected 0.0014 from statistical_reference.json)")
    # V4: F_stat closure
    try:
        f = float(wc.get("F_stat"))
        if not (17.59 <= f <= 17.79):
            fails.append("why_connect.F_stat == %.4f (expected near 17.69, not ~20)" % f)
    except (TypeError, ValueError):
        fails.append("why_connect.F_stat not numeric: %r" % wc.get("F_stat"))
    try:
        if int(wc.get("df1")) != 2:
            fails.append("why_connect.df1 == %r (expected 2)" % wc.get("df1"))
        if int(wc.get("df2")) != 596:
            fails.append("why_connect.df2 == %r (expected 596)" % wc.get("df2"))
    except (TypeError, ValueError):
        fails.append("why_connect.df1 or df2 not int")
    _finish(fails)
main()
