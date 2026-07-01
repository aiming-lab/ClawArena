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
    data, err = _load_json(ws / "output" / "q3_expense_stats.json")
    if err: _finish([err])
    try:
        eb = float(data.get("expense_bottom_mean"))
        et = float(data.get("expense_top_mean"))
    except (TypeError, ValueError):
        _finish(["expense_bottom_mean or expense_top_mean not numeric"])
    # True values computed from pnas_study1_dataset.csv: bottom=10.2226, top=5.7998
    # Tolerance ±0.3
    if not (9.92 <= eb <= 10.52):
        fails.append("expense_bottom_mean == %.4f (expected near 10.22, within 9.92-10.52; read pnas_study1_dataset.csv)" % eb)
    if not (5.50 <= et <= 6.10):
        fails.append("expense_top_mean == %.4f (expected near 5.80, within 5.50-6.10; read pnas_study1_dataset.csv)" % et)
    n = data.get("n_total")
    try:
        if int(n) != 101:
            fails.append("n_total == %d (expected exactly 101)" % int(n))
    except (TypeError, ValueError):
        fails.append("n_total not int: %r" % n)
    # C: require n_bottom and n_top explicitly (cross-check with q2)
    nb = data.get("n_bottom")
    nt = data.get("n_top")
    try:
        nb_i = int(nb)
        nt_i = int(nt)
        if nb_i != 50:
            fails.append("n_bottom == %d (expected 50, from pnas_study1_dataset.csv)" % nb_i)
        if nt_i != 51:
            fails.append("n_top == %d (expected 51, from pnas_study1_dataset.csv)" % nt_i)
        if nb_i + nt_i != 101:
            fails.append("n_bottom + n_top == %d (must sum to n_total 101)" % (nb_i + nt_i))
    except (TypeError, ValueError):
        fails.append("n_bottom and n_top must both be present and integer (got bottom=%r, top=%r)" % (nb, nt))
    # C: cross-check n_total against calcchain_reference.json
    calcchain_path = ws / "cases" / "gino" / "raw_data_analysis" / "calcchain_reference.json"
    ccref, ccerr = _load_json(calcchain_path)
    if ccerr:
        fails.append("calcchain_reference.json not readable for cross-check: " + ccerr)
    else:
        cc_n = ccref.get("n_total")
        try:
            if int(cc_n) != int(n):
                fails.append("n_total %d does not match calcchain_reference.json n_total %d (cross-round consistency)" % (int(n), int(cc_n)))
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
