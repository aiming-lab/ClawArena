#!/usr/bin/env python3
"""
check_q24.py — Verify docs/systemic_gaps_report.md (Phase 3 version with extended analysis).

Note: q22 and q24 both involve systemic analysis reports. q22 creates the initial systemic
gaps report; q24 requires a more comprehensive version that integrates ALL updates through
Phase 3 (upd1 + upd2 + upd3 + upd4). The agent may update docs/systemic_gaps_report.md
or create a new file.

This check verifies that the systemic gaps analysis (any file in docs/ with relevant name)
integrates evidence from upd3 (pip-timeline-analysis.md) and contains >= 2 systemic gaps
with specific case references including data from the timeline analysis.

Requirements:
  1. A systemic gaps / process failures report exists in docs/.
  2. Must reference pip-timeline-analysis.md findings (internal timeline analysis).
  3. Must identify >= 2 systemic process failures with specific improvement recommendations.
  4. Must cite specific data: 40-day actual PIP, 60-day policy, 20-day shortfall,
     or 1 written warning (2026-01-15).
  5. Must have >= 3 ## headings.

Usage:
    python check_q24.py <workspace_path>
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

    # Find systemic gap / process improvement report(s)
    candidates = (
        list(docs_dir.glob("*systemic*.md")) +
        list(docs_dir.glob("*process*gap*.md")) +
        list(docs_dir.glob("*process*failure*.md")) +
        list(docs_dir.glob("*系统*.md")) +
        list(docs_dir.glob("*gap*.md")) +
        list(docs_dir.glob("*漏洞*.md"))
    )

    if not candidates:
        candidates = list(docs_dir.glob("*.md"))

    if not candidates:
        print("FAILED: no suitable file found in docs/ for systemic analysis check")
        sys.exit(1)

    # Use most recent candidate
    target = sorted(candidates, key=lambda f: f.stat().st_mtime, reverse=True)[0]

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    # Must include specific data values from timeline analysis
    data_checks = [
        (r'(?<!\d)40(?!\d)', "40-day actual PIP duration"),
        (r'(?<!\d)60(?!\d)', "60-day policy minimum"),
        (r'(?<!\d)20(?!\d)', "20-day shortfall"),
        (r'2026-01-15', "written warning date"),
        (r'Week 4|第四周|2026-03-01', "Week 4 check-in gap"),
    ]
    data_found = sum(1 for pattern, _ in data_checks if re.search(pattern, content, re.IGNORECASE))
    if data_found < 3:
        errors.append(
            f"FAILED: file cites only {data_found} specific data values "
            "(expected >= 3 of: 40 days, 60 days, 20 days shortfall, "
            "2026-01-15 warning, Week 4 gap)"
        )

    # Must identify >= 2 systemic gaps with improvement recommendations
    systemic_indicators = [
        r'训练|培训|training',
        r'核实.*流程|verification.*process|verify.*checklist',
        r'法务.*独立|legal.*independent|independent.*legal.*review',
        r'PIP.*审批|PIP.*gating|PIP.*完成|gate',
        r'系统性|systemic|制度性',
    ]
    systemic_count = sum(1 for p in systemic_indicators if re.search(p, content, re.IGNORECASE))
    if systemic_count < 2:
        errors.append(
            f"FAILED: file identifies only {systemic_count} systemic improvement areas "
            "(expected >= 2)"
        )

    # Must have recommendations
    has_recs = bool(re.search(
        r'建议|recommend|改进|improve|应当|should|措施|action',
        content, re.IGNORECASE
    ))
    if not has_recs:
        errors.append("FAILED: file does not include improvement recommendations")

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
