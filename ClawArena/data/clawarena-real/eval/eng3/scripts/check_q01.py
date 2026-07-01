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
    data, err = _load_json(ws / "output" / "q01_incident_start.json")
    if err: _finish([err])
    # 字段存在性
    for k in ("incident_start_utc", "component", "message_excerpt"):
        if k not in data:
            fails.append("missing key: " + k)
    if fails: _finish(fails)
    # 真值层：incident_start_utc 必须精确为 2024-06-20T17:47:00Z（无容差，raw_alerts.jsonl 有确切秒数）
    ts = data.get("incident_start_utc", "")
    if ts != "2024-06-20T17:47:00Z":
        fails.append("incident_start_utc == %r (must be exactly \'2024-06-20T17:47:00Z\' — read the CRITICAL alert timestamp verbatim from raw_alerts.jsonl)" % ts)
    # component 必须含 lua 或 rate-limit
    comp = str(data.get("component", "")).lower()
    if "lua" not in comp and "rate" not in comp:
        fails.append("component == %r (must contain \'lua\' or \'rate\')" % data.get("component"))
    # message_excerpt 须包含函数名 get_cookie_key（摘自原始 alert message 前 80 字符）
    excerpt = str(data.get("message_excerpt", ""))
    if "get_cookie_key" not in excerpt:
        fails.append("message_excerpt %r must contain \'get_cookie_key\' (from the CRITICAL alert message in raw_alerts.jsonl)" % excerpt[:60])
    _finish(fails)
main()
