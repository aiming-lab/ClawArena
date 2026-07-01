#!/usr/bin/env python3
"""
check_threshold_violations.py — Validate analysis/threshold_violation_analysis.json

Checks:
  1. File exists and is valid JSON
  2. JSON is an array with ≥7 entries where exceeds_48h == true
  3. Exactly 3 entries where exceeds_60h == true
  4. Entry for Amy Chen (RN-02) has actual_hours close to 68.4 (±0.2 tolerance)
"""
import sys
import json
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_threshold_violations.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "threshold_violation_analysis.json"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"FAILED: invalid JSON: {e}")
        sys.exit(1)

    if not isinstance(data, list):
        print("FAILED: JSON root must be an array")
        sys.exit(1)

    errors = []

    above_48 = [e for e in data if e.get("exceeds_48h") is True]
    above_60 = [e for e in data if e.get("exceeds_60h") is True]

    if len(above_48) != 7:
        errors.append(f"expected exactly 7 entries with exceeds_48h=true, found {len(above_48)}")
    if len(above_60) != 3:
        errors.append(f"expected exactly 3 entries with exceeds_60h=true, found {len(above_60)}")

    # Verify Amy Chen (RN-02) actual hours ≈ 68.4
    amy_entry = None
    for e in data:
        nid = str(e.get("nurse_id", "")).upper()
        name = str(e.get("name", "")).lower()
        if "rn-02" in nid or "rn02" in nid or "amy" in name or "chen" in name:
            amy_entry = e
            break

    if amy_entry is None:
        errors.append("no entry found for Amy Chen / RN-02")
    else:
        actual = amy_entry.get("actual_hours")
        try:
            val = float(actual)
            if abs(val - 68.4) > 0.2:
                errors.append(
                    f"Amy Chen actual_hours={val} is not within ±0.2 of 68.4"
                )
        except (TypeError, ValueError):
            errors.append(f"Amy Chen actual_hours '{actual}' is not a valid number")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
