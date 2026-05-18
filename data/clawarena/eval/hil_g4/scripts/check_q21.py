#!/usr/bin/env python3
"""
check_q21.py — Verify docs/legal_evolution_analysis.md for hil_g4.

After upd4 (legal-updated-assessment.md) is injected, the agent must create
docs/legal_evolution_analysis.md comparing original legal risk assessment vs
the updated assessment from legal-updated-assessment.md.

Requirements:
  1. File exists in docs/ with appropriate name.
  2. Must reference legal-updated-assessment.md as a source.
  3. Must identify what changed between Ma Li's initial assessment and updated assessment:
     - Initial: "sufficient documentation" / "sufficient legal basis"
     - Updated: "some gaps" / "totality of circumstances"
     - Shift from "maintain termination" to "consider negotiation"
  4. Must state the final legal exposure level (high risk given multiple gaps).
  5. Must reference specific gaps mentioned in the legal update:
     - Warning count (1 documented vs 3 claimed)
     - PIP signature missing
     - Week 4 check-in undocumented
  6. Must have >= 3 ## headings.

Ground truth from legal-updated-assessment.md:
  - Ma Li acknowledges 3 specific gaps: warning count, PIP signature, Week 4 check-in
  - Uses hedging language: "totality of circumstances", "not necessarily fatal"
  - Recommends considering negotiation
  - Does NOT explicitly retract initial "sufficient" assessment

Usage:
    python check_q21.py <workspace_path>
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

    # Find the legal evolution analysis file
    candidates = (
        list(docs_dir.glob("*legal*evolution*.md")) +
        list(docs_dir.glob("*legal*analysis*.md")) +
        list(docs_dir.glob("*法务*演变*.md")) +
        list(docs_dir.glob("*法律*分析*.md")) +
        list(docs_dir.glob("*assessment*evolution*.md"))
    )

    if not candidates:
        candidates = [f for f in docs_dir.glob("*.md")
                      if any(kw in f.name.lower() for kw in
                             ["legal", "law", "assessment", "evolution", "法务", "法律", "评估"])]

    if not candidates:
        print("FAILED: no legal evolution analysis file found in docs/")
        sys.exit(1)

    target = sorted(candidates, key=lambda f: f.stat().st_mtime, reverse=True)[0]

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    # Check for reference to legal-updated-assessment.md
    if not re.search(r'legal.updated.assessment|法务.*更新|updated.assessment|马丽|Ma Li',
                     content, re.IGNORECASE):
        errors.append(
            "FAILED: file does not reference legal-updated-assessment.md or Ma Li "
            "(expected: legal-updated-assessment, 法务更新, 马丽, Ma Li)"
        )

    # Check for identification of what changed
    change_terms = [
        r'sufficient|充分|足够', r'gaps?|缺口|缺失',
        r'totality|整体|综合考虑', r'negotiate|协商|和解',
        r'changed|changed|变化|修订|revised',
    ]
    change_found = sum(1 for p in change_terms if re.search(p, content, re.IGNORECASE))
    if change_found < 2:
        errors.append(
            "FAILED: file does not adequately describe what changed in the legal assessment "
            f"(found {change_found} of expected terms: sufficient, gaps, totality, negotiate)"
        )

    # Check for specific gaps mentioned
    gap_terms = [
        r'warning|警告|书面警告', r'signature|签名|未签名',
        r'Week 4|第四周|check.in',
    ]
    gaps_found = sum(1 for p in gap_terms if re.search(p, content, re.IGNORECASE))
    if gaps_found < 2:
        errors.append(
            "FAILED: file does not mention specific documentation gaps "
            f"(found {gaps_found} of 3 expected: warning count, PIP signature, Week 4 check-in)"
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
