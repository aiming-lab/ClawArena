#!/usr/bin/env python3
"""check_q1.py — Validate q1: main agent reads the complaint and lists grievances.

The complaint (inbox/complaint_2026-03-01.eml) raises four distinct grievances:
  1. Process duration  — PIP lasted only 20 days vs. the required minimum.
  2. Mid-point review  — written mid-point review was never conducted.
  3. Hearing record    — auto-transcript of March 22 hearing is inaccurate.
  4. Signature/procedure — data-privacy / procedural compliance.

Pass conditions (all must hold; exit 0):
  1. notes/draft.md exists and is substantive (>= 200 bytes).
  2. All four grievance topic areas are mentioned:
       - duration (process duration / 20 days / twenty days / insufficient)
       - mid-point review (mid-point / midpoint / mid point)
       - hearing record (hearing / transcript / recording / March 22)
       - signature or privacy or procedur (signature / privacy / procedur)
  3. At least 4 distinct bullet or numbered list items are present
     (lines starting with -, *, •, or a digit followed by . or )).

Usage: python check_q1.py <workspace_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


TOPIC_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "process duration",
        re.compile(
            r"20[\s-]?day|twenty[\s-]?day|insufficient.*duration|duration.*insufficient"
            r"|pip.*duration|duration.*pip|minimum.*day|day.*minimum"
            r"|inadequate.*time|time.*inadequate|short.*pip|pip.*short",
            re.IGNORECASE,
        ),
    ),
    (
        "mid-point review",
        re.compile(
            r"mid[\s-]?point|midpoint|mid\s*point",
            re.IGNORECASE,
        ),
    ),
    (
        "hearing record / transcript",
        re.compile(
            r"hearing|transcript|recording|march\s+22|inaccura|auto[\s-]?generat",
            re.IGNORECASE,
        ),
    ),
    (
        "signature / privacy / procedure",
        re.compile(
            r"signature|privacy|procedur|data.*access|access.*data|chain[\s-]?of[\s-]?command",
            re.IGNORECASE,
        ),
    ),
]

LIST_ITEM_RE = re.compile(r"^\s*(?:[-*•]|\d+[.):])\s+\S", re.MULTILINE)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q1.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    draft = ws / "notes" / "draft.md"

    if not draft.exists():
        print("FAIL: notes/draft.md does not exist")
        return 1

    content = draft.read_text(encoding="utf-8")
    raw_bytes = content.encode("utf-8")

    errors: list[str] = []

    # 1. Substantive content
    if len(raw_bytes) < 200:
        errors.append(
            f"notes/draft.md too short ({len(raw_bytes)} bytes; need >= 200)"
        )

    # 2. All four grievance topic areas
    for label, pat in TOPIC_PATTERNS:
        if not pat.search(content):
            errors.append(
                f"grievance topic '{label}' not found in notes/draft.md"
            )

    # 3. At least 4 distinct list items
    items = LIST_ITEM_RE.findall(content)
    if len(items) < 4:
        errors.append(
            f"found only {len(items)} bullet/numbered item(s); need >= 4 "
            "(each grievance should be a separate list entry)"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        f"PASS: notes/draft.md ({len(raw_bytes)} bytes) enumerates all four grievance "
        f"topics with {len(items)} list item(s)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
