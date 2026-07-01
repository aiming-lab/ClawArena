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
    data, err = _load_json(ws / "output" / "q10_anthropic_revoke.json")
    if err: _finish([err])
    # secret_type verbatim
    st = data.get("secret_type")
    if st != "anthropic_api_key":
        fails.append("secret_type == %r (expected verbatim 'anthropic_api_key' — GitHub SS type)" % st)
    # revoked_at 格式 ISO-8601
    rat = str(data.get("revoked_at", ""))
    if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", rat):
        fails.append("revoked_at == %r (must match ^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$)" % rat)
    # operator 字段存在且非空
    op = data.get("operator")
    if not op:
        fails.append("operator field is missing or empty (P2 requirement)")
    _finish(fails)
main()
