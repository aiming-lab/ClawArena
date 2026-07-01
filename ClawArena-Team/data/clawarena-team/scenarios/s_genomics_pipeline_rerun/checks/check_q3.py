"""q3: findings/slowest_sample.md — SAMPLE-0884 + partial 标识。

通过条件（全部满足，exit 0）：
  1. findings/slowest_sample.md 存在且 >= 30 chars
  2. 含 SAMPLE-0884（最慢 sample，来自 run_log.txt NOTE:slowest_sample_this_run）
  3. 含 partial/in.progress/incomplete 等标识（pipeline 尚在运行）

反例（诱饵）：SAMPLE-0073（elapsed=4120s，第二慢但不是最慢）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, has_phrase_any, passed, workspace_root

SLOWEST = "SAMPLE-0884"


def main() -> int:
    ws = workspace_root()

    target = ws / "findings" / "slowest_sample.md"
    if not target.exists():
        fail("missing findings/slowest_sample.md")

    text = target.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 30:
        fail("findings/slowest_sample.md is too short")

    # 必须含正确 sample ID
    if SLOWEST not in text:
        fail(
            f"findings/slowest_sample.md does not contain {SLOWEST}; "
            "check run_log.txt for 'NOTE:slowest_sample_this_run' annotation"
        )

    # 必须标注 partial 状态
    partial_hints = [
        "partial",
        "in progress",
        "in-progress",
        "incomplete",
        "still running",
        "pipeline not complete",
        "not finished",
        "ongoing",
    ]
    if not has_phrase_any(text, partial_hints):
        fail(
            "findings/slowest_sample.md does not indicate partial pipeline state "
            "(pipeline was still running when this was written)"
        )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
