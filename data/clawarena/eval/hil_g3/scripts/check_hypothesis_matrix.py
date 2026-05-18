#!/usr/bin/env python3
"""check_hypothesis_matrix.py — Validates analysis/hypothesis_matrix.json for q8."""
import sys
import json
from pathlib import Path


def main():
    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "hypothesis_matrix.json"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: JSON parse error: {e}")
        sys.exit(1)

    errors = []

    # Must be a JSON array
    if not isinstance(data, list):
        print("FAILED: hypothesis_matrix.json must be a JSON array")
        sys.exit(1)

    # Must have exactly 4 entries
    if len(data) != 4:
        errors.append(f"Expected exactly 4 entries, got {len(data)}")
        if errors:
            for e in errors:
                print(f"FAILED: {e}")
            sys.exit(1)

    # Build a map by hypothesis_id
    h_map = {}
    for entry in data:
        if "hypothesis_id" not in entry:
            errors.append(f"Entry missing 'hypothesis_id' field: {entry}")
            continue
        h_map[entry["hypothesis_id"]] = entry

    # Check required fields on each entry
    required_fields = [
        "hypothesis_id", "hypothesis", "supporting_evidence",
        "contradicting_evidence", "status"
    ]
    for entry in data:
        for field in required_fields:
            if field not in entry:
                errors.append(
                    f"Entry {entry.get('hypothesis_id', '?')} missing field '{field}'"
                )

        # contradicting_evidence must have >= 1 item
        ce = entry.get("contradicting_evidence", [])
        if not isinstance(ce, list) or len(ce) < 1:
            errors.append(
                f"Entry {entry.get('hypothesis_id', '?')} must have >= 1 item in "
                f"'contradicting_evidence'"
            )

    # Check required statuses
    status_checks = {
        "H1": ("refuted",),
        "H2": ("refuted",),
        "H3": ("possible", "unresolved"),
        "H4": ("likely", "probable"),
    }
    for hid, valid_statuses in status_checks.items():
        if hid not in h_map:
            errors.append(f"hypothesis_matrix.json missing entry with hypothesis_id '{hid}'")
            continue
        actual_status = h_map[hid].get("status", "")
        if actual_status not in valid_statuses:
            errors.append(
                f"{hid}.status must be one of {valid_statuses}, got '{actual_status}'"
            )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
