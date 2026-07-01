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
    data, err = _load_json(ws / "output" / "data_quality_report.json")
    if err: _finish([err])
    dates = data.get("jd_method1_dates") or []
    if not isinstance(dates, list) or len(dates) < 3:
        fails.append("jd_method1_dates 须为含至少 3 个日期的列表（实际：%r）" % dates)
    else:
        # 须在 2025-05-13 ~ 2025-05-22 范围内
        valid = [d for d in dates if isinstance(d, str) and d.startswith("2025-05-")]
        if len(valid) < 3:
            fails.append("jd_method1_dates 中至少 3 个须为 2025-05-xx 格式（在 bug 日期范围内）")
    correct = str(data.get("correct_method") or "").lower()
    if "method 2" not in correct and "method2" not in correct:
        fails.append("correct_method == %r (expected 'Method 2')" % data.get("correct_method"))
    _finish(fails)
main()
