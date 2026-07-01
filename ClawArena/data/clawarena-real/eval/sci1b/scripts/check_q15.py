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
    data, err = _load_json(ws / "output" / "q15_case_summary.json")
    if err: _finish([err])
    pnas = data.get("pnas_study1") or {}
    wc   = data.get("why_connect") or {}
    try:
        n = int(pnas.get("n_total"))
        if n != 101:
            fails.append("pnas_study1.n_total == %d (expected exactly 101)" % n)
    except (TypeError, ValueError):
        fails.append("pnas_study1.n_total not int")
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
    try:
        pp = float(pnas.get("p_puzzle"))
        if abs(pp - 0.0013) > 1e-9:
            fails.append("pnas_study1.p_puzzle == %r (expected exactly 0.0013)" % pnas.get("p_puzzle"))
    except (TypeError, ValueError):
        fails.append("pnas_study1.p_puzzle not numeric")
    try:
        if int(pnas.get("suspicious_rows")) != 8:
            fails.append("pnas_study1.suspicious_rows == %r (expected 8)" % pnas.get("suspicious_rows"))
    except (TypeError, ValueError):
        fails.append("pnas_study1.suspicious_rows not int")
    # puzzle_pct tightened to ±1 (true: 82, 43)
    try:
        pb15 = int(pnas.get("puzzle_bottom_pct"))
        if not (81 <= pb15 <= 83):
            fails.append("pnas_study1.puzzle_bottom_pct == %d (expected 82 ±1)" % pb15)
    except (TypeError, ValueError):
        fails.append("pnas_study1.puzzle_bottom_pct missing or not int")
    try:
        pt15 = int(pnas.get("puzzle_top_pct"))
        if not (42 <= pt15 <= 44):
            fails.append("pnas_study1.puzzle_top_pct == %d (expected 43 ±1)" % pt15)
    except (TypeError, ValueError):
        fails.append("pnas_study1.puzzle_top_pct missing or not int")
    # C+F: p_expense must be exactly 0.0014 (from statistical_reference.json)
    pe15 = pnas.get("p_expense")
    try:
        pe15f = float(pe15)
        if abs(pe15f - 0.0014) > 1e-9:
            fails.append("pnas_study1.p_expense == %r (expected exactly 0.0014; read from statistical_reference.json)" % pe15)
    except (TypeError, ValueError):
        fails.append("pnas_study1.p_expense missing or not numeric (expected 0.0014 from statistical_reference.json)")
    # C+F: word_rating_mismatch_count from part4_why_connect.md
    wm15 = wc.get("word_rating_mismatch_count")
    try:
        if int(wm15) != 18:
            fails.append("why_connect.word_rating_mismatch_count == %r (expected 18, from part4_why_connect.md)" % wm15)
    except (TypeError, ValueError):
        fails.append("why_connect.word_rating_mismatch_count missing or not int (expected 18; read part4_why_connect.md)")
    # C+F: prevention_corr_p from part4_why_connect.md
    pcp15 = wc.get("prevention_corr_p")
    try:
        pcp15f = float(pcp15)
        if not (0.025 <= pcp15f <= 0.027):
            fails.append("why_connect.prevention_corr_p == %r (expected 0.026 ±0.001; read part4_why_connect.md)" % pcp15)
    except (TypeError, ValueError):
        fails.append("why_connect.prevention_corr_p missing or not numeric (expected 0.026; read part4_why_connect.md)")
    # why_connect F-stat
    try:
        f = float(wc.get("F_stat"))
        if not (17.59 <= f <= 17.79):
            fails.append("why_connect.F_stat == %.4f (expected near 17.69)" % f)
    except (TypeError, ValueError):
        fails.append("why_connect.F_stat not numeric")
    try:
        if int(wc.get("df1")) != 2:
            fails.append("why_connect.df1 == %r (expected 2)" % wc.get("df1"))
        if int(wc.get("df2")) != 596:
            fails.append("why_connect.df2 == %r (expected 596)" % wc.get("df2"))
    except (TypeError, ValueError):
        fails.append("why_connect.df1 or df2 not int")
    try:
        if int(data.get("retraction_count")) != 4:
            fails.append("retraction_count == %r (expected 4)" % data.get("retraction_count"))
    except (TypeError, ValueError):
        fails.append("retraction_count not int")
    pfm = str(data.get("primary_forensic_method") or "").lower()
    if "calcchain" not in pfm:
        fails.append("primary_forensic_method == %r (must contain 'calcChain')" % data.get("primary_forensic_method"))
    _finish(fails)
main()
