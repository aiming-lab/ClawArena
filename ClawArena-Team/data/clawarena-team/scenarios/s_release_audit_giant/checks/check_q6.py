#!/usr/bin/env python3
"""check_q6.py — Validate q6: findings/deploy_evolution.md (+ genuine session-reuse gate).

Pass conditions (fatal — all must hold):
  1. findings/deploy_evolution.md exists.
  2. The file contains the string "figures/deploy_timeline.mp4"
     (confirms the agent referenced the video asset).
  3. Genuine session reuse: some non-empty session_id appears in >= 2 RunSubagent
     calls. 真 resume 信号 = agent 把同一个 session_id 续传给 >= 2 次 RunSubagent；
     数 subagent_id 重复是假信号（每次新建会话）。

Usage: python check_q6.py <workspace_abs_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Iterator


# ---------------------------------------------------------------------------
# sessions/main.jsonl helpers (inline, no external deps)
# ---------------------------------------------------------------------------

def _iter_events(ws: Path) -> Iterator[dict]:
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
    """统计 RunSubagent 调用中**非空 session_id** 的出现次数（真 resume 信号）。

    只看 args["session_id"]，不回退到 subagent_id/id（后者每次新建会话，是假信号）。
    """
    counts: Counter[str] = Counter()
    for ev in _iter_events(ws):
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
# main
# ---------------------------------------------------------------------------

VIDEO_ASSET_REF = "figures/deploy_timeline.mp4"


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q6.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1]).resolve()
    errors: list[str] = []

    # 1. findings/deploy_evolution.md exists
    evo = ws / "findings" / "deploy_evolution.md"
    if not evo.exists():
        errors.append(f"missing: findings/deploy_evolution.md (expected at {evo})")
    else:
        # 2. Video path reference
        text = evo.read_text(encoding="utf-8", errors="ignore")
        if VIDEO_ASSET_REF not in text:
            errors.append(
                f"findings/deploy_evolution.md does not contain the video asset "
                f"reference '{VIDEO_ASSET_REF}'"
            )

    # 3. Genuine session reuse: some non-empty session_id used in >= 2 RunSubagent calls.
    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    counts = _run_subagent_session_id_counts(ws)
    if not counts or max(counts.values()) < 2:
        errors.append(
            "genuine session reuse not observed — the task asked you to continue the "
            "same subagent session (thread the same session_id), not spawn a fresh one"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
