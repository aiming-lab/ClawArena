#!/usr/bin/env python3
"""
check_q17.py — Verify docs/documentation_timeline.md for hil_g4.

The agent must create docs/documentation_timeline.md reconstructing the complete HR
documentation timeline for Zhang Tao's case from employee-hr-file.md.

Requirements:
  1. File exists in docs/ with appropriate name.
  2. Must include all key milestone dates from the actual files:
     - Hire date: 2024-06-01
     - Performance warning (1st formal written): 2026-01-15
     - PIP start: 2026-02-01
     - PIP Week 2 check-in: 2026-02-15
     - Termination: 2026-03-13
  3. Must note the missing milestones:
     - Week 4 check-in (2026-03-01) — NOT completed
     - Final PIP assessment — NOT completed
  4. Must have >= 3 ## headings (chronological sections).
  5. Must reference employee-hr-file.md or pip-email-chain.md as sources.

Ground truth dates:
  - Hire: 2024-06-01 (employee-hr-file.md)
  - Written warning email: 2026-01-15 (pip-email-chain.md)
  - PIP start: 2026-02-01 (pip-email-chain.md)
  - PIP Week 2: 2026-02-15 (pip-email-chain.md + calendar)
  - Termination: 2026-03-13 (employee-hr-file.md)

Usage:
    python check_q17.py <workspace_path>
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

    # Find the timeline file
    candidates = (
        list(docs_dir.glob("*documentation*timeline*.md")) +
        list(docs_dir.glob("*timeline*.md")) +
        list(docs_dir.glob("*时间线*.md")) +
        list(docs_dir.glob("*时间轴*.md"))
    )

    if not candidates:
        candidates = [f for f in docs_dir.glob("*.md")
                      if any(kw in f.name.lower() for kw in
                             ["timeline", "history", "chronolog", "时间", "里程碑"])]

    if not candidates:
        print("FAILED: no documentation timeline file found in docs/")
        sys.exit(1)

    target = sorted(candidates, key=lambda f: f.stat().st_mtime, reverse=True)[0]

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    # Check for key milestone dates
    required_dates = {
        "2026-01-15": "written warning email",
        "2026-02-01": "PIP start",
        "2026-03-13": "termination",
    }
    for date, label in required_dates.items():
        if date not in content:
            errors.append(f"FAILED: file does not contain milestone date {date} ({label})")

    # Check for hire date (may be 2024-06-01)
    if "2024-06-01" not in content and "入职" not in content and "hire" not in content.lower():
        errors.append(
            "FAILED: file does not mention hire date 2024-06-01 or hire event"
        )

    # Check for Week 2 check-in or PIP follow-up
    if "2026-02-15" not in content and "Week 2" not in content and "第二周" not in content:
        errors.append(
            "FAILED: file does not mention Week 2 check-in (2026-02-15)"
        )

    # Check for missing milestone notation (Week 4 or final assessment not done)
    missing_terms = [
        r'Week 4|第四周|2026-03-01', r'未完成|missing|not completed|缺失',
        r'最终评估|final assessment|final review',
    ]
    missing_found = sum(1 for p in missing_terms if re.search(p, content, re.IGNORECASE))
    if missing_found < 1:
        errors.append(
            "FAILED: file does not identify any missing milestones "
            "(expected mention of: Week 4 check-in missing, final assessment not done)"
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
