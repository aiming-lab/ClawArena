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
    txt = _read(ws / "postmortem" / "DRAFT_v1.md")
    if txt is None:
        _finish(["file not found: postmortem/DRAFT_v1.md"])
    # V9 verbatim Lua function names
    for fn in ("get_cookie_key", "has_valid_cookie_broken", "parent_key_generator"):
        if fn not in txt:
            fails.append("DRAFT_v1.md missing verbatim Lua function name: %r" % fn)
    # DDoS deployment timestamps
    if "14:14" not in txt:
        fails.append("DRAFT_v1.md missing DDoS deploy start time \'14:14\'")
    if "17:06" not in txt:
        fails.append("DRAFT_v1.md missing DDoS deploy complete time \'17:06\'")
    # tail-call mention
    if "tail call" not in txt.lower() and "tail-call" not in txt.lower():
        fails.append("DRAFT_v1.md must mention \'tail call\' or \'tail-call\' recursion mechanism")
    # P3: 所有 ## 标题须含双语斜杠分隔符（静默考察，EM Feishu DM 已通知 P3）
    headings = re.findall(r"^##\s+.+", txt, re.MULTILINE)
    bad_h = [h for h in headings if "/" not in h]
    if bad_h:
        fails.append("DRAFT_v1.md heading(s) missing bilingual \'/\' separator (P3 applies): %s" % bad_h[:2])
    # 必须包含事件开始时间戳的完整 ISO 格式（V4 前置锚点）
    if "2024-06-20T17:47" not in txt:
        fails.append("DRAFT_v1.md must include full ISO timestamp \'2024-06-20T17:47\' for incident start")
    _finish(fails)
main()
