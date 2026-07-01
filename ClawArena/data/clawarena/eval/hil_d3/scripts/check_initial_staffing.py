#!/usr/bin/env python3
"""check_initial_staffing.py — validate q3 outputs:
  analysis/initial_staffing_assessment.md and analysis/hr_metrics_interpretation.json

Checks:
  MD: FTE 11/13, CareScheduler avg 42.3, sick leave 4.2, >=3 ## headings
  JSON: sick_leave_rate_unit=4.2, sick_leave_rate_hospital=4.6,
        presenteeism_risk_higher=true, caresched_avg_weekly_hours=42.3
  Cross: both files agree on 42.3 h/week
"""
import sys
import json
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_initial_staffing.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    # --- File 1: analysis/initial_staffing_assessment.md ---
    md_path = workspace / "analysis" / "initial_staffing_assessment.md"
    if not md_path.exists():
        print(f"FAILED: {md_path} not found")
        sys.exit(1)

    md_content = md_path.read_text(encoding="utf-8")

    if not re.search(r'\b11\b', md_content):
        errors.append("initial_staffing_assessment.md: '11' (actual FTE count) not found as standalone number")
    if not re.search(r'\b13\b', md_content):
        errors.append("initial_staffing_assessment.md: '13' (FTE target) not found as standalone number")
    if not re.search(r'(?<!\d)42\.3(?!\d)', md_content):
        errors.append("initial_staffing_assessment.md: '42.3' (CareScheduler avg) not found")
    if not re.search(r'\b48\b', md_content):
        errors.append("initial_staffing_assessment.md: '48' (legal threshold) not found")
    if not re.search(r'(?<!\d)4\.2(?!\d)', md_content):
        errors.append("initial_staffing_assessment.md: '4.2' (unit sick leave rate) not found")

    headings = re.findall(r'^##\s+.+', md_content, re.MULTILINE)
    if len(headings) < 3:
        errors.append(f"initial_staffing_assessment.md: found {len(headings)} ## headings, need >=3")

    # --- File 2: analysis/hr_metrics_interpretation.json ---
    json_path = workspace / "analysis" / "hr_metrics_interpretation.json"
    if not json_path.exists():
        print(f"FAILED: {json_path} not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: hr_metrics_interpretation.json is not valid JSON: {e}")
        sys.exit(1)

    slr_unit = data.get("sick_leave_rate_unit")
    if slr_unit is None:
        errors.append("hr_metrics_interpretation.json: missing field 'sick_leave_rate_unit'")
    elif abs(float(slr_unit) - 4.2) > 0.05:
        errors.append(f"hr_metrics_interpretation.json: sick_leave_rate_unit expected 4.2, got {slr_unit}")

    slr_hosp = data.get("sick_leave_rate_hospital")
    if slr_hosp is None:
        errors.append("hr_metrics_interpretation.json: missing field 'sick_leave_rate_hospital'")
    elif abs(float(slr_hosp) - 4.6) > 0.05:
        errors.append(f"hr_metrics_interpretation.json: sick_leave_rate_hospital expected 4.6, got {slr_hosp}")

    pres_risk = data.get("presenteeism_risk_higher")
    if pres_risk is None:
        errors.append("hr_metrics_interpretation.json: missing field 'presenteeism_risk_higher'")
    elif pres_risk is not True:
        errors.append(f"hr_metrics_interpretation.json: presenteeism_risk_higher expected true (boolean), got {pres_risk!r}")

    cs_avg = data.get("caresched_avg_weekly_hours")
    if cs_avg is None:
        errors.append("hr_metrics_interpretation.json: missing field 'caresched_avg_weekly_hours'")
    elif abs(float(cs_avg) - 42.3) > 0.1:
        errors.append(f"hr_metrics_interpretation.json: caresched_avg_weekly_hours expected 42.3, got {cs_avg}")

    # --- Cross-file consistency: both files must reference 42.3 ---
    if not re.search(r'(?<!\d)42\.3(?!\d)', md_content) and not errors:
        errors.append("Cross-file check: initial_staffing_assessment.md does not contain '42.3' (inconsistent with hr_metrics_interpretation.json)")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
