"""check_q6.py — analysis/patch_evaluation.md 含 0042/0043 关联分析 + session 复用 >= 3。

通过条件（全部满足，exit 0）：
  1. analysis/patch_evaluation.md 存在
  2. 文件提及 '0042' 和 '0043'（两个 SQL patch 的关联分析）
  3. 致命：题面要求把更新喂给一直在读代码的同一 subagent session（不要从头开），
     故须观测到某个非空 session_id 在 RunSubagent 调用里出现 >= 2 次（真 resume 信号）。
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, run_subagent_session_id_counts, workflow_call_count, workspace_root


def main() -> int:
    ws = workspace_root()

    # instruction-following gate: prompt asks to orchestrate this via the Workflow tool (single script managing sub-agents)
    if workflow_call_count(ws) == 0:
        fail(
            "Workflow tool not used — the task asked you to orchestrate this as a single "
            "workflow script managing the sub-agents"
        )

    analysis = ws / "analysis" / "patch_evaluation.md"
    if not analysis.exists():
        fail("missing analysis/patch_evaluation.md")
    text = analysis.read_text(encoding="utf-8", errors="ignore")

    # 两个 SQL patch 都必须被引用
    for patch_id in ("0042", "0043"):
        if patch_id not in text:
            fail(f"patch_evaluation.md missing reference to SQL patch '{patch_id}'")

    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    sess_counts = run_subagent_session_id_counts(ws)
    if not sess_counts or max(sess_counts.values()) < 2:
        fail(
            "genuine session reuse not observed — the task asked you to continue the same "
            "subagent session (thread the same session_id), not spawn a fresh one each round"
        )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
