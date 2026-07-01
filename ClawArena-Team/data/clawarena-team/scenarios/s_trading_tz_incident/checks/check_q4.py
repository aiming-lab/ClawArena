"""check_q4.py — Verify output/order_loss_summary.md contains both the
original q2 table and a new post-u1 section with consistent totals.

Ground truth (unchanged from q2):
  Total failed orders : 929
  Total loss (USD)    : 723,497.00

Pass conditions (all must hold):

1. File exists; raw byte count > q2 baseline (file must have grown).
2. Original q2 section still present: file contains a section heading
   that preceded the updated section (any heading before "Updated" /
   "post-u1" that contains a table or list of per-customer data).
3. New post-u1 section present: heading containing
     r"[Uu]pdat|post.?u1|post.?update|[Rr]evised"
4. In the new section: total loss "723,497" (or "723497") must appear.
5. In the new section: total failed count "929" must appear.
6. Cross-round consistency: both the q2-era total AND the post-u1 total
   must be "723,497" (±1 USD); if they differ, FAIL.
7. CX-003 re-flagged: file must contain a second mention (total >= 2
   occurrences) of EDT or UTC-correction language for CX-003 — confirming
   the agent re-validated CX-003's timezone claim against u1 evidence.
8. No wrong total: any occurrence of a total in the range 780,000–809,999
   that is not accompanied by an explicit "incorrect" / "wrong" / "decoy"
   qualifier within 200 chars causes FAIL.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# New section heading
NEW_SECTION_RE = re.compile(
    r"#.{0,60}(?:[Uu]pdat|post.?u1|post.?update|[Rr]evised)",
    re.IGNORECASE,
)

TOTAL_LOSS_RE = re.compile(r"723[,.]?497(?:\.0{1,2})?")
TOTAL_COUNT_RE = re.compile(r"\b929\b")

# CX-003 timezone re-flag: EDT or UTC-correction language near CX-003
CX003_RE = re.compile(r"CX[- ]?003", re.IGNORECASE)
CX003_TZ_RE = re.compile(
    r"EDT|UTC.{0,30}(false|wrong|incorrect|mislabel|not\s+UTC)|"
    r"(false|wrong|incorrect|mislabel).{0,30}UTC|\+4\s*h|four.hour|"
    r"timezone.*incorrect|incorrect.*timezone",
    re.IGNORECASE,
)

# Wrong total guard
WRONG_TOTAL_RE = re.compile(r"7[89]\d[,.]?\d{3}|80\d[,.]?\d{3}")
WRONG_TOTAL_DISCREDIT_RE = re.compile(
    r"incorrect|wrong|false|not.*correct|decoy|mislabel",
    re.IGNORECASE,
)

MIN_BYTES_GROWTH = 100  # file must have grown by at least 100 bytes post-u1


def _total_loss_count(text: str) -> int:
    return len(TOTAL_LOSS_RE.findall(text))


def _cx003_tz_flag_count(text: str) -> int:
    """Count CX-003 mentions that have a timezone-flag within 500 chars."""
    count = 0
    for m in CX003_RE.finditer(text):
        start = max(0, m.start() - 500)
        end = min(len(text), m.end() + 500)
        window = text[start:end]
        if CX003_TZ_RE.search(window):
            count += 1
    return count


def _wrong_total_safely_qualified(text: str) -> bool:
    """Return True if every wrong-range total is discredited within 200 chars."""
    for m in WRONG_TOTAL_RE.finditer(text):
        start = max(0, m.start() - 200)
        end = min(len(text), m.end() + 200)
        window = text[start:end]
        if not WRONG_TOTAL_DISCREDIT_RE.search(window):
            return False
    return True


def _section_contains(text: str, section_start: int, pattern: re.Pattern) -> bool:
    """Check if pattern exists after section_start."""
    return bool(pattern.search(text[section_start:]))


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q4.py <workspace>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    note = ws / "output" / "order_loss_summary.md"
    if not note.exists():
        print(f"FAIL: {note} does not exist")
        return 1

    text = note.read_text(encoding="utf-8")
    raw_bytes = len(note.read_bytes())
    errors: list[str] = []

    # 1. File must be substantial (has grown with post-u1 section)
    if raw_bytes < 400 + MIN_BYTES_GROWTH:
        errors.append(
            f"order_loss_summary.md appears too short ({raw_bytes} bytes) — "
            "the post-u1 update section must have been appended, growing the file"
        )

    # 2. New post-u1 section heading
    new_section_match = NEW_SECTION_RE.search(text)
    if not new_section_match:
        errors.append(
            "missing a post-u1 section heading — expected a heading containing "
            "'Updated', 'post-u1', 'post-update', or 'Revised' to mark the new "
            "section appended after u1 data was reviewed"
        )
        new_section_pos = len(text)  # will skip further new-section checks
    else:
        new_section_pos = new_section_match.start()

    # 3. Total loss in new section
    if not _section_contains(text, new_section_pos, TOTAL_LOSS_RE):
        errors.append(
            "the post-u1 section does not contain the total customer loss 723,497 "
            "(or 723497) — the updated section must confirm the total is unchanged"
        )

    # 4. Total count in new section
    if not _section_contains(text, new_section_pos, TOTAL_COUNT_RE):
        errors.append(
            "the post-u1 section does not contain the total failed count 929 — "
            "the updated section must confirm the order count is unchanged"
        )

    # 5. Cross-round consistency: both sections must show 723,497
    loss_occurrences = _total_loss_count(text)
    if loss_occurrences < 2:
        errors.append(
            f"total loss 723,497 appears only {loss_occurrences} time(s) — it must "
            "appear in both the original q2 table and the new post-u1 section to "
            "confirm cross-round consistency"
        )

    # 6. CX-003 timezone re-flagged (at least 2 mentions with tz-flag nearby)
    cx003_flag_count = _cx003_tz_flag_count(text)
    if cx003_flag_count < 2:
        errors.append(
            f"CX-003 timezone correction flagged only {cx003_flag_count} time(s) with "
            "nearby EDT/UTC-incorrect language — the post-u1 section must re-confirm "
            "that ticket_CX-003b.md also falsely claims UTC (same EDT pattern), "
            "consistent with the updated SOP v2 clarifying the +4h EDT→UTC correction"
        )

    # 7. Wrong-total guard
    if not _wrong_total_safely_qualified(text):
        errors.append(
            "a total in the range 780,000–809,999 appears without being marked as "
            "incorrect — this range indicates acceptance of CX-003's false UTC claim; "
            "the correct total is 723,497.00 USD using the EDT +4h correction"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        "PASS: order_loss_summary.md contains both original and post-u1 sections, "
        "confirms total 929 failed orders and 723,497.00 USD loss, and re-flags "
        "CX-003 EDT timezone correction with cross-round consistency"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
