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

def _field_entry(data, name):
    """从 quality report 取某字段 entry，兼容 fields 为 list 或 dict。"""
    fields = data.get("fields")
    if isinstance(fields, list):
        for e in fields:
            if isinstance(e, dict) and e.get("field_name") == name:
                return e
    elif isinstance(fields, dict):
        e = fields.get(name)
        if isinstance(e, dict):
            return e
        if e is not None:
            return {"field_name": name, "null_count": e}
    return None

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q4_quality_report.json")
    if err: _finish([err])
    # passenger_count — exact match from dataset_profile.json
    e = _field_entry(data, "passenger_count")
    if e is None:
        fails.append("no passenger_count entry under 'fields'")
    else:
        nc = e.get("null_count")
        try:
            nc = int(nc)
        except (TypeError, ValueError):
            fails.append("passenger_count.null_count not an int: %r" % nc)
            nc = None
        if nc is not None and nc != 1309356:
            fails.append("passenger_count.null_count == %d (must be exactly 1,309,356 from dataset_profile.json; "
                         "the BOT summary's ~500,000 is a known undercount)" % nc)
    # F: RatecodeID entry also required — same authoritative null_count = 1,309,356
    e2 = _field_entry(data, "RatecodeID")
    if e2 is None:
        fails.append("no RatecodeID entry under 'fields' (report must include both passenger_count and RatecodeID)")
    else:
        nc2 = e2.get("null_count")
        try:
            nc2 = int(nc2)
        except (TypeError, ValueError):
            fails.append("RatecodeID.null_count not an int: %r" % nc2)
            nc2 = None
        if nc2 is not None and nc2 != 1309356:
            fails.append("RatecodeID.null_count == %d (must be exactly 1,309,356 from dataset_profile.json)" % nc2)
    _finish(fails)
main()
