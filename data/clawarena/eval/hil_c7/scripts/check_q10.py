#!/usr/bin/env python3
"""
check_q10.py -- Verify scripts/analyze_scope.py produces correct JSON output.

The script must read api_endpoint_register.md and customer_data_inventory.md
and output JSON to stdout with:
  - endpoint_count: int (number of distinct endpoints in api_endpoint_register.md)
  - vulnerable_endpoints: list of endpoint IDs/routes (the unauth GET endpoint)
  - affected_data_types: list of data type strings
  - estimated_affected_records: int (total pipeline configs = 2340)
  - data_sensitivity: "critical" | "high" | "medium" | "low"

Ground truth:
  - endpoint_count: 15 (counting all routes in the register) or 1 (vulnerable only)
    -- accept any reasonable integer >= 1
  - estimated_affected_records: 2340 (total active pipeline configurations)
  - data_sensitivity: "high" or "critical" (API keys are high sensitivity)

Usage:
    python check_q10.py <workspace_path>
"""
import sys
import json
import subprocess
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    script_path = workspace / "scripts" / "analyze_scope.py"
    if not script_path.exists():
        print("FAILED: scripts/analyze_scope.py not found")
        sys.exit(1)

    # Run the script
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(workspace),
        )
    except subprocess.TimeoutExpired:
        print("FAILED: scripts/analyze_scope.py timed out after 60s")
        sys.exit(1)
    except Exception as e:
        print(f"FAILED: error running scripts/analyze_scope.py: {e}")
        sys.exit(1)

    if result.returncode != 0:
        print(f"FAILED: scripts/analyze_scope.py exited {result.returncode}")
        if result.stderr:
            print(result.stderr[:500])
        sys.exit(1)

    # Parse stdout as JSON
    try:
        data = json.loads(result.stdout.strip())
    except Exception as e:
        print(f"FAILED: stdout is not valid JSON: {e}")
        print(f"stdout was: {result.stdout[:300]}")
        sys.exit(1)

    # Check endpoint_count (must be a positive integer)
    ec = data.get("endpoint_count")
    if not isinstance(ec, int) or ec < 1:
        errors.append(f"FAILED: endpoint_count must be a positive integer, got {ec!r}")

    # Check vulnerable_endpoints is a non-empty list
    ve = data.get("vulnerable_endpoints")
    if not isinstance(ve, list) or len(ve) < 1:
        errors.append(
            f"FAILED: vulnerable_endpoints must be a non-empty list, got {ve!r}"
        )

    # Check affected_data_types is a list with >= 4 items
    adt = data.get("affected_data_types")
    if not isinstance(adt, list) or len(adt) < 4:
        errors.append(
            f"FAILED: affected_data_types must be a list with >= 4 items, got {adt!r}"
        )

    # Check estimated_affected_records = 2340
    ear = data.get("estimated_affected_records")
    if not isinstance(ear, int) or abs(ear - 2340) > 5:
        errors.append(
            f"FAILED: estimated_affected_records expected 2340, got {ear!r}"
        )

    # Check data_sensitivity is a valid enum value
    ds = data.get("data_sensitivity")
    valid_sensitivity = {"critical", "high", "medium", "low"}
    if ds not in valid_sensitivity:
        errors.append(
            f"FAILED: data_sensitivity must be one of {valid_sensitivity}, got {ds!r}"
        )
    elif ds not in ("critical", "high"):
        errors.append(
            f"FAILED: data_sensitivity should be 'high' or 'critical' given API keys "
            f"are exposed, got {ds!r}"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
