#!/usr/bin/env python3
"""
check_resolution_pathway.py — Validates analysis/resolution_pathway.json.

Checks:
  1. File exists at analysis/resolution_pathway.json
  2. Valid JSON
  3. "corrigendum" key or entry present
  4. "supplementary" method addition present
  5. ≥3 resolution steps
"""
import sys
import json
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_resolution_pathway.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "resolution_pathway.json"

    if not target.exists():
        print(f"FAILED: {target} does not exist")
        sys.exit(1)

    # JSON parse
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"FAILED: JSON parse error — {e}")
        sys.exit(1)

    raw = target.read_text(encoding="utf-8").lower()
    failures = []

    # corrigendum
    if "corrigendum" not in raw:
        failures.append("FAILED: 'corrigendum' not found in JSON")

    # supplementary
    if "supplementary" not in raw:
        failures.append("FAILED: 'supplementary' not found in JSON")

    # ≥3 resolution steps
    # Try to count steps from list structures
    def count_steps(obj):
        """Recursively count list items across the JSON."""
        if isinstance(obj, list):
            return len(obj)
        if isinstance(obj, dict):
            for key in ("steps", "actions", "recommendations", "measures",
                        "pathway", "items", "resolution"):
                if key in obj and isinstance(obj[key], list):
                    return len(obj[key])
            # Sum all list values
            totals = [count_steps(v) for v in obj.values()]
            return max(totals) if totals else 0
        return 0

    step_count = count_steps(data)
    if step_count < 3:
        # Fallback: count top-level items
        if isinstance(data, list):
            step_count = len(data)
        elif isinstance(data, dict):
            step_count = len(data)

    if step_count < 3:
        failures.append(
            f"FAILED: fewer than 3 resolution steps found in JSON "
            f"(counted {step_count})"
        )

    if failures:
        for f in failures:
            print(f)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
