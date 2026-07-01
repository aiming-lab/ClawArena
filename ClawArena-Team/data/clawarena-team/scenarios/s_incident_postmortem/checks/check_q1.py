"""check_q1.py — verify output/notes/q1_scope.md captures the incident scope.

Required anchors (all four must be present; case-insensitive):
  (a) Time window  — any 14:1x or 14:2x timestamp in the file.
  (b) Services     — at least 3 distinct names from the candidate set
                     {payments-api, orders-api, redis-fleet-2, shipments,
                      postgres-primary, auth-edge}.
  (c) Initial blame — at least one of: cache / eviction / redis  (the
                      wrong attribution the bench wants surfaced).
  (d) Severity / scope — at least one of: sev / severity / sev-2 / sev2 /
                          degraded / degradation / outage / incident /
                          impacted / affected / customers / users.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SERVICE_CANDIDATES = (
    "payments-api",
    "orders-api",
    "redis-fleet-2",
    "shipments",
    "postgres-primary",
    "auth-edge",
)

WINDOW_RE = re.compile(r"14:[12]\d", re.IGNORECASE)

INITIAL_BLAME_RE = re.compile(r"\b(cache|eviction|redis)\b", re.IGNORECASE)

SCOPE_RE = re.compile(
    r"\b(sev[- ]?2|sev[- ]?[0-9]|severity|degraded|degradation|outage|incident"
    r"|impacted|affected|customer|user)\b",
    re.IGNORECASE,
)

MIN_SERVICES = 3


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q1.py <workspace>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    note = ws / "output" / "notes" / "q1_scope.md"
    if not note.exists():
        print(f"FAIL: {note} does not exist")
        return 1

    text = note.read_text(encoding="utf-8")
    errors: list[str] = []

    if len(text.strip()) < 80:
        errors.append(f"q1_scope.md is too short ({len(text.strip())} chars)")

    # (a) time window
    if not WINDOW_RE.search(text):
        errors.append(
            "no time-window anchor found — expected a timestamp like '14:14' or "
            "'14:23' (14:1x or 14:2x) to mark the degradation window"
        )

    # (b) services — at least 3 distinct
    services_hit = sum(1 for s in SERVICE_CANDIDATES if s.lower() in text.lower())
    if services_hit < MIN_SERVICES:
        errors.append(
            f"only {services_hit} service name(s) from the candidate set mentioned "
            f"(need >= {MIN_SERVICES} from {SERVICE_CANDIDATES})"
        )

    # (c) initial blame
    if not INITIAL_BLAME_RE.search(text):
        errors.append(
            "no initial-blame anchor found — expected at least one of: "
            "cache / eviction / redis (on-call's original hypothesis)"
        )

    # (d) severity / scope
    if not SCOPE_RE.search(text):
        errors.append(
            "no severity/scope anchor found — expected at least one of: "
            "sev-2, degraded, outage, incident, impacted, affected, customers, users"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        "PASS: q1_scope.md captures window, >=3 services, initial blame, and severity"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
