#!/usr/bin/env python3
"""check_q6.py — Validate q6: HR interview addendum report + session reuse.

Ground truth:
  - findings/interview_addendum.md must exist, >= 150 characters, contain at
    least one of the keywords 'interview', 'witness', 'statement'.
  - The report must reference the wav file path 'hr_interview_addendum.wav'.
  - The report must cite content from >= 2 prior-round output files
    (e.g. output/contradiction_log.md, output/initial_evidence_compilation.md).
  - sessions/main.jsonl must show the same non-empty session_id threaded into
    >= 2 RunSubagent calls (genuine session reuse).

真 resume 信号 = agent 把同一个 session_id 续传给 >= 2 次 RunSubagent。复用
subagent_id 而不传 session_id 是假信号（每次新建会话）。此处只看 session_id，
>= 2 次 → 真复用，否则致命 FAIL。

Pass conditions (all must hold; exit 0):
  1. findings/interview_addendum.md exists and is substantive (>= 150 chars).
  2. At least one of 'interview', 'witness', 'statement' appears in the file.
  3. 'hr_interview_addendum.wav' (or 'audio/hr_interview_addendum') is referenced.
  4. At least 2 prior-round file references appear (output/ files or named prior docs).
  5. sessions/main.jsonl: some non-empty session_id appears in >= 2 RunSubagent calls.

Usage: python check_q6.py <workspace_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterator


# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

KEYWORD_RE = re.compile(r"\b(?:interview|witness|statement)\b", re.IGNORECASE)

WAV_REF_RE = re.compile(r"hr_interview_addendum(?:\.wav)?|audio/hr_interview_addendum", re.IGNORECASE)

# Prior-round file references: output/*.md or named output files
PRIOR_ROUND_RE = re.compile(
    r"output/(?:contradiction_log|initial_evidence_compilation|audio_timeline|"
    r"slack_relevant_messages|scope_memo)(?:\.md)?|"
    r"contradiction_log|initial_evidence_compilation|audio_timeline|"
    r"slack_relevant_messages|scope_memo",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# sessions/main.jsonl helpers
# ---------------------------------------------------------------------------


def _iter_main_events(ws: Path) -> Iterator[dict]:
    p = ws / "sessions" / "main.jsonl"
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue


def _tool_calls(ev: dict) -> list[dict]:
    """Extract tool call entries from a jsonl event (multiple fallback formats)."""
    if "tool_calls" in ev and isinstance(ev["tool_calls"], list):
        return ev["tool_calls"]
    if ev.get("tool") or ev.get("name"):
        return [ev]
    return []


def run_subagent_session_id_counts(ws: Path) -> Counter:
    """Count RunSubagent calls per non-empty session_id from sessions/main.jsonl.

    只看 args["session_id"]，不回退到 subagent_id/id（后者每次新建会话，是假信号）。
    """
    counts: Counter[str] = Counter()
    for ev in _iter_main_events(ws):
        for tc in _tool_calls(ev):
            name = tc.get("tool") or tc.get("name")
            if name != "RunSubagent":
                continue
            args = tc.get("args") or tc.get("arguments") or {}
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {}
            sid = args.get("session_id")
            if sid:
                counts[str(sid)] += 1
    return counts


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q6.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    addendum = ws / "findings" / "interview_addendum.md"
    errors: list[str] = []

    # --- 1. File exists and is substantive ---
    if not addendum.exists():
        print(
            "FAIL: findings/interview_addendum.md does not exist — "
            "use the reused investigation subagent session to write the interview "
            "addendum report after extracting key statements from "
            "audio/hr_interview_addendum.wav"
        )
        return 1

    content = addendum.read_text(encoding="utf-8")
    char_count = len(content)

    if char_count < 150:
        errors.append(
            f"findings/interview_addendum.md too short ({char_count} chars; need >= 150) — "
            "the addendum must include key witness statements from the supplementary "
            "interview audio and cross-reference analysis with prior-round findings"
        )

    # --- 2. Interview / witness / statement keyword ---
    if not KEYWORD_RE.search(content):
        errors.append(
            "findings/interview_addendum.md must contain at least one of the keywords "
            "'interview', 'witness', or 'statement' — the report should clearly identify "
            "this as an interview addendum document"
        )

    # --- 3. WAV file path reference ---
    if not WAV_REF_RE.search(content):
        errors.append(
            "findings/interview_addendum.md does not reference the wav file path "
            "'audio/hr_interview_addendum.wav' — the source audio must be cited "
            "to establish the chain of evidence for the supplementary statement"
        )

    # --- 4. At least 2 prior-round file references ---
    prior_refs = PRIOR_ROUND_RE.findall(content)
    # Deduplicate by normalised lower-case match text
    unique_prior = {m.lower().split("/")[-1].replace(".md", "") for m in prior_refs}
    if len(unique_prior) < 2:
        errors.append(
            f"findings/interview_addendum.md cites only {len(unique_prior)} prior-round "
            "file(s); need >= 2 — the addendum must cross-reference at least two files "
            "from previous rounds (e.g. output/contradiction_log.md and "
            "output/initial_evidence_compilation.md) to establish incremental context"
        )

    # --- 5. Genuine session reuse: same non-empty session_id RunSubagent >= 2 times ---
    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    counts = run_subagent_session_id_counts(ws)
    if not counts or counts.most_common(1)[0][1] < 2:
        errors.append(
            "genuine session reuse not observed — the task asked you to continue the "
            "same subagent session (thread the same session_id), not spawn a fresh one"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        f"PASS: findings/interview_addendum.md ({char_count} chars) — "
        "interview/witness/statement keyword present; "
        "audio/hr_interview_addendum.wav referenced; "
        f"{len(unique_prior)} prior-round file(s) cited; "
        "genuine session reuse confirmed (same session_id RunSubagent >= 2)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
