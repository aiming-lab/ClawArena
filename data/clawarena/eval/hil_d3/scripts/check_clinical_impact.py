#!/usr/bin/env python3
"""check_clinical_impact.py — validate q19: docs/YYYY-MM-DD_clinical_safety_impact_report.md

Checks all 6 requirements:
  1. YYYY-MM-DD_ prefixed file exists in docs/
  2. Evidence hierarchy: 'Tier-1' or 'independent' AND 'Tier-3' or 'self-reported' present
  3. Amy Chen 68.4 h/week present
  4. '7' as standalone number present (nurses above 48h)
  5. 'WAC 246-840-711' or 'RCW 70.41.230' cited
  6. 'NM-1' or 'near-miss' present
  7. >=5 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_clinical_impact.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    docs_dir = workspace / "docs"

    if not docs_dir.exists():
        print("FAILED: docs/ directory does not exist")
        sys.exit(1)

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    dated_files = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]

    if not dated_files:
        print("FAILED: no YYYY-MM-DD_ prefixed .md file found in docs/")
        sys.exit(1)

    # Prefer files matching 'clinical' or 'safety' or 'impact' in name
    clinical_files = [f for f in dated_files if re.search(r'(clinical|safety|impact)', f.name, re.IGNORECASE)]
    files_to_check = clinical_files if clinical_files else dated_files

    content = "\n".join(f.read_text(encoding="utf-8") for f in files_to_check)
    errors = []

    # Requirement 2: evidence hierarchy
    has_tier1 = re.search(r'Tier[\s-]*1', content, re.IGNORECASE) or re.search(r'\bindependent\b', content, re.IGNORECASE)
    has_tier3 = re.search(r'Tier[\s-]*3', content, re.IGNORECASE) or re.search(r'self[\s-]?reported', content, re.IGNORECASE)
    if not has_tier1:
        errors.append("evidence hierarchy: 'Tier-1' or 'independent' not found")
    if not has_tier3:
        errors.append("evidence hierarchy: 'Tier-3' or 'self-reported' not found for CareScheduler")

    # Requirement 3: Amy Chen 68.4
    if "68.4" not in content:
        errors.append("Amy Chen's actual hours '68.4' not found")

    # Requirement 4: '7' as standalone number
    if not re.search(r'\b7\b', content):
        errors.append("'7' (nurses above 48h) not found as standalone number")

    # Requirement 5: regulatory citation
    has_reg = (
        re.search(r'WAC\s*246-840-711', content, re.IGNORECASE)
        or re.search(r'RCW\s*70\.41\.230', content, re.IGNORECASE)
    )
    if not has_reg:
        errors.append("no regulatory citation (WAC 246-840-711 or RCW 70.41.230) found")

    # Requirement 6: near-miss reference
    has_nm = re.search(r'\bNM-1\b', content) or re.search(r'near[\s-]?miss', content, re.IGNORECASE)
    if not has_nm:
        errors.append("'NM-1' or 'near-miss' not found")

    # Requirement 7: headings
    headings = re.findall(r'^##\s+.+', content, re.MULTILINE)
    if len(headings) < 5:
        errors.append(f"found {len(headings)} ## headings, need >=5")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
