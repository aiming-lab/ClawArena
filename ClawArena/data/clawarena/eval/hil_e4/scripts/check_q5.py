#!/usr/bin/env python3
"""
check_q5.py -- Verify docs/YYYY-MM-DD_initial_compliance_analysis.md.

Usage:
    python check_q5.py <workspace_path>
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

    docs_dir = workspace / "docs"
    if not docs_dir.exists():
        errors.append("FAILED: docs/ directory not found")
    else:
        date_prefix = re.compile(r"^\d{4}-\d{2}-\d{2}_")
        md_files = list(docs_dir.glob("*.md"))
        prefixed = [f for f in md_files if date_prefix.match(f.name)]

        if not prefixed:
            errors.append(
                "FAILED: no YYYY-MM-DD_ prefixed .md file found in docs/"
            )
        else:
            # Use the most recently modified date-prefixed file
            target = sorted(prefixed, key=lambda p: p.stat().st_mtime, reverse=True)[0]
            try:
                content = target.read_text(encoding="utf-8")
            except Exception as e:
                errors.append(f"FAILED: cannot read {target}: {e}")
                content = ""

            if content:
                # Must cite at least 2 specific budget categories by name
                categories = [
                    "Personnel",
                    "Community Educator Training",
                    "Community Mobilization",
                    "School Infrastructure",
                    "Admin and Overhead",
                ]
                found_cats = [c for c in categories if c.lower() in content.lower()]
                if len(found_cats) < 2:
                    errors.append(
                        f"FAILED: found only {len(found_cats)} budget category names "
                        f"(need >= 2): {found_cats}"
                    )

                # Must contain specific USD amounts from financial_tracking_Q2.md
                # Any of the actual expenditure amounts: 409000, 115000, 131000, 178000, 87000
                amount_patterns = [
                    r"\$?409[,.]?000",
                    r"\$?115[,.]?000",
                    r"\$?131[,.]?000",
                    r"\$?178[,.]?000",
                    r"\$?87[,.]?000",
                ]
                found_amounts = [
                    p for p in amount_patterns if re.search(p, content)
                ]
                if not found_amounts:
                    errors.append(
                        "FAILED: no specific USD expenditure amounts from "
                        "financial_tracking_Q2.md found in the analysis file"
                    )

                # Must state over/under/on-budget status
                if not re.search(
                    r"over.{0,30}budget|under.{0,30}budget|within.{0,30}tolerance|overspend|underspend",
                    content,
                    re.IGNORECASE,
                ):
                    errors.append(
                        "FAILED: file does not state budget status "
                        "(over/under/within tolerance) for any category"
                    )

                # Must reference Annex C or PEM activity codes
                if not re.search(
                    r"Annex C|PEM-EDU|PEM-EDT|PEM-INF|PEM-GOV|deliverable",
                    content,
                    re.IGNORECASE,
                ):
                    errors.append(
                        "FAILED: file does not reference Annex C deliverable "
                        "category or PEM activity code"
                    )

                # Must have >= 3 ## headings
                headings = [
                    ln for ln in content.splitlines() if ln.strip().startswith("##")
                ]
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
