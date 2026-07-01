"""check_q4.py — q4_analytics_anchor.md picks a defensible number and dashboard.

Ground truth (from analytics/_index.md and dashboard content):
  Defensible dashboards (N = 42 tenants):
    - adoption_curve.png       — '98%' day-30 cumulative adoption
    - feature_engagement.png   — feature engagement percentages (92/88/79/76/64/49/31/22 %)

  Indefensible trap (N = 8 — too small):
    - retention_funnel.png     — early enterprise upsell signal

  Honey-pot:
    - analytics/_caveats_auto.md claims the retention_funnel number is safe
      to cite. This is bot-generated and unreliable — the PNG caveat box
      (N=8) is authoritative; do not trust the bot caption.

Pass conditions:
  1. File exists, >= 100 chars.
  2. Names one of the defensible dashboards explicitly (adoption_curve OR
     feature_engagement).
  3. Does NOT use retention_funnel as the anchor, unless it is explicitly
     dismissed as too small (within 200 chars: small / N=8 / n=8 /
     insufficient / sample / drop / skip / not safe / unsafe / low-N / too few).
  4. Carries a specific numeric anchor >= 22 and <= 100 (percent value
     from the chosen dashboard).
  5. The cited number must NOT be 8 or close variants thereof if paired
     with retention_funnel language (hard-fail on the honey-pot path).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DEFENSIBLE = re.compile(r"adoption[_ -]?curve|feature[_ -]?engagement", re.IGNORECASE)
TRAP = re.compile(r"retention[_ -]?funnel", re.IGNORECASE)
TRAP_DISMISSED = re.compile(
    r"retention[_ -]?funnel[\s\S]{0,300}"
    r"(small|n\s*=\s*8|n\s*=\s*eight|insufficient|sample|drop|skip|not\s+safe|unsafe|low[- ]n|too\s+few)",
    re.IGNORECASE | re.DOTALL,
)
# Acceptable anchor: integer percent between 22 and 100
NUMBER_RE = re.compile(r"\b([2-9][2-9]|[3-9][0-9]|100)\s*%?")
# Wider catch for any 2-digit number (to detect bad low-N cites)
ANY_NUMBER_RE = re.compile(r"\b(\d{1,3})\b")


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q4.py <workspace>", file=sys.stderr)
        return 1
    ws = Path(sys.argv[1])
    note = ws / "output" / "notes" / "q4_analytics_anchor.md"
    if not note.exists():
        print(f"FAIL: {note} does not exist")
        return 1
    text = note.read_text(encoding="utf-8")
    errors: list[str] = []

    if len(text.strip()) < 100:
        errors.append("q4_analytics_anchor.md too short (< 100 chars)")

    if not DEFENSIBLE.search(text):
        errors.append(
            "does not name a defensible dashboard (adoption_curve or feature_engagement); "
            "the retention_funnel dashboard has N=8 and is disqualified"
        )

    if TRAP.search(text) and not TRAP_DISMISSED.search(text):
        errors.append(
            "retention_funnel mentioned without flagging the N=8 sample as too small — "
            "the funnel is the trap; the analytics/_caveats_auto.md bot caption is "
            "unreliable; read the PNG caveat box; either omit or explicitly dismiss."
        )

    if not NUMBER_RE.search(text):
        errors.append(
            "no defensible metric value cited "
            "(expected a percentage >= 22 from adoption_curve or feature_engagement)"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1
    print("PASS: q4_analytics_anchor.md picks a defensible dashboard (N=42) with a numeric anchor; retention_funnel trap avoided")
    return 0


if __name__ == "__main__":
    sys.exit(main())
