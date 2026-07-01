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
    data, err = _load_json(ws / "output" / "q6_peeking_analysis.json")
    if err: _finish([err])
    for key in ("actual_fpr", "nominal_fpr", "ratio"):
        if key not in data:
            fails.append("missing key: %s" % key)
    if fails: _finish(fails)
    try:
        afpr = float(data["actual_fpr"])
        nfpr = float(data["nominal_fpr"])
        ratio = float(data["ratio"])
    except (TypeError, ValueError) as e:
        _finish(["non-numeric field: %s" % e])
    # actual_fpr must be 0.57 (exact Optimizely value)
    if not (0.55 <= afpr <= 0.59):
        fails.append("actual_fpr == %.4f (expected 0.57 from Optimizely blog)" % afpr)
    # nominal_fpr must be 0.05
    if not (0.04 <= nfpr <= 0.06):
        fails.append("nominal_fpr == %.4f (expected 0.05)" % nfpr)
    # ratio must be ~11.4 (0.57/0.05)
    if not (11.0 <= ratio <= 12.0):
        fails.append("ratio == %.4f (expected ~11.4 = 0.57/0.05)" % ratio)
    _finish(fails)
main()
