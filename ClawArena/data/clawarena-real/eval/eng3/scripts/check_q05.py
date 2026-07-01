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
    data, err = _load_json(ws / "output" / "q05_buggy_functions.json")
    if err: _finish([err])
    funcs = set(str(f) for f in (data.get("functions") or []))
    # 必须包含全部三个缺陷函数名（均出自 rule_engine_v1.lua 文件头注释及代码）
    for need in ("get_cookie_key", "has_valid_cookie_broken", "parent_key_generator"):
        if need not in funcs:
            fails.append("functions missing verbatim name %r (from rule_engine_v1.lua Bug functions annotation)" % need)
    # source_file 必须含 rule_engine_v1（V6 guard：不能用 LEGACY）
    src = str(data.get("source_file", "")).lower()
    if "rule_engine_v1" not in src:
        fails.append("source_file %r must contain \'rule_engine_v1\'" % data.get("source_file"))
    if "legacy" in src:
        fails.append("source_file %r must NOT be the LEGACY file" % data.get("source_file"))
    # rejected_file 必须含 LEGACY
    rej = str(data.get("rejected_file", "")).lower()
    if "legacy" not in rej:
        fails.append("rejected_file %r must contain \'LEGACY\' (the deprecated archive)" % data.get("rejected_file"))
    _finish(fails)
main()
