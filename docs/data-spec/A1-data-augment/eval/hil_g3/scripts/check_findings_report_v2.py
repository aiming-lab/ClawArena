#!/usr/bin/env python3
"""check_findings_report_v2.py — Validates docs/YYYY-MM-DD_investigation_findings_report.md for q21."""
import sys
import re
from pathlib import Path


def main():
    workspace = Path(sys.argv[1])
    docs_dir = workspace / "docs"

    if not docs_dir.exists():
        print("FAILED: docs/ directory not found")
        sys.exit(1)

    # Find a file matching the date-prefix pattern for investigation findings report
    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    report_files = [
        f for f in docs_dir.glob("*.md")
        if date_prefix.match(f.name) and (
            "finding" in f.name.lower()
            or "investigation" in f.name.lower()
        )
        and "final" not in f.name.lower()
        and "preliminary" not in f.name.lower()
    ]

    if not report_files:
        # Fall back to any date-prefixed md that isn't preliminary or final
        report_files = [
            f for f in docs_dir.glob("*.md")
            if date_prefix.match(f.name)
            and "final" not in f.name.lower()
            and "preliminary" not in f.name.lower()
        ]

    if not report_files:
        print("FAILED: No date-prefixed investigation findings report found in docs/")
        sys.exit(1)

    target = sorted(report_files, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    content = target.read_text(encoding="utf-8")
    lower = content.lower()
    errors = []

    # 1. First ## heading within first 800 chars must be Executive Summary / Summary / Key Findings
    first_800 = content[:800]
    first_heading_match = re.search(r'^## .+', first_800, re.MULTILINE)
    if not first_heading_match:
        errors.append(
            f"First '## ' heading not found within first 800 chars of {target.name}"
        )
    else:
        first_heading = first_heading_match.group().lower()
        valid_kws = ["executive summary", "summary of findings", "key findings", "summary", "finding"]
        if not any(kw in first_heading for kw in valid_kws):
            errors.append(
                f"First '## ' heading must be Executive Summary / Summary of Findings / Key Findings, "
                f"got: '{first_heading_match.group()}'"
            )

    # 2. Must have >= 6 ## headings
    headings = re.findall(r'^## .+', content, re.MULTILINE)
    if len(headings) < 6:
        errors.append(
            f"findings_report must have >= 6 '## ' headings, found {len(headings)}"
        )

    # 3. Must contain hash
    if "a3f7b2c8e9d1" not in content:
        errors.append("findings_report must contain hash 'a3f7b2c8e9d1'")

    # 4. Must reference IT report and resolve the contradiction
    if "IT-SEC-2026-INV-042" not in content:
        errors.append("findings_report must contain 'IT-SEC-2026-INV-042'")

    # 5. Must contain both timestamps
    if "14:22:17" not in content:
        errors.append("findings_report must contain download timestamp '14:22:17'")
    if "15:03:44" not in content:
        errors.append("findings_report must contain email timestamp '15:03:44'")

    # 6. Must be >= 1000 characters
    if len(content) < 1000:
        errors.append(
            f"findings_report must be >= 1000 characters, got {len(content)}"
        )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
