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
    # Check q011_partial_index.sql
    sql_txt = _read(ws / "work" / "q011_partial_index.sql")
    if sql_txt is None:
        _finish(["file not found: work/q011_partial_index.sql"])
    low_sql = sql_txt.lower()
    # Must have WHERE clause for billed IS NOT TRUE (or equivalent billed = FALSE / billed IS FALSE)
    has_where_billed = bool(
        re.search(r"where\s+billed\s+is\s+not\s+true", low_sql) or
        re.search(r"where\s+billed\s*=\s*false", low_sql) or
        re.search(r"where\s+not\s+billed", low_sql) or
        re.search(r"where\s+billed\s+is\s+false", low_sql)
    )
    if not has_where_billed:
        fails.append("q011_partial_index.sql must contain a WHERE clause equivalent to 'billed IS NOT TRUE'")
    # Must use CONCURRENTLY (P4, implicit)
    if "concurrently" not in low_sql:
        fails.append("q011_partial_index.sql must use CONCURRENTLY (production DDL requirement P4)")
    # Check rationale file
    rationale_txt = _read(ws / "work" / "q011_partial_index_rationale.md")
    if rationale_txt is None:
        fails.append("file not found: work/q011_partial_index_rationale.md")
    else:
        low_rat = rationale_txt.lower()
        # Must reference partial index documentation
        if "partial" not in low_rat:
            fails.append("q011_partial_index_rationale.md must discuss partial indexes")
        if "postgresql.org" not in low_rat and "http" not in low_rat:
            fails.append("q011_partial_index_rationale.md must cite a documentation URL")
    _finish(fails)
main()
