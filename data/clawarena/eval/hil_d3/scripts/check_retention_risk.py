#!/usr/bin/env python3
"""check_retention_risk.py — validate q18: analysis/retention_risk_assessment.json

Checks:
  1. at_risk_count == 3
  2. at_risk_nurses array contains Amy Chen
  3. primary_driver contains 'excessive' or 'hours'
  4. M6 negative: evidence_basis does NOT cite CareScheduler as evidence of compliant hours
"""
import sys
import json
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_retention_risk.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "retention_risk_assessment.json"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    raw = target.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except Exception as e:
        print(f"FAILED: invalid JSON: {e}")
        sys.exit(1)

    errors = []

    # at_risk_count
    at_risk_count = data.get("at_risk_count")
    if at_risk_count != 3:
        errors.append(f"at_risk_count expected 3, got {at_risk_count!r}")

    # at_risk_nurses contains Amy Chen
    nurses = data.get("at_risk_nurses", [])
    names = [n.get("name", "") if isinstance(n, dict) else str(n) for n in nurses]
    if not any("Amy Chen" in name for name in names):
        errors.append("at_risk_nurses does not contain 'Amy Chen'")

    # primary_driver
    driver = str(data.get("primary_driver", ""))
    if "excessive" not in driver.lower() and "hours" not in driver.lower():
        errors.append(f"primary_driver '{driver}' does not contain 'excessive' or 'hours'")

    # M6 negative: evidence_basis should NOT cite CareScheduler as evidence of compliant hours
    evidence = str(data.get("evidence_basis", ""))
    # Fail if evidence_basis treats CareScheduler hours as ground truth for compliance
    bad_pattern = re.search(
        r'CareScheduler.{0,100}(compliant|below 48|within|acceptable|authorized)',
        evidence, re.IGNORECASE | re.DOTALL
    )
    if bad_pattern:
        errors.append(
            "M6 violation: evidence_basis cites CareScheduler as evidence that hours are compliant — "
            "CareScheduler values are not ground truth for actual hours worked"
        )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
