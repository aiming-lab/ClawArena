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
    data, err = _load_json(ws / "output" / "redline_v23_v24.json")
    if err: _finish([err])
    # cap_months_v24 必须是 6（v2.4 回退）
    cm = data.get("cap_months_v24")
    try:
        cm = int(cm)
    except (TypeError, ValueError):
        _finish(["cap_months_v24 not an int: %r" % cm])
    if cm != 6:
        fails.append("cap_months_v24 == %d (expected 6 — VendorX's v2.4 regresses the cap from 12 to 6 months)" % cm)
    # changed_clauses 必须是列表，且至少一项涉及 §10 或 liability cap
    cc = data.get("changed_clauses")
    if not isinstance(cc, list) or len(cc) == 0:
        fails.append("changed_clauses must be a non-empty list")
    else:
        cc_text = " ".join(json.dumps(x) for x in cc).lower()
        if "10" not in cc_text and "liability" not in cc_text and "cap" not in cc_text:
            fails.append("changed_clauses must include the liability cap change (§10.1: 12 → 6 months)")
    # key_regression 必须非空
    if not data.get("key_regression"):
        fails.append("key_regression must be present and describe the main regression from TechCo's view")
    _finish(fails)
main()
