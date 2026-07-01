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
    # Check index_ddl_batch1.sql
    sql_txt = _read(ws / "work" / "index_ddl_batch1.sql")
    if sql_txt is None:
        _finish(["file not found: work/index_ddl_batch1.sql"])
    low_sql = sql_txt.lower()
    # Must contain CONCURRENTLY
    if "concurrently" not in low_sql:
        fails.append("index_ddl_batch1.sql does not contain CONCURRENTLY keyword")
    # All CREATE INDEX statements must use CONCURRENTLY (no exceptions)
    for line in sql_txt.splitlines():
        ll = line.lower().strip()
        if "create index" in ll and "concurrently" not in ll:
            if not ll.startswith("--") and not ll.startswith("#"):
                fails.append("index_ddl_batch1.sql: CREATE INDEX without CONCURRENTLY: %r" % line[:80])
    # Must have at least 3 CREATE INDEX statements
    ci_count = len(re.findall(r"create\s+index", low_sql))
    if ci_count < 3:
        fails.append("index_ddl_batch1.sql has only %d CREATE INDEX statements (expected >= 3)" % ci_count)
    # Must target events or notifications tables (per question specification)
    if "events" not in low_sql and "notifications" not in low_sql:
        fails.append("index_ddl_batch1.sql must create indexes on events and/or notifications tables")
    # Check optimization_log.jsonl
    log_txt = _read(ws / "work" / "optimization_log.jsonl")
    if log_txt is None:
        _finish(["file not found: work/optimization_log.jsonl"])
    log_lines = [l.strip() for l in log_txt.splitlines() if l.strip()]
    if not log_lines:
        _finish(["optimization_log.jsonl is empty"])
    entries = []
    for i, line in enumerate(log_lines):
        try:
            entry = json.loads(line)
            entries.append(entry)
        except json.JSONDecodeError as e:
            fails.append("optimization_log.jsonl line %d is not valid JSON: %s" % (i+1, str(e)[:80]))
    # HARDENED: log entry count must exactly match CREATE INDEX count in SQL
    if entries and ci_count > 0 and len(entries) != ci_count:
        fails.append(
            "optimization_log.jsonl has %d entries but index_ddl_batch1.sql has %d CREATE INDEX statements "
            "(each DDL must have exactly one log entry)" % (len(entries), ci_count)
        )
    # Each entry must have action == "create_index"
    for i, e in enumerate(entries):
        if not isinstance(e, dict):
            fails.append("log entry %d is not a JSON object" % i); continue
        if e.get("action") != "create_index":
            fails.append("log entry %d: action == %r (expected \"create_index\")" % (i, e.get("action")))
        if not e.get("ddl"):
            fails.append("log entry %d: ddl field is empty" % i)
        if not e.get("timestamp"):
            fails.append("log entry %d: timestamp field missing" % i)
        # HARDENED: rationale field must be present and non-empty
        if not e.get("rationale"):
            fails.append("log entry %d: rationale field missing or empty (required for audit trail)" % i)
    _finish(fails)
main()
