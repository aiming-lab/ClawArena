#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, math
from pathlib import Path

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON: " + str(e)

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
    data, err = _load_json(ws / "output" / "q13_bonferroni_correction.json")
    if err: _finish([err])
    for key in ("alpha_adjusted", "method", "n_tests", "significant_metrics"):
        if key not in data:
            fails.append("missing key: %s" % key)
    if fails: _finish(fails)
    method = str(data.get("method", "")).lower()
    # V10: must be bonferroni (NOT benjamini_hochberg — VP email was superseded)
    if "bonferroni" not in method:
        fails.append("method == %r (must be bonferroni — VP BH directive was superseded by CFO notice)" % data.get("method"))
    if "benjamini" in method or "bh" in method.replace("bonferroni", ""):
        fails.append("method must NOT be BH (the VP email using BH was superseded)")
    try:
        n = int(data["n_tests"])
        aa = float(data["alpha_adjusted"])
        sm = int(data["significant_metrics"])
    except (TypeError, ValueError) as e:
        _finish(["non-numeric field: %s" % e])
    if n != 8:
        fails.append("n_tests == %d (expected 8 secondary metrics)" % n)
    # alpha_adjusted = 0.05/8 = 0.00625
    if not (0.005 <= aa <= 0.008):
        fails.append("alpha_adjusted == %.6f (expected 0.05/8=0.00625)" % aa)
    # significant_metrics should be 0 (none of the given p-values < 0.00625)
    if sm < 0:
        fails.append("significant_metrics cannot be negative: %d" % sm)
    _finish(fails)
main()
