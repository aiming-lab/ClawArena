"""q6: analysis/pool_trend.md 含趋势数字（pool size history）+ 真 session 复用（致命门控）。"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (
    fail,
    has_phrase_any,
    passed,
    run_subagent_session_id_counts,
    workspace_root,
)

# u1 update 中 redis pool size history csv 关键数字：最终 max_pool_size 缩到 5
POOL_EXPECTED_NUMBERS = ["5", "10", "20"]  # 历史中出现过的 pool size 值，至少提及其中 2 个
TREND_KEYWORDS = ["trend", "decreas", "reduc", "shrink", "下降", "减少", "收缩", "pool size"]


def main() -> int:
    ws = workspace_root()
    f = ws / "analysis" / "pool_trend.md"
    if not f.exists():
        fail("missing analysis/pool_trend.md")
    text = f.read_text(encoding="utf-8", errors="ignore")

    # 必须包含 pool 相关趋势关键词
    if not has_phrase_any(text, TREND_KEYWORDS):
        fail("analysis/pool_trend.md must describe pool size trend")

    # 至少提及 2 个历史 pool size 数字
    found_nums = [n for n in POOL_EXPECTED_NUMBERS if re.search(rf"\b{re.escape(n)}\b", text)]
    if len(found_nums) < 2:
        fail(
            f"analysis/pool_trend.md should reference ≥2 pool size history values "
            f"from {POOL_EXPECTED_NUMBERS}; found {found_nums}"
        )

    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    counts = run_subagent_session_id_counts(ws)
    if not counts or max(counts.values()) < 2:
        fail(
            "genuine session reuse not observed — the task asked you to continue the "
            "same subagent session (thread the same session_id), not spawn a fresh one"
        )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
