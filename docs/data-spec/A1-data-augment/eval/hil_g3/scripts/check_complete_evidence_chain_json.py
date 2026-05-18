#!/usr/bin/env python3
"""check_complete_evidence_chain_json.py — Validates analysis/complete_evidence_chain.json for q20."""
import sys
import json
from pathlib import Path


def main():
    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "complete_evidence_chain.json"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: JSON parse error: {e}")
        sys.exit(1)

    errors = []

    if not isinstance(data, list):
        print("FAILED: complete_evidence_chain.json must be a JSON array")
        sys.exit(1)

    # Must have exactly 6 items
    if len(data) != 6:
        errors.append(f"Expected exactly 6 items, got {len(data)}")
        if errors:
            for e in errors:
                print(f"FAILED: {e}")
            sys.exit(1)

    # Build step map
    step_map = {}
    for entry in data:
        step = entry.get("step")
        if step is not None:
            step_map[step] = entry

    # Steps must be in order 1-6
    steps_present = sorted(step_map.keys())
    if steps_present != [1, 2, 3, 4, 5, 6]:
        errors.append(
            f"Steps must be 1–6 in order, got: {steps_present}"
        )

    # All confidence fields must be "high"
    for entry in data:
        if entry.get("confidence") != "high":
            errors.append(
                f"Step {entry.get('step')} confidence must be 'high', "
                f"got '{entry.get('confidence')}'"
            )

    # Step 1 must have exact timestamp
    step1 = step_map.get(1, {})
    ts1 = step1.get("timestamp", "")
    if "2026-09-25T14:22:17" not in str(ts1):
        errors.append(
            f"Step 1 timestamp must contain '2026-09-25T14:22:17', got '{ts1}'"
        )

    # Step 4 must have exact timestamp
    step4 = step_map.get(4, {})
    ts4 = step4.get("timestamp", "")
    if "2026-09-25T15:03:44" not in str(ts4):
        errors.append(
            f"Step 4 timestamp must contain '2026-09-25T15:03:44', got '{ts4}'"
        )

    # Step 3 must reference the hash a3f7b2c8e9d1
    step3 = step_map.get(3, {})
    step3_text = json.dumps(step3)
    if "a3f7b2c8e9d1" not in step3_text:
        errors.append(
            "Step 3 must contain 'a3f7b2c8e9d1' (SHA-256 hash confirmation)"
        )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
