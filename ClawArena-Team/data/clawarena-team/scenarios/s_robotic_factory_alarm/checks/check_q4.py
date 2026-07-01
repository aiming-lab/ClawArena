"""check_q4.py — video frame analysis + torque over threshold + genuine session reuse.

通过条件（全部满足，exit 0）：
  1. findings/panel_reading.md 存在
  2. 文件中含 "frame" 关键词并出现 36（±3）的帧号（12 fps × 3s）
  3. 文件中含 torque 超阈值的表述（torque + threshold/exceed/over/超阈值 等）
  4. [致命门控] sessions/main.jsonl 中某个非空 session_id 被 RunSubagent 续传 >= 2 次（真实续接信号）
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (
    fail,
    find_first_int_near,
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
    reading = ws / "findings" / "panel_reading.md"
    if not reading.exists():
        fail("missing findings/panel_reading.md")
    text = reading.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 30:
        fail("findings/panel_reading.md is too short")
    # frame 36 ± 3 anchor
    if find_first_int_near(text, 36, tolerance=3) is None:
        fail("frame number near 36 (±3) not found in panel_reading.md")
    # torque over threshold
    if not has_phrase_any(text, [
        "torque", "扭矩",
    ]):
        fail("'torque' or '扭矩' not mentioned in panel_reading.md")
    if not has_phrase_any(text, [
        "threshold", "exceed", "over", "超阈值", "超过", "超出", "above",
    ]):
        fail("no threshold-exceeded assertion found in panel_reading.md")
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
