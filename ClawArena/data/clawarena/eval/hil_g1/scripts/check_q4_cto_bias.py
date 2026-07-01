#!/usr/bin/env python3
"""
check_q4_cto_bias.py — Validates analysis/cto_urgency_bias_analysis.md.

Checks:
  - 'Q2' or 'board' present (CTO urgency context)
  - 'urgency' or 'pressure' or 'deadline' present
  - Bias or integrity risk analyzed
  - Explicit warning about proceeding without resolving discrepancies
  - >= 2 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q4_cto_bias.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "cto_urgency_bias_analysis.md"

    if not target.exists():
        print(f"FAILED: file not found: analysis/cto_urgency_bias_analysis.md")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    if not re.search(r'\bQ2\b|board|business.critical', content, re.IGNORECASE):
        failures.append("Missing CTO urgency context ('Q2', 'board', or 'business-critical')")

    if not re.search(r'urgency|pressure|deadline|timeline', content, re.IGNORECASE):
        failures.append("Missing urgency/pressure language")

    if not re.search(r'bias|integrity|risk|compromise|rigor|shortcut', content, re.IGNORECASE):
        failures.append("Missing bias or integrity risk analysis")

    if not re.search(
        r'without.resolv|not.resolv|proceed.without|hiring.risk|legal|reputat',
        content, re.IGNORECASE
    ):
        failures.append(
            "Missing explicit warning about proceeding without resolving discrepancies "
            "(e.g. 'without resolving', 'hiring risk', 'legal', 'reputational')"
        )

    headings = re.findall(r'^## ', content, re.MULTILINE)
    if len(headings) < 2:
        failures.append(f"Only {len(headings)} ## headings (expected >= 2)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
