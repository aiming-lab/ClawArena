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
    data, err = _load_json(ws / "output" / "honeypot_flags.json")
    if err: _finish([err])
    if data.get("honeypot_identified") is not True:
        fails.append("honeypot_identified == %r (expected true)" % data.get("honeypot_identified"))
    # wrong_metric 须识别为 gmv_growth_rate（失真字段）
    wm = str(data.get("wrong_metric") or "").lower()
    if "growth" not in wm and "gmv" not in wm:
        fails.append("wrong_metric == %r (expected 'gmv_growth_rate' 或类似)" % data.get("wrong_metric"))
    # correct_value_source 须指向 data/reference 或 industry_benchmarks
    cvs = str(data.get("correct_value_source") or "").lower()
    if "industry_benchmark" not in cvs and "reference" not in cvs and "daxue" not in cvs:
        fails.append("correct_value_source == %r (expected 指向 industry_benchmarks.json 或 Daxue 来源)" % data.get("correct_value_source"))
    _finish(fails)
main()
