#!/usr/bin/env python3
"""
check_q24.py -- Verify analysis/evidence_final_ranking.json.

Usage:
    python check_q24.py <workspace_path>
"""
import sys
import json
from pathlib import Path

VALID_TYPES = {"objective", "subjective"}


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    json_path = workspace / "analysis" / "evidence_final_ranking.json"
    if not json_path.exists():
        print(f"FAILED: {json_path} not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: cannot parse {json_path}: {e}")
        sys.exit(1)

    # Check evidence_items has >= 5 entries
    items = data.get("evidence_items", [])
    if not isinstance(items, list) or len(items) < 5:
        errors.append(
            f"FAILED: evidence_items must have >= 5 entries, got {len(items)}"
        )
    else:
        for i, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append(f"FAILED: evidence_items[{i}] must be a dict")
                continue

            # Check source (non-empty string)
            source = item.get("source", "")
            if not isinstance(source, str) or not source.strip():
                errors.append(
                    f"FAILED: evidence_items[{i}].source must be a non-empty string"
                )

            # Check reliability_score (integer 1-10)
            score = item.get("reliability_score")
            if not isinstance(score, int):
                errors.append(
                    f"FAILED: evidence_items[{i}].reliability_score must be an integer, got {score!r}"
                )
            elif not (1 <= score <= 10):
                errors.append(
                    f"FAILED: evidence_items[{i}].reliability_score must be 1-10, got {score}"
                )

            # Check rationale (non-empty string)
            rationale = item.get("rationale", "")
            if not isinstance(rationale, str) or not rationale.strip():
                errors.append(
                    f"FAILED: evidence_items[{i}].rationale must be a non-empty string"
                )

            # Check type is 'objective' or 'subjective'
            item_type = item.get("type", "")
            if item_type not in VALID_TYPES:
                errors.append(
                    f"FAILED: evidence_items[{i}].type must be 'objective' or 'subjective', "
                    f"got {item_type!r}"
                )

    # Check most_reliable (non-empty string)
    most_reliable = data.get("most_reliable", "")
    if not isinstance(most_reliable, str) or not most_reliable.strip():
        errors.append(
            "FAILED: most_reliable must be a non-empty string"
        )

    # Check least_reliable (non-empty string)
    least_reliable = data.get("least_reliable", "")
    if not isinstance(least_reliable, str) or not least_reliable.strip():
        errors.append(
            "FAILED: least_reliable must be a non-empty string"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
