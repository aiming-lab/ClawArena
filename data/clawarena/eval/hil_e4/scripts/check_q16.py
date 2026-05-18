#!/usr/bin/env python3
"""
check_q16.py -- Verify analysis/field_narrative_vs_financials.json.

Ground truth financial allocations (actual USD from financial_tracking_Q2.md):
  Community Educator Training:   115000
  Community Mobilization:        131000
  School Infrastructure:         178000
  Personnel (Staff/Enrollment):  409000

Usage:
    python check_q16.py <workspace_path>
"""
import sys
import json
from pathlib import Path

TOLERANCE_USD = 1.0


def find_activity(comparisons, fragment):
    """Find activity entry whose name contains the fragment (case-insensitive)."""
    for item in comparisons:
        if fragment.lower() in item.get("activity", "").lower():
            return item
    return None


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    json_path = workspace / "analysis" / "field_narrative_vs_financials.json"
    if not json_path.exists():
        errors.append(f"FAILED: {json_path} not found")
    else:
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"FAILED: cannot parse {json_path}: {e}")
            data = {}

        if data:
            if "activity_comparisons" not in data:
                errors.append("FAILED: missing 'activity_comparisons' key")
            else:
                comps = data["activity_comparisons"]
                if not isinstance(comps, list) or len(comps) < 3:
                    errors.append(
                        f"FAILED: 'activity_comparisons' has {len(comps) if isinstance(comps, list) else 'N/A'} "
                        "items, need >= 3"
                    )
                else:
                    # Verify Community Educator Training financial allocation
                    training = find_activity(comps, "educator training") or find_activity(comps, "training")
                    if training is None:
                        errors.append(
                            "FAILED: no Community Educator Training activity entry found"
                        )
                    else:
                        alloc = training.get("financial_allocation_usd")
                        if alloc is None:
                            errors.append(
                                "FAILED: Community Educator Training missing 'financial_allocation_usd'"
                            )
                        elif abs(float(alloc) - 115000.0) > TOLERANCE_USD:
                            errors.append(
                                f"FAILED: Community Educator Training financial_allocation_usd "
                                f"expected 115000, got {alloc}"
                            )
                        # narrative_count should be 47 (specific number given in field narrative)
                        nc = training.get("narrative_count")
                        if nc is not None and nc != 47:
                            errors.append(
                                f"FAILED: Community Educator Training narrative_count "
                                f"expected 47, got {nc}"
                            )

                    # Verify Community Mobilization financial allocation
                    mob = find_activity(comps, "mobilization")
                    if mob is None:
                        errors.append(
                            "FAILED: no Community Mobilization activity entry found"
                        )
                    else:
                        alloc = mob.get("financial_allocation_usd")
                        if alloc is None:
                            errors.append(
                                "FAILED: Community Mobilization missing 'financial_allocation_usd'"
                            )
                        elif abs(float(alloc) - 131000.0) > TOLERANCE_USD:
                            errors.append(
                                f"FAILED: Community Mobilization financial_allocation_usd "
                                f"expected 131000, got {alloc}"
                            )

                    # Must have at least one null narrative_count (qualitative activity)
                    has_null = any(item.get("narrative_count") is None for item in comps)
                    if not has_null:
                        errors.append(
                            "FAILED: no activity with narrative_count==null; "
                            "qualitative activities (mobilization, infrastructure) should be null"
                        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
