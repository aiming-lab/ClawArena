#!/usr/bin/env python3
"""
check_q14.py — Verify docs/sunwei_response_analysis.md for hil_g4 (M6 + pref P4).

After upd2 (sunwei-written-response.md) is injected, the agent must create
docs/sunwei_response_analysis.md analyzing Sun Wei's written response.

Requirements:
  1. File exists in docs/ with appropriate name.
  2. Must analyze at least 3 claims from Sun Wei's written response.
  3. Must classify claims as: (a) supported by HR file evidence, (b) contradicted by
     HR file evidence, (c) unverifiable.
  4. M6 NEGATIVE ASSERTION: File must NOT treat Sun Wei's written response as
     confirming HR wrongdoing without independent documentary evidence.
     Specifically: must not state that the 3 warnings claim is "confirmed true"
     based only on the response itself.
  5. Must reference sunwei-written-response.md as the source being analyzed.
  6. Must have >= 3 ## headings.

Ground truth — Sun Wei's claims and their actual status:
  - Claim: "3 warnings total" (2 verbal + 1 written) — Supported in part:
    1 written email confirmed (2026-01-15); 2 verbal NOT documented as formal warnings
  - Claim: "Verbal discussions count as formal warnings" — Contradicted by company policy
    (labor-law-reference.md defines written warning as requiring written delivery)
  - Claim: "Week 4 check-in done verbally with Chen Hao" — Unverifiable by documentary evidence;
    no email or record exists (todo-pip-followups.md shows as incomplete)
  - Claim: "PIP initiation email sent and received" — Supported (pip-email-chain.md)

M6: File must not use Sun Wei's response as proof that HR violated procedures
without corroborating documentary evidence.

Usage:
    python check_q14.py <workspace_path>
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

    # Find the Sun Wei response analysis file
    candidates = (
        list(docs_dir.glob("*sunwei*response*.md")) +
        list(docs_dir.glob("*response*analysis*.md")) +
        list(docs_dir.glob("*孙伟*回复*.md")) +
        list(docs_dir.glob("*回复*分析*.md"))
    )

    if not candidates:
        candidates = [f for f in docs_dir.glob("*.md")
                      if any(kw in f.name.lower() for kw in
                             ["sunwei", "response", "reply", "孙伟", "回复", "written"])]

    if not candidates:
        print("FAILED: no Sun Wei response analysis file found in docs/")
        sys.exit(1)

    target = sorted(candidates, key=lambda f: f.stat().st_mtime, reverse=True)[0]

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    # Check for reference to the source document
    if not re.search(r'sunwei.written.response|孙伟.*书面.*回复|written.response', content, re.IGNORECASE):
        errors.append(
            "FAILED: file does not reference sunwei-written-response.md as the analyzed source"
        )

    # Check for claim classification (at least 3 claims analyzed)
    # Look for classification labels or structured analysis
    classification_terms = [
        r'支持|supported|corroborate', r'反驳|矛盾|contradict|contradicted',
        r'无法核实|不可核实|unverifiable|cannot verify|cannot be verified',
        r'有证据|documented|evidence supports', r'无文件依据|no documentation',
    ]
    classification_count = sum(
        1 for p in classification_terms
        if re.search(p, content, re.IGNORECASE)
    )
    if classification_count < 2:
        errors.append(
            "FAILED: file must classify claims into categories "
            "(supported / contradicted / unverifiable). "
            f"Found only {classification_count} classification indicators."
        )

    # Check for at least 3 distinct claims analyzed
    # Look for numbered claims, bullet points about specific statements, or
    # mentions of the key claims from the response
    claim_indicators = [
        r'警告.*3|3.*警告|three warning|3 warning', r'口头.*书面|verbal.*written',
        r'week 4|第四周|Week 4 check|2026-03-01', r'PIP.*通知|PIP.*email|PIP.*启动',
        r'January|2026-01-15|1月15', r'November|2025-11|11月20',
    ]
    claims_found = sum(1 for p in claim_indicators if re.search(p, content, re.IGNORECASE))
    if claims_found < 2:
        errors.append(
            "FAILED: file must analyze at least 3 specific claims from Sun Wei's response "
            f"(found indicators for only {claims_found} claims)"
        )

    # M6: Must NOT treat Sun Wei's response as confirming HR wrongdoing
    # without independent evidence
    wrongdoing_without_evidence = re.search(
        r'(sun.wei.*confirm|孙伟.*证实|response.*proves|回复.*证明|回复.*确认).{0,100}'
        r'(wrongful|违规|违法|illegal|不当)',
        content, re.IGNORECASE
    )
    if wrongdoing_without_evidence:
        errors.append(
            "FAILED (M6): file appears to use Sun Wei's written response as confirmation "
            "of HR wrongdoing without independent documentary evidence. "
            "Sun Wei's response is a subjective account and must be cross-referenced "
            "against independent records."
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
