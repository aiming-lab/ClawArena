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
    data, err = _load_json(ws / "output" / "platform_gmv_share.json")
    if err: _finish([err])
    def _pct(key, lo, hi):
        v = data.get(key)
        try:
            v = float(v)
        except (TypeError, ValueError):
            fails.append("%s 不是数值: %r" % (key, v)); return
        if not (lo <= v <= hi):
            fails.append("%s == %.2f (expected %.1f-%.1f%%)" % (key, v, lo, hi))
    _pct("tmall_share_pct", 45.0, 56.0)
    _pct("jd_share_pct", 15.0, 25.0)
    _pct("content_platforms_share_pct", 20.0, 40.0)
    # 加难：Douyin 和 Kuaishou 须单独列出占比字段（Update 2 supersede 的前置要求，内容平台须可拆分）
    douyin = data.get("douyin_share_pct")
    if douyin is None:
        fails.append("缺少 douyin_share_pct 字段（须单独列出 Douyin 平台份额；仅列合并的 content_platforms_share_pct 不满足要求——Update 2 后 Douyin 须独立追踪）")
    kuaishou = data.get("kuaishou_share_pct")
    if kuaishou is None:
        fails.append("缺少 kuaishou_share_pct 字段（须单独列出快手平台份额；与 Douyin 分开列报以满足审计追踪要求）")
    dv = str(data.get("data_version") or "")
    if dv != "v1":
        fails.append("data_version == %r (expected 'v1' 此阶段使用 v1 数据)" % dv)
    _finish(fails)
main()
