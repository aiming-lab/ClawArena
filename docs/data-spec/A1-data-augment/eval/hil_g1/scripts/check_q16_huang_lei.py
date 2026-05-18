#!/usr/bin/env python3
"""
check_q16_huang_lei.py — Validates analysis/huang_lei_assessment_analysis.md.

Checks:
  - '4.3' present (technical score)
  - '2.8' present (leadership score)
  - Technical genuine vs leadership inflated contrast stated
  - Signal weighting or prioritization language present
  - >= 3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q16_huang_lei.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "huang_lei_assessment_analysis.md"

    if not target.exists():
        print("FAILED: file not found: analysis/huang_lei_assessment_analysis.md")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    if not re.search(r'\b4\.3\b', content):
        failures.append("Missing technical score '4.3'")

    if not re.search(r'\b2\.8\b', content):
        failures.append("Missing leadership score '2.8'")

    # Technical genuine vs leadership inflated contrast
    if not re.search(r'technical|tech\b', content, re.IGNORECASE):
        failures.append("Missing technical competence discussion")
    if not re.search(
        r'inflat|overstat|generic|textbook|leadership.{0,60}(concern|low|below|insuff)',
        content, re.IGNORECASE
    ):
        failures.append(
            "Missing contrast: leadership claims inflated / generic answers "
            "(e.g. 'inflated', 'overstated', 'textbook', 'leadership concern')"
        )

    # Signal weighting
    if not re.search(
        r'weight|priorit|more relevant|signal|consider|balance',
        content, re.IGNORECASE
    ):
        failures.append(
            "Missing signal weighting language "
            "('weight', 'prioritize', 'more relevant', 'signal')"
        )

    headings = re.findall(r'^## ', content, re.MULTILINE)
    if len(headings) < 3:
        failures.append(f"Only {len(headings)} ## headings (expected >= 3)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
