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
    data, err = _load_json(ws / "output" / "q04_honeybot_discrepancies.json")
    if err: _finish([err])
    disc = data.get("discrepancies")
    if not isinstance(disc, list) or len(disc) == 0:
        _finish(["discrepancies must be a non-empty array"])
    # 必须含 error_rate 失真（0.21 vs 2.1）
    has_err = False
    has_dur = False
    for d in disc:
        if not isinstance(d, dict): continue
        # 检查字段 field 或 bot_value 或 correct_value 含关键词
        all_text = " ".join(str(v) for v in d.values()).lower()
        if "0.21" in all_text and ("2.1" in all_text or "error" in all_text):
            has_err = True
        if ("37" in all_text and "100" in all_text) or ("duration" in all_text and "37" in all_text):
            has_dur = True
        if not has_err and ("cdn" in all_text or "error" in all_text or "rate" in all_text):
            if "0.21" in all_text:
                has_err = True
        if not has_dur and ("duration" in all_text or "minute" in all_text):
            if "37" in all_text:
                has_dur = True
    if not has_err:
        fails.append("discrepancies missing error_rate distortion (bot 0.21% vs real 2.1%)")
    if not has_dur:
        fails.append("discrepancies missing duration distortion (bot 37 min vs real 100 min)")
    # 每条须含 source 字段（非空）
    for i, d in enumerate(disc):
        if isinstance(d, dict) and not d.get("source"):
            fails.append("discrepancies[%d] missing non-empty 'source' field" % i)
    _finish(fails)
main()
