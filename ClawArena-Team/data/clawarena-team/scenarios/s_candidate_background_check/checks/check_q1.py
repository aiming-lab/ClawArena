#!/usr/bin/env python3
"""check_q1.py — Validate q1: intake note enumerating the four evidence channels.

The diligence brief (requests/diligence_brief.md) and candidate intake email
(requests/candidate_intake.eml) surface four evidence channels and several
pre-flagged concerns. The agent must write output/intake_note.md listing all of them.

Pass conditions (all must hold; exit 0):
  Layer 1 — Structure:
    1. output/intake_note.md exists.
    2. >= 300 bytes.
    3. >= 4 distinct list items (lines starting with -, *, •, or digit followed by . or )).
  Layer 2 — Field presence:
    4. Evidence channel: resume / cover letter / cover email.
    5. Evidence channel: LinkedIn / screenshot / profile.
    6. Evidence channel: GitHub / commit log / repository.
    7. Evidence channel: audio / reference call / phone call / recording.
    8. Deadline: 48-hour / 48 hour.
  Layer 3 — Anti-decoy:
    9. File must NOT contain "pii/" or "compensation_benchmarks" (task-irrelevant paths).

Usage: python check_q1.py <workspace_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


LIST_ITEM_RE = re.compile(r"^\s*(?:[-*•]|\d+[.):])\s+\S", re.MULTILINE)

CHANNEL_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "resume / cover letter",
        re.compile(r"resume|cover[\s-]?letter|cover[\s-]?email", re.IGNORECASE),
    ),
    (
        "LinkedIn / screenshot / profile",
        re.compile(r"[Ll]inked[Ii]n|screenshot|profile", re.IGNORECASE),
    ),
    (
        "GitHub / commit log",
        re.compile(r"[Gg]it[Hh]ub|commit[\s-]?log|repositor", re.IGNORECASE),
    ),
    (
        "audio / reference call",
        re.compile(r"audio|reference[\s-]?call|phone[\s-]?call|recording", re.IGNORECASE),
    ),
]

DEADLINE_RE = re.compile(r"48[\s-]?h(?:our)?", re.IGNORECASE)

DECOY_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("pii/ path", re.compile(r"\bpii/", re.IGNORECASE)),
    ("compensation_benchmarks", re.compile(r"compensation_benchmarks", re.IGNORECASE)),
]


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q1.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    target = ws / "output" / "intake_note.md"

    if not target.exists():
        print("FAIL: output/intake_note.md does not exist")
        return 1

    content = target.read_text(encoding="utf-8")
    raw_bytes = content.encode("utf-8")
    errors: list[str] = []

    # Layer 1: structure
    if len(raw_bytes) < 300:
        errors.append(
            f"output/intake_note.md too short ({len(raw_bytes)} bytes; need >= 300)"
        )

    items = LIST_ITEM_RE.findall(content)
    if len(items) < 4:
        errors.append(
            f"found only {len(items)} list item(s); need >= 4 "
            "(each evidence channel and concern should be a separate bullet or numbered item)"
        )

    # Layer 2: field presence
    for label, pat in CHANNEL_PATTERNS:
        if not pat.search(content):
            errors.append(f"evidence channel '{label}' not found in output/intake_note.md")

    if not DEADLINE_RE.search(content):
        errors.append("the 48-hour deadline is not mentioned in output/intake_note.md")

    # Layer 3: anti-decoy
    for label, pat in DECOY_PATTERNS:
        if pat.search(content):
            errors.append(
                f"output/intake_note.md references '{label}' — this path is "
                "task-irrelevant and indicates the agent read files outside the brief scope"
            )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        f"PASS: output/intake_note.md ({len(raw_bytes)} bytes) enumerates all four "
        f"evidence channels, the 48-hour deadline, with {len(items)} list item(s); "
        "no decoy path contamination detected"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
