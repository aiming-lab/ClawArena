#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_ropa.py — RoPA field validation utility.

Checks each processing activity in a RoPA JSON file against the required
Art. 30(1) controller fields per the CIRCL JSON Schema.

Usage: python scripts/validate_ropa.py <ropa_json_file>
"""
import json
import sys
from pathlib import Path

REQUIRED_FIELDS = [
    "name_and_contact_details",
    "purposes",
    "data_subject_categories",
    "personal_data_categories",
    "recipient_categories",
    "third_country_transfers",
    "retention_periods",
    "security_measures",
]


def validate_ropa(path: str) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    activities = data.get("activities", [])
    results = {"total": len(activities), "gap_count": 0, "activities": []}

    for act in activities:
        act_id = act.get("activity_id", "UNKNOWN")
        missing = [f for f in REQUIRED_FIELDS if f not in act or act[f] is None]
        status = "OK" if not missing else "MISSING_FIELDS"
        if missing:
            results["gap_count"] += 1
        results["activities"].append({
            "activity_id": act_id,
            "status": status,
            "missing_fields": missing,
        })

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_ropa.py <ropa_json_file>")
        sys.exit(1)
    r = validate_ropa(sys.argv[1])
    print(json.dumps(r, indent=2))
    if r["gap_count"] > 0:
        print(f"\n[GAPS FOUND] {r['gap_count']} activities have missing required fields.")
        sys.exit(1)
    else:
        print("\n[OK] All activities have required fields.")
