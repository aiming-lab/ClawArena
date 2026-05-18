#!/usr/bin/env python3
"""
check_q6.py — Verify analysis/pip_compliance_calc.json for hil_g4 (M1 numeric exact match).

The agent must create analysis/pip_compliance_calc.json with the following exact values:
  {
    "pip_start_date": "2026-02-01",
    "termination_date": "2026-03-13",
    "legal_notice_days_required": 60,
    "actual_pip_days": 40,
    "days_shortfall": 20,
    "compliant": false
  }

Ground truth derivation:
  - PIP start date: 2026-02-01 (pip-email-chain.md)
  - Termination date: 2026-03-13 (employee-hr-file.md)
  - Company policy minimum PIP: 60 days (labor-law-reference.md)
  - Actual PIP days: 2026-03-13 minus 2026-02-01 = 40 days
  - days_shortfall: 60 - 40 = 20 days
  - compliant: false (40 < 60)

Usage:
    python check_q6.py <workspace_path>
"""
import sys
import json
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    json_path = workspace / "analysis" / "pip_compliance_calc.json"
    if not json_path.exists():
        print("FAILED: analysis/pip_compliance_calc.json not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: cannot parse analysis/pip_compliance_calc.json: {e}")
        sys.exit(1)

    # Check pip_start_date
    if data.get("pip_start_date") != "2026-02-01":
        errors.append(
            f"FAILED: pip_start_date expected '2026-02-01', got {data.get('pip_start_date')!r}"
        )

    # Check legal_notice_days_required (must be 60)
    legal_days = data.get("legal_notice_days_required") or data.get("legal_minimum_days") or data.get("policy_minimum_days")
    if legal_days != 60:
        errors.append(
            f"FAILED: legal_notice_days_required expected 60, got {legal_days!r}"
        )

    # Check actual_pip_days or actual_notice_days (must be 40)
    actual_days = (
        data.get("actual_pip_days")
        or data.get("actual_notice_days")
        or data.get("actual_days")
        or data.get("pip_duration_days")
    )
    if actual_days != 40:
        errors.append(
            f"FAILED: actual_pip_days expected 40, got {actual_days!r}"
        )

    # Check days_shortfall (must be exactly 20)
    days_shortfall = data.get("days_shortfall")
    if days_shortfall is None:
        errors.append("FAILED: missing 'days_shortfall' field")
    elif days_shortfall != 20:
        errors.append(
            f"FAILED: days_shortfall expected exactly 20, got {days_shortfall!r}"
        )

    # Check compliant (must be false)
    if "compliant" not in data:
        errors.append("FAILED: missing 'compliant' field")
    elif data.get("compliant") is not False:
        errors.append(
            f"FAILED: compliant expected false, got {data.get('compliant')!r}"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
