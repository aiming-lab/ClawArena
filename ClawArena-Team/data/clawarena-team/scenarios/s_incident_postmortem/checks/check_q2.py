"""check_q2.py — verify output/notes/q2_first_error.md identifies payments-api
as the first-error service at 14:23 and explicitly states the cache-eviction
story is downstream.

Required (all must hold):
  1. File exists, >= 80 chars.
  2. Mentions 'payments-api' (the actual first-error service).
  3. Carries a first-error timestamp anchor matching 14:23 at second-level
     precision (14:23:[0-5][0-9]) OR the bare form '14:23'. The first
     incident-relevant ERROR in payments-api lands in the 14:23 minute
     (first [ERROR] at 14:23:29; the memory_pressure/oom_kill ERRORs at
     14:23:42–14:23:54). There are ZERO ERROR lines at 14:21 (only normal
     200-status WARNs), so '14:21' is NOT a valid anchor — the question's
     'e.g. 14:21:08' is only a format example, not the answer.
  4. The redis / cache / eviction story must be explicitly framed as
     downstream / symptom / not-the-cause — checked via a proximity
     co-occurrence within ~160 chars.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Require specifically 14:23 (with optional seconds) — the minute of the first
# payments-api ERROR / memory-pressure-onset. 14:21 carries no ERROR lines.
TIMESTAMP_FIRST_ERROR_RE = re.compile(r"14:23(?::[0-5][0-9])?(?!\d)", re.IGNORECASE)

# Downstream framing: redis/cache/eviction near a not-the-cause qualifier.
#
# The vocabulary is deliberately tightened so it fires ONLY on language that
# genuinely asserts the cache story is a symptom / downstream / not-the-cause.
# Earlier revisions accepted bare generic words (a lone temporal "after",
# "secondary", "consequence", "aftermath", bare "later"/"subsequent", generic
# "trail"), which let decoy prose pass — e.g. "we restarted the redis cache
# AFTER the on-call paged us", "the redis cache is our SECONDARY store", or
# "checked the cache; as a CONSEQUENCE we looked at logs". Those describe a
# benign temporal/structural relationship, not a downstream-symptom framing.
#
# Tokens that imply ordering ("after", "follow", "result", "caused", "triggered")
# are now bound to the real causal object (payments / memory / OOM / mem pressure)
# so they cannot be satisfied by an unrelated "after the page" clause.
_FRAME = (
    r"downstream"
    r"|symptom"
    r"|not\s+the\s+(?:cause|root\s*cause|root|trigger)"
    r"|not\s+first"
    r"|does\s+not\s+hold(?:\s+up)?"
    r"|did\s+not\s+hold(?:\s+up)?"
    r"|side[- ]effect"
    r"|after[- ]?effect"
    r"|misattribut"
    r"|incorrect"
    r"|\bwrong\b"
    r"|consequence\s+of"
    r"|secondary\s+(?:to|effect)"
    r"|follow(?:ed|ing|s)?\s+(?:from\s+)?(?:the\s+)?(?:payments|memory|oom|mem(?:ory)?\s*pressure)"
    r"|caused\s+by\s+(?:payments|memory|the\s+memory|the\s+oom|oom|mem)"
    r"|triggered\s+by\s+(?:payments|memory|the\s+memory|the\s+oom|oom)"
    r"|result(?:ed|ing|s)?\s+(?:from|of)\s+(?:the\s+)?(?:payments|memory|oom|mem)"
)
DOWNSTREAM_FRAME_RE = re.compile(
    r"(?:redis|cache|eviction)[^.]{0,160}(?:" + _FRAME + r")"
    r"|"
    r"(?:" + _FRAME + r")[^.]{0,160}(?:redis|cache|eviction)",
    re.IGNORECASE,
)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q2.py <workspace>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    note = ws / "output" / "notes" / "q2_first_error.md"
    if not note.exists():
        print(f"FAIL: {note} does not exist")
        return 1

    text = note.read_text(encoding="utf-8")
    errors: list[str] = []

    if len(text.strip()) < 80:
        errors.append("q2_first_error.md too short")

    # payments-api must be named
    if "payments-api" not in text.lower():
        errors.append("missing 'payments-api' (the actual first-error service)")

    # Must carry a 14:23 timestamp specifically
    if not TIMESTAMP_FIRST_ERROR_RE.search(text):
        errors.append(
            "no 14:23 timestamp anchor found — the first incident-relevant ERROR "
            "in payments-api is at 14:23 (14:23:29 first [ERROR]; oom_kill at "
            "14:23:42); 14:21 carries no ERROR lines"
        )

    # Must address redis/cache/eviction AND frame it as downstream
    if (
        "redis" not in text.lower()
        and "cache" not in text.lower()
        and "eviction" not in text.lower()
    ):
        errors.append(
            "does not address the cache/redis/eviction theory at all — the note "
            "must state whether it holds up against the log evidence"
        )
    elif not DOWNSTREAM_FRAME_RE.search(text):
        errors.append(
            "addresses redis/cache/eviction but does not explicitly frame it as "
            "downstream / symptom / not-the-cause; the note must state that the "
            "cache story does not hold up as the primary cause"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        "PASS: q2_first_error.md identifies payments-api at 14:23 as first-error "
        "service and frames the cache story as downstream"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
