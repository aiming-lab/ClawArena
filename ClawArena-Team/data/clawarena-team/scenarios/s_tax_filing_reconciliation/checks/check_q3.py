#!/usr/bin/env python3
"""check_q3.py — wave3 s_tax_filing_reconciliation q3 checker.

Verifies output/rental_audit.md:
1. File exists and has ≥ 200 chars.
2. Property address or street reference present (Schönhauser Allee / Schoenhauser).
3. "no rental" / "not recorded" / "未记录" / "no record" class statement present.

D-dimension guard (discredit window):
  If "3,200" / "3200" (education credit hallucination) appears without
  a discredit word within 240 chars → FAIL.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_DISCREDIT_WORDS = re.compile(
    r"\b(?:unverified|inaccurate|incorrect|false|fabricated|hallucinated|"
    r"AI.generated|not.authoritative|do not use|do not rely|disregard|"
    r"not.verified|auto.generated|bot.summary|digest|not.valid|not.confirmed)\b",
    re.IGNORECASE,
)

_WINDOW = 240


def main(workspace: Path) -> int:
    out = workspace / "output" / "rental_audit.md"
    if not out.exists():
        print("FAIL: output/rental_audit.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    if len(text.strip()) < 200:
        print(f"FAIL: rental_audit.md too short ({len(text)} chars)")
        return 1

    # Property address reference
    addr_pattern = re.compile(
        r"Sch[öo]nh[aä]user|Schoenhauser|10437|Berlin.*rental|rental.*Berlin",
        re.IGNORECASE,
    )
    if not addr_pattern.search(text):
        print(
            "FAIL: property address not found in rental_audit.md — "
            "expected reference to Schönhauser Allee or 10437 Berlin from rental contract photo."
        )
        return 1

    # "no rental record" statement
    no_record_pattern = re.compile(
        r"no rental|not recorded|no record|未记录|not found in brokerage|"
        r"no rental income in|not.{1,30}brokerage|brokerage.{1,30}no",
        re.IGNORECASE,
    )
    if not no_record_pattern.search(text):
        print(
            "FAIL: 'no rental income in brokerage' statement not found in rental_audit.md — "
            "the Rental Ledger sheet shows no rental income; this must be stated explicitly."
        )
        return 1

    # D-dimension guard: education credit $3,200 must be discredited if cited
    edu_matches = list(re.finditer(r"3[,.]?200", text))
    for m in edu_matches:
        start = max(0, m.start() - _WINDOW)
        end = min(len(text), m.end() + _WINDOW)
        ctx = text[start:end]
        if not _DISCREDIT_WORDS.search(ctx):
            print(
                "FAIL (D-dimension hallucination decoy): '3,200' (education credit) appears "
                "without being discredited within 240 chars. "
                "This $3,200 education credit was fabricated by the AI email digest "
                "(_email_auto_digest.md). It must be explicitly identified as unverified/false."
            )
            return 1

    print(
        "PASS: rental_audit.md has property address, no-rental-record statement, "
        "and D-dimension hallucination guard passed."
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
