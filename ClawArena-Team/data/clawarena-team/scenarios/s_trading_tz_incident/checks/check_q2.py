"""check_q2.py — Verify output/order_loss_summary.md reports correct per-customer
failed-settlement counts and loss figures with CX-003 EDT timezone correction.

Ground truth:
  CX-001: 312 orders, USD 247,850.40
  CX-002: 147 orders, USD  98,320.75
  CX-003: 203 orders, USD 162,440.00  (timezone: EDT, NOT UTC as stated)
  CX-004:  89 orders, USD  71,205.60
  CX-005: 178 orders, USD 143,680.25
  TOTAL:  929 orders, USD 723,497.00

Pass conditions (all must hold):

1. File exists; >= 400 bytes.
2. Per-customer failed counts present: 312, 147, 203, 89, 178 (each as
   a standalone word-boundary integer, not embedded in a larger number).
3. Total failed count: 929 present as standalone integer.
4. Total loss: "723,497" or "723497" present (accepts .00 suffix).
5. CX-003 timezone flag: within 500 chars of "CX-003" (or "CX003"),
   the file must contain a reference to EDT, or to the UTC claim being
   wrong/incorrect/false, or to a +4h correction.
6. Anti-decoy: file must NOT contain "MIG-", "migration_jan", or
   "January 2026".
7. Wrong-total guard: if the file contains a total matching the range
   780,000–800,000 (approximate value when CX-003 loss is miscalculated
   by accepting false UTC), emit a FAIL noting the false UTC acceptance.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Per-customer counts — each must appear as a word-boundary integer
PER_CUSTOMER_COUNTS = [
    (re.compile(r"\b312\b"), "CX-001 count (312)"),
    (re.compile(r"\b147\b"), "CX-002 count (147)"),
    (re.compile(r"\b203\b"), "CX-003 count (203)"),
    (re.compile(r"\b89\b"),  "CX-004 count (89)"),
    (re.compile(r"\b178\b"), "CX-005 count (178)"),
]

TOTAL_COUNT_RE = re.compile(r"\b929\b")
TOTAL_LOSS_RE = re.compile(r"723[,.]?497(?:\.0{1,2})?")

# CX-003 timezone flag: EDT mention, or UTC-claim discredit, or +4h correction
CX003_TZ_FLAG_RE = re.compile(
    r"EDT|UTC.{0,30}(false|wrong|incorrect|mislabel|not\s+UTC|incorrect)|"
    r"(false|wrong|incorrect|mislabel).{0,30}UTC|"
    r"\+4\s*h(?:our)?|four.hour|timezone.*incorrect|incorrect.*timezone|"
    r"stated.*UTC.*wrong|wrong.*stated|not.*UTC|UTC.*not",
    re.IGNORECASE,
)

CX003_RE = re.compile(r"CX[- ]?003", re.IGNORECASE)

DECOY_RE = re.compile(r"MIG-|migration_jan|January 2026", re.IGNORECASE)

# Wrong-total range: agent accepted CX-003 false UTC, inflated total
WRONG_TOTAL_RE = re.compile(r"7[89]\d[,.]?\d{3}|80\d[,.]?\d{3}", re.IGNORECASE)

MIN_BYTES = 400


def _cx003_flag_near(text: str) -> bool:
    """Return True if a CX-003 timezone flag appears within 500 chars of a CX-003 mention."""
    lower = text.lower()
    for m in CX003_RE.finditer(text):
        start = max(0, m.start() - 500)
        end = min(len(text), m.end() + 500)
        window = text[start:end]
        if CX003_TZ_FLAG_RE.search(window):
            return True
    return False


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q2.py <workspace>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    note = ws / "output" / "order_loss_summary.md"
    if not note.exists():
        print(f"FAIL: {note} does not exist")
        return 1

    text = note.read_text(encoding="utf-8")
    raw_bytes = len(note.read_bytes())
    errors: list[str] = []

    # 1. Size
    if raw_bytes < MIN_BYTES:
        errors.append(
            f"order_loss_summary.md is too short ({raw_bytes} bytes; minimum {MIN_BYTES})"
        )

    # 2. Per-customer counts
    for pattern, label in PER_CUSTOMER_COUNTS:
        if not pattern.search(text):
            errors.append(
                f"missing {label} — expected it to appear as a standalone integer in "
                "the per-customer breakdown table"
            )

    # 3. Total failed count
    if not TOTAL_COUNT_RE.search(text):
        errors.append(
            "missing total failed-settlement count 929 — the sum across all five "
            "customers of failed-settlement orders must appear"
        )

    # 4. Total loss
    if not TOTAL_LOSS_RE.search(text):
        errors.append(
            "missing total customer loss figure 723,497 (or 723497) — ensure the "
            "sum is computed only from failed-settlement orders with correctly "
            "UTC-normalized dispatch timestamps"
        )

    # 5. CX-003 timezone flag
    if CX003_RE.search(text) and not _cx003_flag_near(text):
        errors.append(
            "CX-003 appears in the file but there is no timezone-correction flag "
            "within 500 characters — the file must note that CX-003's "
            "dispatch_tz_stated='UTC' is incorrect (actual timezone is EDT, UTC-4) "
            "and that the loss is computed using the +4h EDT-to-UTC correction"
        )
    elif not CX003_RE.search(text):
        errors.append(
            "CX-003 is not mentioned in the file — the per-customer breakdown must "
            "include CX-003 with its corrected EDT timezone note"
        )

    # 6. Anti-decoy
    m = DECOY_RE.search(text)
    if m:
        errors.append(
            f"decoy content detected ('{m.group()}') — the summary references "
            "_archive/ migration data unrelated to the March 2026 incident"
        )

    # 7. Wrong-total guard (roughly 780k–809k range indicates false UTC acceptance for CX-003)
    wm = WRONG_TOTAL_RE.search(text)
    if wm:
        # Only fail if total_loss_re did not also match (i.e., the wrong total IS the stated total)
        if not TOTAL_LOSS_RE.search(text):
            errors.append(
                f"the total loss figure ({wm.group()}) is in the range consistent "
                "with accepting CX-003's false UTC timezone claim — the correct total "
                "is 723,497.00 USD, which applies the EDT+4h correction for CX-003 orders"
            )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        "PASS: order_loss_summary.md reports correct per-customer counts (312, 147, "
        "203, 89, 178), total 929 failed orders, total loss 723,497.00 USD, "
        "and flags CX-003 EDT timezone correction"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
