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
    txt = _read(ws / "pipeline" / "silver" / "clean.py")
    if txt is None:
        _finish(["file not found: pipeline/silver/clean.py"])
    low = txt.lower()
    if "fare_amount" not in txt:
        fails.append("clean.py does not reference fare_amount filter")
    if "trip_distance" not in txt:
        fails.append("clean.py does not reference trip_distance filter")
    # must reference the verbatim official pickup column name
    if "tpep_pickup_datetime" not in txt:
        fails.append("clean.py does not reference verbatim column 'tpep_pickup_datetime' for the year filter")
    if not re.search(r"2009|2024|valid_year|year", low):
        fails.append("clean.py does not apply a pickup-year/timestamp validity filter")
    # must reference the authoritative max_valid trip_distance threshold (300 miles)
    if not re.search(r"300|max_valid|max_trip", low):
        fails.append("clean.py does not reference the max_valid trip_distance threshold (300 miles from quality_rules.yaml)")
    # F: must have a module-level docstring (triple-quoted string or comment block after header)
    has_docstring = bool(re.search(r'"{3}[^"]{5,}"{3}', txt[:600]) or re.search(r"'{3}[^']{5,}'{3}", txt[:600]))
    if not has_docstring:
        fails.append("clean.py must have a module-level docstring explaining the filters (triple-quoted string within first 600 chars)")
    _finish(fails)
main()
