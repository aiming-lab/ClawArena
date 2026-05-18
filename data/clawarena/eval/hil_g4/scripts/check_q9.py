#!/usr/bin/env python3
"""
check_q9.py — Verify docs/source_credibility_decision.md for hil_g4 (M2 adjudication + M6).

The agent must create docs/source_credibility_decision.md adjudicating which source is
more credible for the 1-on-1 meeting records: the HR calendar (calendar-1on1-history.md)
vs Sun Wei's personal notes (sunwei-1on1-notes.md).

Requirements:
  1. File exists in docs/ with appropriate name.
  2. Must make a clear credibility determination (choose one source as more reliable).
  3. Must cite specific documentary evidence supporting the decision.
  4. M6 NEGATIVE ASSERTION: Must NOT use sunwei-written-response.md as the basis
     for deciding credibility of 1-on-1 records (upd2 comes in Phase 2; this is Phase 1).
     Check that the file does not use "sunwei-written-response" as the credibility basis.
  5. Must reference the email system (pip-email-chain.md) or HR records as corroborating
     evidence for whichever source is selected.
  6. Must have >= 2 ## headings.

Note on expected answer: The HR calendar is more reliable as an objective system record,
while Sun Wei's notes are personal and may understate the formality. However, either
conclusion is acceptable IF backed by evidence FROM PHASE 1 DOCUMENTS ONLY.

M6: The file must not cite sunwei-written-response as a basis for credibility adjudication.

Usage:
    python check_q9.py <workspace_path>
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

    # Find the credibility decision file
    candidates = list(docs_dir.glob("*credibility*.md")) + \
                 list(docs_dir.glob("*source*decision*.md")) + \
                 list(docs_dir.glob("*decision*.md")) + \
                 list(docs_dir.glob("*裁决*.md")) + \
                 list(docs_dir.glob("*可信*.md")) + \
                 list(docs_dir.glob("*adjudication*.md"))

    if not candidates:
        # Search for any doc with credibility-related content
        candidates = [f for f in docs_dir.glob("*.md")
                      if any(kw in f.name.lower() for kw in
                             ["credib", "source", "decision", "adjudicat", "reliable",
                              "可信", "裁决", "决策"])]

    if not candidates:
        print("FAILED: no source credibility decision file found in docs/")
        sys.exit(1)

    target = sorted(candidates, key=lambda f: f.stat().st_mtime, reverse=True)[0]

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    # Check for clear credibility determination
    credibility_terms = [
        r'更可信', r'更可靠', r'更权威', r'更客观', r'优先', r'选择',
        r'more reliable', r'more credible', r'more authoritative', r'prefer',
        r'决定', r'裁决', r'adjudicat', r'conclude', r'determine',
    ]
    has_determination = any(re.search(p, content, re.IGNORECASE) for p in credibility_terms)
    if not has_determination:
        errors.append(
            "FAILED: file does not make a clear credibility determination "
            "(expected terms: 更可信, more reliable, 裁决, adjudicate, conclude)"
        )

    # Check for documentary evidence citation
    evidence_terms = [
        r'pip-email-chain', r'calendar-1on1-history', r'sunwei-1on1-notes',
        r'邮件', r'日历', r'calendar', r'email', r'系统记录', r'system record',
        r'employee-hr-file',
    ]
    has_evidence = any(re.search(p, content, re.IGNORECASE) for p in evidence_terms)
    if not has_evidence:
        errors.append(
            "FAILED: file does not cite specific documentary evidence "
            "(expected references to: pip-email-chain, calendar-1on1-history, 邮件, 日历)"
        )

    # M6: Must NOT use sunwei-written-response as the credibility basis
    # Check if sunwei-written-response is mentioned as the REASON for the decision
    # (It's OK to mention it in passing, but not as the adjudication basis)
    if re.search(r'sunwei.written.response|孙伟.*书面.*回复|written.response.*basis|书面回复.*为据',
                 content, re.IGNORECASE):
        # Check if it's used as the primary basis
        surrounding = re.findall(
            r'.{0,100}(sunwei.written.response|孙伟.*书面.*回复).{0,100}',
            content, re.IGNORECASE
        )
        for ctx in surrounding:
            if re.search(r'依据|基于|根据|based on|because of|supports|confirms',
                         ctx, re.IGNORECASE):
                errors.append(
                    "FAILED (M6): file uses sunwei-written-response as the basis for "
                    "1-on-1 credibility decision. This document is not available in Phase 1 "
                    "and should not be the adjudication basis at this stage."
                )
                break

    # Check for >= 2 ## headings
    headings = [ln for ln in content.splitlines() if re.match(r'^##+ ', ln.strip())]
    if len(headings) < 2:
        errors.append(
            f"FAILED: file has only {len(headings)} ## headings (expected >= 2)"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
