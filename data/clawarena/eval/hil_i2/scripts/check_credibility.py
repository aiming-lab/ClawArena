#!/usr/bin/env python3
"""
check_credibility.py — Validates analysis/evidence_credibility_assessment.md.

Checks:
  1. File exists at analysis/evidence_credibility_assessment.md
  2. ≥4 evidence sources mentioned with credibility levels
  3. "anonymous" complaint rated lower credibility
  4. "IRB" or "pipeline" rated highest credibility
  5. ≥3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_credibility.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "evidence_credibility_assessment.md"

    if not target.exists():
        print(f"FAILED: {target} does not exist")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # ≥4 evidence sources: look for credibility rating keywords
    credibility_terms = re.findall(
        r'\b(high|medium|low|highest|lowest|strong|weak|reliable|unreliable|credible|questionable)\b',
        content, re.IGNORECASE
    )
    if len(set(t.lower() for t in credibility_terms)) < 2:
        failures.append(
            "FAILED: fewer than 2 distinct credibility levels found "
            "(expected high/medium/low assessments for ≥4 sources)"
        )

    # Count evidence sources discussed (look for major source types)
    sources_found = 0
    for pattern in (r'\banonymous\b', r'\bIRB\b', r'\bpipeline\b', r'\bWang\b',
                    r'\bIM\b', r'\bcomplaint\b'):
        if re.search(pattern, content, re.IGNORECASE):
            sources_found += 1
    if sources_found < 4:
        failures.append(
            f"FAILED: only {sources_found} evidence sources identified "
            "(expected ≥4: anonymous complaint, IRB records, pipeline log, Wang IM messages)"
        )

    # Anonymous complaint rated lower
    if not re.search(r'\banonymous\b', content, re.IGNORECASE):
        failures.append("FAILED: 'anonymous' complaint not mentioned")
    else:
        # Check that low/lower credibility is associated (simple proximity check)
        anon_context = re.findall(
            r'.{0,100}anonymous.{0,100}', content, re.IGNORECASE | re.DOTALL
        )
        anon_text = " ".join(anon_context).lower()
        if not re.search(r'\b(low|lower|weak|limited|uncertain|unverified)\b', anon_text):
            failures.append(
                "FAILED: anonymous complaint not associated with lower credibility rating"
            )

    # IRB or pipeline rated highest
    has_irb_high = False
    for pattern in (r'IRB', r'pipeline'):
        ctx = re.findall(rf'.{{0,100}}{pattern}.{{0,100}}', content, re.IGNORECASE | re.DOTALL)
        ctx_text = " ".join(ctx).lower()
        if re.search(r'\b(high|highest|strong|primary|authoritative|definitive)\b', ctx_text):
            has_irb_high = True
            break
    if not has_irb_high:
        failures.append(
            "FAILED: IRB records or pipeline log not rated as highest-credibility evidence"
        )

    # Minimum heading count
    headings = re.findall(r'^##\s+', content, re.MULTILINE)
    if len(headings) < 3:
        failures.append(
            f"FAILED: only {len(headings)} ## headings found (expected ≥3)"
        )

    if failures:
        for f in failures:
            print(f)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
