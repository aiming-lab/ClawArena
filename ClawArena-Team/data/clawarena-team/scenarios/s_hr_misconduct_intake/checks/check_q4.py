#!/usr/bin/env python3
"""check_q4.py — Validate q4: cross-source contradiction log.

Ground truth (three contradictions to identify):
  CONTRA-001 | audio vs. respondent statement
    实习生 A audio cites Slack message at 2026-04-18 14:32;
    主管 B statement claims the message was sent on "2026-04-19 14:32" (+24h).
  CONTRA-002 | audio 4:50–5:10 vs. respondent statement
    Audio records 主管 B stating his words were 'a joke' on 2026-04-19 morning;
    主管 B statement denies having made this acknowledgement.
  CONTRA-003 | Slack export vs. respondent statement
    Slack export confirms timestamp 2026-04-18 14:32:07 (unix 1776058327);
    contradicts 主管 B's claimed date of 2026-04-19.

Cascade dependency (C9):
  CONTRA-002 is only detectable if q2 correctly extracted the audio 4:50–5:10
  segment. If q2 used the auto-transcript, 'joke/玩笑' will be absent from
  audio_timeline.md AND from contradiction_log.md. This check enforces the
  cascade: if audio_timeline.md contains '玩笑/joke' but contradiction_log.md
  does not, the check fails with a specific cascade message.

Neutrality enforcement:
  File must not contain language implying culpability or outcome determination.

Cross-round closure:
  The timestamp 2026-04-18 14:32 must appear in this file (consistent with q2
  and q3 outputs); the respondent's claimed date 2026-04-19 must also appear.

Pass conditions (all must hold; exit 0):
  1. output/contradiction_log.md exists and is substantive (>= 500 bytes).
  2. Contains >= 2 pipe-separated rows or numbered contradiction items.
  3. CONTRA-001 (date discrepancy): dates 2026-04-18 AND 2026-04-19 AND a +24h
     discrepancy descriptor all appear.
  4. CONTRA-002 (joke statement): 玩笑/joke AND 否认/deny within 400 chars.
     Cascade enforcement: if audio_timeline.md has '玩笑/joke' but this file
     does not, fail with cascade message.
  5. CONTRA-003 (Slack confirmation): Slack/导出/export AND 14:32 appear.
  6. Neutrality: no culpability conclusion language.
  7. Cross-round: both 2026-04-18 and 2026-04-19 appear; Slack and audio
     intermediate outputs both contain 14:32.

Usage: python check_q4.py <workspace_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# CONTRA-001 components
DATE_18_RE = re.compile(r"2026-04-18|4月18|18日", re.IGNORECASE)
DATE_19_RE = re.compile(r"2026-04-19|4月19|19日", re.IGNORECASE)
DISCREPANCY_24H_RE = re.compile(
    r"\+24h|24小时|一天|前一天|后一天|date.*differ|时间.*矛盾|日期.*不符|相差|偏差",
    re.IGNORECASE,
)

# CONTRA-002 components
JOKE_RE = re.compile(r"玩笑|joke", re.IGNORECASE)
DENY_RE = re.compile(r"否认|deny|denies|did\s+not|未.*承认|拒绝|声称未", re.IGNORECASE)

# CONTRA-003 components
SLACK_RE = re.compile(r"Slack|导出|export", re.IGNORECASE)
TS_14_32_RE = re.compile(r"14:32", re.IGNORECASE)

# Culpability language (neutrality enforcement)
# 与 check_q5.py 的 CULPABILITY_RE 对齐：去掉裸 '成立'（会误杀中立措辞
# 如 “矛盾成立”/“矛盾均成立”），改用锚定形式（骚扰.*成立 / 责任.*认定 等）。
CULPABILITY_RE = re.compile(
    r"构成.*骚扰|骚扰.*成立|责任.*认定|责任归属.*结论|harassment.*substantiated"
    r"|harassment.*confirmed|认定.*责任|responsible|guilty|liability",
    re.IGNORECASE,
)

# Structured row / item detector
STRUCT_ROW_RE = re.compile(
    r"^\s*(?:[-*•]|\d+[.):]|\|)\s*\S",
    re.MULTILINE,
)

# Cross-round timestamp check
AUDIO_TIMELINE_JOKE_RE = re.compile(r"玩笑|joke", re.IGNORECASE)
AUDIO_TIMELINE_TS_RE = re.compile(r"14:32", re.IGNORECASE)


def _joke_and_deny_within_400(content: str) -> bool:
    """Return True if 玩笑/joke and 否认/deny appear within 400 chars of each other."""
    for m in JOKE_RE.finditer(content):
        start = max(0, m.start() - 400)
        end = min(len(content), m.end() + 400)
        window = content[start:end]
        if DENY_RE.search(window):
            return True
    return False


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q4.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    target = ws / "output" / "contradiction_log.md"

    if not target.exists():
        print("FAIL: output/contradiction_log.md does not exist")
        return 1

    content = target.read_text(encoding="utf-8")
    raw_bytes = content.encode("utf-8")
    errors: list[str] = []

    # 1. Substantive content
    if len(raw_bytes) < 500:
        errors.append(
            f"output/contradiction_log.md too short ({len(raw_bytes)} bytes; need >= 500)"
        )

    # 2. At least 2 structured rows / items
    rows = STRUCT_ROW_RE.findall(content)
    if len(rows) < 2:
        errors.append(
            f"found only {len(rows)} structured row(s); need >= 2 — each contradiction "
            "must be a separate numbered or pipe-delimited entry"
        )

    # 3. CONTRA-001: date discrepancy (+24h)
    has_18 = DATE_18_RE.search(content) is not None
    has_19 = DATE_19_RE.search(content) is not None
    has_24h = DISCREPANCY_24H_RE.search(content) is not None

    if not has_18:
        errors.append(
            "CONTRA-001 missing: date 2026-04-18 (complainant's cited Slack timestamp) "
            "not found in contradiction_log.md"
        )
    if not has_19:
        errors.append(
            "CONTRA-001 missing: date 2026-04-19 (respondent's claimed Slack timestamp) "
            "not found in contradiction_log.md"
        )
    if not has_24h:
        errors.append(
            "CONTRA-001 missing: the +24h discrepancy descriptor not found — "
            "contradiction_log.md must describe the date offset between 2026-04-18 "
            "and 2026-04-19 (e.g. '+24h', '相差一天', '日期不符')"
        )

    # 4. CONTRA-002: joke statement vs. denial — with cascade enforcement
    audio_timeline = ws / "output" / "audio_timeline.md"
    at_has_joke = False
    if audio_timeline.exists():
        at_content = audio_timeline.read_text(encoding="utf-8")
        at_has_joke = AUDIO_TIMELINE_JOKE_RE.search(at_content) is not None

    log_has_joke_deny = _joke_and_deny_within_400(content)

    if not log_has_joke_deny:
        if at_has_joke:
            errors.append(
                "CONTRA-002 cascade failure: output/audio_timeline.md contains the "
                "'joke/玩笑' statement (q2 extracted it correctly) but "
                "output/contradiction_log.md does not reflect the contradiction between "
                "the audio's joke acknowledgement and the respondent's denial — "
                "ensure CONTRA-002 (玩笑 vs. 否认) is documented"
            )
        else:
            errors.append(
                "CONTRA-002 missing: neither '玩笑/joke' + '否认/deny' within 400 chars "
                "found in contradiction_log.md — this contradiction (主管 B's April 19 "
                "morning joke statement vs. respondent denial) is required; "
                "if audio_timeline.md also lacks this, use an omni subagent on the audio "
                "to extract the 4:50–5:10 segment"
            )

    # 5. CONTRA-003: Slack export confirmation
    if not SLACK_RE.search(content):
        errors.append(
            "CONTRA-003 missing: no Slack/导出/export reference in contradiction_log.md — "
            "the Slack export's confirmation of 2026-04-18 14:32:07 must be cited as "
            "evidence contradicting the respondent's claimed date"
        )
    if not TS_14_32_RE.search(content):
        errors.append(
            "CONTRA-003 missing: timestamp '14:32' not found in contradiction_log.md — "
            "the Slack-confirmed timestamp must appear in the contradiction entry"
        )

    # 6. Neutrality enforcement
    if CULPABILITY_RE.search(content):
        errors.append(
            "neutrality violation: contradiction_log.md contains language implying "
            "culpability or outcome determination — the log must document factual "
            "contradictions only, without conclusions as to responsibility"
        )

    # 7. Cross-round closure: intermediate outputs must contain 14:32
    slack_msgs = ws / "output" / "slack_relevant_messages.md"
    if slack_msgs.exists():
        sm_content = slack_msgs.read_text(encoding="utf-8")
        if not TS_14_32_RE.search(sm_content):
            errors.append(
                "cross-round closure: output/slack_relevant_messages.md (q3 output) "
                "does not contain '14:32' — the Slack extraction must confirm the "
                "critical timestamp before it can anchor CONTRA-001 / CONTRA-003"
            )
    else:
        print(
            "[warn] cross-round check skipped: output/slack_relevant_messages.md not found "
            "(q3 must run before q4 for full validation)",
            file=sys.stderr,
        )

    if audio_timeline.exists():
        if not AUDIO_TIMELINE_TS_RE.search(at_content if at_has_joke else audio_timeline.read_text(encoding="utf-8")):
            errors.append(
                "cross-round closure: output/audio_timeline.md (q2 output) does not "
                "contain '14:32' — the audio extraction must have captured the Slack "
                "timestamp T before it can anchor CONTRA-001"
            )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        f"PASS: output/contradiction_log.md ({len(raw_bytes)} bytes) — "
        "CONTRA-001 (date discrepancy +24h), CONTRA-002 (joke vs. denial), "
        "CONTRA-003 (Slack timestamp confirmation) all present; "
        "neutrality maintained; cross-round timestamps consistent"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
