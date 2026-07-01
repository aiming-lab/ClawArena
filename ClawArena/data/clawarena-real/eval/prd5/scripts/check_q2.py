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
    data, err = _load_json(ws / "output" / "q2_srm_exp002.json")
    if err: _finish([err])
    # Structure check
    for key in ("chi2_stat", "p_value", "srm_detected"):
        if key not in data:
            fails.append("missing key: %s" % key)
    if fails: _finish(fails)
    # True-value check
    try:
        chi2 = float(data["chi2_stat"])
    except (TypeError, ValueError):
        _finish(["chi2_stat not numeric: %r" % data["chi2_stat"]])
    # chi2 = (5234-5062.5)^2/5062.5 + (4891-5062.5)^2/5062.5 = 11.7... +/- 10%
    if not (9.0 <= chi2 <= 15.0):
        fails.append("chi2_stat == %.4f (expected ~11.83 ±tolerance)" % chi2)
    try:
        pv = float(data["p_value"])
    except (TypeError, ValueError):
        _finish(["p_value not numeric: %r" % data["p_value"]])
    if pv >= 0.01:
        fails.append("p_value == %.6f (expected < 0.01 — SRM clearly detected)" % pv)
    if data.get("srm_detected") is not True:
        fails.append("srm_detected == %r (expected true)" % data.get("srm_detected"))
    _finish(fails)
main()
