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
    data, err = _load_json(ws / "work" / "q001_index_recommendation.json")
    if err: _finish([err])
    # index_type must be a valid PostgreSQL index type and NOT hash (range query on created_at)
    valid_types = {"btree", "hash", "gin", "gist", "spgist", "brin"}
    idx_type = str(data.get("index_type") or "").lower()
    if idx_type not in valid_types:
        fails.append("index_type %r is not a valid PostgreSQL index type (%s)" % (idx_type, sorted(valid_types)))
    if idx_type == "hash":
        fails.append("index_type == \"hash\" is incorrect: Hash indexes support only = equality, not range queries on created_at (see https://www.postgresql.org/docs/current/indexes-types.html)")
    # columns must include service_id
    cols = [str(c).lower() for c in (data.get("columns") or [])]
    if not any("service_id" in c for c in cols):
        fails.append("columns must include service_id (the filter column in Query-001)")
    # rationale must cite a URL
    rationale = str(data.get("rationale") or "")
    if "http" not in rationale and "postgresql.org" not in rationale:
        fails.append("rationale must cite a documentation URL (e.g. https://www.postgresql.org/docs/current/indexes-types.html)")
    # table_name must reference events
    tname = str(data.get("table_name") or "").lower()
    if "event" not in tname:
        fails.append("table_name %r must reference the events table" % data.get("table_name"))
    _finish(fails)
main()
