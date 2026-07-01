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
    data, err = _load_json(ws / "output" / "liability_cap.json")
    if err: _finish([err])
    # cap_months 必须是 12（v2.3 活跃版本，非 v2.1 的 6 个月）
    cm = data.get("cap_months")
    try:
        cm = int(cm)
    except (TypeError, ValueError):
        _finish(["cap_months not an int: %r" % cm])
    if cm != 12:
        fails.append("cap_months == %d (expected 12 from active MSA v2.3 §10.1, NOT the superseded v2.1's 6 months)" % cm)
    # excluded_damages 必须含 consequential 和 indirect
    excl = [str(x).lower() for x in (data.get("excluded_damages") or [])]
    excl_str = " ".join(excl)
    if "consequ" not in excl_str:
        fails.append("excluded_damages must include 'consequential' damages")
    if "indirect" not in excl_str:
        fails.append("excluded_damages must include 'indirect' damages")
    # exceptions 必须非空（至少有 indemnification 例外）
    exc = data.get("exceptions")
    if not isinstance(exc, list) or len(exc) == 0:
        fails.append("exceptions must be a non-empty list (cap carve-outs)")
    _finish(fails)
main()
