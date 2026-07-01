#!/usr/bin/env python3
"""
check_q20.py — Verify docs/timeline_analysis_integration.md for hil_g4.

After upd3 (pip-timeline-analysis.md) is injected, the agent must create
docs/timeline_analysis_integration.md integrating findings from the internal
PIP timeline analysis.

Requirements:
  1. File exists in docs/ with appropriate name.
  2. Must reference pip-timeline-analysis.md as the source.
  3. Must identify at least 2 specific findings from pip-timeline-analysis.md:
     - PIP period: 40 days actual vs 60-day policy (20-day shortfall)
     - Week 4 check-in: not completed (no record)
     - March 4 meeting: was termination conversation, not PIP review
     - Warning count: only 1 formal written warning (not 3)
  4. Must note what the internal timeline reveals that wasn't in original records.
  5. Must have >= 3 ## headings.

Ground truth from pip-timeline-analysis.md:
  - PIP启动日: 2026-02-01 (Day 0)
  - 解雇日: 2026-03-13 (Day 40)
  - 政策要求: 60天
  - 差距: 20天
  - Week 4 check-in (2026-03-01): 未完成
  - 2026-03-04: 终止谈话，非PIP review
  - 书面警告: 仅1封 (2026-01-15)

Usage:
    python check_q20.py <workspace_path>
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

    # Find the timeline integration file
    candidates = (
        list(docs_dir.glob("*timeline*integration*.md")) +
        list(docs_dir.glob("*timeline*analysis*.md")) +
        list(docs_dir.glob("*时间线*整合*.md")) +
        list(docs_dir.glob("*整合*.md"))
    )

    if not candidates:
        candidates = [f for f in docs_dir.glob("*.md")
                      if any(kw in f.name.lower() for kw in
                             ["timeline", "integration", "integrat", "时间", "整合", "分析"])]

    if not candidates:
        print("FAILED: no timeline analysis integration file found in docs/")
        sys.exit(1)

    target = sorted(candidates, key=lambda f: f.stat().st_mtime, reverse=True)[0]

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    # Check for reference to pip-timeline-analysis.md
    if not re.search(r'pip.timeline.analysis|时间线分析|timeline.analysis', content, re.IGNORECASE):
        errors.append(
            "FAILED: file does not reference pip-timeline-analysis.md "
            "(expected: pip-timeline-analysis, 时间线分析)"
        )

    # Check for specific findings from the timeline analysis (at least 2)
    findings = [
        (r'(?<!\d)40(?!\d)', "40 days actual PIP duration"),
        (r'(?<!\d)60(?!\d)', "60-day policy minimum"),
        (r'(?<!\d)20(?!\d)', "20-day shortfall"),
        (r'Week 4|第四周|2026-03-01', "Week 4 check-in not completed"),
        (r'2026-03-04', "March 4 meeting characterization"),
        (r'终止.*谈话|termination.*talk|termination.*notification|终止通知',
         "March 4 as termination conversation"),
    ]
    findings_found = sum(1 for pattern, _ in findings if re.search(pattern, content, re.IGNORECASE))
    if findings_found < 3:
        errors.append(
            f"FAILED: file references only {findings_found} findings from pip-timeline-analysis.md "
            "(expected >= 3 of: 40-day duration, 60-day minimum, 20-day shortfall, "
            "Week 4 missing, March 4 termination conversation)"
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
