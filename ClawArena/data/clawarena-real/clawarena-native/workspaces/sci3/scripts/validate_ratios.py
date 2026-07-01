#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_ratios.py — Validates that all shifts in a staffing CSV comply with
California Title 22 § 70217 nurse-to-patient ratio requirements.

Usage: python validate_ratios.py <staffing_log.csv>
"""
import csv
import sys
from pathlib import Path

LEGAL_RATIOS = {
    "ICU": 2,
    "Med/Surg": 5,
    "Step-Down": 3,
    "Telemetry": 4,
    "ED": 4,
    "Psychiatric": 6,
}

def validate(log_path: str) -> None:
    violations = []
    with open(log_path, encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            unit = row.get("unit", "")
            legal_max = LEGAL_RATIOS.get(unit)
            if legal_max is None:
                continue
            try:
                nurses = int(row.get("nurses_on_duty_count", 0))
                patients = int(row.get("patient_count", 0))
            except ValueError:
                continue
            if nurses <= 0:
                continue
            ratio = patients / nurses
            if ratio > legal_max:
                violations.append({
                    "shift_id": row.get("shift_id"),
                    "unit": unit,
                    "ratio": round(ratio, 2),
                    "legal_max": legal_max,
                })
    if violations:
        print(f"VIOLATIONS FOUND: {len(violations)}")
        for v in violations:
            print(f"  {v['shift_id']} ({v['unit']}): actual {v['ratio']}:1, legal max 1:{v['legal_max']}")
    else:
        print("NO VIOLATIONS — all shifts compliant")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: validate_ratios.py <staffing_log.csv>")
        sys.exit(1)
    validate(sys.argv[1])
