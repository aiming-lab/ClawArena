#!/usr/bin/env python3
"""
check_q13.py -- Verify analysis/incident_report.json (M1 + M4 strict schema).

Usage:
    python check_q13.py <workspace_path>
"""
import sys
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "incident_report.json"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: cannot parse JSON: {e}")
        sys.exit(1)

    errors = []

    # Required fields with exact values
    if data.get("offset_minutes") != 60:
        errors.append(f"offset_minutes expected 60 (int), got {data.get('offset_minutes')!r}")

    if data.get("seconds_over_cutoff") != 5:
        errors.append(f"seconds_over_cutoff expected 5 (int), got {data.get('seconds_over_cutoff')!r}")

    if data.get("bug_line") != 127:
        errors.append(f"bug_line expected 127 (int), got {data.get('bug_line')!r}")

    if data.get("silence_days") != 7:
        errors.append(f"silence_days expected 7 (int), got {data.get('silence_days')!r}")

    if data.get("timestamp") != "2026-03-16T11:30:05+08:00":
        errors.append(f"timestamp expected '2026-03-16T11:30:05+08:00', got {data.get('timestamp')!r}")

    # Required fields presence check
    required_fields = ["incident_id", "affected_order", "timestamp", "offset_minutes",
                       "seconds_over_cutoff", "root_cause", "bug_file", "bug_line",
                       "silence_rule", "silence_days"]
    for field in required_fields:
        if field not in data:
            errors.append(f"missing required field: '{field}'")

    if data.get("bug_file") != "strategy/scheduler.py":
        errors.append(f"bug_file expected 'strategy/scheduler.py', got {data.get('bug_file')!r}")

    if data.get("silence_rule") != "rule_007":
        errors.append(f"silence_rule expected 'rule_007', got {data.get('silence_rule')!r}")

    # Non-empty string fields
    for field in ["incident_id", "affected_order"]:
        if not isinstance(data.get(field), str) or not data.get(field):
            errors.append(f"field '{field}' must be a non-empty string")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
