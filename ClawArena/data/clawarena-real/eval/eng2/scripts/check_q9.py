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
    txt = _read(ws / "pipeline" / "silver" / "enrich.py")
    if txt is None:
        _finish(["file not found: pipeline/silver/enrich.py"])
    low = txt.lower()
    if "pulocationid" not in low or "locationid" not in low:
        fails.append("enrich.py must join on PULocationID = LocationID")
    # must be a LEFT JOIN specifically
    if "left" not in low:
        fails.append("enrich.py must perform a LEFT JOIN (not inner join) — rows with no zone match must be kept as 'Unknown'")
    if "join" not in low:
        fails.append("enrich.py does not perform a join")
    if "unknown" not in low:
        fails.append("enrich.py does not provide an 'Unknown' Borough fallback for unmatched IDs")
    # must reference the authoritative lookup file name
    if "taxi_zone_lookup" not in low:
        fails.append("enrich.py does not reference the authoritative 'taxi_zone_lookup' file")
    _finish(fails)
main()
