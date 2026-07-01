"""check_q3.py — Wave3 s_strategy_backtest_review q3 checker.

Verifies output/ratios_audit.md:
1. File exists
2. claimed_sharpe = 2.31 (from notebook HTML + xlsx ratios sheet)
3. cherry-pick: 2022-Q3 mentioned as the omitted/largest-drawdown quarter
4. survivorship_delisted_count = 7 (from voice memo — authoritative audio)
5. xlsx evidence: all 3 sheets mentioned (trades, yearly_summary, ratios)

C9 modality-decoy guard:
- If delisted count = 12 appears without discredit window → FAIL
  (model used transcript_auto.txt decoy instead of wav audio)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


# Delisted / survivorship context words. The delisted-count assertion ('7') and
# the C9 decoy guard ('12') both only fire when the number sits in this context,
# so a stray digit elsewhere in the prose (e.g. a date, a percentage, a Sharpe
# value) cannot satisfy or trip either check.
_DELISTED_CTX = re.compile(
    r"delist|ticker|survivorship|surviv|excluded|filtered.?out|dropped",
    re.IGNORECASE,
)
_CTX_WINDOW = 120


def _has_count_in_delisted_ctx(text: str, count: int) -> bool:
    """Return True iff the bare number ``count`` appears within a window of
    delisted/survivorship-context language (not merely anywhere in the file)."""
    for m in re.finditer(r"\b" + str(count) + r"\b", text):
        start = max(0, m.start() - _CTX_WINDOW)
        end = min(len(text), m.end() + _CTX_WINDOW)
        if _DELISTED_CTX.search(text[start:end]):
            return True
    return False


_DISCREDIT = re.compile(
    r"\b(?:incorrect|wrong|error|inaccurate|"
    r"not.?authoritative|not.?correct|do.?not.?rely|hallucinate|fabricate|"
    r"disregard|ignore|overridden.?by|wav.?is.?authoritative|audio.?says|"
    r"from.?the.?wav|from.?the.?audio|from.?the.?recording|"
    r"transcription.?error|auto.transcript.{0,10}error|"
    r"known.?error|not.?accurate)\b",
    re.IGNORECASE,
)
_WINDOW = 240


# The decoy count appears in the auto-transcript both as the digit '12' and as
# the spelled-out word 'twelve'; the guard must catch either form, otherwise a
# model that copies "twelve delisted tickers" slips past a digit-only matcher.
_DECOY_COUNT_TOKEN = re.compile(r"\b(?:12|twelve)\b", re.IGNORECASE)


def _count_12_safely_quoted(text: str) -> bool:
    """Return True if every '12'/'twelve' in delisted context is discredited."""
    # Only look for the decoy count token adjacent to delisted-context words
    for m in _DECOY_COUNT_TOKEN.finditer(text):
        start = max(0, m.start() - _WINDOW)
        end = min(len(text), m.end() + _WINDOW)
        ctx = text[start:end]
        # Only trigger if the token is near delisted/survivorship language
        if not re.search(r"delist|ticker|survivorship|excluded|filter", ctx, re.IGNORECASE):
            continue
        # decoy count near delisted context: must be discredited
        if not _DISCREDIT.search(ctx):
            return False
    return True


def main(workspace: Path) -> int:
    out = workspace / "output" / "ratios_audit.md"
    if not out.exists():
        print("FAIL: output/ratios_audit.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. claimed_sharpe = 2.31
    if not re.search(r"2\.31", text):
        print("FAIL: claimed Sharpe '2.31' not found in ratios_audit.md")
        return 1

    # 2. cherry-pick: 2022-Q3 mentioned
    if not re.search(r"2022.{0,5}Q3|Q3.{0,5}2022", text, re.IGNORECASE):
        print(
            "FAIL: '2022-Q3' not found in ratios_audit.md. "
            "The audit must identify 2022-Q3 as the omitted/cherry-picked quarter."
        )
        return 1

    # 3. survivorship_delisted_count = 7 (from voice memo)
    #    Must be '7' in delisted/survivorship context, not a bare '7' anywhere
    #    (a date, percentage, or Sharpe digit must NOT satisfy this).
    if not _has_count_in_delisted_ctx(text, 7):
        print(
            "FAIL: delisted count '7' not found in delisted/survivorship context in "
            "ratios_audit.md. The voice memo (researcher_memo.wav) states 7 delisted "
            "tickers. This is the authoritative value — do not rely on the transcript "
            "file. State it next to 'delisted'/'survivorship'/'tickers' language."
        )
        return 1

    # 4. C9 modality-decoy guard: '12' near delisted context without discredit → FAIL
    if not _count_12_safely_quoted(text):
        print(
            "FAIL (C9 modality-decoy guard): ratios_audit.md contains '12'/'twelve' as "
            "the delisted ticker count without discrediting it. "
            "The transcript_auto.txt incorrectly states 12 (twelve) delisted tickers; "
            "the voice memo (wav audio) is authoritative and says 7. "
            "If you cited 12 as the delisted count, you used the wrong source."
        )
        return 1

    # 5. xlsx three sheets evidence: trades + yearly_summary (or yearly) + ratios
    sheet_patterns = {
        "trades": r"trade[s]?|trading.?detail",
        "yearly_summary": r"yearly|annual|year.?by.?year|yearly.?summary",
        "ratios": r"ratios?|ratio.?sheet|sharpe.?ratio.?sheet",
    }
    sheet_hits = [k for k, pat in sheet_patterns.items() if re.search(pat, text, re.IGNORECASE)]
    if len(sheet_hits) < 2:
        print(
            f"FAIL: only {len(sheet_hits)} xlsx sheets referenced (need ≥ 2, ideally 3): "
            f"{sheet_hits}. Must reference trades, yearly_summary, and ratios sheets."
        )
        return 1

    print(
        f"PASS: ratios_audit.md — Sharpe=2.31, 2022-Q3 cherry-pick, "
        f"delisted=7 (audio), xlsx sheets={sheet_hits}, C9 guard OK"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
