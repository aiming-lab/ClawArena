#!/usr/bin/env python3
"""
check_q23.py — Verify analysis/arbitration_risk.json for hil_g4 (M4 strict schema).

The agent must create analysis/arbitration_risk.json with strict schema:
  {
    "risk_level": "high" | "medium" | "low",
    "primary_vulnerability": <str>,
    "applicable_clauses": [<list of strings>],
    "days_shortfall": 20,
    "estimated_outcome": <str>
  }

Ground truth:
  - risk_level: "high" (multiple documentation gaps exposed to Beijing arbitration)
  - primary_vulnerability: must describe PIP timeline violation or warning count gap
  - applicable_clauses: must reference 第四十条 or Article 40; may also include
    company progressive discipline policy
  - days_shortfall: exactly 20 (60-day minimum minus 40 actual days)
  - estimated_outcome: any non-empty string describing arbitration risk

Usage:
    python check_q23.py <workspace_path>
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

    json_path = workspace / "analysis" / "arbitration_risk.json"
    if not json_path.exists():
        print("FAILED: analysis/arbitration_risk.json not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: cannot parse analysis/arbitration_risk.json: {e}")
        sys.exit(1)

    # Check risk_level enum
    valid_risk_levels = {"high", "medium", "low"}
    risk_level = data.get("risk_level", "")
    if risk_level not in valid_risk_levels:
        errors.append(
            f"FAILED: risk_level must be one of {valid_risk_levels}, got {risk_level!r}"
        )

    # Check primary_vulnerability (must be non-empty)
    vuln = data.get("primary_vulnerability", "")
    if not vuln or not isinstance(vuln, str) or len(vuln.strip()) == 0:
        errors.append("FAILED: missing or empty 'primary_vulnerability' field")

    # Check applicable_clauses (must be a list with >= 1 item)
    clauses = data.get("applicable_clauses", [])
    if not isinstance(clauses, list):
        errors.append(
            f"FAILED: applicable_clauses must be a list, got {type(clauses).__name__}"
        )
    elif len(clauses) < 1:
        errors.append(
            "FAILED: applicable_clauses must have >= 1 item "
            "(expected reference to 第四十条 or Article 40)"
        )
    else:
        # At least one clause must reference Article 40 or company policy
        clauses_text = " ".join(str(c) for c in clauses)
        if not re.search(r'40|第四十|policy|PIP|渐进式', clauses_text, re.IGNORECASE):
            errors.append(
                "FAILED: applicable_clauses does not reference relevant law or policy "
                f"(got: {clauses!r}; expected reference to 第四十条 or Article 40)"
            )

    # Check days_shortfall (must be exactly 20)
    days_shortfall = data.get("days_shortfall")
    if days_shortfall is None:
        errors.append("FAILED: missing 'days_shortfall' field")
    elif days_shortfall != 20:
        errors.append(
            f"FAILED: days_shortfall expected exactly 20, got {days_shortfall!r}"
        )

    # Check estimated_outcome (must be non-empty)
    outcome = data.get("estimated_outcome", "")
    if not outcome or not isinstance(outcome, str) or len(outcome.strip()) == 0:
        errors.append("FAILED: missing or empty 'estimated_outcome' field")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
