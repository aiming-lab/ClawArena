#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib
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
    txt = _read(ws / "rca_outputs" / "ivenix_tech_summary_v1.md")
    if txt is None:
        _finish(["file not found: rca_outputs/ivenix_tech_summary_v1.md"])
    low = txt.lower()
    # 必须含召回号和产品码
    if "z-0885-2026" not in low:
        fails.append("ivenix_tech_summary_v1.md does not contain recall number Z-0885-2026")
    if "lvp-sw-0005" not in low:
        fails.append("ivenix_tech_summary_v1.md does not contain product code LVP-SW-0005")
    # 必须记录初始版本（5.10.0 — pre-update 状态）
    if "5.10.0" not in txt:
        fails.append("ivenix_tech_summary_v1.md must record the pre-update version 5.10.0 as stated in initial session")
    # 必须记录修复版本 5.10.2
    if "5.10.2" not in txt:
        fails.append("ivenix_tech_summary_v1.md must reference the fixed version 5.10.2")
    # 必须说明电池健康阈值 70%
    if "70" not in txt and "seventy" not in low:
        fails.append(
            "ivenix_tech_summary_v1.md must reference the 70% battery health threshold "
            "from the anomaly investigation (batteries with health below 70% most affected)"
        )
    # 文档须达到技术摘要基本长度
    word_count = len(txt.split())
    if word_count < 200:
        fails.append("ivenix_tech_summary_v1.md is %d words (expected >= 200 for a technical summary)" % word_count)
    _finish(fails)
main()
