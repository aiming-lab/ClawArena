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
    data, err = _load_json(ws / "output" / "platform_gmv_share_v3.json")
    if err: _finish([err])
    # douyin_gmv 须为独立字段（数值 > 0）
    dg = data.get("douyin_gmv")
    try:
        dg = float(dg)
        if dg <= 0:
            fails.append("douyin_gmv == %s (expected > 0, 独立字段)" % dg)
    except (TypeError, ValueError):
        fails.append("douyin_gmv 须为数值（独立字段，非 content_platforms 合计的一部分）")
    # superseded_rule 须包含 pm_correction_note.md 和 channel_aggregation
    sr = str(data.get("superseded_rule") or "").lower()
    if "pm_correction_note" not in sr:
        fails.append("superseded_rule 须包含 'pm_correction_note.md': %r" % data.get("superseded_rule"))
    if "channel_aggregation" not in sr and "channel" not in sr:
        fails.append("superseded_rule 须包含 'channel_aggregation': %r" % data.get("superseded_rule"))
    # 加难：superseded_rule 须同时标注 finance_audit_memo.md（Update 2 中实际发出撤销指令的文件）
    if "finance_audit_memo" not in sr:
        fails.append("superseded_rule 须包含 'finance_audit_memo.md'（Update 2 的财务审计备忘录，该文件才是发出 supersede 指令的权威来源；仅标注 pm_correction_note.md 不完整）: %r" % data.get("superseded_rule"))
    # data_version 须为 v2
    dv = str(data.get("data_version") or "")
    if dv != "v2":
        fails.append("data_version == %r (expected 'v2')" % dv)
    _finish(fails)
main()
