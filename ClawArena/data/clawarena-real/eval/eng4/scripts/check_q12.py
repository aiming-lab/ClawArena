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
    data, err = _load_json(ws / "work" / "scan_type_summary.json")
    if err: _finish([err])
    # total_queries must be exactly 12
    tq = data.get("total_queries")
    try:
        tq = int(tq)
        if tq != 12:
            fails.append("total_queries == %d (expected exactly 12: 9 original + 3 from Update 2)" % tq)
    except (TypeError, ValueError):
        fails.append("total_queries not an int: %r" % data.get("total_queries"))
    # scan_type_distribution must be a non-empty object with string keys and int values
    std = data.get("scan_type_distribution")
    if not isinstance(std, dict) or not std:
        fails.append("scan_type_distribution must be a non-empty object")
    else:
        for k, v in std.items():
            try:
                int(v)
            except (TypeError, ValueError):
                fails.append("scan_type_distribution[%r] value must be an int, got %r" % (k, v))
    # seq_scan_remaining must be a list with < 4 entries (most queries were optimized)
    ssr = data.get("seq_scan_remaining")
    if not isinstance(ssr, list):
        fails.append("seq_scan_remaining must be an array")
    elif len(ssr) >= 4:
        fails.append("seq_scan_remaining has %d entries (expected < 4 — most queries should be optimized)" % len(ssr))
    _finish(fails)
main()
