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
    txt = _read(ws / "output" / "final_report_draft.md")
    if txt is None:
        _finish(["file not found: output/final_report_draft.md"])
    low = txt.lower()
    lines = txt.splitlines()
    if len(lines) < 100:
        fails.append("final_report_draft.md 仅 %d 行（需 > 100 行）" % len(lines))
    if "gmv = transactions" not in low and "gmv=transactions" not in low:
        fails.append("须包含字符串 'GMV = transactions × AOV'（verbatim 引用）")
    if "360" not in txt:
        fails.append("须包含 '×360' 或 '× 360'（JD 库存天数口径）")
    if "method 2" not in low and "method2" not in low:
        fails.append("须包含 'Method 2'（GMV 口径说明）")
    if "data_version" not in low or "v2" not in low:
        fails.append("须包含 'data_version: v2' 或类似字样")
    _finish(fails)
main()
