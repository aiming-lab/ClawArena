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
    txt = _read(ws / "output" / "q13_incident_timeline.md")
    if txt is None:
        _finish(["file not found: output/q13_incident_timeline.md"])
    # 必须含修正日期 2022-12-29
    if "2022-12-29" not in txt:
        fails.append("timeline must contain '2022-12-29' (corrected CircleCI customer detection date per postmortem_FINAL)")
    # 不得含废弃的草稿日期 2022-12-25
    if "2022-12-25" in txt:
        fails.append("timeline must NOT contain '2022-12-25' (superseded draft date — use the Update 2 corrected date 2022-12-29)")
    # 是 Markdown 表格（含 | 字符）
    if "|" not in txt:
        fails.append("timeline must be a Markdown table (containing | column separators)")
    _finish(fails)
main()
