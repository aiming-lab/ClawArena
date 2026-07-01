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
    data, err = _load_json(ws / "output" / "q01_alert_parsed.json")
    if err: _finish([err])
    # 结构层
    for key in ("alert_number", "secret_type", "validity", "state", "file_path", "commit_sha"):
        if key not in data:
            fails.append("missing required key: " + key)
    if fails: _finish(fails)
    # 真值层 — 精确枚举值（verbatim GitHub SS API）
    if data.get("secret_type") != "openai_api_key":
        fails.append("secret_type == %r (expected verbatim 'openai_api_key')" % data.get("secret_type"))
    if data.get("validity") != "active":
        fails.append("validity == %r (expected 'active'; valid enum: active|inactive|unknown)" % data.get("validity"))
    if data.get("state") != "open":
        fails.append("state == %r (expected 'open'; valid enum: open|resolved)" % data.get("state"))
    if data.get("alert_number") != 1:
        fails.append("alert_number == %r (expected 1 for the triggering alert)" % data.get("alert_number"))
    _finish(fails)
main()
