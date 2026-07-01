"""check_q3.py — q3_competitor_threats.md lists exactly three current-profile competitors.

Ground truth (from market_intel/_index.md, reference date 2026-05):
  Current profiles (last updated >= 2025-12-01, within ~6 months):
    - Steerline Insights       (2026-01-19) — low-latency ingest
    - Meridian Telemetry       (2025-12-08) — compliance certification
    - SkyDeck Data Ops         (2026-02-04) — transparent pricing
    - AtlasView                (2026-01-10) — vertical SI relationships

  Stale profiles (older than 6 months relative to 2026-05 — MUST NOT drive top-3 pick):
    - Omniscope Cloud          (2025-10-02)
    - Pulsewave Analytics      (2025-11-14)
    - ClearSight Observability (2024-03-21)  ← hardest trap (2 years stale)
    - LumenPath                (2025-09-30)

Pass conditions:
  1. File exists, >= 300 chars.
  2. At least 3 of the 4 current competitor names appear.
  3. None of the 4 stale competitor names appear as a top-3 pick.
     Exception (discredit window): stale name is OK only if flagged within 80 chars
     with explicit exclusion language (stale / outdated / skipped / dropped /
     no longer current / older than six months / excluded). A bare copied date
     (e.g. the profile's own "Last updated 2025-11-14") does NOT count.
  4. A differentiator keyword appears: ingest / pricing / compliance / vertical /
     certification / SaaS / integration.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

CURRENT_COMPETITORS: list[str] = [
    "Steerline Insights",
    "Meridian Telemetry",
    "SkyDeck Data Ops",
    "AtlasView",
]

STALE_COMPETITORS: list[str] = [
    "Omniscope Cloud",
    "Pulsewave Analytics",
    "ClearSight Observability",
    "LumenPath",
]

# Discredit must reflect a genuine exclusion judgement ("stale / outdated /
# skipped / dropped"), NOT a bare date. The earlier pattern matched bare years
# and 2025-MM tokens, so a model that wrongly picked a stale competitor and
# copied its own "Last updated 2025-11-14" date would have that date satisfy the
# discredit window — masking the over-pick. Bare dates are removed; only explicit
# exclusion language counts.
DISCREDIT_RE = re.compile(
    r"stale|outdated|out\s+of\s+date|skipp?ed|skip|old\s+profile|too\s+old"
    r"|no\s+longer\s+current|not\s+current|de[- ]?priorit|dropped?|drop"
    r"|exclud|omit|disregard|ignore[d]?|more\s+than\s+six\s+months"
    r"|over\s+six\s+months|older\s+than\s+six\s+months|>\s*6\s*months"
    r"|past\s+six\s+months|dismiss",
    re.IGNORECASE,
)

DIFFERENTIATOR_KW = re.compile(
    r"ingest|pricing|compliance|vertical|certification|SaaS|integration|"
    r"low[- ]latency|transparent",
    re.IGNORECASE,
)


def _stale_safely_discredited(name: str, text: str) -> bool:
    """Return True if every occurrence of the stale competitor name is within
    80 chars of a discredit phrase."""
    lower_name = name.lower()
    lower_text = text.lower()
    idx = 0
    found_any = False
    while True:
        i = lower_text.find(lower_name, idx)
        if i < 0:
            break
        found_any = True
        window = text[max(0, i - 80): i + len(name) + 80]
        if not DISCREDIT_RE.search(window):
            return False
        idx = i + 1
    return found_any  # True only if found and all occurrences are discredited.


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q3.py <workspace>", file=sys.stderr)
        return 1
    ws = Path(sys.argv[1])
    note = ws / "output" / "notes" / "q3_competitor_threats.md"
    if not note.exists():
        print(f"FAIL: {note} does not exist")
        return 1
    text = note.read_text(encoding="utf-8")
    lower = text.lower()
    errors: list[str] = []

    if len(text.strip()) < 300:
        errors.append("q3_competitor_threats.md too short (< 300 chars)")

    current_hit = [c for c in CURRENT_COMPETITORS if c.lower() in lower]
    if len(current_hit) < 3:
        errors.append(
            f"only {len(current_hit)} current competitor(s) named "
            f"({current_hit}); need >= 3 from {CURRENT_COMPETITORS}"
        )

    for name in STALE_COMPETITORS:
        if name.lower() in lower:
            if not _stale_safely_discredited(name, text):
                errors.append(
                    f"stale competitor '{name}' cited without flagging the profile as "
                    f"outdated — profiles older than 6 months should not drive the top-3 "
                    f"pick; explicitly dismiss or omit."
                )

    if not DIFFERENTIATOR_KW.search(text):
        errors.append(
            "no differentiator keyword found "
            "(ingest / pricing / compliance / vertical / certification / SaaS / integration)"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1
    print("PASS: q3_competitor_threats.md picks three current-profile competitors with differentiators; no stale profiles drive the pick")
    return 0


if __name__ == "__main__":
    sys.exit(main())
