#!/usr/bin/env python3
"""
check_q12.py — Verify analysis/legal_risk_assessment.json for hil_g4 (M4 strict schema).

The agent must create analysis/legal_risk_assessment.json with strict schema:
  {
    "risk_level": "high" | "medium" | "low",
    "applicable_clause": <str — must reference 第四十条 or Article 40 or company policy>,
    "days_shortfall": 20,
    "documentation_gaps": [<list of strings>],
    "recommendation": <str>
  }

Ground truth:
  - risk_level: "high" (multiple documentation gaps, truncated PIP, single warning)
  - applicable_clause: must reference 第四十条 or Article 40 (无过失性辞退 provision)
  - days_shortfall: exactly 20 (60-day minimum minus 40 actual days)
  - documentation_gaps: must list at least 2 specific gaps
  - recommendation: any non-empty string

Usage:
    python check_q12.py <workspace_path>
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

    json_path = workspace / "analysis" / "legal_risk_assessment.json"
    if not json_path.exists():
        print("FAILED: analysis/legal_risk_assessment.json not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: cannot parse analysis/legal_risk_assessment.json: {e}")
        sys.exit(1)

    # Check risk_level enum
    valid_risk_levels = {"high", "medium", "low"}
    risk_level = data.get("risk_level", "")
    if risk_level not in valid_risk_levels:
        errors.append(
            f"FAILED: risk_level must be one of {valid_risk_levels}, got {risk_level!r}"
        )

    # Check applicable_clause (must reference labor law article or company policy)
    clause = data.get("applicable_clause", "")
    if not clause or not isinstance(clause, str):
        errors.append("FAILED: missing or invalid 'applicable_clause' field")
    else:
        # Should reference 第四十条 or Article 40 or PIP policy
        clause_terms = [r'第四十条', r'40', r'Article', r'policy', r'PIP', r'渐进式']
        if not any(re.search(p, clause, re.IGNORECASE) for p in clause_terms):
            errors.append(
                f"FAILED: applicable_clause does not reference labor law "
                f"(got: {clause!r}; expected reference to 第四十条 or Article 40)"
            )

    # Check days_shortfall (must be exactly 20)
    days_shortfall = data.get("days_shortfall")
    if days_shortfall is None:
        errors.append("FAILED: missing 'days_shortfall' field")
    elif days_shortfall != 20:
        errors.append(
            f"FAILED: days_shortfall expected exactly 20, got {days_shortfall!r}"
        )

    # Check documentation_gaps (must be a list with >= 2 items)
    gaps = data.get("documentation_gaps", [])
    if not isinstance(gaps, list):
        errors.append(
            f"FAILED: documentation_gaps must be a list, got {type(gaps).__name__}"
        )
    elif len(gaps) < 2:
        errors.append(
            f"FAILED: documentation_gaps must have >= 2 items, got {len(gaps)}"
        )

    # Check recommendation (must be non-empty string)
    recommendation = data.get("recommendation", "")
    if not recommendation or not isinstance(recommendation, str) or len(recommendation.strip()) == 0:
        errors.append("FAILED: missing or empty 'recommendation' field")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
