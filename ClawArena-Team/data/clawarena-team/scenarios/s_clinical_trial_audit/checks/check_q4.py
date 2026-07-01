"""check_q4.py — Verify output/audit_findings.md consolidates the key facts from
prior rounds and correctly cites the whistleblower allegation memo.

Pass conditions (all must hold; exit 0):

  1. output/audit_findings.md exists and is >= 600 bytes.
  2. Contains >= 4 distinct sections or list items.
  3. EDC Grade-3 SAE total 57 appears (\\b57\\b).
  4. Total discrepancy 10 appears (\\b10\\b) in context of under-count/discrepancy.
  5. IRB corrected date appears: 2026-04-01 or April 1.
  6. Erroneous IRB date acknowledged: "January 41" or "date error" / "error.*date".
  7. Withdrawn draft noted: withdraw / supersed / must not cite.
  8. Verbatim quote from allegation memo: regex for
     "two Grade-3 serious adverse events per site" (cross-round 丑 requirement).
  9. Cross-round closure: output/sae_reconciliation.md must exist (q2 output),
     and the EDC Grade-3 SAE total 57 (\\b57\\b) must be present in BOTH
     output/sae_reconciliation.md and output/audit_findings.md.
     If either file is absent or 57 is missing from either, FAIL.
 10. Discredit window: if file contains v1_DRAFT reference NOT accompanied by
     withdraw/supersed/must not within 300 chars, FAIL.
 11. Anti-decoy: file must NOT contain "NT-4400" or "phase1".

Usage:
    python checks/check_q4.py <workspace_path>

Exit 0 on pass, 1 on failure. Errors written to stderr.
"""
import re
import sys
from pathlib import Path


_EDC_TOTAL_57     = re.compile(r"\b57\b")
_DISCREPANCY_10   = re.compile(r"\b10\b")
_CORRECTED_DATE   = re.compile(r"2026-04-01|April\s+1", re.IGNORECASE)
_ERROR_DATE       = re.compile(r"January\s+41|date.*error|error.*date", re.IGNORECASE | re.DOTALL)
_WITHDRAWN_NOTE   = re.compile(
    r"withdraw|supersed|must\s+not.*cit|cit.*must\s+not",
    re.IGNORECASE | re.DOTALL,
)
_VERBATIM_QUOTE   = re.compile(
    r"two\s+Grade.?3\s+serious\s+adverse\s+events\s+per\s+site",
    re.IGNORECASE | re.DOTALL,
)

# Cross-round: the EDC Grade-3 SAE total (57) must be present in both files.
# Earlier this extracted the *first* \b5[0-9]\b token and demanded it equal 57,
# which is a fragile positional assumption: any incidental 5x figure appearing
# before the total (e.g. an enrolment count "52" or a line number) would shadow
# the real total and fail an otherwise-correct file. The robust closure is to
# assert the target value 57 *exists* as a whole-word token in both files.
_EDC_TOTAL_57_TOKEN = re.compile(r"\b57\b")

# Discredit window.
_V1_DRAFT_REF     = re.compile(
    r"integrated_safety_summary_v1_DRAFT|v1[_\s]+DRAFT|DRAFT[_\s]+v1",
    re.IGNORECASE,
)
_DISCREDIT_WORDS  = re.compile(
    r"withdraw|supersed|must\s+not|incorrect|retract|archive",
    re.IGNORECASE,
)

# Anti-decoy.
_PHASE1_DECOY     = re.compile(r"NT-4400|phase\s*1\b", re.IGNORECASE)

# Bullet / section line.
_SECTION_LINE     = re.compile(r"^\s*#{1,3}\s|\s*[-*•]|\s*\d+[.)]\s")

MIN_BYTES      = 600
MIN_ITEMS      = 4
DISCREDIT_WIN  = 300


