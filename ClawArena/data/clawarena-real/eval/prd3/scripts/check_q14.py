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
    data, err = _load_json(ws / "output" / "return_rate_analysis_v2.json")
    if err: _finish([err])
    # electronics_benchmark_source 须为 China platform (revised)
    ebs = str(data.get("electronics_benchmark_source") or "").lower()
    if "china" not in ebs and "revised" not in ebs:
        fails.append("electronics_benchmark_source == %r (expected 'China platform (revised)')" % data.get("electronics_benchmark_source"))
    # electronics_upper_bound 须为 25（修订后基准）
    eub = data.get("electronics_upper_bound")
    try:
        eub = float(eub)
        if abs(eub - 25.0) > 0.5:
            fails.append("electronics_upper_bound == %s (expected 25, 修订后中国平台基准，非原 15)" % eub)
    except (TypeError, ValueError):
        fails.append("electronics_upper_bound 须为数值（25）")
    # 须有 flagged 字段在某品类中
    cats = data.get("categories") or []
    has_flagged = any(isinstance(c, dict) and "flagged" in c for c in cats)
    if not has_flagged and not data.get("flagged"):
        fails.append("须有 flagged: true 字段标记异常品类（P3 要求）")
    _finish(fails)
main()
