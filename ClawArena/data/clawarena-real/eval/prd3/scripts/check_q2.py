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
    data, err = _load_json(ws / "output" / "conflicts.json")
    if err: _finish([err])
    cc = data.get("conflict_count")
    try:
        cc = int(cc)
    except (TypeError, ValueError):
        cc = 0
    if cc < 3:
        fails.append("conflict_count == %r (expected >= 3: 补贴口径 + 360/365分母 + GMV同比增速三条冲突)" % data.get("conflict_count"))
    conflicts = data.get("conflicts") or []
    if not isinstance(conflicts, list) or len(conflicts) < 3:
        fails.append("conflicts array 须含至少 3 条")
    # 检查是否含补贴冲突
    all_text = " ".join(str(c) for c in conflicts).lower()
    if not any(kw in all_text for kw in ("subsid", "补贴", "platform subsidy")):
        fails.append("conflicts 中未发现 GMV 补贴口径冲突（须含 subsid/补贴 关键词）")
    if not any(kw in all_text for kw in ("360", "365")):
        fails.append("conflicts 中未发现 360 vs 365 库存天数分母冲突")
    if not any(kw in all_text for kw in ("增速", "growth", "yoy", "同比", "22.5", "15.2")):
        fails.append("conflicts 中未发现 GMV 同比增速冲突（bot 摘要 22.5%% vs Daxue 权威 15.2%%）")
    # 每条须有 from 字段
    for i, c in enumerate(conflicts):
        if isinstance(c, dict) and not c.get("from"):
            fails.append("conflicts[%d] 缺少 'from' 字段（P2 要求标注 session 来源）" % i)
    _finish(fails)
main()
