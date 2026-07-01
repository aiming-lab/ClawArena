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
    data, err = _load_json(ws / "output" / "case_index.json")
    if err: _finish([err])
    # P3: schema_version must be "1.0"
    if str(data.get("schema_version")) != "1.0":
        fails.append("schema_version == %r (expected \"1.0\" per P3 format rule)" % data.get("schema_version"))
    if data.get("case_id") != "RIO-2023-GINO":
        fails.append("case_id == %r (expected 'RIO-2023-GINO')" % data.get("case_id"))
    if str(data.get("analyst_version")) != "1.0":
        fails.append("analyst_version == %r (expected exactly \"1.0\")" % data.get("analyst_version"))
    case_ids = data.get("case_ids") or []
    if "gino" not in [str(x).lower() for x in case_ids]:
        fails.append("case_ids must include 'gino' (got %s)" % case_ids)
    fc = data.get("file_count")
    try:
        fc_int = int(fc)
        if not (17 <= fc_int <= 23):
            fails.append("file_count == %d (must be between 17 and 23)" % fc_int)
    except (TypeError, ValueError):
        fails.append("file_count not an int: %r" % fc)
    _finish(fails)
main()
