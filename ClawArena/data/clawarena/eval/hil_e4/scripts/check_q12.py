#!/usr/bin/env python3
"""
check_q12.py -- Verify analysis/compliance_status.json (M4 strict schema).

Usage:
    python check_q12.py <workspace_path>
"""
import sys
import json
from pathlib import Path

VALID_OVERALL_STATUS = {"compliant", "non-compliant", "at-risk"}
TOLERANCE_PCT = 0.15


def find_category(categories, fragment):
    """Find category by name fragment (case-insensitive)."""
    for cat in categories:
        if fragment.lower() in cat.get("category", "").lower():
            return cat
    return None


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    json_path = workspace / "analysis" / "compliance_status.json"
    if not json_path.exists():
        errors.append(f"FAILED: {json_path} not found")
    else:
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"FAILED: cannot parse {json_path}: {e}")
            data = {}

        if data:
            if "compliance_report" not in data:
                errors.append("FAILED: missing top-level 'compliance_report' key")
            else:
                report = data["compliance_report"]

                # Check reporting_period
                if report.get("reporting_period") != "Q2":
                    errors.append(
                        f"FAILED: reporting_period expected 'Q2', "
                        f"got {report.get('reporting_period')!r}"
                    )

                # Check categories array
                cats = report.get("categories", [])
                if not isinstance(cats, list) or len(cats) < 5:
                    errors.append(
                        f"FAILED: 'categories' has {len(cats) if isinstance(cats, list) else 'N/A'} "
                        "entries, need 5"
                    )
                else:
                    # Verify Community Mobilization is non-compliant with ~139.4% utilization
                    mob = find_category(cats, "mobilization")
                    if mob is None:
                        errors.append(
                            "FAILED: no Community Mobilization category found"
                        )
                    else:
                        util = mob.get("utilization_pct")
                        if util is not None:
                            if abs(float(util) - 139.4) > TOLERANCE_PCT:
                                errors.append(
                                    f"FAILED: Community Mobilization utilization_pct "
                                    f"expected ~139.4, got {util}"
                                )
                        if mob.get("compliant") is not False:
                            errors.append(
                                "FAILED: Community Mobilization 'compliant' must be false"
                            )

                # Check overall_status
                overall_status = report.get("overall_status", "")
                if overall_status not in VALID_OVERALL_STATUS:
                    errors.append(
                        f"FAILED: overall_status '{overall_status}' not in "
                        f"{sorted(VALID_OVERALL_STATUS)}"
                    )
                elif overall_status != "non-compliant":
                    errors.append(
                        f"FAILED: overall_status expected 'non-compliant' "
                        f"(Mobilization at 139.4%), got '{overall_status}'"
                    )

                # Check petrova_flagged_items
                flagged = report.get("petrova_flagged_items", [])
                if not isinstance(flagged, list) or len(flagged) < 1:
                    errors.append(
                        "FAILED: 'petrova_flagged_items' must be a non-empty list"
                    )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
