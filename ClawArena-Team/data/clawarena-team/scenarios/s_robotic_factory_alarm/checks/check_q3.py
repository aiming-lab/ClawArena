"""check_q3.py — partial diagnostic output consumed + initial hypothesis written.

通过条件（全部满足，exit 0）：
  1. notes/initial_hypothesis.md 存在
  2. 文件中含 "gripper" 或 "joint" 或等价中文（关节 / 夹爪 / joint wear）
  3. 文件中含 "partial" 或 "preliminary" 或 "initial" 等提示这是初步判断的词
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, has_phrase_any, passed, workspace_root


def main() -> int:
    ws = workspace_root()
    hyp = ws / "notes" / "initial_hypothesis.md"
    if not hyp.exists():
        fail("missing notes/initial_hypothesis.md")
    text = hyp.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 30:
        fail("notes/initial_hypothesis.md is too short (< 30 chars)")
    # 根因候选 — gripper / joint 词族
    if not has_phrase_any(text, ["gripper", "joint", "关节", "夹爪", "grip", "joint wear", "磨损"]):
        fail("initial hypothesis does not mention gripper/joint root cause candidate")
    # 标明这是初步 / partial 判断
    if not has_phrase_any(text, [
        "partial", "preliminary", "initial", "tentative", "awaiting",
        "pending", "incomplete", "partial result", "初步", "待定", "暂定",
    ]):
        fail("hypothesis does not indicate it is based on partial diagnostic output")
    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
