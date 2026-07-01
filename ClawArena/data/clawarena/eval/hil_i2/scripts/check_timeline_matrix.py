#!/usr/bin/env python3
"""
check_timeline_matrix.py — Validates analysis/timeline_verification_matrix.json.

Checks:
  1. File exists at analysis/timeline_verification_matrix.json
  2. Valid JSON
  3. ≥7 events in the list/array
  4. "2025-08-01" (IRB approval) present
  5. "2025-09-15" (data extraction) present
  6. Events appear in chronological order (no earlier date after a later one)
"""
import sys
import json
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_timeline_matrix.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "timeline_verification_matrix.json"

    if not target.exists():
        print(f"FAILED: {target} does not exist")
        sys.exit(1)

    # JSON parse
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"FAILED: JSON parse error — {e}")
        sys.exit(1)

    failures = []

    # Determine event list (support both list-at-root and dict-with-events-key)
    if isinstance(data, list):
        events = data
    elif isinstance(data, dict):
        # Try common keys
        events = None
        for key in ("events", "timeline", "items", "entries"):
            if key in data and isinstance(data[key], list):
                events = data[key]
                break
        if events is None:
            # Fall back to first list value
            for v in data.values():
                if isinstance(v, list):
                    events = v
                    break
        if events is None:
            failures.append("FAILED: JSON structure does not contain a recognizable event list")
            for f in failures:
                print(f)
            sys.exit(1)
    else:
        failures.append("FAILED: JSON root must be a list or object with an event array")
        for f in failures:
            print(f)
        sys.exit(1)

    # ≥7 events
    if len(events) < 7:
        failures.append(
            f"FAILED: only {len(events)} events found (expected ≥7)"
        )

    # Serialize full JSON text for substring checks
    raw = target.read_text(encoding="utf-8")

    if "2025-08-01" not in raw:
        failures.append("FAILED: '2025-08-01' (IRB approval date) not found")

    if "2025-09-15" not in raw:
        failures.append("FAILED: '2025-09-15' (data extraction date) not found")

    # Chronological order check: collect all YYYY-MM-DD dates in order of appearance
    dates_found = re.findall(r'\b(\d{4}-\d{2}-\d{2})\b', raw)
    out_of_order = False
    prev = None
    for d in dates_found:
        if prev is not None and d < prev:
            out_of_order = True
            break
        prev = d
    if out_of_order:
        failures.append(
            "FAILED: events are not in chronological order "
            "(an earlier date appears after a later one)"
        )

    if failures:
        for f in failures:
            print(f)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
