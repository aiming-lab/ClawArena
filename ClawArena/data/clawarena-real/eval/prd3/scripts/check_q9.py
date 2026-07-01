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
    data, err = _load_json(ws / "output" / "gmv_revision_v2.json")
    if err: _finish([err])
    v1 = data.get("v1_total_gmv")
    v2 = data.get("v2_total_gmv")
    try:
        v1 = float(v1); v2 = float(v2)
    except (TypeError, ValueError):
        _finish(["v1_total_gmv / v2_total_gmv 须为数值"])
    # delta_pct 须在 -5% 到 -8% 范围（v2 比 v1 低 5-8%）
    dp = data.get("delta_pct")
    try:
        dp = float(dp)
    except (TypeError, ValueError):
        fails.append("delta_pct 不是数值: %r" % data.get("delta_pct"))
        dp = None
    if dp is not None:
        if not (-8.0 <= dp <= -5.0):
            fails.append("delta_pct == %.2f (expected -5%% to -8%%, v2 须比 v1 低 5-8%%)" % dp)
    # reason 须含 Method 2 和 subsidy excluded
    reason = str(data.get("reason") or "").lower()
    if "method 2" not in reason and "method2" not in reason:
        fails.append("reason 未包含 'Method 2': %r" % data.get("reason"))
    if "subsidy" not in reason:
        fails.append("reason 未包含 'subsidy excluded': %r" % data.get("reason"))
    # 加难：reason 须引用 pm_correction_note.md 作为口径修正依据（Update 1 注入的说明文件）
    if "pm_correction_note" not in reason:
        fails.append("reason 未引用 'pm_correction_note.md'（Update 1 的 PM 修正说明文件，须在 reason 中明确引用该文件名作为修正依据）: %r" % data.get("reason"))
    _finish(fails)
main()
