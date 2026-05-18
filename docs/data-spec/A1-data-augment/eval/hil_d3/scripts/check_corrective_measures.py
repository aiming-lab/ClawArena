#!/usr/bin/env python3
"""check_corrective_measures.py — (not used in v2 question set; retained for backward compatibility).

v2 replaces old q27 (interim_corrective_measures.md) with q27 producing
  docs/YYYY-MM-DD_mandatory_reporting_memo.md and analysis/regulatory_citation_index.json
  — checked by check_mandatory_reporting.py.

If called directly, validates analysis/interim_corrective_measures.md if it exists,
otherwise exits 0 (not required in v2).
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_corrective_measures.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "interim_corrective_measures.md"

    if not target.exists():
        # Not required in v2 — pass gracefully
        print("PASSED (interim_corrective_measures.md not required in v2)")
        sys.exit(0)

    content = target.read_text(encoding="utf-8")
    errors = []

    headings = re.findall(r'^##\s+.+', content, re.MULTILINE)
    if len(headings) < 4:
        errors.append(f"found {len(headings)} ## headings, need >=4")

    has_clinalert = (
        re.search(r'\bClinAlert\b', content, re.IGNORECASE)
        or re.search(r'incident\s+report', content, re.IGNORECASE)
    )
    if not has_clinalert:
        errors.append("no ClinAlert or incident reporting reference found")

    has_agency = (
        re.search(r'\bagency\b', content, re.IGNORECASE)
        or re.search(r'\btemporary\b', content, re.IGNORECASE)
        or re.search(r'\bsupplemental\b', content, re.IGNORECASE)
        or re.search(r'\bper\s+diem\b', content, re.IGNORECASE)
    )
    if not has_agency:
        errors.append("no agency/temporary/supplemental staffing reference found")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
