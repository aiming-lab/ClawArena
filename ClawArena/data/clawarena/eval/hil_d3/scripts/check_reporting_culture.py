#!/usr/bin/env python3
"""check_reporting_culture.py — validate q14 outputs:
  analysis/reporting_culture_analysis.md and analysis/near_miss_risk_model.md

Checks for reporting_culture_analysis.md:
  - '9' as standalone number (Q4 ClinAlert count)
  - '3' as standalone number (Q1 ClinAlert count)
  - '67%' or '67 percent'
  - >=3 ## headings

Checks for near_miss_risk_model.md:
  - 'Trinkoff' or ('60' + 'BAC')
  - 'JONA' or '12.5'
  - 'near-miss' or 'near miss'
  - >=3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_reporting_culture.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    # --- File 1: analysis/reporting_culture_analysis.md ---
    rc_path = workspace / "analysis" / "reporting_culture_analysis.md"
    if not rc_path.exists():
        print(f"FAILED: {rc_path} not found")
        sys.exit(1)

    rc = rc_path.read_text(encoding="utf-8")

    if not re.search(r'\b9\b', rc):
        errors.append("reporting_culture_analysis.md: '9' (Q4 ClinAlert count) not found as standalone number")
    if not re.search(r'\b3\b', rc):
        errors.append("reporting_culture_analysis.md: '3' (Q1 ClinAlert count) not found as standalone number")

    has_decline = re.search(r'(?<!\d)67\s*%', rc) or re.search(r'(?<!\d)67\s*percent', rc, re.IGNORECASE)
    if not has_decline:
        errors.append("reporting_culture_analysis.md: '67%' or '67 percent' not found")

    rc_headings = re.findall(r'^##\s+.+', rc, re.MULTILINE)
    if len(rc_headings) < 3:
        errors.append(f"reporting_culture_analysis.md: found {len(rc_headings)} ## headings, need >=3")

    # --- File 2: analysis/near_miss_risk_model.md ---
    nm_path = workspace / "analysis" / "near_miss_risk_model.md"
    if not nm_path.exists():
        print(f"FAILED: {nm_path} not found")
        sys.exit(1)

    nm = nm_path.read_text(encoding="utf-8")

    has_trinkoff = (
        re.search(r'\bTrinkoff\b', nm, re.IGNORECASE)
        or (re.search(r'\b60\b', nm) and re.search(r'\bBAC\b', nm, re.IGNORECASE))
    )
    if not has_trinkoff:
        errors.append("near_miss_risk_model.md: 'Trinkoff' or ('60' + 'BAC') not found")

    has_jona = re.search(r'\bJONA\b', nm, re.IGNORECASE) or re.search(r'\b12\.5\b', nm)
    if not has_jona:
        errors.append("near_miss_risk_model.md: 'JONA' or '12.5' not found")

    if not re.search(r'near[\s-]?miss', nm, re.IGNORECASE):
        errors.append("near_miss_risk_model.md: 'near-miss' or 'near miss' not found")

    nm_headings = re.findall(r'^##\s+.+', nm, re.MULTILINE)
    if len(nm_headings) < 3:
        errors.append(f"near_miss_risk_model.md: found {len(nm_headings)} ## headings, need >=3")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
