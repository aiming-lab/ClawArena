#!/usr/bin/env python3
"""
check_q26_hierarchy.py — Validates analysis/source_reliability_hierarchy.md.

Checks:
  - Reliability hierarchy or tier structure established
  - 'GitHub' or 'commits' or 'LinkedIn' identified as high-reliability evidence
  - 'resume' identified as low-reliability or least credible for team size claims
  - >= 3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q26_hierarchy.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "source_reliability_hierarchy.md"

    if not target.exists():
        print("FAILED: file not found: analysis/source_reliability_hierarchy.md")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # Hierarchy/tier structure established
    if not re.search(
        r'tier|hierarch|rank|highest|lowest|most reliable|least reliable|level [1-4]',
        content, re.IGNORECASE
    ):
        failures.append(
            "Missing reliability hierarchy or tier structure "
            "('tier', 'hierarchy', 'ranked', 'highest/lowest', 'most/least reliable')"
        )

    # GitHub/LinkedIn as high-reliability
    if not re.search(
        r'GitHub|commit|LinkedIn',
        content, re.IGNORECASE
    ):
        failures.append(
            "Missing 'GitHub', 'commits', or 'LinkedIn' as high-reliability evidence sources"
        )

    if not re.search(
        r'(GitHub|LinkedIn|commit).{0,100}(high|tier 1|highest|most reliable|strong|direct)|'
        r'(high|tier 1|highest|most reliable|strong|direct).{0,100}(GitHub|LinkedIn|commit)',
        content, re.IGNORECASE
    ):
        failures.append(
            "GitHub/LinkedIn not identified as high-reliability tier "
            "(must be positioned at or near top of hierarchy)"
        )

    # Resume as low-reliability for team size
    if not re.search(r'resume', content, re.IGNORECASE):
        failures.append("Missing 'resume' in reliability discussion")

    if not re.search(
        r'resume.{0,100}(low|least|unverif|self.report|least credib|least reliable)|'
        r'(low|least|unverif|self.report|least credib|least reliable).{0,100}resume',
        content, re.IGNORECASE
    ):
        failures.append(
            "Resume not explicitly identified as low-reliability / least credible "
            "for team size claims (M2 requirement)"
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
