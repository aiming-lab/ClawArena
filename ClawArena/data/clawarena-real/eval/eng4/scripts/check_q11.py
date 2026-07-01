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
    sql_txt = _read(ws / "work" / "q012_covering_index.sql")
    if sql_txt is None:
        _finish(["file not found: work/q012_covering_index.sql"])
    low_sql = sql_txt.lower()
    # Must use INCLUDE keyword
    if "include" not in low_sql:
        fails.append("q012_covering_index.sql must use the INCLUDE clause (for covering index / Index Only Scan)")
    # Must use CONCURRENTLY (P4 implicit)
    if "concurrently" not in low_sql:
        fails.append("q012_covering_index.sql must use CONCURRENTLY (production DDL requirement)")
    # Must reference users table
    if "users" not in low_sql:
        fails.append("q012_covering_index.sql must reference the users table")
    # HARDENED: email must appear as the index key column (in ON clause, before INCLUDE)
    # Strip SQL comments to avoid matching email from comment text
    sql_no_comments_raw = re.sub(r"--[^\n]*", "", low_sql)
    # email must be in the ON (...) key, not only in INCLUDE (...)
    # Pattern: ON <table> (email ...) INCLUDE (...)
    m_on_key = re.search(r"\bon\s+\w+\s*\(([^)]+)\)\s*include", sql_no_comments_raw)
    m_email_any = re.search(r"\bemail\b", sql_no_comments_raw)
    if not m_email_any:
        fails.append("q012_covering_index.sql must index on email column (the WHERE predicate in query_012)")
    elif m_on_key:
        key_cols = m_on_key.group(1)
        if "email" not in key_cols:
            fails.append(
                "q012_covering_index.sql: email must be the index key column (in ON users (email) before INCLUDE), "
                "not placed inside INCLUDE — email is the filter column, so it must be the indexed key"
            )
    # HARDENED: INCLUDE clause must contain both name and updated_at
    # Strip SQL comments (-- to end of line) to avoid false positives from comment text
    sql_no_comments = re.sub(r"--[^\n]*", "", low_sql)
    # Find the INCLUDE keyword in actual DDL (not in comments)
    m_include = re.search(r"\binclude\s*\(([^)]+)\)", sql_no_comments)
    if m_include:
        include_cols = m_include.group(1)
        if "name" not in include_cols:
            fails.append(
                "q012_covering_index.sql: INCLUDE clause must contain \'name\' column "
                "(required to cover SELECT u.name without heap fetch)"
            )
        if "updated_at" not in include_cols:
            fails.append(
                "q012_covering_index.sql: INCLUDE clause must contain \'updated_at\' column "
                "(required to cover SELECT u.updated_at without heap fetch)"
            )
    elif "include" in sql_no_comments:
        fails.append("q012_covering_index.sql: INCLUDE clause has no valid parenthesized column list")
    _finish(fails)
main()
