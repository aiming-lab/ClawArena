"""check_q5.py — q5_repositioning.md surfaces the Apex Cloud surprise and pivots
to historical-context depth as the durable advantage.

Pass conditions:
  1. File exists, >= 200 chars.
  2. Names 'Apex Cloud' (the new competitor).
  3. Names the overlapping feature: 'real-time correlation' OR 'correlation engine'.
  4. Carries the durable-advantage anchor (regex: durable|enduring|defensible|moat
     OR 'historical context' OR '18-month' OR 'depth of context' OR 'rolling window').
  5. Proposes a sharpened positioning sentence that includes the analytics number
     from round 4 — extracted live from q4_analytics_anchor.md (cross-round closure):
     the number in q5_repositioning.md must match the number used in
     q4_analytics_anchor.md (accepting ±0 tolerance for the leading value).
  6. Must reference a customer-evidence anchor: 'BlueRidge' OR 'MTTD' OR '94%'.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

APEX = re.compile(r"apex\s*cloud", re.IGNORECASE)
OVERLAP = re.compile(r"real[- ]time\s+correlation|correlation\s+engine", re.IGNORECASE)
DURABLE = re.compile(
    r"durable|enduring|defensible|moat|"
    r"historical\s+context|18[- ]?month|depth\s+of\s+context|rolling\s+window",
    re.IGNORECASE,
)
CUSTOMER_EVIDENCE = re.compile(r"blueridge|mttd|94\s*%", re.IGNORECASE)

# Extract numeric anchor from q4_analytics_anchor.md: prefer numbers paired with '%',
# then fall back to a number >= 22 that is not a year.
_Q4_NUMBER_PCT_RE = re.compile(r"\b(\d{2,3})\s*%")
_Q4_NUMBER_FALLBACK_RE = re.compile(r"\b([2-9][0-9]|100)\b")
# Must see same number in q5
_NUMBER_IN_TEXT_RE = re.compile(r"\b(\d{2,3})\b")


def _extract_q4_anchor(ws: Path) -> int | None:
    """Extract the leading numeric anchor from q4_analytics_anchor.md.

    Prefer a number explicitly paired with '%' (e.g. '98%'), then fall back
    to the first two-digit number >= 20 that is not a year (1900-2099).
    """
    q4 = ws / "output" / "notes" / "q4_analytics_anchor.md"
    if not q4.exists():
        return None
    text = q4.read_text(encoding="utf-8")
    # Preferred: explicit percent value.
    for m in _Q4_NUMBER_PCT_RE.finditer(text):
        n = int(m.group(1))
        if 10 <= n <= 100:
            return n
    # Fallback: first two-digit number that is clearly not a year.
    for m in _Q4_NUMBER_FALLBACK_RE.finditer(text):
        n = int(m.group(1))
        if not (1900 <= n <= 2099):
            return n
    return None


def _numbers_in_text(text: str) -> list[int]:
    return [int(m.group(1)) for m in _NUMBER_IN_TEXT_RE.finditer(text)]


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q5.py <workspace>", file=sys.stderr)
        return 1
    ws = Path(sys.argv[1])
    note = ws / "output" / "notes" / "q5_repositioning.md"
    if not note.exists():
        print(f"FAIL: {note} does not exist")
        return 1
    text = note.read_text(encoding="utf-8")
    errors: list[str] = []

    if len(text.strip()) < 200:
        errors.append("q5_repositioning.md too short (< 200 chars)")
    if not APEX.search(text):
        errors.append("does not name the new competitor 'Apex Cloud'")
    if not OVERLAP.search(text):
        errors.append(
            "does not name the overlapping feature "
            "('real-time correlation' / 'correlation engine')"
        )
    if not DURABLE.search(text):
        errors.append(
            "does not anchor on the durable advantage "
            "('durable' / 'enduring' / 'defensible' / 'moat' / "
            "'historical context' / '18-month' / 'rolling window')"
        )
    if not CUSTOMER_EVIDENCE.search(text):
        errors.append(
            "does not reference customer-evidence anchor "
            "('BlueRidge' / 'MTTD' / '94%')"
        )

    # Cross-round closure: analytics number in q5 must match q4.
    q4_num = _extract_q4_anchor(ws)
    if q4_num is None:
        errors.append(
            "could not read analytics anchor from q4_analytics_anchor.md "
            "for cross-round closure check"
        )
    else:
        q5_nums = _numbers_in_text(text)
        if q4_num not in q5_nums:
            errors.append(
                f"analytics anchor number from round 4 ({q4_num}) does not appear "
                f"in q5_repositioning.md (found: {q5_nums[:8]}); "
                "the sharpened positioning sentence must be anchored to the q4 metric"
            )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1
    print("PASS: q5_repositioning.md names Apex Cloud + overlap + durable advantage, cross-round analytics anchor matches, and customer-evidence present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
