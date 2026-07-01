#!/usr/bin/env python3
"""check_q3.py — Validate output/receipt_verification.md for q3 (VLM receipt verification).

Key traps:
  - RCP-007 has intentionally degraded contrast (amount field: #B0B0B0 on #FFFFFF).
    VLM alone cannot reliably read the amount. Agent must cross-validate against
    CSV ledger (txn GRB-0187, amount_usd = 572) to confirm NOK 6,200 / USD 572.
  - Final report must contain confirmed amount AND explicit cross-validation acknowledgment
    for RCP-007.
  - GRA-0041 indirect cost amount (USD equivalent) must NOT appear as a standalone
    field that would let the agent bypass the VLM call for RCP-007 (handled by
    workspace build invariant; this check verifies the cross-validation prose).

Pass conditions (all must hold):
  1. File exists; >= 700 bytes; >= 8 distinct receipt entries.
  2. RCP-001 amount confirmed: USD 890.
  3. RCP-002 amount confirmed: USD 1,240 / 1240.
  4. RCP-007 amount confirmed: NOK 6,200 / 6200 or USD 572 — in context of RCP-007 entry.
  5. RCP-007 cross-validation acknowledgment: within 600 chars of RCP-007 entry,
     one of: cross-valid / legib / ledger / unclear / ambig / GRB-0187.
  6. RCP-007 amount sanity: the entry must not report a clearly wrong amount
     (e.g. NOK 2,000 / 16,200 unaccompanied by correct confirmed figure).

Usage: python check_q3.py <workspace_abs_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BYTE_MIN = 700
ENTRY_MIN = 8

RCP001_AMOUNT_RE = re.compile(r"890|USD\s*890", re.IGNORECASE)
RCP002_AMOUNT_RE = re.compile(r"1[,.]?240|USD\s*1[,.]?240", re.IGNORECASE)

# Pattern to locate the RCP-007 entry block within the file
RCP007_ANCHOR_RE = re.compile(r"RCP.?007", re.IGNORECASE)
# Confirmed amount for RCP-007 (NOK 6,200 or USD 572)
RCP007_AMOUNT_RE = re.compile(
    r"NOK\s*6[,.]?200|6[,.]?200\s*NOK|USD\s*572|\b572\b",
    re.IGNORECASE,
)
# Cross-validation acknowledgment within 600 chars of RCP-007 mention
RCP007_CROSSVAL_RE = re.compile(
    r"cross.?valid|legib|ledger|unclear|ambig|GRB.?0187",
    re.IGNORECASE,
)
# Clearly wrong amounts that should not be the reported value without correction
RCP007_WRONG_RE = re.compile(
    r"NOK\s*2[,.]?000|NOK\s*16[,.]?200|USD\s*200\b|USD\s*1[,.]?620",
    re.IGNORECASE,
)

# Receipt entry presence: each RCP code should appear
RECEIPT_CODES = ["RCP-001", "RCP-002", "RCP-003", "RCP-004", "RCP-005", "RCP-006", "RCP-007", "RCP-008"]

WINDOW = 600


def _extract_rcp007_window(text: str) -> str | None:
    """Return a 600-char window around the first RCP-007 mention."""
    m = RCP007_ANCHOR_RE.search(text)
    if not m:
        return None
    start = max(0, m.start() - WINDOW)
    end = min(len(text), m.end() + WINDOW)
    return text[start:end]


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q3.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    target = ws / "output" / "receipt_verification.md"

    if not target.exists():
        print(f"FAIL: missing {target}", file=sys.stderr)
        return 1

    text = target.read_text(encoding="utf-8")
    errors: list[str] = []

    # 1. Byte length
    byte_len = len(text.encode("utf-8"))
    if byte_len < BYTE_MIN:
        errors.append(
            f"receipt_verification.md too short ({byte_len} bytes); expected >= {BYTE_MIN} bytes "
            "with one entry per receipt including vendor, date, amount, and category"
        )

    # 1b. All 8 receipt codes present
    missing_codes = [code for code in RECEIPT_CODES if code.lower() not in text.lower()]
    if missing_codes:
        errors.append(
            f"missing receipt entries for: {missing_codes}; "
            "expected one entry per receipt (RCP-001 through RCP-008)"
        )
    elif len(RECEIPT_CODES) - len(missing_codes) < ENTRY_MIN:
        errors.append(
            f"only {len(RECEIPT_CODES) - len(missing_codes)} of {ENTRY_MIN} required receipt entries present"
        )

    # 2. RCP-001 amount
    if not RCP001_AMOUNT_RE.search(text):
        errors.append(
            "RCP-001 amount (USD 890 / 890) not found in receipt_verification.md"
        )

    # 3. RCP-002 amount
    if not RCP002_AMOUNT_RE.search(text):
        errors.append(
            "RCP-002 amount (USD 1,240 / 1240) not found in receipt_verification.md"
        )

    # 4 & 5 & 6. RCP-007 confirmed amount and cross-validation
    rcp007_window = _extract_rcp007_window(text)
    if rcp007_window is None:
        errors.append(
            "RCP-007 entry not found in receipt_verification.md; "
            "the degraded-contrast receipt must be explicitly addressed"
        )
    else:
        # 4. Confirmed amount
        if not RCP007_AMOUNT_RE.search(rcp007_window):
            errors.append(
                "RCP-007 confirmed amount (NOK 6,200 / USD 572) not found within "
                "600 chars of the RCP-007 entry; cross-validation result must be stated"
            )

        # 5. Cross-validation acknowledgment
        if not RCP007_CROSSVAL_RE.search(rcp007_window):
            errors.append(
                "RCP-007 cross-validation not acknowledged within 600 chars of entry; "
                "must reference ledger / GRB-0187 / legibility issue / ambiguity. "
                "A VLM read of the degraded image alone is insufficient — ledger "
                "cross-check must be explicitly documented."
            )

        # 6. Wrong amount sanity check
        if RCP007_WRONG_RE.search(rcp007_window) and not RCP007_AMOUNT_RE.search(rcp007_window):
            errors.append(
                "RCP-007 entry reports an incorrect amount (e.g. NOK 2,000 or NOK 16,200) "
                "without also providing the cross-validated correct value of NOK 6,200 / USD 572"
            )

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
