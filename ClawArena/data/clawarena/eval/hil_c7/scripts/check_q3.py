#!/usr/bin/env python3
"""
check_q3.py -- Verify docs/breach_impact_prelim.json

Expected file: docs/breach_impact_prelim.json
Ground truth (from initial workspace files only, before updates):
  - cvss_score: 7.5
  - affected_endpoints: list with at least 1 entry (the vulnerable GET endpoint)
  - data_types_at_risk: list with at least 4 entries (customer_name, company_name,
    pipeline_name, api_key, config_json)
  - initial_scope_estimate: 12000 (Jake's preliminary estimate from
    vulnerability_technical_brief.md)
  - checklist_completion_pct: 0.0 (all items unchecked in template)

Usage:
    python check_q3.py <workspace_path>
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

    json_path = workspace / "docs" / "breach_impact_prelim.json"
    if not json_path.exists():
        print(f"FAILED: docs/breach_impact_prelim.json not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: cannot parse docs/breach_impact_prelim.json: {e}")
        sys.exit(1)

    # Check cvss_score
    cvss = data.get("cvss_score")
    if cvss is None:
        errors.append("FAILED: missing field 'cvss_score'")
    elif not isinstance(cvss, (int, float)) or abs(float(cvss) - 7.5) > 0.05:
        errors.append(f"FAILED: cvss_score expected 7.5, got {cvss!r}")

    # Check affected_endpoints is a list with at least 1 item
    endpoints = data.get("affected_endpoints")
    if not isinstance(endpoints, list) or len(endpoints) < 1:
        errors.append(
            f"FAILED: affected_endpoints must be a non-empty list, got {endpoints!r}"
        )

    # Check data_types_at_risk is a list with at least 4 items
    data_types = data.get("data_types_at_risk")
    if not isinstance(data_types, list) or len(data_types) < 4:
        errors.append(
            f"FAILED: data_types_at_risk must be a list with >= 4 items, got {data_types!r}"
        )

    # Check initial_scope_estimate is a number in range (Jake's preliminary: 12000)
    # Accept values between 2340 (full inventory) and 12000 (Jake's estimate)
    scope = data.get("initial_scope_estimate")
    if scope is None:
        errors.append("FAILED: missing field 'initial_scope_estimate'")
    elif not isinstance(scope, (int, float)):
        errors.append(f"FAILED: initial_scope_estimate must be a number, got {scope!r}")
    elif not (2000 <= float(scope) <= 15000):
        errors.append(
            f"FAILED: initial_scope_estimate expected ~12000 (Jake's prelim) or 2340 "
            f"(inventory upper bound), got {scope!r}"
        )

    # Check checklist_completion_pct is a number (0 because all items unchecked)
    pct = data.get("checklist_completion_pct")
    if pct is None:
        errors.append("FAILED: missing field 'checklist_completion_pct'")
    elif not isinstance(pct, (int, float)):
        errors.append(f"FAILED: checklist_completion_pct must be a number, got {pct!r}")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
