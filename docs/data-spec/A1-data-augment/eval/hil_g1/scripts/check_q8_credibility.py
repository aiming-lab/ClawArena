#!/usr/bin/env python3
"""
check_q8_credibility.py — Validates analysis/source_credibility_assessment.md.

Checks:
  - All three sources mentioned: resume (or candidate), Liu Wei, Huang Lei (or interview)
  - Credibility hierarchy or ranking established
  - Resume explicitly identified as least reliable/credible for team size claim
  - >= 3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q8_credibility.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "source_credibility_assessment.md"

    if not target.exists():
        print("FAILED: file not found: analysis/source_credibility_assessment.md")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # Three sources
    if not re.search(r'resume|self.report', content, re.IGNORECASE):
        failures.append("Missing resume as a source in credibility comparison")
    if not re.search(r'Liu Wei|reference', content, re.IGNORECASE):
        failures.append("Missing Liu Wei reference as a source")
    if not re.search(r'Huang Lei|interview observation|hesitat|self.correct', content, re.IGNORECASE):
        failures.append("Missing Huang Lei interview observation as a source")

    # Credibility hierarchy stated
    if not re.search(
        r'hierarch|rank|reliable|credib|weight|tier|priorit',
        content, re.IGNORECASE
    ):
        failures.append(
            "Missing credibility hierarchy or ranking language "
            "(e.g. 'hierarchy', 'most reliable', 'ranked', 'weighted')"
        )

    # Resume identified as least credible for team size
    if not re.search(
        r'resume.{0,80}(least|low|unreliab|unverif|self.report)|'
        r'(least|low|unreliab|unverif|self.report).{0,80}resume',
        content, re.IGNORECASE
    ):
        failures.append(
            "Missing explicit statement that resume is least credible/reliable "
            "for the team size claim (M2 requirement)"
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
