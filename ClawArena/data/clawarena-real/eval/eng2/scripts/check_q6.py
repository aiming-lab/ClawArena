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
    data, err = _load_json(ws / "output" / "q6_timestamp_anomalies.json")
    if err: _finish([err])
    ac = data.get("anomaly_count")
    if not isinstance(ac, int) or ac <= 0:
        fails.append("anomaly_count == %r (expected positive int)" % ac)
    yrs = set()
    for y in (data.get("future_year_examples") or []):
        try:
            yrs.add(int(y))
        except (TypeError, ValueError):
            pass
    if not (2088 in yrs or 2084 in yrs):
        fails.append("future_year_examples must include 2088 or 2084 (got %s)" % sorted(yrs))
    _finish(fails)
main()
