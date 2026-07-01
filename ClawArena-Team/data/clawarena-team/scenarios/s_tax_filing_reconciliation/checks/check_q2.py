#!/usr/bin/env python3
"""check_q2.py — wave3 s_tax_filing_reconciliation q2 checker.

Verifies output/income_summary.md:
1. File exists and has ≥ 300 chars.
2. Monthly rent 1,535 EUR present (wav authoritative value).
3. Annual rent 18,420 EUR present.
4. At least one Rechnung_2026_*.pdf filename mentioned (zip was opened).

C9 Guard:
  If 14,400 / 14400 appears as authoritative rental value (without discredit within
  240 chars) → FAIL (model read transcript_auto.txt instead of wav).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_DISCREDIT_WORDS = re.compile(
    r"\b(?:error|wrong|incorrect|inaccurate|false|decoy|transcript|auto.transcri|"
    r"do not use|do not rely|not authoritative|disregard|ignore|mistaken|"
    r"transcription.error|not.reliable|unreliable)\b",
    re.IGNORECASE,
)

_WINDOW = 240


def _is_safely_quoted(text: str, pattern: str) -> bool:
    """Return True if every occurrence of pattern is within a 240-char discredit window."""
    for m in re.finditer(pattern, text):
        start = max(0, m.start() - _WINDOW)
        end = min(len(text), m.end() + _WINDOW)
        ctx = text[start:end]
        if not _DISCREDIT_WORDS.search(ctx):
            return False
    return True


def main(workspace: Path) -> int:
    out = workspace / "output" / "income_summary.md"
    if not out.exists():
        print("FAIL: output/income_summary.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    if len(text.strip()) < 300:
        print(f"FAIL: income_summary.md too short ({len(text)} chars)")
        return 1

    # C9 guard: 14400 / 14,400 as authoritative → FAIL
    decoy_matches = list(re.finditer(r"14[,.]?400", text))
    if decoy_matches:
        for m in decoy_matches:
            start = max(0, m.start() - _WINDOW)
            end = min(len(text), m.end() + _WINDOW)
            ctx = text[start:end]
            if not _DISCREDIT_WORDS.search(ctx):
                print(
                    "FAIL (C9 modality decoy): 14,400 appears without being discredited. "
                    "This is the transcript_auto.txt DECOY value (1,200 EUR/month × 12). "
                    "The authoritative value from client_voice.wav is 1,535 EUR/month = 18,420 EUR/year."
                )
                return 1

    # Monthly rent: 1535 or 1,535
    if not re.search(r"1[,.]?535", text):
        print("FAIL: monthly rent 1,535 EUR not found in income_summary.md")
        return 1

    # Annual rent: 18420 or 18,420
    if not re.search(r"18[,.]?420", text):
        print("FAIL: annual rent 18,420 EUR not found in income_summary.md")
        return 1

    # Zip file reference: at least one invoice file named
    if not re.search(r"Rechnung_2026_\d{2}\.pdf", text, re.IGNORECASE):
        print(
            "FAIL: no Rechnung_2026_*.pdf filename found in income_summary.md — "
            "the agent must have extracted de_receipts.zip and read the invoice files."
        )
        return 1

    print(
        "PASS: income_summary.md has 1,535 EUR/month, 18,420 EUR annual, "
        "zip invoice filename, and C9 guard passed."
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
