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
    data, err = _load_json(ws / "output" / "gmv_validation_v1.json")
    if err: _finish([err])
    status = data.get("status")
    if status != "FAIL":
        fails.append("status == %r (expected FAIL; v1 数据含 Method 1 口径污染，校验须返回 FAIL)" % status)
    # delta_pct 须在 4%-8% 范围（calc_gmv.py 真实输出；不得填 0 或占位值）
    dp = data.get("delta_pct")
    try:
        dp = float(dp)
        if not (4.0 <= dp <= 8.0):
            fails.append("delta_pct == %.2f (expected 4%%–8%% 范围；须实际运行 scripts/calc_gmv.py 获取真实差异，不得填 0 或估计值)" % dp)
    except (TypeError, ValueError):
        fails.append("delta_pct 须为数值（须实际运行 calc_gmv.py 脚本获得，取绝对差异百分比）")
    # affected_date_range 须存在且 start/end 在 2025-05-13 ~ 2025-05-22 范围
    adr = data.get("affected_date_range")
    if not isinstance(adr, dict):
        fails.append("affected_date_range 须为含 start/end 的对象（status=FAIL 时必须记录日期范围）")
    else:
        start = str(adr.get("start") or "")
        end = str(adr.get("end") or "")
        if not start.startswith("2025-05"):
            fails.append("affected_date_range.start == %r (expected 2025-05-xx)" % start)
        if not end.startswith("2025-05"):
            fails.append("affected_date_range.end == %r (expected 2025-05-xx)" % end)
    _finish(fails)
main()
