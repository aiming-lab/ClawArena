"""check_q6.py — Wave3 s_partnership_term_sheet q6 checker.

Term-sheet negotiation final analysis: session reuse + findings/term_evolution.md.

Pass conditions (all must hold, exit 0):

  1. findings/term_evolution.md exists.
  2. File is >= 200 characters.
  3. File references >= 2 slack screenshot paths (thread_*.png inside 'slack/').
  4. File references >= 2 prior-round output files (e.g. output/ts_diff.md,
     output/final_recommendation.md, output/audit_plan.md, output/gc_email.md,
     output/oral_commitment.md).
  5. File mentions >= 2 conceded or revised terms (economic split, IP first refusal,
     board seats, performance bonus, or synonyms thereof).
  6. Genuine session reuse (FATAL): sessions/main.jsonl shows some non-empty
     session_id used in RunSubagent >= 2 times.
     真 resume 信号 = agent 把同一个 session_id 续传给 >= 2 次 RunSubagent；数
     subagent_id 重复是假信号（每次新建会话），故只看 session_id。
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterator


# ---------------------------------------------------------------------------
# Inline helpers (self-contained — no cross-scenario _common dependency)
# ---------------------------------------------------------------------------

def _workspace_root() -> Path:
    if len(sys.argv) < 2:
        print("usage: check_q6.py <workspace>", file=sys.stderr)
        sys.exit(2)
    return Path(sys.argv[1]).resolve()


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
    if "tool_calls" in ev and isinstance(ev["tool_calls"], list):
        return ev["tool_calls"]
    if ev.get("tool") or ev.get("name"):
        return [ev]
    return []


def _run_subagent_session_id_counts(ws: Path) -> Counter:
    """Count non-empty session_id occurrences across RunSubagent calls (genuine resume).

    Only looks at args["session_id"]; does not fall back to subagent_id/id (those
    spawn a fresh session each time and are a fake reuse signal).
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


def _fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Known prior-round output file basenames (any of these count as a reference)
# ---------------------------------------------------------------------------

_PRIOR_OUTPUTS = [
    "audit_plan.md",
    "ts_diff.md",
    "signature_status.md",
    "oral_commitment.md",
    "final_recommendation.json",
    "final_recommendation.md",
    "gc_email.md",
]

# Terms that count as "conceded / revised" across v1→v2→v3 negotiation history
_CONCESSION_PATTERNS = [
    r"economic\s+split",
    r"\d+\s*/\s*\d+",           # e.g. 60/40, 55/45, 50/50
    r"ip\s+first\s+refusal",
    r"first\s+refusal",
    r"board\s+(seat|governance|composition|member)",
    r"performance\s+bonus",
    r"helios\s+bonus",
    r"concede|concession|conceded",
    r"revised\s+term",
    r"removed|removal|dropped",
    r"increased|decreased|adjusted",
    r"royalt",
    r"ip\s+ownership",
]


def main() -> int:
    ws = _workspace_root()
    report = ws / "findings" / "term_evolution.md"

    # 1. File exists
    if not report.exists():
        _fail("missing findings/term_evolution.md")

    text = report.read_text(encoding="utf-8", errors="ignore")
    text_low = text.lower()

    # 2. Minimum length
    if len(text.strip()) < 200:
        _fail(
            f"findings/term_evolution.md is too short "
            f"({len(text.strip())} chars; need >= 200)"
        )

    # 3. References >= 2 slack screenshot paths (thread_*.png)
    slack_refs = re.findall(r"slack[/\\]thread_\w+\.png", text)
    if len(slack_refs) < 2:
        _fail(
            f"findings/term_evolution.md must reference >= 2 slack screenshot "
            f"paths (e.g. 'slack/thread_01_split_concession.png'); "
            f"found {len(slack_refs)}: {slack_refs}"
        )

    # 4. References >= 2 prior-round output files
    prior_refs = [f for f in _PRIOR_OUTPUTS if f in text]
    if len(prior_refs) < 2:
        _fail(
            f"findings/term_evolution.md must cite >= 2 prior-round output "
            f"files (e.g. output/ts_diff.md, output/final_recommendation.md); "
            f"found {len(prior_refs)}: {prior_refs}"
        )

    # 5. >= 2 distinct conceded/revised terms
    matched_patterns: list[str] = []
    for pat in _CONCESSION_PATTERNS:
        if re.search(pat, text_low):
            matched_patterns.append(pat)
    if len(matched_patterns) < 2:
        _fail(
            f"findings/term_evolution.md must discuss >= 2 conceded or revised "
            f"terms (economic split, board seats, IP first refusal, performance "
            f"bonus, etc.); matched patterns: {matched_patterns}"
        )

    # 6. Genuine session reuse: some non-empty session_id used in >= 2 RunSubagent calls.
    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    counts = _run_subagent_session_id_counts(ws)
    if not counts or max(counts.values()) < 2:
        _fail(
            "genuine session reuse not observed — the task asked you to continue the "
            "same subagent session (thread the same session_id), not spawn a fresh one"
        )

    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
