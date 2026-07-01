#!/usr/bin/env python3
"""check_claim_vs_evidence_json.py — Validates analysis/claim_vs_evidence.json for q6."""
import sys
import json
from pathlib import Path


def main():
    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "claim_vs_evidence.json"

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
        print("FAILED: claim_vs_evidence.json must be a JSON array")
        sys.exit(1)

    # Must have exactly 3 entries
    if len(data) != 3:
        errors.append(f"Expected exactly 3 entries, got {len(data)}")
    else:
        for i, entry in enumerate(data):
            # Required fields
            if "claim" not in entry:
                errors.append(f"Entry {i+1} missing 'claim' field")
            if "evidence_against" not in entry:
                errors.append(f"Entry {i+1} missing 'evidence_against' field")
            elif not isinstance(entry["evidence_against"], list):
                errors.append(f"Entry {i+1} 'evidence_against' must be an array")
            elif len(entry["evidence_against"]) < 2:
                errors.append(
                    f"Entry {i+1} 'evidence_against' must have >= 2 items, "
                    f"got {len(entry['evidence_against'])}"
                )
            if "verdict" not in entry:
                errors.append(f"Entry {i+1} missing 'verdict' field")
            elif entry["verdict"] != "refuted":
                errors.append(
                    f"Entry {i+1} verdict must be 'refuted', got '{entry['verdict']}'"
                )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
