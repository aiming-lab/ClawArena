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
    data, err = _load_json(ws / "output" / "q09_impact_v2.json")
    if err: _finish([err])
    # affected_keys_count == 3（Update 1 扩大范围）
    akc = data.get("affected_keys_count")
    try:
        akc = int(akc)
    except (TypeError, ValueError):
        _finish(["affected_keys_count not an int: %r" % akc])
    if akc != 3:
        fails.append("affected_keys_count == %d (expected 3 after Update 1 expanded scope)" % akc)
    # superseded_fields 含 affected_keys_count
    sf = [str(s).lower() for s in (data.get("superseded_fields") or [])]
    if not any("affected_keys_count" in s for s in sf):
        fails.append("superseded_fields must include 'affected_keys_count' (V10 supersede documentation)")
    # affected_services 含 anthropic
    svcs = [str(s).lower() for s in (data.get("affected_services") or [])]
    if not any("anthropic" in s for s in svcs):
        fails.append("affected_services must include 'anthropic' (newly discovered in Update 1)")
    _finish(fails)
main()
