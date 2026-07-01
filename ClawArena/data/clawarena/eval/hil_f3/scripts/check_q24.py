#!/usr/bin/env python3
"""
check_q24.py -- Verify analysis/incident_postmortem.json (M4 strict schema).

Usage:
    python check_q24.py <workspace_path>
"""
import sys
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "incident_postmortem.json"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: cannot parse JSON: {e}")
        sys.exit(1)

    errors = []

    # Numeric field exact-value checks (M1)
    if data.get("offset_minutes") != 60:
        errors.append(f"offset_minutes expected 60, got {data.get('offset_minutes')!r}")

    if data.get("root_cause_line") != 127:
        errors.append(f"root_cause_line expected 127, got {data.get('root_cause_line')!r}")

    if data.get("seconds_over_cutoff") != 5:
        errors.append(f"seconds_over_cutoff expected 5, got {data.get('seconds_over_cutoff')!r}")

    if data.get("duration_days") != 8:
        errors.append(f"duration_days expected 8, got {data.get('duration_days')!r}")

    contributing_factors = data.get("contributing_factors", [])
    if not isinstance(contributing_factors, list) or len(contributing_factors) < 3:
        errors.append(f"contributing_factors must be list with >= 3 items, got {contributing_factors!r}")

    # Required fields presence
    required_fields = ["incident_id", "severity", "duration_days", "offset_minutes",
                       "seconds_over_cutoff", "root_cause_file", "root_cause_line",
                       "contributing_factors", "immediate_actions", "long_term_actions"]
    for field in required_fields:
        if field not in data:
            errors.append(f"missing required field: '{field}'")

    if data.get("root_cause_file") != "strategy/scheduler.py":
        errors.append(f"root_cause_file expected 'strategy/scheduler.py', got {data.get('root_cause_file')!r}")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
