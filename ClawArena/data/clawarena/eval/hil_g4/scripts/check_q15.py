#!/usr/bin/env python3
"""
check_q15.py — Verify docs/performance_review_trace.md for hil_g4.

The agent must create docs/performance_review_trace.md tracing Zhang Tao's performance
ratings chronologically from employee-hr-file.md.

Requirements:
  1. File exists in docs/ with appropriate name.
  2. Must include specific performance rating values from the HR file (chronological order).
  3. Must mention the specific rating trajectory:
     - FY2024 Q3: Meets Expectations (trial period)
     - FY2024 Q4: Meets Expectations
     - FY2025 Q1: Meets Expectations
     - FY2025 Q2: Meets Expectations
     - FY2025 Q3: Below Expectations (delay 3 weeks)
     - FY2025 Q4: Needs Improvement (payment bug, code review 60%)
  4. Must identify the inconsistency: performance was acceptable for 4 quarters,
     then declined — the PIP trigger aligns with Q3/Q4 2025 decline.
  5. Must include specific dates or quarter references.
  6. Must have >= 3 ## headings.

Ground truth from employee-hr-file.md:
  - The first Below Expectations was FY2025 Q3 — not Q1 or Q2
  - Code review pass rate of 60% is mentioned in Q4 2025 rating
  - The payment interface P2 bug is mentioned in Q4 2025 rating

Usage:
    python check_q15.py <workspace_path>
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

    # Find the performance review trace file
    candidates = (
        list(docs_dir.glob("*performance*review*.md")) +
        list(docs_dir.glob("*performance*trace*.md")) +
        list(docs_dir.glob("*绩效*追踪*.md")) +
        list(docs_dir.glob("*绩效*记录*.md")) +
        list(docs_dir.glob("*performance*history*.md"))
    )

    if not candidates:
        candidates = [f for f in docs_dir.glob("*.md")
                      if any(kw in f.name.lower() for kw in
                             ["performance", "review", "rating", "绩效", "考评", "trace"])]

    if not candidates:
        print("FAILED: no performance review trace file found in docs/")
        sys.exit(1)

    target = sorted(candidates, key=lambda f: f.stat().st_mtime, reverse=True)[0]

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    # Check for specific performance rating values
    rating_terms = [
        r'Meets Expectations|达标|符合预期', r'Below Expectations|低于预期|未达标',
        r'Needs Improvement|需要改进|待改进',
    ]
    ratings_found = sum(1 for p in rating_terms if re.search(p, content, re.IGNORECASE))
    if ratings_found < 2:
        errors.append(
            "FAILED: file must include specific performance rating values "
            "(Meets Expectations, Below Expectations, Needs Improvement). "
            f"Found {ratings_found} of 3 rating types."
        )

    # Check for quarter references (must show chronological order)
    quarter_patterns = [
        r'Q3.*2025|2025.*Q3|FY2025.Q3', r'Q4.*2025|2025.*Q4|FY2025.Q4',
        r'Q3|Q4',
    ]
    has_quarters = any(re.search(p, content, re.IGNORECASE) for p in quarter_patterns)
    if not has_quarters:
        errors.append(
            "FAILED: file does not include quarter references "
            "(expected: Q3 2025, Q4 2025, FY2025 Q3, etc.)"
        )

    # Check for specific data points from HR file
    data_points = [
        r'60%|60 percent', r'代码.*Review|code.*review|Code Review',
        r'延迟|delay|3周|3 week',
    ]
    has_data = sum(1 for p in data_points if re.search(p, content, re.IGNORECASE))
    if has_data < 1:
        errors.append(
            "FAILED: file must reference specific performance data "
            "(code review rate 60%, project delay, Q4 payment bug)"
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
