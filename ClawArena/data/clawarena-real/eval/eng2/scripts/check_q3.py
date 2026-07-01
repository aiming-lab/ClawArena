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
    txt = _read(ws / "pipeline" / "bronze" / "ingest.py")
    if txt is None:
        _finish(["file not found: pipeline/bronze/ingest.py"])
    if "tpep_pickup_datetime" not in txt:
        fails.append("ingest.py does not reference verbatim column 'tpep_pickup_datetime'")
    # F: schema_v2 adds airport_fee and cbd_congestion_fee — both must appear verbatim
    if "airport_fee" not in txt:
        fails.append("ingest.py does not reference verbatim schema_v2 column 'airport_fee'")
    if "cbd_congestion_fee" not in txt:
        fails.append("ingest.py does not reference verbatim schema_v2 column 'cbd_congestion_fee'")
    if not re.search(r"read_parquet|read_csv_auto|read_csv", txt):
        fails.append("ingest.py does not call a DuckDB read function (read_parquet/read_csv_auto)")
    _finish(fails)
main()
