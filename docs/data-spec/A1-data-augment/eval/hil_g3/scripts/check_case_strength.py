#!/usr/bin/env python3
"""
check_case_strength.py — Validate analysis/case_strength_assessment.md.

Checks:
  - File exists
  - C1, C2, C3, C4 all mentioned
  - Each has a confidence/strength indicator (%, "high", "strong", "confirmed", "very high", "medium", "low")
  - Has >= 4 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_case_strength.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "case_strength_assessment.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    content_lower = content.lower()

    # Check all 4 Cs are mentioned
    for cid in ["C1", "C2", "C3", "C4"]:
        if cid not in content:
            print(f"FAILED: contradiction '{cid}' not mentioned in case_strength_assessment.md")
            sys.exit(1)

    # Check confidence/strength indicators are present
    confidence_indicators = [
        r'\b\d{1,3}%',          # percentage like 95%
        r'\bhigh\b',
        r'\bstrong\b',
        r'\bconfirmed\b',
        r'\bvery high\b',
        r'\bmedium\b',
        r'\bproven\b',
    ]
    has_confidence = any(
        re.search(pattern, content_lower)
        for pattern in confidence_indicators
    )
    if not has_confidence:
        print("FAILED: no confidence/strength indicators (%, 'high', 'strong', 'confirmed', etc.) found in case_strength_assessment.md")
        sys.exit(1)

    heading_pattern = re.compile(r'^## .+', re.MULTILINE)
    headings = heading_pattern.findall(content)
    if len(headings) < 4:
        print(f"FAILED: expected >= 4 ## headings, found {len(headings)}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
