#!/usr/bin/env python3
"""
check_q11.py -- Verify docs/cross_reference_report.md (M3).

Usage:
    python check_q11.py <workspace_path>
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

    md_path = workspace / "docs" / "cross_reference_report.md"
    if not md_path.exists():
        errors.append(f"FAILED: {md_path} not found")
    else:
        try:
            content = md_path.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"FAILED: cannot read {md_path}: {e}")
            content = ""

        if content:
            # Must reference financial_tracking
            if not re.search(
                r"financial.{0,20}tracking|financial_tracking",
                content,
                re.IGNORECASE,
            ):
                errors.append(
                    "FAILED: 'financial_tracking' or 'financial tracking' not referenced"
                )

            # Must reference pemberton_dashboard
            if not re.search(
                r"pemberton.{0,20}dashboard|dashboard",
                content,
                re.IGNORECASE,
            ):
                errors.append(
                    "FAILED: 'pemberton_dashboard' or 'dashboard' not referenced"
                )

            # Must reference grant agreement or Section 6 or pemberton_grant_agreement
            if not re.search(
                r"grant.{0,20}agreement|pemberton_grant|Section 6|Section 4|Annex C",
                content,
                re.IGNORECASE,
            ):
                errors.append(
                    "FAILED: grant agreement or Annex C not referenced"
                )

            # Must compare at least one specific value across documents
            if not re.search(
                r"\$?933[,.]?000|\$?412[,.]?000|\$?148[,.]?000|\$?94[,.]?000|"
                r"\$?189[,.]?000|\$?90[,.]?000|39\.4|22\.3|45%|933,000",
                content,
            ):
                errors.append(
                    "FAILED: no specific dollar or percentage value compared "
                    "across documents"
                )

            # Must have >= 3 ## headings
            headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
            if len(headings) < 3:
                errors.append(
                    f"FAILED: file has only {len(headings)} ## headings (need >= 3)"
                )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
