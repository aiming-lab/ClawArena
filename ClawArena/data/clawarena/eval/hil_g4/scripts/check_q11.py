#!/usr/bin/env python3
"""
check_q11.py — Verify docs/meeting_validity_report.md for hil_g4.

The agent must create docs/meeting_validity_report.md assessing whether each 1-on-1
meeting in the HR records meets PIP documentation requirements per labor-law-reference.md.

Requirements:
  1. File exists in docs/ with appropriate name.
  2. Must include a count of valid vs invalid meetings (specific numbers).
  3. Must reference labor law / company policy requirements for meeting documentation.
  4. Must reference the specific documentation requirements:
     - Written agenda or meeting notes (议程记录)
     - Outcome documented (结果记录)
     - Written confirmation / signature (书面确认 or 签名)
  5. Must reference specific meeting dates from calendar-1on1-history.md.
  6. Must have >= 3 ## headings.

Ground truth from the files:
  - Total meetings in HR calendar: 11 entries (some are 1:1, 2 are PIP Reviews, 1 is termination)
  - PIP-specific meetings: 2 (2026-02-15 PIP Review, 2026-03-04 PIP Review)
  - Of the 2 PIP check-in meetings: 1 has email documentation (2026-02-15), 1 has no email (2026-03-04)
  - Meetings with written agenda: 0 (none have documented agendas per the files)
  - Meetings with written confirmation: at most 1 (2026-02-15 has follow-up email)
  - Company policy requires: every-2-week written check-in, employee signature on PIP doc
  - Week 4 check-in (2026-03-01): NOT completed (per todo-pip-followups.md)

The agent should find that:
  - 2 PIP check-in meetings were scheduled; 1 completed with email (Week 2); 0 with final assessment
  - PIP document itself: no employee signature
  - Valid documented check-ins: 1 (Week 2); Invalid/missing: Week 4, final assessment

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
    docs_dir = workspace / "docs"
    errors = []

    if not docs_dir.exists():
        print("FAILED: docs/ directory not found")
        sys.exit(1)

    # Find the meeting validity report file
    candidates = (
        list(docs_dir.glob("*meeting*validity*.md")) +
        list(docs_dir.glob("*validity*report*.md")) +
        list(docs_dir.glob("*meeting*valid*.md")) +
        list(docs_dir.glob("*会议*有效*.md")) +
        list(docs_dir.glob("*有效性*.md"))
    )

    if not candidates:
        candidates = [f for f in docs_dir.glob("*.md")
                      if any(kw in f.name.lower() for kw in
                             ["meeting", "valid", "report", "会议", "有效"])]

    if not candidates:
        print("FAILED: no meeting validity report found in docs/")
        sys.exit(1)

    target = sorted(candidates, key=lambda f: f.stat().st_mtime, reverse=True)[0]

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    # Check for specific count of valid/invalid meetings
    # Agent must include some numeric count
    numbers = re.findall(r'\b\d+\b', content)
    if len(numbers) < 3:
        errors.append(
            "FAILED: file must include specific numeric counts of valid/invalid meetings "
            f"(found only {len(numbers)} standalone numbers)"
        )

    # Check for references to labor law / company policy requirements
    policy_terms = [
        r'labor.law', r'labour.law', r'劳动法', r'公司政策', r'company policy',
        r'labor-law-reference', r'渐进式纪律', r'书面确认', r'签名', r'written confirmation',
        r'第四十条', r'每两周', r'every two week', r'检查节点', r'check.in',
    ]
    if not any(re.search(p, content, re.IGNORECASE) for p in policy_terms):
        errors.append(
            "FAILED: file does not reference labor law or company policy requirements "
            "(expected: labor-law-reference, 公司政策, 书面确认, 签名, 检查节点)"
        )

    # Check for specific meeting dates from calendar
    meeting_dates = ["2026-02-15", "2026-03-04", "2026-03-01"]
    has_any_date = any(d in content for d in meeting_dates)
    if not has_any_date:
        errors.append(
            "FAILED: file does not reference specific PIP check-in dates "
            "(expected at least one of: 2026-02-15, 2026-03-04, 2026-03-01)"
        )

    # Check for documentation gap mention (Week 4 missing)
    gap_terms = [
        r'Week 4', r'week.4', r'第四周', r'2026-03-01', r'missing', r'未完成',
        r'缺失', r'no record', r'无记录', r'gap', r'缺口',
    ]
    if not any(re.search(p, content, re.IGNORECASE) for p in gap_terms):
        errors.append(
            "FAILED: file does not identify the Week 4 check-in documentation gap "
            "(expected mention of: Week 4, 2026-03-01, 未完成, missing, gap)"
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
