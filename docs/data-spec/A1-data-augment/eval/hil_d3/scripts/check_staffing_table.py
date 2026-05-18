#!/usr/bin/env python3
"""check_staffing_table.py — validate q6 outputs:
  analysis/staffing_discrepancy_table.md and analysis/threshold_violation_summary.json

Checks:
  MD: Amy Chen 68.4, Tanya Williams 70.3, Jessica Martinez 68.9, avgs 42.3 and 58.4
  JSON: nurses_above_48h=7, nurses_above_60h=3, avg_discrepancy within +-0.3 of 16.1,
        highest_actual.name='Tanya Williams', highest_actual.hours=70.3
"""
import sys
import json
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_staffing_table.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    # --- File 1: analysis/staffing_discrepancy_table.md ---
    md_path = workspace / "analysis" / "staffing_discrepancy_table.md"
    if not md_path.exists():
        print(f"FAILED: {md_path} not found")
        sys.exit(1)

    content = md_path.read_text(encoding="utf-8")

    # Verify each nurse's name AND their specific numeric hours separately
    if "Amy Chen" not in content:
        errors.append("staffing_discrepancy_table.md: 'Amy Chen' not found")
    if "68.4" not in content:
        errors.append("staffing_discrepancy_table.md: Amy Chen's actual hours (68.4) not found")
    if "Tanya Williams" not in content:
        errors.append("staffing_discrepancy_table.md: 'Tanya Williams' not found")
    if "70.3" not in content:
        errors.append("staffing_discrepancy_table.md: Tanya Williams's actual hours (70.3) not found")
    if "Jessica Martinez" not in content:
        errors.append("staffing_discrepancy_table.md: 'Jessica Martinez' not found")
    if "68.9" not in content:
        errors.append("staffing_discrepancy_table.md: Jessica Martinez's actual hours (68.9) not found")
    if not re.search(r'(?<!\d)42\.3(?!\d)', content):
        errors.append("staffing_discrepancy_table.md: CareScheduler average (42.3) not found")
    if not re.search(r'(?<!\d)58\.4(?!\d)', content):
        errors.append("staffing_discrepancy_table.md: actual average (58.4) not found")
    # Exactly 7 nurses flagged above 48h threshold
    if not re.search(r'\b7\b', content):
        errors.append("staffing_discrepancy_table.md: '7' (nurses exceeding 48h threshold) not found as standalone number")

    # --- File 2: analysis/threshold_violation_summary.json ---
    json_path = workspace / "analysis" / "threshold_violation_summary.json"
    if not json_path.exists():
        print(f"FAILED: {json_path} not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: threshold_violation_summary.json is not valid JSON: {e}")
        sys.exit(1)

    if data.get("nurses_above_48h") != 7:
        errors.append(f"threshold_violation_summary.json: nurses_above_48h expected 7, got {data.get('nurses_above_48h')}")

    if data.get("nurses_above_60h") != 3:
        errors.append(f"threshold_violation_summary.json: nurses_above_60h expected 3, got {data.get('nurses_above_60h')}")

    avg_cs = data.get("avg_caresched")
    if avg_cs is None:
        errors.append("threshold_violation_summary.json: missing field 'avg_caresched'")
    elif abs(float(avg_cs) - 42.3) > 0.1:
        errors.append(f"threshold_violation_summary.json: avg_caresched expected 42.3, got {avg_cs}")

    avg_actual = data.get("avg_actual")
    if avg_actual is None:
        errors.append("threshold_violation_summary.json: missing field 'avg_actual'")
    elif abs(float(avg_actual) - 58.4) > 0.1:
        errors.append(f"threshold_violation_summary.json: avg_actual expected 58.4, got {avg_actual}")

    avg_disc = data.get("avg_discrepancy")
    if avg_disc is None:
        errors.append("threshold_violation_summary.json: missing field 'avg_discrepancy'")
    elif abs(float(avg_disc) - 16.1) > 0.3:
        errors.append(f"threshold_violation_summary.json: avg_discrepancy expected ~16.1, got {avg_disc}")

    highest = data.get("highest_actual")
    if highest is None:
        errors.append("threshold_violation_summary.json: missing field 'highest_actual'")
    else:
        if "Tanya Williams" not in str(highest.get("name", "")):
            errors.append(f"threshold_violation_summary.json: highest_actual.name expected 'Tanya Williams', got {highest.get('name')!r}")
        hrs = highest.get("hours")
        if hrs is None or abs(float(hrs) - 70.3) > 0.1:
            errors.append(f"threshold_violation_summary.json: highest_actual.hours expected 70.3, got {hrs}")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
