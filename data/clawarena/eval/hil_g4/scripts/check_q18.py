#!/usr/bin/env python3
"""
check_q18.py — Verify docs/YYYY-MM-DD_midterm_investigation_report.md for hil_g4.

The agent must create a comprehensive mid-investigation report (date-prefixed in docs/).

Requirements:
  1. File in docs/ must have YYYY-MM-DD_ prefix in filename.
  2. Must include PIP compliance status with exact days_shortfall (20 days).
  3. Must include 1-on-1 discrepancy summary (verbal discussions vs written warnings).
  4. Must include key risk areas.
  5. Must have >= 4 ## headings.
  6. Must reference the exact warning count: 1 documented written warning (2026-01-15).
  7. Must reference PIP duration issue: 40 days actual vs 60-day policy.

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
    docs_dir = workspace / "docs"
    errors = []

    if not docs_dir.exists():
        print("FAILED: docs/ directory not found")
        sys.exit(1)

    # Find a date-prefixed markdown file in docs/
    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_.*\.md$')
    prefixed_files = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]

    if not prefixed_files:
        print("FAILED: no YYYY-MM-DD_*.md file found in docs/ (P2 requirement)")
        sys.exit(1)

    # Find the midterm report (most recent date-prefixed file, or one with relevant name)
    candidate = None
    for f in prefixed_files:
        name_lower = f.name.lower()
        if any(kw in name_lower for kw in ["midterm", "mid", "interim", "中期", "调查"]):
            candidate = f
            break
    if candidate is None:
        candidate = sorted(prefixed_files, key=lambda f: f.stat().st_mtime, reverse=True)[0]

    try:
        content = candidate.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {candidate}: {e}")
        sys.exit(1)

    # Check for exact days_shortfall (20 days)
    if not re.search(r'(?<!\d)20(?!\d)', content):
        errors.append(
            "FAILED: file does not mention the days_shortfall of 20 days "
            "(60-day policy minimum minus 40 actual days = 20)"
        )

    # Check for 60-day policy reference
    if not re.search(r'(?<!\d)60(?!\d)', content):
        errors.append(
            "FAILED: file does not mention the 60-day policy minimum"
        )

    # Check for 1 written warning reference
    warning_check = re.search(r'(?<!\d)1(?!\d).{0,30}(written warning|书面警告)|（书面警告.{0,30}(?<!\d)1(?!\d)', content, re.IGNORECASE)
    email_date = "2026-01-15" in content
    if not (warning_check or email_date):
        errors.append(
            "FAILED: file does not reference the single documented written warning "
            "(expected: '1 written warning' or '2026-01-15' email date)"
        )

    # Check for 1-on-1 discrepancy or verbal vs written issue
    discrepancy_terms = [
        r'口头.*书面|verbal.*written|1.on.1.*差异|discrepancy',
        r'孙伟.*笔记|Sun Wei.*note', r'1:1.*差异|1:1.*conflict',
    ]
    if not any(re.search(p, content, re.IGNORECASE) for p in discrepancy_terms):
        errors.append(
            "FAILED: file does not include 1-on-1 discrepancy summary "
            "(verbal discussions vs written warnings issue)"
        )

    # Check for risk areas
    risk_terms = [r'风险|risk|legal exposure|法律风险|仲裁']
    if not any(re.search(p, content, re.IGNORECASE) for p in risk_terms):
        errors.append(
            "FAILED: file does not identify key risk areas (expected: 风险, risk, 仲裁)"
        )

    # Check for >= 4 ## headings
    headings = [ln for ln in content.splitlines() if re.match(r'^##+ ', ln.strip())]
    if len(headings) < 4:
        errors.append(
            f"FAILED: file has only {len(headings)} ## headings (expected >= 4)"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
