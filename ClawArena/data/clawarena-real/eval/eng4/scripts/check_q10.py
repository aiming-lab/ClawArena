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
    # Check q010_join_analysis.json — recommendation must now be create_statistics
    data, err = _load_json(ws / "work" / "q010_join_analysis.json")
    if err: _finish([err])
    rec = str(data.get("recommendation") or "")
    if rec != "create_statistics":
        fails.append("q010_join_analysis.json: recommendation == %r (expected \"create_statistics\" per architect\'s supersede; NOT \"increase_work_mem\")" % rec)
    # Check q010_create_statistics.sql
    sql_txt = _read(ws / "work" / "q010_create_statistics.sql")
    if sql_txt is None:
        _finish(["file not found: work/q010_create_statistics.sql"])
    low_sql = sql_txt.lower()
    # Must use CREATE STATISTICS syntax
    if "create statistics" not in low_sql:
        fails.append("q010_create_statistics.sql must use CREATE STATISTICS syntax")
    # Must include "dependencies" statistics kind (from planner-stats docs / Render case study)
    if "dependencies" not in low_sql:
        fails.append("q010_create_statistics.sql must specify \'dependencies\' statistics kind (functional dependencies, per planner-stats docs)")
    # Must reference events table
    if "events" not in low_sql:
        fails.append("q010_create_statistics.sql must reference the events table")
    _finish(fails)
main()
