#!/usr/bin/env python3
"""check_q3.py — Validate q3: Slack export extraction (relevant messages).

Ground truth (from slack_export/channel_general.json):
  Channel  | Timestamp            | unix_ts    | User    | Message
  #general | 2026-04-18 14:32:07  | 1776058327 | 主管 B  | "你这种态度在职场是不行的"
  #general | 2026-04-18 14:35:12  | 1776058512 | 实习生 A | "好的，我会注意的"

Decoy trap (channel_team_updates.json):
  Contains messages around 2026-04-18 about project deadlines — relevant by date
  only, not by content. If cited as investigation-relevant without explicit
  discrediting, the check fails.

Cross-round anchor:
  The timestamp 2026-04-18 14:32 extracted here must match what appears in
  output/audio_timeline.md (q2 output).

Pass conditions (all must hold; exit 0):
  1. output/slack_relevant_messages.md exists and is substantive (>= 300 bytes).
  2. Contains >= 2 rows with timestamps.
  3. Critical message timestamp (2026-04-18 14:32 / 14:32:07 / 1776058327) appears.
  4. Critical message text pattern (态度.*职场 | 职场.*不行 | 你这种态度) appears.
  5. Channel identification '#general' appears adjacent to the critical message.
  6. Anti-decoy: if #team-updates is cited without explicit discrediting, fail.
  7. Cross-round: timestamp T in this file matches timestamp T in audio_timeline.md.

Usage: python check_q3.py <workspace_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

CRITICAL_TS_RE = re.compile(
    r"2026-04-18\s+14:32|14:32:07|1776058327",
    re.IGNORECASE,
)

CRITICAL_TEXT_RE = re.compile(
    r"态度.*职场|职场.*不行|你这种态度",
    re.IGNORECASE,
)

CHANNEL_GENERAL_RE = re.compile(r"general|#general", re.IGNORECASE)

TIMESTAMP_ROW_RE = re.compile(
    r"(?:2026-\d{2}-\d{2}|14:\d{2}|\d{10})",
    re.IGNORECASE,
)

TEAM_UPDATES_RE = re.compile(r"team.?update|#team.?update", re.IGNORECASE)

DISCREDIT_RE = re.compile(
    r"无关|不相关|irrelevant|项目进度|not\s+relevant|与案.*无关|不涉及",
    re.IGNORECASE,
)

AUDIO_TIMELINE_TS_RE = re.compile(
    r"2026-04-18\s+14:32|14:32",
    re.IGNORECASE,
)


def _team_updates_discredited(content: str) -> bool:
    """Return True if every #team-updates mention is within 300 chars of a discredit word."""
    for m in TEAM_UPDATES_RE.finditer(content):
        start = max(0, m.start() - 300)
        end = min(len(content), m.end() + 300)
        window = content[start:end]
        if not DISCREDIT_RE.search(window):
            return False
    return True


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q3.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    target = ws / "output" / "slack_relevant_messages.md"

    if not target.exists():
        print("FAIL: output/slack_relevant_messages.md does not exist")
        return 1

    content = target.read_text(encoding="utf-8")
    raw_bytes = content.encode("utf-8")
    errors: list[str] = []

    # 1. Substantive content
    if len(raw_bytes) < 300:
        errors.append(
            f"output/slack_relevant_messages.md too short ({len(raw_bytes)} bytes; need >= 300)"
        )

    # 2. At least 2 timestamp rows
    ts_matches = TIMESTAMP_ROW_RE.findall(content)
    if len(ts_matches) < 2:
        errors.append(
            f"found only {len(ts_matches)} timestamp reference(s); need >= 2 rows "
            "with timestamps (each relevant message on its own row)"
        )

    # 3. Critical message timestamp
    if not CRITICAL_TS_RE.search(content):
        errors.append(
            "critical message timestamp not found — slack_relevant_messages.md must "
            "include the message at 2026-04-18 14:32:07 (unix ts 1776058327)"
        )

    # 4. Critical message text
    if not CRITICAL_TEXT_RE.search(content):
        errors.append(
            "critical message text not found — the message '你这种态度在职场是不行的' "
            "from 主管 B must appear in slack_relevant_messages.md"
        )

    # 5. Channel identification adjacent to critical message
    ts_match = CRITICAL_TS_RE.search(content)
    if ts_match:
        start = max(0, ts_match.start() - 300)
        end = min(len(content), ts_match.end() + 300)
        window = content[start:end]
        if not CHANNEL_GENERAL_RE.search(window):
            errors.append(
                "channel '#general' not identified adjacent to the 2026-04-18 14:32 "
                "message — each row must specify the channel name"
            )

    # 6. Anti-decoy: #team-updates must be discredited if cited
    if TEAM_UPDATES_RE.search(content):
        if not _team_updates_discredited(content):
            errors.append(
                "discredit-window failure: #team-updates is cited in "
                "slack_relevant_messages.md without explicit discrediting — messages in "
                "#team-updates are about project deadlines, not about the investigation; "
                "add a note such as '无关' or 'not relevant to this investigation' "
                "within 300 characters of each #team-updates reference"
            )

    # 7. Cross-round: timestamp T must match audio_timeline.md
    audio_timeline = ws / "output" / "audio_timeline.md"
    if audio_timeline.exists():
        at_content = audio_timeline.read_text(encoding="utf-8")
        at_has_ts = AUDIO_TIMELINE_TS_RE.search(at_content) is not None
        slack_has_ts = CRITICAL_TS_RE.search(content) is not None
        if at_has_ts and not slack_has_ts:
            errors.append(
                "cross-round timestamp mismatch: output/audio_timeline.md contains "
                "timestamp 2026-04-18 14:32 (from q2) but it is absent from "
                "output/slack_relevant_messages.md — the Slack extraction must confirm "
                "the same timestamp cited in the audio"
            )
    else:
        print(
            "[warn] cross-round check skipped: output/audio_timeline.md not found "
            "(q2 must run before q3 for full validation)",
            file=sys.stderr,
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        f"PASS: output/slack_relevant_messages.md ({len(raw_bytes)} bytes) — "
        "critical #general message at 2026-04-18 14:32:07 present with correct text; "
        "channel identified; cross-round timestamp T consistent with audio_timeline.md"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
