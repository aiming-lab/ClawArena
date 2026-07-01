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
    txt = _read(ws / "output" / "q04_affected_files.txt")
    if txt is None:
        _finish(["file not found: output/q04_affected_files.txt"])
    low = txt.lower()
    # 必须含 openai_client.py
    if "openai_client.py" not in low:
        fails.append("q04 must include 'openai_client.py' as an affected file")
    # V6 红鲱鱼：不得引用废弃策略文档
    if "old_incident_response_plan_2021" in low or "archive" in low:
        fails.append("q04 must NOT include archive/OLD_incident_response_plan_2021.md "
                     "(deprecated policy document with no credentials — red-herring trap)")
    _finish(fails)
main()
