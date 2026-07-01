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
    data, err = _load_json(ws / "output" / "validation_result.json")
    if err: _finish([err])
    # extract from wrapper if present
    if isinstance(data, dict) and "validated_count" not in data:
        # may be wrapped in metadata
        inner = data.get("script_output") or data.get("result") or data
        if isinstance(inner, dict):
            data = inner
    vc = data.get("validated_count")
    ec = data.get("error_count")
    try:
        vc_i = int(vc); ec_i = int(ec)
    except (TypeError, ValueError):
        _finish(["validated_count or error_count not numeric: %r %r" % (vc, ec)])
    if vc_i < 0 or ec_i < 0:
        fails.append("validated_count or error_count is negative")
    total_v = vc_i + ec_i
    if total_v <= 0:
        fails.append("validated_count + error_count == %d (expected > 0)" % total_v)
    # cross-check against breach_tickets_Q4_v3.json
    q11, e11 = _load_json(ws / "output" / "breach_tickets_Q4_v3.json")
    if not e11 and q11 is not None:
        q11t = q11 if isinstance(q11, list) else q11.get("tickets", [])
        if len(q11t) > 0 and total_v != len(q11t):
            fails.append("validated_count+error_count=%d != breach_tickets_Q4_v3 ticket count=%d" % (total_v, len(q11t)))
    _finish(fails)
main()
