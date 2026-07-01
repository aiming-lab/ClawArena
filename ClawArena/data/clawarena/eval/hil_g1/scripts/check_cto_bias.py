#!/usr/bin/env python3
"""
check_cto_bias.py — Validates analysis/cto_bias_risk_analysis.md.

Checks:
- CTO's minimization narrative discussed ("everyone inflates" or "minimize")
- "bias" or "pressure" present
- HR process integrity mentioned
- >= 2 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_cto_bias.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "cto_bias_risk_analysis.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # CTO minimization narrative
    if not re.search(r'CTO|minimiz|everyone inflat|dismisses|downplays', content, re.IGNORECASE):
        failures.append("Missing CTO minimization narrative")

    # Bias / pressure
    if not re.search(r'bias|pressure|influence|conflict', content, re.IGNORECASE):
        failures.append("Missing 'bias' or 'pressure' analysis")

    # HR process integrity
    if not re.search(r'integrity|process|HR|procedure|protocol', content, re.IGNORECASE):
        failures.append("Missing HR process integrity mention")

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
