#!/usr/bin/env python3
"""
check_q24_final_json.py — Validates analysis/final_assessment.json.

Checks:
  - recommendation contains 'not' and 'clarification'
  - critical_flags is a list with >= 3 items
  - technical_rating within ±0.1 of 4.3
  - action_required is a list with >= 2 items
"""
import sys
import re
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q24_final_json.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "final_assessment.json"

    if not target.exists():
        print("FAILED: file not found: analysis/final_assessment.json")
        sys.exit(1)

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"FAILED: invalid JSON — {exc}")
        sys.exit(1)

    failures = []

    # recommendation
    rec = str(data.get("recommendation", ""))
    if not ("not" in rec.lower() and "clarification" in rec.lower()):
        failures.append(
            f"recommendation '{rec}' must contain both 'not' and 'clarification'"
        )

    # critical_flags
    flags = data.get("critical_flags", [])
    if not isinstance(flags, list) or len(flags) < 3:
        failures.append(
            f"critical_flags has {len(flags) if isinstance(flags, list) else 'N/A'} items (expected >= 3)"
        )

    # technical_rating
    rating = data.get("technical_rating")
    if rating is None or abs(float(rating) - 4.3) > 0.1:
        failures.append(
            f"technical_rating == {rating} (expected within ±0.1 of 4.3)"
        )

    # action_required
    actions = data.get("action_required", [])
    if not isinstance(actions, list) or len(actions) < 2:
        failures.append(
            f"action_required has {len(actions) if isinstance(actions, list) else 'N/A'} items (expected >= 2)"
        )

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
