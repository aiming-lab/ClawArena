"""check_q4.py — verify output/notes/q4_comms_vs_data.md surfaces the
misattribution: on-call originally blamed redis-fleet-2 / cache eviction,
but dashboards/logs show payments-api was the leading signal.

Required (all must hold):
  1. File exists, >= 80 chars.
  2. Explicitly names redis-fleet-2 (or redis / cache / eviction) as the
     on-call's wrong initial blame target.
  3. Explicitly names payments-api as the actual leading signal from the
     data (dashboards/logs).
  4. Uses reconciliation language showing the two attributions disagreed —
     at least one of: wrong / misattribut / discrepan / mismatch / differ /
     contradict / reverse / downstream / symptom / lesson / misread /
     incorrect / backwards.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ORIGINAL_BLAME_RE = re.compile(
    r"\b(redis(?:[- ]fleet[- ]2)?|cache|eviction)\b", re.IGNORECASE
)
ACTUAL_SIGNAL_RE = re.compile(r"\bpayments[- ]api\b", re.IGNORECASE)
RECONCILE_RE = re.compile(
    r"wrong|misattribut|discrepan|mismatch|differ|contradict|reverse|"
    r"downstream|symptom|lesson|misread|incorrect|backwards",
    re.IGNORECASE,
)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q4.py <workspace>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    note = ws / "output" / "notes" / "q4_comms_vs_data.md"
    if not note.exists():
        print(f"FAIL: {note} does not exist")
        return 1

    text = note.read_text(encoding="utf-8")
    errors: list[str] = []

    if len(text.strip()) < 80:
        errors.append("q4_comms_vs_data.md too short")

    if not ORIGINAL_BLAME_RE.search(text):
        errors.append(
            "does not name the original (mistaken) blame target — "
            "expected redis-fleet-2, redis, cache, or eviction"
        )

    if not ACTUAL_SIGNAL_RE.search(text):
        errors.append(
            "does not name 'payments-api' as the actual leading signal — "
            "the reconciliation must contrast the original blame against the "
            "data (dashboards/logs) which pointed to payments-api"
        )

    if not RECONCILE_RE.search(text):
        errors.append(
            "does not use reconciliation language — expected at least one of: "
            "wrong / misattribution / discrepancy / mismatch / downstream / "
            "symptom / lesson / incorrect / backwards"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        "PASS: q4_comms_vs_data.md names redis/cache as the wrong blame, "
        "payments-api as the actual signal, and uses reconciliation language"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