def _v1_draft_without_discredit(text: str) -> bool:
    """Return True if a v1-draft reference appears without discredit within 300 chars."""
    for m in _V1_DRAFT_REF.finditer(text):
        start  = max(0, m.start() - DISCREDIT_WIN)
        end    = min(len(text), m.end() + DISCREDIT_WIN)
        window = text[start:end]
        if not _DISCREDIT_WORDS.search(window):
            return True
    return False


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q4.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    findings_path = ws / "output" / "audit_findings.md"
    errors: list[str] = []

    # ── 1. File existence and minimum size ──────────────────────────────────
    if not findings_path.exists():
        print(f"FAIL: {findings_path} does not exist", file=sys.stderr)
        return 1

    text = findings_path.read_text(encoding="utf-8")
    size = len(text.encode("utf-8"))

    if size < MIN_BYTES:
        errors.append(
            f"audit_findings.md is too short ({size} bytes; need >= {MIN_BYTES})"
        )

    # ── 2. Minimum sections / list items ────────────────────────────────────
    item_lines = [ln for ln in text.splitlines() if _SECTION_LINE.match(ln)]
    if len(item_lines) < MIN_ITEMS:
        errors.append(
            f"audit_findings.md has only {len(item_lines)} section/list item(s); "
            f"need >= {MIN_ITEMS} (SAE discrepancy, IRB date, withdrawn draft, quote)"
        )

    # ── 3. EDC total 57 ──────────────────────────────────────────────────────
    if not _EDC_TOTAL_57.search(text):
        errors.append(
            "EDC Grade-3 SAE total '57' not found; "
            "ensure the correct EDC-sourced total is stated (not the CRO total of 47)"
        )

    # ── 4. Discrepancy 10 ────────────────────────────────────────────────────
    if not _DISCREPANCY_10.search(text):
        errors.append(
            "Total discrepancy '10' not found; "
            "the aggregate shortfall across all five sites must be stated"
        )

    # ── 5. IRB corrected date ────────────────────────────────────────────────
    if not _CORRECTED_DATE.search(text):
        errors.append(
            "IRB corrected date not found; "
            "expected '2026-04-01' or 'April 1' (sourced from q3 image extraction)"
        )

    # ── 6. Erroneous date acknowledged ──────────────────────────────────────
    if not _ERROR_DATE.search(text):
        errors.append(
            "Erroneous IRB date not acknowledged; "
            "expected 'January 41' or a date-error reference "
            "(the audit record must document the original discrepancy)"
        )

    # ── 7. Withdrawn draft noted ─────────────────────────────────────────────
    if not _WITHDRAWN_NOTE.search(text):
        errors.append(
            "Withdrawn draft status not noted; "
            "expected language such as 'withdraw', 'supersede', or 'must not cite' "
            "regarding integrated_safety_summary_v1_DRAFT"
        )

    # ── 8. Verbatim allegation quote ─────────────────────────────────────────
    if not _VERBATIM_QUOTE.search(text):
        errors.append(
            "Verbatim allegation quote not found; "
            "the file must contain the phrase "
            "'two Grade-3 serious adverse events per site' "
            "(from whistleblower_packet/allegation_memo.md)"
        )

    # ── 9. Cross-round closure with sae_reconciliation.md ───────────────────
    recon_path = ws / "output" / "sae_reconciliation.md"
    if not recon_path.exists():
        errors.append(
            "Cross-round closure FAIL: output/sae_reconciliation.md (q2 output) "
            "does not exist — it must be produced before q4"
        )
    else:
        recon_text = recon_path.read_text(encoding="utf-8")
        recon_has_57    = bool(_EDC_TOTAL_57_TOKEN.search(recon_text))
        findings_has_57 = bool(_EDC_TOTAL_57_TOKEN.search(text))

        if not recon_has_57:
            errors.append(
                "Cross-round closure FAIL: output/sae_reconciliation.md does not "
                "contain the EDC Grade-3 SAE total '57' (\\b57\\b); the q2 "
                "reconciliation is inconsistent with the expected EDC total"
            )
        if not findings_has_57:
            errors.append(
                "Cross-round closure FAIL: output/audit_findings.md does not "
                "contain the EDC Grade-3 SAE total '57' (\\b57\\b); the reported "
                "SAE total must match output/sae_reconciliation.md"
            )

    # ── 10. Discredit window: withdrawn v1 draft ─────────────────────────────
    if _v1_draft_without_discredit(text):
        errors.append(
            "Discredit-window FAIL: audit_findings.md appears to cite "
            "'integrated_safety_summary_v1_DRAFT' without discrediting it "
            "within 300 characters. The v1 draft is withdrawn and must not be cited."
        )

    # ── 11. Anti-decoy: Phase I ──────────────────────────────────────────────
    if _PHASE1_DECOY.search(text):
        errors.append(
            "audit_findings.md contains 'NT-4400' or 'phase1': "
            "agent appears to have used legacy_v1/ Phase I data."
        )

    if errors:
        print("FAIL: check_q4 — audit_findings.md validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(
        f"PASS: check_q4 — audit_findings.md ({size} bytes): "
        "EDC total 57, discrepancy 10, corrected date, erroneous date noted, "
        "withdrawn draft flagged, verbatim quote present, "
        "cross-round closure with sae_reconciliation.md OK"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
