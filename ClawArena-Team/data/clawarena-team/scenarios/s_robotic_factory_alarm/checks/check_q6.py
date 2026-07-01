"""check_q6.py — incremental context load: dispatch_constraints consumed + 24h window cited.

通过条件（全部满足，exit 0）：
  1. analysis/dispatch_plan.md 存在
  2. 文件中含 "24" 以及 hour/h/小时等单位（24h 维修窗口约束）
  3. 文件中含 "schedule" 或 "maintain" 或 "dispatch" 或等价中文（排期 / 维修 / 调度）
  4. [致命门控] sessions/main.jsonl 中某非空 session_id 被 RunSubagent 续传 >= 2 次（真实续接信号）
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (
    fail,
    has_phrase_any,
    iter_main_events,
    passed,
    workspace_root,
    _tool_calls,
)


def session_id_counts(ws: Path) -> Counter:
    """统计被 RunSubagent 显式续传的非空 session_id 出现次数。

    真实续接信号：harness 仅当同一 session_id 被再次传入时才视为续接
    （new_session = session_id is None or session_id not in harnesses）。
    复用 subagent_id 并不会续接 session，故只按 session_id 计数。
    """
    counts: Counter[str] = Counter()
    for ev in iter_main_events(ws):
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


def main() -> int:
    ws = workspace_root()
    plan = ws / "analysis" / "dispatch_plan.md"
    if not plan.exists():
        fail("missing analysis/dispatch_plan.md")
    text = plan.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 30:
        fail("analysis/dispatch_plan.md is too short")
    # 24h 约束
    if not re.search(r"\b24\s*[hH](?:our|rs?|小时)?", text) and "24" not in text:
        fail("24-hour window constraint not mentioned in analysis/dispatch_plan.md")
    # 调度 / 维修意图
    if not has_phrase_any(text, [
        "schedule", "maintenance", "dispatch", "repair", "排期", "维修", "调度",
        "schedule_maintenance", "service",
    ]):
        fail("dispatch/maintenance intent not found in analysis/dispatch_plan.md")
    # 真实 session 续接（致命门控）
    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    counts = session_id_counts(ws)
    if not counts or max(counts.values()) < 2:
        fail(
            "genuine session reuse not observed — the task asked you to continue the same "
            "subagent session: thread the same session_id, not spawn a fresh one. "
            "No non-empty session_id appears in >= 2 RunSubagent calls."
        )
    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
