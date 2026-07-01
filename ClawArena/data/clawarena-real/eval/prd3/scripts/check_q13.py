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
    data, err = _load_json(ws / "output" / "legacy_report_flags.json")
    if err: _finish([err])
    if data.get("is_legacy") is not True:
        fails.append("is_legacy == %r (expected true)" % data.get("is_legacy"))
    # wrong_formula 须含 365（旧版错误乘数）
    wf = str(data.get("wrong_formula") or "").lower()
    if "365" not in wf:
        fails.append("wrong_formula 须包含 '365'（旧版 ×365 错误公式）: %r" % data.get("wrong_formula"))
    # correct_formula 须含 360 和 5 quarters
    cf = str(data.get("correct_formula") or "").lower()
    if "360" not in cf:
        fails.append("correct_formula 须包含 '360'（JD 官方乘数）: %r" % data.get("correct_formula"))
    if "5 quarter" not in cf and "five quarter" not in cf and "5q" not in cf:
        fails.append("correct_formula 须包含 '5 quarters': %r" % data.get("correct_formula"))
    _finish(fails)
main()
