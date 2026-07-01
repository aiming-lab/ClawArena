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
    data, err = _load_json(ws / "output" / "q2_schema_diff.json")
    if err: _finish([err])
    added = set(str(x) for x in (data.get("added_fields") or []))
    EXACT = {"airport_fee", "cbd_congestion_fee"}
    for need in sorted(EXACT):
        if need not in added:
            fails.append("added_fields missing %r" % need)
    # guard: must not pull deprecated lon/lat field names from the legacy archive
    for bad in ("pickup_longitude", "dropoff_longitude", "pickup_latitude", "dropoff_latitude",
                "pickup_datetime", "dropoff_datetime"):
        if bad in added:
            fails.append("added_fields wrongly contains deprecated legacy field %r" % bad)
    # added_fields must be EXACTLY the two new v2 fields, no more
    extra = added - EXACT
    if extra:
        fails.append("added_fields contains unexpected extra entries %s (v2 adds exactly 2 fields)" % sorted(extra))
    # v1_missing_count must equal 2 exactly
    vmc = data.get("v1_missing_count")
    try:
        if int(vmc) != 2:
            fails.append("v1_missing_count == %r (expected exactly 2)" % vmc)
    except (TypeError, ValueError):
        fails.append("v1_missing_count must be int 2 (got %r)" % vmc)
    _finish(fails)
main()
