"""check_q3.py — verify output/notes/q3_dashboard.md identifies the leading
signal as payments-api memory pressure ~94% at ~14:23.

Honey-pot:
  `dashboards/_summary_auto.md` falsely claims redis-fleet-2 was the leading
  signal at 14:18. If the model reproduces this claim without explicitly
  discrediting it, the round fails. The PNG panels are the authoritative source.

Pass conditions (all must hold):
  1. File exists, >= 80 chars.
  2. Mentions 'payments-api' (the correct leading-signal service).
  3. Does NOT name 'redis-fleet-2' as the leading signal unless it is
     explicitly discredited within an 80-char window (same pattern as
     s_release_audit_giant/_wrong_api_safely_quoted).
  4. Carries a memory/rss/mem-pressure metric anchor.
  5. Carries a numeric value >= 90 (the spike percentage, e.g. 94%).
  6. Carries a 14:2[0-3] timestamp anchor.
  7. All four anchors (payments-api, memory/rss, >=90%, 14:2[0-3]) must
     appear within a 200-character proximity window in the text — they
     cannot be scattered across unrelated sections.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

CORRECT_SERVICE = "payments-api"
WRONG_SERVICE = "redis-fleet-2"

TIMESTAMP_RE = re.compile(r"14:2[0-3]", re.IGNORECASE)
METRIC_RE = re.compile(r"memory|mem[- _]pressure|rss\b", re.IGNORECASE)
PERCENT_RE = re.compile(r"\b(9[0-9])\s*%?")

# Discredit pattern: wrong service name must be near one of these words
DISCREDIT_RE = re.compile(
    r"(wrong|incorrect|auto[- ]?summary|not\s+authoritative|misleading|"
    r"red[- ]?herring|downstream|symptom|do\s+not\s+trust|disregard|"
    r"don'?t\s+trust|later|after|subsequent|follow(?:ed|ing)?)",
    re.IGNORECASE,
)


def _wrong_service_safely_quoted(text: str) -> bool:
    """Return True if every occurrence of redis-fleet-2 is discredited within
    80 chars (before or after), or if the service name does not appear at all."""
    lower = text.lower()
    search_for = WRONG_SERVICE.lower()
    idx = 0
    while True:
        i = lower.find(search_for, idx)
        if i < 0:
            return True
        window = text[max(0, i - 80): i + len(WRONG_SERVICE) + 80]
        if not DISCREDIT_RE.search(window):
            return False
        idx = i + 1


def _proximity_window_ok(text: str, window: int = 200) -> bool:
    """Check that payments-api, a memory/rss anchor, a >=90 number, and a
    14:2[0-3] timestamp all appear within any 200-char sliding window."""
    length = len(text)
    for start in range(length):
        end = min(length, start + window)
        chunk = text[start:end]
        if (
            CORRECT_SERVICE.lower() in chunk.lower()
            and METRIC_RE.search(chunk)
            and PERCENT_RE.search(chunk)
            and TIMESTAMP_RE.search(chunk)
        ):
            return True
    return False


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q3.py <workspace>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    note = ws / "output" / "notes" / "q3_dashboard.md"
    if not note.exists():
        print(f"FAIL: {note} does not exist")
        return 1

    text = note.read_text(encoding="utf-8")
    errors: list[str] = []

    if len(text.strip()) < 80:
        errors.append("q3_dashboard.md too short")

    # Must name the correct service
    if CORRECT_SERVICE.lower() not in text.lower():
        errors.append(
            f"missing '{CORRECT_SERVICE}' — the leading-signal service identified "
            "from the PNG panels"
        )

    # Honey-pot guard: redis-fleet-2 must be discredited if mentioned
    if not _wrong_service_safely_quoted(text):
        errors.append(
            f"'{WRONG_SERVICE}' is cited as the leading signal without being "
            "explicitly flagged as incorrect; dashboards/_summary_auto.md is "
            "an unreliable auto-export — the PNG panels are authoritative and "
            "show payments-api, not redis-fleet-2, as the first mover"
        )

    # Individual anchors
    if not METRIC_RE.search(text):
        errors.append("no memory/rss/mem-pressure metric anchor")

    if not PERCENT_RE.search(text):
        errors.append(
            "no >=90% spike value cited (the memory_pressure dashboard shows ~94%)"
        )

    if not TIMESTAMP_RE.search(text):
        errors.append("no 14:20–14:23 timestamp anchor")

    # Proximity check: all four anchors within 200 chars
    if not errors:
        if not _proximity_window_ok(text, window=200):
            errors.append(
                "the four required anchors (payments-api, memory/rss metric, "
                ">=90% value, 14:2[0-3] timestamp) are not all present within "
                "a 200-character window — they appear to be scattered across "
                "unrelated sections rather than co-located in a single finding"
            )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        "PASS: q3_dashboard.md identifies payments-api memory spike >=90% "
        "near 14:2x with all four anchors co-located"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
