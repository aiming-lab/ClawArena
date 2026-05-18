#!/usr/bin/env python3
"""
check_q5.py — Verify docs/YYYY-MM-DD_initial_pip_analysis.md for hil_g4.

The agent must create a date-prefixed markdown file in docs/ with an initial PIP
compliance analysis. Requirements:
  1. File in docs/ must have YYYY-MM-DD_ prefix in filename.
  2. File must mention the exact PIP start date: 2026-02-01.
  3. File must mention the company policy minimum PIP duration: 60 days.
  4. File must reference the labor law article (第四十条 / Article 40) or company policy.
  5. File must include a compliance status determination.
  6. File must have >= 3 ## headings.

Ground truth:
  - PIP start date: 2026-02-01 (from pip-email-chain.md)
  - Company policy minimum: 60 days (from labor-law-reference.md)
  - PIP plan duration as written: 30 days (already non-compliant with policy)
  - Termination at Day 40, shortfall vs 60-day minimum: 20 days

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

    # Find the most relevant file (one containing 'pip' or 'analysis' or 'initial')
    candidate = None
    for f in prefixed_files:
        name_lower = f.name.lower()
        if any(kw in name_lower for kw in ["pip", "analysis", "initial", "compliance", "合规", "分析"]):
            candidate = f
            break
    if candidate is None:
        candidate = sorted(prefixed_files, key=lambda f: f.stat().st_mtime, reverse=True)[0]

    try:
        content = candidate.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {candidate}: {e}")
        sys.exit(1)

    # Check for PIP start date
    if "2026-02-01" not in content:
        errors.append("FAILED: file does not contain PIP start date '2026-02-01'")

    # Check for 60-day policy minimum
    if not re.search(r'(?<!\d)60(?!\d)', content):
        errors.append("FAILED: file does not mention the 60-day policy minimum")

    # Check for labor law or policy reference
    law_refs = [
        r'第四十条', r'Article\s+40', r'labor.law', r'labour.law',
        r'劳动合同法', r'labor-law-reference', r'渐进式纪律', r'progressive.discipline',
        r'公司政策', r'company policy',
    ]
    if not any(re.search(p, content, re.IGNORECASE) for p in law_refs):
        errors.append(
            "FAILED: file does not reference labor law or company policy "
            "(expected: 第四十条, Article 40, 劳动合同法, labor-law-reference, etc.)"
        )

    # Check for compliance status determination
    compliance_terms = [
        r'不合规', r'合规', r'违规', r'compliant', r'non-compliant', r'violation',
        r'违反', r'未达标', r'不符合', r'不满足',
    ]
    if not any(re.search(p, content, re.IGNORECASE) for p in compliance_terms):
        errors.append(
            "FAILED: file does not include a compliance status determination "
            "(expected terms: 合规, 不合规, compliant, violation, 违反)"
        )

    # Check for >= 3 ## headings
    headings = [ln for ln in content.splitlines() if re.match(r'^##+ ', ln.strip())]
    if len(headings) < 3:
        errors.append(
            f"FAILED: file has only {len(headings)} ## headings (expected >= 3)"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
