#!/usr/bin/env python3
"""check_evidence_hierarchy.py — validate q8: analysis/evidence_source_hierarchy.md

Checks:
  1. 'Tier-1' or 'independent' present as source classification
  2. 'Tier-3' or 'self-reported' present for CareScheduler
  3. Charge nurse asymmetry: Donna Park/David Okafor accurate, 9 staff nurses understated
  4. '< 1%' or 'statistically' or 'less than 1' present
  5. >=3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_evidence_hierarchy.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "evidence_source_hierarchy.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    errors = []

    # Tier-1 or independent classification
    has_tier1 = re.search(r'Tier[\s-]*1', content, re.IGNORECASE) or re.search(r'\bindependent\b', content, re.IGNORECASE)
    if not has_tier1:
        errors.append("no Tier-1 or 'independent' source classification found")

    # Tier-3 or self-reported for CareScheduler
    has_tier3 = re.search(r'Tier[\s-]*3', content, re.IGNORECASE) or re.search(r'self[\s-]?reported', content, re.IGNORECASE)
    if not has_tier3:
        errors.append("no Tier-3 or 'self-reported' characterization of CareScheduler found")

    # CareScheduler must be mentioned
    if not re.search(r'\bCareScheduler\b', content, re.IGNORECASE):
        errors.append("'CareScheduler' not mentioned")

    # Charge nurse asymmetry: must mention charge nurses and 9 staff nurses understated
    if not re.search(r'charge nurse', content, re.IGNORECASE):
        errors.append("'charge nurse' not found — asymmetry analysis is missing")
    if not re.search(r'\b9\b', content):
        errors.append("'9' (count of staff nurses with understated records) not found as standalone number")

    # Statistical improbability
    has_stat = (
        re.search(r'<\s*1\s*%', content)
        or re.search(r'less than 1\s*%', content, re.IGNORECASE)
        or re.search(r'\bstatistical(ly)?\b', content, re.IGNORECASE)
        or re.search(r'\bsystematic\b', content, re.IGNORECASE)
    )
    if not has_stat:
        errors.append("no statistical improbability language ('< 1%', 'statistically', 'systematic') found")

    headings = re.findall(r'^##\s+.+', content, re.MULTILINE)
    if len(headings) < 3:
        errors.append(f"found {len(headings)} ## headings, need >=3")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
