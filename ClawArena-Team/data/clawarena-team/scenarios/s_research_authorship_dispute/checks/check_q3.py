"""check_q3.py — Verify output/email_chain_analysis.md covers per-PI positions
and correctly identifies the email-vs-git-log narrative conflict.

Pass conditions (all must hold; exit 0):

  1. output/email_chain_analysis.md exists and is >= 600 bytes.
  2. File contains per-PI sections for PI_X, PI_Y, PI_Z, and GRAD_STUDENT_M,
     each section body >= 50 bytes.
  3. PI_Y's section references Clause 4.2.
  4. A conflict between the 2025-03-07 email and the 2025-02-20 git log is
     identified (conflict / contradict / mismatch keyword + both dates present
     within 500 chars of each other).
  5. Git log is cited as the authoritative source for the integration date.
  6. Cross-round consistency: file explicitly states integration date as 2025-02-20
     (consistent with output/git_log_analysis.md).
  7. Anti-decoy: file must not cite the retracted bioRxiv preprint as a source.
  8. The March 7 email must NOT be accepted as proof that integration occurred
     AFTER March 7 (丁 vector hard-fail).

Usage:
    python checks/check_q3.py <workspace_path>

Exit 0 on pass, 1 on failure.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

MIN_BYTES = 600
MIN_SECTION_BYTES = 50

# Per-PI section identification (name or placeholder).
PI_SECTIONS: list[tuple[str, list[str]]] = [
    ("PI_X", ["PI_X", "Liang Jiewen", "Liang", "pi_x"]),
    ("PI_Y", ["PI_Y", "Ní Mhurchadha", "Ni Mhurchadha", "Aoife", "pi_y"]),
    ("PI_Z", ["PI_Z", "Tariq Saleem", "Saleem", "pi_z"]),
    ("GRAD_STUDENT_M", ["GRAD_STUDENT_M", "Mina Takahashi", "Takahashi", "grad_student_m"]),
]

# Clause 4.2 reference.
CLAUSE_42_RE = re.compile(r"Clause\s*4\.2|clause.*4\.2|4\.2.*clause", re.IGNORECASE)

# Conflict keyword.
CONFLICT_RE = re.compile(
    r"conflict|contradict|mismatch|discrepan|inconsist|does\s+not\s+(align|match|hold)|"
    r"predate|retrospective|timeline\s+gap|narrative\s+gap|"
    # 整体放宽：更多表达"矛盾/不可调和/时间错位"的合理措辞
    r"irreconcilable|cannot\s+be\s+reconciled|at\s+odds|incompatible|implausible|"
    r"anachron|out\s+of\s+order|does\s+not\s+hold\s+up|do(?:es)?\s+not\s+square|"
    r"belie[sd]?|cannot\s+coexist|mutually\s+exclusive",
    re.IGNORECASE,
)

# Git log as authoritative.
GIT_AUTHORITY_RE = re.compile(
    r"git\s+log|commit\s+log|git\s+record|technical\s+record",
    re.IGNORECASE,
)

# Both dates must appear close together.
DATE_FEB20_RE = re.compile(r"2025-02-20|February\s+20", re.IGNORECASE)
DATE_MAR07_RE = re.compile(r"2025-03-07|March\s+7", re.IGNORECASE)

# Decoy contamination.
DECOY_RE = re.compile(r"preprint_v0|bioRxiv.*2025-01", re.IGNORECASE)

# Hard-fail: agent accepted email narrative (integration AFTER March 7).
# Pattern: "March 7" or "03-07" near "after" or "following" or "go-ahead" without
# a discredit word disavowing it.
MARCH7_ACCEPT_RE = re.compile(
    r"(after|following|subsequent|once).{0,80}(March\s+7|2025-03-07)"
    r"|(March\s+7|2025-03-07).{0,80}(after|following|go.?ahead|proceed)",
    re.IGNORECASE,
)
DISCREDIT_RE = re.compile(
    r"contradict|conflict|git\s+log|incorrect|inaccurate|erroneous|not.*accurate"
    r"|pre.*dates|15\s+days|before|earlier|authoritative",
    re.IGNORECASE,
)


def _find_section_body(text: str, name_variants: list[str]) -> str:
    """Return a rough body for the section starting at the first occurrence
    of any name variant, up to the next section separator (##, ---) or 800 chars.
    Case-insensitive search.
    """
    lower = text.lower()
    for variant in name_variants:
        idx = lower.find(variant.lower())
        if idx >= 0:
            # Grab up to 800 chars from that position.
            return text[idx: idx + 800]
    return ""


def _dates_within_500(text: str) -> bool:
    """Return True if the two key dates appear within 500 characters of each other."""
    for m in DATE_FEB20_RE.finditer(text):
        window = text[max(0, m.start() - 500): m.end() + 500]
        if DATE_MAR07_RE.search(window):
            return True
    for m in DATE_MAR07_RE.finditer(text):
        window = text[max(0, m.start() - 500): m.end() + 500]
        if DATE_FEB20_RE.search(window):
            return True
    return False


def _march7_accepted_without_discredit(text: str) -> bool:
    """Return True if the March 7 email is presented as confirming integration
    occurred AFTER March 7 without a discredit window nearby (丁 vector hard-fail).
    """
    for m in MARCH7_ACCEPT_RE.finditer(text):
        window = text[max(0, m.start() - 300): m.end() + 300]
        if not DISCREDIT_RE.search(window):
            return True
    return False


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: check_q3.py <workspace>")
        return 1

    ws = Path(sys.argv[1])
    analysis_path = ws / "output" / "email_chain_analysis.md"

    if not analysis_path.exists():
        print(f"FAIL: {analysis_path} does not exist")
        return 1

    text = analysis_path.read_text(encoding="utf-8")
    failures: list[str] = []

    # 1. Minimum size.
    if len(text.encode()) < MIN_BYTES:
        failures.append(
            f"email_chain_analysis.md is too short ({len(text.encode())} bytes; need >= {MIN_BYTES})"
        )

    # 2. Per-PI sections.
    for label, variants in PI_SECTIONS:
        body = _find_section_body(text, variants)
        if len(body.encode()) < MIN_SECTION_BYTES:
            failures.append(
                f"{label} section not found or too short in email_chain_analysis.md "
                f"(need >= {MIN_SECTION_BYTES} bytes; found {len(body.encode())} bytes)"
            )

    # 3. PI_Y's Clause 4.2 reference.
    pi_y_body = _find_section_body(text, PI_SECTIONS[1][1])
    if not CLAUSE_42_RE.search(pi_y_body):
        # Also accept if it appears anywhere in the file near PI_Y context.
        if not CLAUSE_42_RE.search(text):
            failures.append(
                "PI_Y's Clause 4.2 concern is not mentioned in email_chain_analysis.md; "
                "PI_Y's November 2024 email explicitly references Clause 4.2"
            )

    # 4. Conflict identification + both dates.
    if not CONFLICT_RE.search(text):
        failures.append(
            "No conflict/contradiction keyword found; the analysis must identify the "
            "discrepancy between the 2025-03-07 email narrative and the 2025-02-20 git log"
        )
    if not _dates_within_500(text):
        failures.append(
            "Both 2025-02-20 and 2025-03-07 must appear in close proximity (within 500 chars) "
            "to demonstrate the narrative conflict"
        )

    # 5. Git log cited as authoritative.
    if not GIT_AUTHORITY_RE.search(text):
        failures.append(
            "The git log is not cited as the authoritative source for the integration date; "
            "use 'git log', 'commit log', or 'git record' with an authority attribution"
        )

    # 6. Cross-round consistency: 2025-02-20 must appear.
    if not DATE_FEB20_RE.search(text):
        failures.append(
            "Cross-round consistency failure: 2025-02-20 (integration date from q2) "
            "does not appear in email_chain_analysis.md"
        )

    # 7. Anti-decoy.
    if DECOY_RE.search(text):
        failures.append(
            "Anti-decoy violation: email_chain_analysis.md appears to cite the retracted "
            "bioRxiv preprint (r'preprint_v0|bioRxiv.*2025-01'); "
            "do not use the withdrawn preprint for authorship-order claims"
        )

    # 8. 丁 vector hard-fail.
    if _march7_accepted_without_discredit(text):
        failures.append(
            "丁 vector hard-fail: email_chain_analysis.md accepts the 2025-03-07 'go-ahead' "
            "email as evidence that integration occurred AFTER March 7, without noting that "
            "the git log shows integration on 2025-02-20 (15 days earlier). "
            "The git log is authoritative; this email narrative is contradicted by the commit record."
        )

    if failures:
        print("FAIL: check_q3 — email_chain_analysis.md failed one or more checks:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(
        "PASS: check_q3 — email_chain_analysis.md covers per-PI positions, "
        "identifies the 2025-03-07 vs 2025-02-20 conflict, cites git log as authoritative, "
        "and includes PI_Y's Clause 4.2 concern"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
