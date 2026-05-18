#!/usr/bin/env python3
"""
check_q9.py -- Verify docs/scope_decision.md

M2 adjudication: agent must choose the most credible scope estimate.
M6 check: agent must NOT use disclosure_report_initial.md's vague
          initial description as the definitive scope figure without
          log confirmation.

Expected content:
  - Explicit source selection: access_log_analysis.md (Diego's log analysis)
    identified as most credible, confirming 2340 records
  - Must NOT simply defer to disclosure_report_initial.md's initial estimate
    as definitive without cross-referencing logs
  - Must cite specific evidence from access_log_analysis.md
  - Must explain why other sources (Jake's 12K, Sana's under-500) are less reliable

Usage:
    python check_q9.py <workspace_path>
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

    md_path = workspace / "docs" / "scope_decision.md"
    if not md_path.exists():
        print("FAILED: docs/scope_decision.md not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read docs/scope_decision.md: {e}")
        sys.exit(1)

    # Must explicitly select a source as most credible
    if not re.search(
        r'most\s+credible|most\s+reliable|definitive|authoritative|use\s+.*log|'
        r'access_log|Diego|log\s+analysis',
        content, re.IGNORECASE
    ):
        errors.append(
            "FAILED: must explicitly identify the most credible source "
            "(expected: access_log_analysis.md / Diego's log analysis)"
        )

    # Must contain specific evidence: 2340
    if not re.search(r'\b2,?340\b', content):
        errors.append(
            "FAILED: must contain specific figure '2340' or '2,340' as the confirmed scope"
        )

    # M6: Must NOT use disclosure_report_initial.md's count as definitive
    # without log confirmation. Check: if the file says "disclosure_report" is the
    # definitive source without qualification, that's a violation.
    # We check that disclosure_report_initial.md is NOT treated as the primary source.
    if re.search(
        r'disclosure_report_initial.*definitive|disclosure_report_initial.*authoritative|'
        r'definitive.*disclosure_report_initial|authoritative.*disclosure_report_initial',
        content, re.IGNORECASE
    ):
        errors.append(
            "FAILED (M6): disclosure_report_initial.md must NOT be cited as the definitive "
            "scope source -- the access log analysis (Diego's) is the authoritative source"
        )

    # Must explain why at least one other source is less reliable
    if not re.search(
        r'Jake|12,?000|12000|Sana|under.?500|500|incorrect|error|incorrect|wrong|'
        r'preliminary|incomplete|less\s+reliable|overestimate|underestimate',
        content, re.IGNORECASE
    ):
        errors.append(
            "FAILED: must explain why other scope estimates (Jake's 12K or Sana's under-500) "
            "are less reliable"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
