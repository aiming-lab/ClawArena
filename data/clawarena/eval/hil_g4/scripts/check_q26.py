#!/usr/bin/env python3
"""
check_q26.py — Verify docs/YYYY-MM-DD_final_investigation_report.md for hil_g4.

The agent must create a comprehensive final investigation report (date-prefixed in docs/)
satisfying all P1-P5 preferences.

Requirements:
  1. File in docs/ with YYYY-MM-DD_ prefix.
  2. Must include exact PIP start date: 2026-02-01.
  3. Must include exact days_shortfall: 20 (as a standalone number).
  4. Must include termination date: 2026-03-13.
  5. Must reference applicable law/policy clause (第四十条 or Article 40).
  6. Must summarize 1-on-1 discrepancies (verbal discussions vs written warnings).
  7. Must state legal risk conclusion (risk_level or risk description).
  8. Must have >= 5 ## headings.
  9. Must reference the written warning email date: 2026-01-15.
  10. Must include a recommendation or conclusion section.

Ground truth summary for final report:
  - PIP start: 2026-02-01
  - Termination: 2026-03-13 (Day 40)
  - Policy minimum: 60 days
  - Shortfall: 20 days
  - Written warnings documented: 1 (2026-01-15)
  - Written warnings required: 2 (per progressive discipline policy)
  - Risk level: high
  - Recommendation: consider negotiated settlement

Usage:
    python check_q26.py <workspace_path>
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

    # Find the final report (most recent date-prefixed file)
    candidate = None
    for f in prefixed_files:
        name_lower = f.name.lower()
        if any(kw in name_lower for kw in
               ["final", "investigation", "report", "最终", "调查", "报告"]):
            candidate = f
            break
    if candidate is None:
        candidate = sorted(prefixed_files, key=lambda f: f.stat().st_mtime, reverse=True)[0]

    try:
        content = candidate.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {candidate}: {e}")
        sys.exit(1)

    # Check for exact PIP start date
    if "2026-02-01" not in content:
        errors.append("FAILED: file does not contain PIP start date '2026-02-01'")

    # Check for termination date
    if "2026-03-13" not in content:
        errors.append("FAILED: file does not contain termination date '2026-03-13'")

    # Check for written warning email date
    if "2026-01-15" not in content:
        errors.append(
            "FAILED: file does not contain written warning email date '2026-01-15'"
        )

    # Check for days_shortfall = 20 (exact standalone number)
    if not re.search(r'(?<!\d)20(?!\d)', content):
        errors.append(
            "FAILED: file does not contain the days_shortfall of 20 "
            "(60-day minimum minus 40 actual days = 20)"
        )

    # Check for 60-day policy minimum
    if not re.search(r'(?<!\d)60(?!\d)', content):
        errors.append("FAILED: file does not mention the 60-day policy minimum")

    # Check for law/policy clause reference
    law_terms = [
        r'第四十条', r'Article\s+40', r'劳动合同法', r'labor.law',
        r'company.policy', r'公司政策', r'渐进式纪律',
    ]
    if not any(re.search(p, content, re.IGNORECASE) for p in law_terms):
        errors.append(
            "FAILED: file does not reference applicable law/policy clause "
            "(expected: 第四十条, Article 40, 劳动合同法, company policy)"
        )

    # Check for 1-on-1 discrepancy summary
    discrepancy_terms = [
        r'口头.*书面|verbal.*written', r'1.on.1|1:1|一对一',
        r'sunwei.1on1|孙伟.*笔记|Sun Wei.*note',
        r'discrepancy|差异|不一致',
    ]
    if not any(re.search(p, content, re.IGNORECASE) for p in discrepancy_terms):
        errors.append(
            "FAILED: file does not summarize 1-on-1 discrepancies "
            "(verbal discussions vs written warnings)"
        )

    # Check for legal risk conclusion
    risk_terms = [r'风险|risk|high|高|仲裁|arbitration|negotiate|协商']
    if not any(re.search(p, content, re.IGNORECASE) for p in risk_terms):
        errors.append(
            "FAILED: file does not include legal risk conclusion "
            "(expected: 风险, risk, 仲裁, negotiate)"
        )

    # Check for recommendation or conclusion
    rec_terms = [r'建议|recommend|结论|conclusion|settlement|和解|处理意见']
    if not any(re.search(p, content, re.IGNORECASE) for p in rec_terms):
        errors.append(
            "FAILED: file does not include a recommendation or conclusion section"
        )

    # Check for >= 5 ## headings
    headings = [ln for ln in content.splitlines() if re.match(r'^##+ ', ln.strip())]
    if len(headings) < 5:
        errors.append(
            f"FAILED: file has only {len(headings)} ## headings (expected >= 5 for final report)"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
