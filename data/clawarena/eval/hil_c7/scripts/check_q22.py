#!/usr/bin/env python3
"""
check_q22.py -- Verify docs/root_cause_analysis.md

Expected content:
  - CVSS score 7.5 present
  - Specific endpoint name: /api/v2/pipeline-configs (or GET pipeline-configs)
  - Specific deployment event: PR #847, October 14 deploy
  - Root cause: missing @require_auth on GET method + ?list=true enumeration
  - Must have >= 3 ## headings

Usage:
    python check_q22.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    md_path = workspace / "docs" / "root_cause_analysis.md"
    if not md_path.exists():
        print("FAILED: docs/root_cause_analysis.md not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read docs/root_cause_analysis.md: {e}")
        sys.exit(1)

    # Must contain CVSS score 7.5
    if not re.search(r'\b7\.5\b', content):
        errors.append("FAILED: must contain CVSS score '7.5'")

    # Must reference specific endpoint
    if not re.search(
        r'pipeline.config|/api/v2|GET.*pipeline|pipeline.*GET',
        content, re.IGNORECASE
    ):
        errors.append(
            "FAILED: must reference the specific affected endpoint "
            "(/api/v2/pipeline-configs or GET pipeline-configs)"
        )

    # Must reference specific deployment event (PR #847 or October 14)
    if not re.search(r'PR\s*#?\s*847|#847|Oct\w*\s+14|October\s+14|2024-10-14', content, re.IGNORECASE):
        errors.append(
            "FAILED: must reference specific deployment event "
            "(PR #847 or October 14 deployment)"
        )

    # Must reference the authentication failure as root cause
    if not re.search(
        r'require_auth|authentication|auth|unauthenticat',
        content, re.IGNORECASE
    ):
        errors.append(
            "FAILED: must identify missing authentication (@require_auth) as root cause"
        )

    # Must have >= 3 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 3:
        errors.append(
            f"FAILED: must have >= 3 ## headings, found {len(headings)}"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
