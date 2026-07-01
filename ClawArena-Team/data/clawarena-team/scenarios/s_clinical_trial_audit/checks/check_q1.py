"""check_q1.py — Verify output/intake_triage.md covers all three allegations,
the 14-day deadline, and the conflicting data sources.

Pass conditions (all must hold; exit 0):

  1. output/intake_triage.md exists and is >= 300 bytes.
  2. Contains >= 3 distinct list items (lines starting with -, *, bullet, or digit.)
  3. Allegation 1 (Grade-3 SAE under-count) matched by regex.
  4. Allegation 2 (IRB date discrepancy) matched by regex.
  5. Allegation 3 (withdrawn v1 draft retained) matched by regex.
  6. Deadline matched by regex (14-day / 2026-05-12 / May 12).
  7. Anti-decoy: file must NOT contain "phase1" or "NT-4400" (would indicate
     agent read legacy_v1/ instead of the requests/).

Usage:
    python checks/check_q1.py <workspace_path>

Exit 0 on pass, 1 on failure. Errors written to stderr.
"""
import re
import sys
from pathlib import Path


# Regexes for the three allegations (case-insensitive).
_ALLEGATION_1 = re.compile(
    r"grade.?3|SAE|under.?report|under.?count|systematic",
    re.IGNORECASE,
)
_ALLEGATION_2 = re.compile(
    r"IRB|date.*discrepan|discrepan.*date|month.*day|day.*month|swap",
    re.IGNORECASE,
)
_ALLEGATION_3 = re.compile(
    r"withdraw|supersed|v1.*draft|draft.*v1|red.?herring|retain",
    re.IGNORECASE,
)
_DEADLINE = re.compile(
    r"14.?day|2026-05-12|May\s+12",
    re.IGNORECASE,
)

# Bullet / numbered list line pattern.
_BULLET_LINE = re.compile(r"^\s*[-*•]|\s*\d+[.)]\s")

# Anti-decoy: references to the legacy Phase I dataset.
_PHASE1_DECOY = re.compile(r"phase1|NT-4400", re.IGNORECASE)

MIN_BYTES = 300
MIN_BULLETS = 3


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q1.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    triage_path = ws / "output" / "intake_triage.md"

    errors: list[str] = []

    # ── 1. File existence and minimum size ──────────────────────────────────
    if not triage_path.exists():
        print(f"FAIL: {triage_path} does not exist", file=sys.stderr)
        return 1

    text = triage_path.read_text(encoding="utf-8")
    size = len(text.encode("utf-8"))

    if size < MIN_BYTES:
        errors.append(
            f"intake_triage.md is too short ({size} bytes; need >= {MIN_BYTES})"
        )

    # ── 2. Minimum number of list items ─────────────────────────────────────
    bullet_lines = [ln for ln in text.splitlines() if _BULLET_LINE.match(ln)]
    if len(bullet_lines) < MIN_BULLETS:
        errors.append(
            f"intake_triage.md has only {len(bullet_lines)} list item(s) "
            f"(need >= {MIN_BULLETS} — one per allegation minimum)"
        )

    # ── 3–5. Three allegations ───────────────────────────────────────────────
    if not _ALLEGATION_1.search(text):
        errors.append(
            "Allegation 1 (Grade-3 SAE under-count) not found; "
            "expected keywords: grade-3 / SAE / under-report / under-count / systematic"
        )
    if not _ALLEGATION_2.search(text):
        errors.append(
            "Allegation 2 (IRB date discrepancy) not found; "
            "expected keywords: IRB / date discrepancy / month-day swap"
        )
    if not _ALLEGATION_3.search(text):
        errors.append(
            "Allegation 3 (withdrawn draft retained) not found; "
            "expected keywords: withdraw / supersede / v1 draft / retain"
        )

    # ── 6. Deadline ──────────────────────────────────────────────────────────
    if not _DEADLINE.search(text):
        errors.append(
            "14-day deadline not found; "
            "expected: '14-day', '2026-05-12', or 'May 12'"
        )

    # ── 7. Anti-decoy guard ──────────────────────────────────────────────────
    if _PHASE1_DECOY.search(text):
        errors.append(
            "intake_triage.md contains 'phase1' or 'NT-4400': agent appears "
            "to have read legacy_v1/ Phase I data, which is irrelevant to this audit"
        )

    if errors:
        print("FAIL: check_q1 — intake_triage.md validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(
        f"PASS: check_q1 — intake_triage.md exists ({size} bytes), "
        f"all three allegations present, deadline noted, no decoy contamination"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
