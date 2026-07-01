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
    data, err = _load_json(ws / "output" / "q7_multi_test_correction.json")
    if err: _finish([err])
    for key in ("bh_significant", "method", "n_tests", "raw_significant"):
        if key not in data:
            fails.append("missing key: %s" % key)
    if fails: _finish(fails)
    method = str(data.get("method", "")).lower()
    if "benjamini" not in method and "bh" not in method:
        fails.append("method == %r (expected benjamini_hochberg or bh)" % data.get("method"))
    try:
        n = int(data["n_tests"])
        raw = int(data["raw_significant"])
        bh = int(data["bh_significant"])
    except (TypeError, ValueError) as e:
        _finish(["non-integer field: %s" % e])
    if n != 3:
        fails.append("n_tests == %d (expected 3 pairwise comparisons)" % n)
    # All 3 p-values (0.31, 0.43, 0.67) > 0.05, so raw_significant = 0
    if raw != 0:
        fails.append("raw_significant == %d (expected 0: p-values 0.31,0.43,0.67 all > 0.05)" % raw)
    if bh != 0:
        fails.append("bh_significant == %d (expected 0: no p-value passes BH with these values)" % bh)
    _finish(fails)
main()
