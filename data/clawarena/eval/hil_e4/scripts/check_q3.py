#!/usr/bin/env python3
"""
check_q3.py -- Verify docs/compliance_discrepancy_map.json.

Usage:
    python check_q3.py <workspace_path>
"""
import sys
import json
from pathlib import Path

VALID_SEVERITIES = {"critical", "moderate", "minor"}
REQUIRED_FIELDS = {"id", "source_a", "source_b", "field", "value_a", "value_b", "severity"}


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    json_path = workspace / "docs" / "compliance_discrepancy_map.json"
    if not json_path.exists():
        errors.append(f"FAILED: {json_path} not found")
    else:
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"FAILED: cannot parse {json_path}: {e}")
            data = {}

        if data:
            if "discrepancies" not in data:
                errors.append("FAILED: compliance_discrepancy_map.json missing 'discrepancies' key")
            else:
                items = data["discrepancies"]
                if not isinstance(items, list):
                    errors.append("FAILED: 'discrepancies' must be an array")
                elif len(items) < 3:
                    errors.append(f"FAILED: 'discrepancies' has {len(items)} items, need >= 3")
                else:
                    has_critical = False
                    for i, item in enumerate(items):
                        missing = REQUIRED_FIELDS - set(item.keys())
                        if missing:
                            errors.append(
                                f"FAILED: discrepancy item {i} missing fields: {missing}"
                            )
                        severity = item.get("severity", "")
                        if severity not in VALID_SEVERITIES:
                            errors.append(
                                f"FAILED: item {i} severity '{severity}' not in "
                                f"['critical','moderate','minor']"
                            )
                        if severity == "critical":
                            has_critical = True
                    if not has_critical:
                        errors.append(
                            "FAILED: no 'critical' severity entry found; "
                            "Community Mobilization overspend should be critical"
                        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
