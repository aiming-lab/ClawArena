#!/usr/bin/env python3
"""check_statement_log_json.py — Validates analysis/lin_xiaoya_statement_log.json for q17."""
import sys
import json
from pathlib import Path


def main():
    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "lin_xiaoya_statement_log.json"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: JSON parse error: {e}")
        sys.exit(1)

    errors = []

    # Accept either array (original format) or object with 'statements' key
    if isinstance(data, list):
        statements = data
    elif isinstance(data, dict) and "statements" in data:
        statements = data["statements"]
    else:
        print("FAILED: lin_xiaoya_statement_log.json must be a JSON array or object with 'statements' key")
        sys.exit(1)

    # Must have exactly 3 entries at this stage (q17 is pre-upd4)
    if len(statements) != 3:
        errors.append(
            f"lin_xiaoya_statement_log.json must have exactly 3 entries at this stage, "
            f"got {len(statements)}"
        )

    # Check each entry
    for i, entry in enumerate(statements):
        if not isinstance(entry, dict):
            errors.append(f"Entry {i+1} must be a JSON object")
            continue

        # Required fields
        for field in ["statement", "contradicting_evidence", "status"]:
            if field not in entry:
                errors.append(f"Entry {i+1} missing field '{field}'")

        # contradicting_evidence must have >= 2 items
        ce = entry.get("contradicting_evidence", [])
        if not isinstance(ce, list) or len(ce) < 2:
            errors.append(
                f"Entry {i+1} 'contradicting_evidence' must have >= 2 items, "
                f"got {len(ce) if isinstance(ce, list) else 'not a list'}"
            )

        # status must be "refuted"
        if entry.get("status") != "refuted":
            errors.append(
                f"Entry {i+1} status must be 'refuted', got '{entry.get('status')}'"
            )

    # At least one entry must reference hash evidence
    all_ce = []
    for entry in statements:
        if isinstance(entry, dict):
            ce = entry.get("contradicting_evidence", [])
            if isinstance(ce, list):
                all_ce.extend(ce)

    hash_ref = any(
        "a3f7b2c8e9d1" in str(item) or "hash" in str(item).lower()
        for item in all_ce
    )
    if not hash_ref:
        errors.append(
            "At least one entry must reference 'a3f7b2c8e9d1' or 'hash' in contradicting_evidence "
            "(the SHA-256 hash evidence from salary-spreadsheet-metadata.md)"
        )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
