#!/usr/bin/env python3
"""
check_q6.py -- Verify analysis/budget_utilization.json.

Ground truth (from financial_tracking_Q2.md):
  Personnel (Staff):                actual=409000, approved=412000, util=99.3%
  Community Educator Training:      actual=115000, approved=148000, util=77.7%
  Community Mobilization:           actual=131000, approved=94000,  util=139.4%
  School Infrastructure Materials:  actual=178000, approved=189000, util=94.2%
  Admin and Overhead:               actual=87000,  approved=90000,  util=96.7%
  Total actual: 920000, Total approved: 933000

Usage:
    python check_q6.py <workspace_path>
"""
import sys
import json
from pathlib import Path

GROUND_TRUTH = [
    {"name_fragment": "personnel", "actual": 409000.0, "approved": 412000.0, "util": 99.3, "status": "on_track"},
    {"name_fragment": "educator training", "actual": 115000.0, "approved": 148000.0, "util": 77.7, "status": "under"},
    {"name_fragment": "mobilization", "actual": 131000.0, "approved": 94000.0, "util": 139.4, "status": "over"},
    {"name_fragment": "infrastructure", "actual": 178000.0, "approved": 189000.0, "util": 94.2, "status": "on_track"},
    {"name_fragment": "admin", "actual": 87000.0, "approved": 90000.0, "util": 96.7, "status": "on_track"},
]

TOLERANCE_USD = 0.01
TOLERANCE_PCT = 0.15


def find_category(categories, fragment):
    """Find category entry whose name contains the fragment (case-insensitive)."""
    for cat in categories:
        if fragment.lower() in cat.get("name", "").lower():
            return cat
    return None


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    json_path = workspace / "analysis" / "budget_utilization.json"
    if not json_path.exists():
        errors.append(f"FAILED: {json_path} not found")
    else:
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"FAILED: cannot parse {json_path}: {e}")
            data = {}

        if data:
            if "categories" not in data:
                errors.append("FAILED: missing 'categories' key")
            else:
                cats = data["categories"]
                if not isinstance(cats, list) or len(cats) < 5:
                    errors.append(
                        f"FAILED: 'categories' has {len(cats) if isinstance(cats, list) else 'N/A'} "
                        "items, need 5"
                    )
                else:
                    for gt in GROUND_TRUTH:
                        cat = find_category(cats, gt["name_fragment"])
                        if cat is None:
                            errors.append(
                                f"FAILED: no category found matching '{gt['name_fragment']}'"
                            )
                            continue

                        util = cat.get("utilization_pct")
                        if util is None:
                            errors.append(
                                f"FAILED: category '{cat.get('name')}' missing 'utilization_pct'"
                            )
                        elif abs(float(util) - gt["util"]) > TOLERANCE_PCT:
                            errors.append(
                                f"FAILED: category '{cat.get('name')}' utilization_pct "
                                f"expected {gt['util']:.1f}%, got {util}"
                            )

                        status = cat.get("status", "")
                        if status not in {"over", "under", "on_track"}:
                            errors.append(
                                f"FAILED: category '{cat.get('name')}' status '{status}' "
                                "not in ['over','under','on_track']"
                            )
                        elif status != gt["status"]:
                            errors.append(
                                f"FAILED: category '{cat.get('name')}' status "
                                f"expected '{gt['status']}', got '{status}'"
                            )

            # Verify totals
            total_actual = data.get("total_actual_usd")
            if total_actual is not None:
                if abs(float(total_actual) - 920000.0) > TOLERANCE_USD:
                    errors.append(
                        f"FAILED: total_actual_usd expected 920000.0, got {total_actual}"
                    )
            else:
                errors.append("FAILED: missing 'total_actual_usd' field")

            total_approved = data.get("total_approved_usd")
            if total_approved is not None:
                if abs(float(total_approved) - 933000.0) > TOLERANCE_USD:
                    errors.append(
                        f"FAILED: total_approved_usd expected 933000.0, got {total_approved}"
                    )
            else:
                errors.append("FAILED: missing 'total_approved_usd' field")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
