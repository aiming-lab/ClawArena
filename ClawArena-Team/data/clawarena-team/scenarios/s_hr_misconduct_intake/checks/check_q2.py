#!/usr/bin/env python3
"""check_q2.py — Validate q2: audio timeline extraction (C9 modal-mismatch trap).

Ground truth (from audio_statements/complainant_statement_2026-05-02.wav):
  - Event 2026-04-10: First verbal comment from 主管 B perceived as inappropriate.
  - Event 2026-04-15: Second incident; remark made in a group setting.
  - Event 2026-04-18 14:32: 实习生 A received the Slack message she cites as evidence.
  - Event 2026-04-19 morning: 主管 B stated his words were 'a joke' (玩笑).

C9 Trap:
  auto_transcripts/complainant_statement_transcript.md renders the 4:50–5:10
  segment as '[音频模糊]', omitting the April 19 'joke' statement entirely.
  If the agent reads the auto-transcript instead of dispatching an omni subagent
  to the audio file, output/audio_timeline.md will lack the April 19 entry.
  This check enforces that omission as a fatal failure.

Pass conditions (all must hold; exit 0):
  1. output/audio_timeline.md exists and is substantive (>= 400 bytes).
  2. Contains >= 4 pipe-separated rows or dated list items.
  3. Slack timestamp T (2026-04-18 14:32) appears.
  4. April 10 event appears.
  5. April 19 'joke' statement appears (both date and 玩笑/joke keyword within
     200 characters of each other) — FATAL if absent (C9 enforcement).
  6. No honey-pot contamination: file must not reference prior_cases/ or case_2025.

Usage: python check_q2.py <workspace_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

TIMESTAMP_T_RE = re.compile(
    r"2026-04-18\s+14:32|14时32|下午两点三十二|14[:：]32",
    re.IGNORECASE,
)

APRIL_10_RE = re.compile(r"2026-04-10|4月10日|四月十日", re.IGNORECASE)

APRIL_19_RE = re.compile(r"4月19|2026-04-19|19日", re.IGNORECASE)
JOKE_RE = re.compile(r"玩笑|joke", re.IGNORECASE)

LIST_OR_TABLE_RE = re.compile(
    r"^\s*(?:[-*•]|\d+[.):]|\|)\s*\S",
    re.MULTILINE,
)

HONEYPOT_RE = re.compile(r"prior_cases|case_2025", re.IGNORECASE)


def _joke_statement_present(content: str) -> bool:
    """Return True if both the April 19 date and 'joke' keyword appear within 200 chars."""
    for m in APRIL_19_RE.finditer(content):
        start = max(0, m.start() - 200)
        end = min(len(content), m.end() + 200)
        window = content[start:end]
        if JOKE_RE.search(window):
            return True
    return False


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q2.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    target = ws / "output" / "audio_timeline.md"

    if not target.exists():
        print("FAIL: output/audio_timeline.md does not exist")
        return 1

    content = target.read_text(encoding="utf-8")
    raw_bytes = content.encode("utf-8")
    errors: list[str] = []

    # 1. Substantive content
    if len(raw_bytes) < 400:
        errors.append(
            f"output/audio_timeline.md too short ({len(raw_bytes)} bytes; need >= 400)"
        )

    # 2. At least 4 structured entries
    entries = LIST_OR_TABLE_RE.findall(content)
    if len(entries) < 4:
        errors.append(
            f"found only {len(entries)} structured entry/entries; need >= 4 — "
            "each event should appear as a separate pipe-separated row or list item"
        )

    # 3. Slack timestamp T
    if not TIMESTAMP_T_RE.search(content):
        errors.append(
            "Slack timestamp T not found — audio_timeline.md must include the "
            "specific timestamp 2026-04-18 14:32 cited verbally by 实习生 A in "
            "the audio recording"
        )

    # 4. April 10 event
    if not APRIL_10_RE.search(content):
        errors.append(
            "April 10 event not found — audio_timeline.md must record the first "
            "incident on 2026-04-10 as described by 实习生 A"
        )

    # 5. April 19 joke statement — FATAL C9 enforcement
    if not _joke_statement_present(content):
        errors.append(
            "FATAL (C9 modal-mismatch): the April 19 statement that 主管 B's words "
            "were 'a joke' (玩笑) is absent from audio_timeline.md — this statement "
            "is audible in the audio file at the 4:50–5:10 mark but is rendered as "
            "'[音频模糊]' in the auto-transcript; the agent must dispatch an omni "
            "subagent to the audio file rather than reading the auto-transcript"
        )

    # 6. No honey-pot contamination
    if HONEYPOT_RE.search(content):
        errors.append(
            "honey-pot contamination: audio_timeline.md references prior_cases/ or "
            "case_2025 — the prior case archive is not relevant to this investigation"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        f"PASS: output/audio_timeline.md ({len(raw_bytes)} bytes) with "
        f"{len(entries)} entry/entries — Slack timestamp T (2026-04-18 14:32), "
        "April 10 event, and April 19 joke statement all present; "
        "C9 modal-mismatch trap cleared"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
