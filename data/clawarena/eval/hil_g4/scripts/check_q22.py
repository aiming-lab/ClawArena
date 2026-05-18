#!/usr/bin/env python3
"""
check_q22.py — Verify docs/systemic_gaps_report.md for hil_g4.

The agent must create docs/systemic_gaps_report.md identifying at least 2 systemic
process failures (not just individual mistakes) revealed by this case.

Requirements:
  1. File exists in docs/ with appropriate name.
  2. Must identify >= 2 SYSTEMIC process failures (not individual mistakes).
     Examples:
       - Systemic: Company lacks clear written definition / training on "written warning" vs verbal
       - Systemic: HRBP verification checklist doesn't require independent email system verification
       - Systemic: Legal review process accepts HRBP summaries without independent document check
       - Systemic: No gating mechanism ensures PIP is completed before termination approval
  3. Each gap must include: (a) what the gap is, (b) how it manifested in this case,
     (c) an improvement recommendation.
  4. Must reference specific events from the case (specific dates or names).
  5. Must have >= 3 ## headings.

Ground truth systemic failures:
  1. Manager training gap: No training on formal definition of "written warning"
     → Sun Wei counted verbal 1:1 discussions as written warnings
  2. HRBP verification gap: No requirement to independently verify documentation claims
     → Chen Hao accepted Sun Wei's "3 warnings" without checking email system
  3. Legal review gap: Legal relies on HRBP summary package without independent verification
     → Ma Li's initial "sufficient" assessment based on unverified package
  4. PIP governance gap: No system gate to ensure PIP completion before termination
     → Termination at Day 40, Week 4 check-in and final assessment skipped

Usage:
    python check_q22.py <workspace_path>
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

    # Find the systemic gaps report file
    candidates = (
        list(docs_dir.glob("*systemic*gaps*.md")) +
        list(docs_dir.glob("*systemic*failure*.md")) +
        list(docs_dir.glob("*系统性*漏洞*.md")) +
        list(docs_dir.glob("*系统*缺口*.md")) +
        list(docs_dir.glob("*process*gap*.md"))
    )

    if not candidates:
        candidates = [f for f in docs_dir.glob("*.md")
                      if any(kw in f.name.lower() for kw in
                             ["systemic", "system", "gap", "failure", "漏洞", "系统", "流程"])]

    if not candidates:
        print("FAILED: no systemic gaps report found in docs/")
        sys.exit(1)

    target = sorted(candidates, key=lambda f: f.stat().st_mtime, reverse=True)[0]

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    # Check for systemic (not individual) framing
    systemic_terms = [
        r'systemic|系统性|流程性|institutional|制度', r'training|培训|流程|checklist|清单',
        r'process.gap|流程.缺口|系统缺失', r'governance|治理|监督机制',
    ]
    systemic_count = sum(1 for p in systemic_terms if re.search(p, content, re.IGNORECASE))
    if systemic_count < 2:
        errors.append(
            "FAILED: file does not adequately frame gaps as SYSTEMIC issues "
            f"(found {systemic_count} systemic framing terms; expected >= 2)"
        )

    # Check for >= 2 distinct gap identifications
    gap_indicators = [
        r'(written warning|书面警告).{0,200}(training|培训|定义|definition)',
        r'(HRBP|陈浩).{0,200}(verify|核实|verification|check)',
        r'(legal|法务|马丽).{0,200}(independent|独立|verify|核实)',
        r'(PIP|改进计划).{0,200}(complete|完成|gate|审批|gating)',
        r'(gap|漏洞|缺口|缺失).{0,50}(\d)',
    ]
    gaps_identified = sum(1 for p in gap_indicators if re.search(p, content, re.IGNORECASE | re.DOTALL))
    if gaps_identified < 2:
        errors.append(
            f"FAILED: file identifies only {gaps_identified} specific systemic gaps "
            "(expected >= 2 of: manager training gap, HRBP verification gap, "
            "legal review gap, PIP governance gap)"
        )

    # Check for improvement recommendations
    recommendation_terms = [
        r'建议|recommend|改进|improvement|should|应当|应该',
        r'培训|train|checklist|清单|policy|政策',
    ]
    has_recommendations = any(re.search(p, content, re.IGNORECASE) for p in recommendation_terms)
    if not has_recommendations:
        errors.append(
            "FAILED: file does not include improvement recommendations "
            "(expected: 建议, recommend, 改进, checklist)"
        )

    # Check for case-specific references
    case_refs = [
        r'孙伟|Sun Wei', r'陈浩|Chen Hao', r'2026-01-15|January 15',
        r'2026-02-01|February 1', r'书面警告|written warning',
    ]
    has_case_refs = any(re.search(p, content, re.IGNORECASE) for p in case_refs)
    if not has_case_refs:
        errors.append(
            "FAILED: file does not reference specific case events or people "
            "(expected: 孙伟, 陈浩, specific dates from the case)"
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
