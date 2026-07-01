#!/usr/bin/env python3
"""check_q1.py — 校验 q1 落盘的模块影响评估笔记。

期望产物：
  output/notes/q1_modules.md  （main agent 落盘）

校验规则（C10 精确匹配）：
  - 文件存在
  - 含 "core.pipeline"（issue-1 模块）
  - 含 "core.scheduler"（issue-1 模块）
  - 含 "api.gateway"（issue-2 模块）
  - 含 "api.auth"（issue-2 模块）
  - 含 "tasks.worker"（issue-3 模块）
  - 含 "tasks.retry"（issue-3 模块）

用法：python check_q1.py <workspace_abs_path>
退出码：0=通过，1=失败
"""
import sys
from pathlib import Path


REQUIRED_KEYWORDS = [
    # 接受 module 风格 (core.pipeline) 或 路径风格 (src/core/pipeline.py / core/pipeline.py)
    ["core.pipeline", "core/pipeline"],
    ["core.scheduler", "core/scheduler"],
    ["api.gateway", "api/gateway"],
    ["api.auth", "api/auth"],
    ["tasks.worker", "tasks/worker"],
    ["tasks.retry", "tasks/retry"],
]


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: check_q1.py <workspace_path>", file=sys.stderr)
        sys.exit(1)

    ws = Path(sys.argv[1])
    notes = ws / "output" / "notes" / "q1_modules.md"

    if not notes.exists():
        print(f"MISSING: {notes}", file=sys.stderr)
        sys.exit(1)

    text = notes.read_text(encoding="utf-8").lower()
    missing = [kws for kws in REQUIRED_KEYWORDS if not any(k.lower() in text for k in kws)]

    if missing:
        print(f"NOT FOUND in q1_modules.md: {missing}", file=sys.stderr)
        sys.exit(1)

    print("OK")
    sys.exit(0)


if __name__ == "__main__":
    main()
