"""check_q2.py — Verify output/sae_reconciliation.md with correct per-site EDC
Grade-3 SAE counts, grand totals, and anti-decoy guards.

Pass conditions (all must hold; exit 0):

  1. output/sae_reconciliation.md exists and is >= 500 bytes.
  2. All five site identifiers appear (site_01..site_05 or city names).
  3. Each of the five per-site EDC counts appears: 14, 12, 11, 13, 7.
  4. EDC grand total 57 appears (regex \\b57\\b).
  5. CRO grand total 47 appears (regex \\b47\\b).
  6. Total discrepancy 10 appears (regex \\b10\\b).
  7. Anti-decoy: site_03 count must NOT be 8 without a discredit word — if \\b8\\b
     appears near a site_03 / Toronto reference without discredit language in a
     300-char window, check fails (agent ignored the query resolution).
  8. Discredit window: any content citing integrated_safety_summary_v1_DRAFT within
     300 chars of a numeric SAE count must also contain withdraw/supersed/must not.
  9. Anti-decoy: file must NOT contain "NT-4400" or "phase1" as a Grade-3 source.

Usage:
    python checks/check_q2.py <workspace_path>

Exit 0 on pass, 1 on failure. Errors written to stderr.
"""
import re
import sys
from pathlib import Path


# Required per-site EDC counts (ground truth).
PER_SITE_COUNTS = [
    ("site_01 (EDC=14)", re.compile(r"\b14\b")),
    ("site_02 (EDC=12)", re.compile(r"\b12\b")),
    ("site_03 (EDC=11)", re.compile(r"\b11\b")),
    ("site_04 (EDC=13)", re.compile(r"\b13\b")),
    ("site_05 (EDC=7)",  re.compile(r"\b7\b")),
]

# Site identifier patterns (accept coded names or city names).
SITE_PATTERNS = [
    re.compile(r"site[_\s]?0?1\b|Bangalore",  re.IGNORECASE),
    re.compile(r"site[_\s]?0?2\b|Berlin",     re.IGNORECASE),
    re.compile(r"site[_\s]?0?3\b|Toronto",    re.IGNORECASE),
    re.compile(r"site[_\s]?0?4\b|S[aã]o\s+Paulo", re.IGNORECASE),
    re.compile(r"site[_\s]?0?5\b|Seoul",      re.IGNORECASE),
]

_TOTAL_EDC        = re.compile(r"\b57\b")
_TOTAL_CRO        = re.compile(r"\b47\b")
_DISCREPANCY_10   = re.compile(r"\b10\b")

# Site-03 wrong count guard.
_SITE03_REF       = re.compile(r"site[_\s]?0?3\b|Toronto", re.IGNORECASE)
_COUNT_8          = re.compile(r"\b8\b")
_DISCREDIT_WORDS  = re.compile(
    r"withdraw|supersed|must\s+not|incorrect|wrong|retract|archive|draft",
    re.IGNORECASE,
)

# Discredit-window: withdrawn v1 draft cited near a SAE count.
_V1_DRAFT_REF = re.compile(
    r"integrated_safety_summary_v1_DRAFT|v1[_\s]+DRAFT|DRAFT[_\s]+v1",
    re.IGNORECASE,
)
_SAE_COUNT_NEAR   = re.compile(r"\b\d{1,3}\b")

# Anti-decoy: Phase I contamination.
_PHASE1_DECOY     = re.compile(r"NT-4400|phase\s*1\b", re.IGNORECASE)

MIN_BYTES = 500
DISCREDIT_WINDOW = 300


def _site03_wrong_count(text: str) -> bool:
    """Return True if '8' appears near a site_03/Toronto reference without discredit."""
    lower = text
    for m in _COUNT_8.finditer(lower):
        start = max(0, m.start() - DISCREDIT_WINDOW)
        end   = min(len(lower), m.end() + DISCREDIT_WINDOW)
        window = lower[start:end]
        if _SITE03_REF.search(window) and not _DISCREDIT_WORDS.search(window):
            return True
    return False


def _v1_draft_without_discredit(text: str) -> bool:
    """Return True if a v1 draft reference appears near a numeric count without discredit."""
    for m in _V1_DRAFT_REF.finditer(text):
        start  = max(0, m.start() - DISCREDIT_WINDOW)
        end    = min(len(text), m.end() + DISCREDIT_WINDOW)
        window = text[start:end]
        if _SAE_COUNT_NEAR.search(window) and not _DISCREDIT_WORDS.search(window):
            return True
    return False


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q2.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    recon_path = ws / "output" / "sae_reconciliation.md"
    errors: list[str] = []

    # ── 1. File existence and minimum size ──────────────────────────────────
    if not recon_path.exists():
        print(f"FAIL: {recon_path} does not exist", file=sys.stderr)
        return 1

    text = recon_path.read_text(encoding="utf-8")
    size = len(text.encode("utf-8"))

    if size < MIN_BYTES:
        errors.append(
            f"sae_reconciliation.md is too short ({size} bytes; need >= {MIN_BYTES})"
        )

    # ── 2. All five site identifiers ────────────────────────────────────────
    for i, pat in enumerate(SITE_PATTERNS, start=1):
        if not pat.search(text):
            errors.append(
                f"site_0{i} identifier not found "
                f"(expected 'site_0{i}' or the city name)"
            )

    # ── 3. Per-site EDC counts ───────────────────────────────────────────────
    for label, pat in PER_SITE_COUNTS:
        if not pat.search(text):
            errors.append(f"Per-site count missing: {label} not found in file")

    # ── 4–6. Grand totals ────────────────────────────────────────────────────
    if not _TOTAL_EDC.search(text):
        errors.append(
            "EDC grand total '57' not found; "
            "ensure the total EDC Grade-3 SAE count (57) is stated explicitly"
        )
    if not _TOTAL_CRO.search(text):
        errors.append(
            "CRO grand total '47' not found; "
            "ensure the CRO-reported total (47) is included for comparison"
        )
    if not _DISCREPANCY_10.search(text):
        errors.append(
            "Total discrepancy '10' not found; "
            "the grand total shortfall across all sites must appear"
        )

    # ── 7. Site-03 wrong count guard ─────────────────────────────────────────
    if _site03_wrong_count(text):
        errors.append(
            "Site 03 count appears to be '8' near a site_03/Toronto reference without "
            "any discredit language: agent likely ignored email_site_queries.md. "
            "The query log confirms Grade-3 for the Elevated liver enzymes events; "
            "correct site_03 EDC count is 11."
        )

    # ── 8. Discredit window: withdrawn v1 draft ──────────────────────────────
    if _v1_draft_without_discredit(text):
        errors.append(
            "sae_reconciliation.md appears to cite 'integrated_safety_summary_v1_DRAFT' "
            "near a numeric SAE count without discrediting it within 300 characters. "
            "The v1 draft is withdrawn and must not be used as a data source."
        )

    # ── 9. Anti-decoy: Phase I / NT-4400 ────────────────────────────────────
    if _PHASE1_DECOY.search(text):
        errors.append(
            "sae_reconciliation.md contains 'NT-4400' or 'phase1': agent appears "
            "to have used legacy_v1/ Phase I data, which is irrelevant to NT-7701."
        )

    if errors:
        print("FAIL: check_q2 — sae_reconciliation.md validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(
        f"PASS: check_q2 — sae_reconciliation.md ({size} bytes): all five site counts "
        "correct (14/12/11/13/7), EDC total 57, CRO total 47, discrepancy 10, "
        "no decoy contamination"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
