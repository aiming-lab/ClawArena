#!/usr/bin/env python3
"""
check_q18.py -- Verify docs/YYYY-MM-DD_midterm_compliance_report.md.

Usage:
    python check_q18.py <workspace_path>
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
                # Must include budget utilization percentage values
                # Any of the five utilization percentages: 99.3, 77.7, 139.4, 94.2, 96.7
                util_patterns = [r"\b99\.3\b", r"\b77\.7\b", r"\b139\.4\b", r"\b94\.2\b", r"\b96\.7\b"]
                # Also accept approximate forms: 99%, 78%, 139%, 94%, 97%
                approx_patterns = [r"\b99\b.{0,5}%", r"\b78\b.{0,5}%", r"\b139\b.{0,5}%",
                                   r"\b94\b.{0,5}%", r"\b97\b.{0,5}%"]
                util_found = sum(1 for p in util_patterns if re.search(p, content))
                approx_found = sum(1 for p in approx_patterns if re.search(p, content))
                if util_found + approx_found < 2:
                    errors.append(
                        "FAILED: budget utilization percentages for categories not present "
                        "(expected at least 2 of: 99.3%, 77.7%, 139.4%, 94.2%, 96.7%)"
                    )

                # Must cite Petrova's 58% and 63%
                if not re.search(r"\b58\b", content):
                    errors.append(
                        "FAILED: Petrova's conservative estimate '58' not cited"
                    )
                if not re.search(r"\b63\b", content):
                    errors.append(
                        "FAILED: Petrova's inclusive estimate '63' not cited"
                    )

                # Must state non-compliant status
                if not re.search(r"non.compliant|noncompliant", content, re.IGNORECASE):
                    errors.append(
                        "FAILED: 'non-compliant' compliance status not stated"
                    )

                # Must include 14-day waiver deadline
                if not re.search(r"\b14\b.{0,20}(day|calendar)", content, re.IGNORECASE):
                    errors.append(
                        "FAILED: 14-day waiver deadline not cited"
                    )

                # Must have >= 4 ## headings
                headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
                if len(headings) < 4:
                    errors.append(
                        f"FAILED: file has only {len(headings)} ## headings (need >= 4)"
                    )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
