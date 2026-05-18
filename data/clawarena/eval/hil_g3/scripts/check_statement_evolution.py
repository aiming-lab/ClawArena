#!/usr/bin/env python3
"""
check_statement_evolution.py — Validate analysis/lin_xiaoya_statement_evolution.json.

Checks:
  - File exists and is valid JSON
  - Has 3 entries (three statements/denials)
  - Statement 3 mentions hash or metadata
  - Statement 1 mentions DOWNLOAD or cloud log
"""
import sys
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_statement_evolution.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "lin_xiaoya_statement_evolution.json"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"FAILED: invalid JSON in {target}: {e}")
        sys.exit(1)

    if isinstance(data, list):
        entries = data
    elif isinstance(data, dict):
        entries = []
        for v in data.values():
            if isinstance(v, list):
                entries.extend(v)
    else:
        print(f"FAILED: unexpected JSON structure: {type(data).__name__}")
        sys.exit(1)

    if len(entries) < 3:
        print(f"FAILED: expected 3 statement entries, found {len(entries)}")
        sys.exit(1)

    # Find statement 1 and statement 3
    def find_entry(num):
        for e in entries:
            if not isinstance(e, dict):
                continue
            sn = e.get("statement_number") or e.get("statement_num") or e.get("id") or e.get("number")
            if str(sn) == str(num) or sn == num:
                return e
        # Fallback: use index
        if num - 1 < len(entries):
            return entries[num - 1]
        return None

    stmt1 = find_entry(1)
    stmt3 = find_entry(3)

    if stmt1 is None:
        print("FAILED: statement 1 entry not found in lin_xiaoya_statement_evolution.json")
        sys.exit(1)

    if stmt3 is None:
        print("FAILED: statement 3 entry not found in lin_xiaoya_statement_evolution.json")
        sys.exit(1)

    stmt1_text = json.dumps(stmt1).lower()
    if "download" not in stmt1_text and "cloud log" not in stmt1_text and "cloud" not in stmt1_text:
        print("FAILED: statement 1 does not reference DOWNLOAD or cloud log")
        sys.exit(1)

    stmt3_text = json.dumps(stmt3).lower()
    if "hash" not in stmt3_text and "metadata" not in stmt3_text and "sha" not in stmt3_text and "a3f7b2c8e9d1" not in stmt3_text:
        print("FAILED: statement 3 does not reference hash or metadata")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
