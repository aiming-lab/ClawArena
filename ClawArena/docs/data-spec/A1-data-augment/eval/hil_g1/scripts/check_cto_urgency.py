#!/usr/bin/env python3
"""
check_cto_urgency.py — Validates analysis/cto_urgency_context.md.

Checks:
- "Q2" or "business-critical" or "board" present (CTO urgency context)
- "pressure" or "urgency" or "timeline" present
- Bias or integrity risk mentioned
- >= 2 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_cto_urgency.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "cto_urgency_context.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # CTO urgency context
    if not re.search(r'\bQ2\b|business.critical|board', content, re.IGNORECASE):
        failures.append("Missing CTO urgency context ('Q2', 'business-critical', or 'board')")

    # Pressure / urgency language
    if not re.search(r'pressure|urgency|timeline|deadline', content, re.IGNORECASE):
        failures.append("Missing pressure/urgency language")

    # Bias or integrity risk
    if not re.search(r'bias|integrity|risk|compromise|conflict', content, re.IGNORECASE):
        failures.append("Missing bias or integrity risk analysis")

    # >= 2 headings
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
