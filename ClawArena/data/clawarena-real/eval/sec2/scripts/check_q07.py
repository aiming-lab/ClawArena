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
    data, err = _load_json(ws / "output" / "q07_impact_v1.json")
    if err: _finish([err])
    # pre-update 范围：2 个密钥
    akc = data.get("affected_keys_count")
    try:
        akc = int(akc)
    except (TypeError, ValueError):
        _finish(["affected_keys_count not an int: %r" % akc])
    if akc != 2:
        fails.append("affected_keys_count == %d (expected 2 for pre-Update-1 scope)" % akc)
    # affected_services 含 openai 和 aws
    svcs = [str(s).lower() for s in (data.get("affected_services") or [])]
    if not any("openai" in s for s in svcs):
        fails.append("affected_services must include 'openai'")
    if not any("aws" in s for s in svcs):
        fails.append("affected_services must include 'aws'")
    _finish(fails)
main()
