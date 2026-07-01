"""check_q1.py — output/review_plan.md 存在 + >= 5 section + 引用 merchant-portal-v7 / v6 / v7.

通过条件（全部满足，exit 0）：
  1. output/review_plan.md 存在
  2. >= 5 个 '## ' 级标题
  3. 包含 'merchant-portal-v7'（不区分大小写可接受连字符变体）
  4. 同时引用 v6 与 v7 两个版本
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root


def main() -> int:
    ws = workspace_root()
    plan = ws / "output" / "review_plan.md"
    if not plan.exists():
        fail("missing output/review_plan.md")

    text = plan.read_text(encoding="utf-8", errors="ignore")

    # 结构层：>= 5 个 ## / ### 级标题（允许嵌套层级；只要语义上 5 个区分清晰即可）
    sections = re.findall(r"^#{2,4}\s+\S.*$", text, flags=re.MULTILINE)
    if len(sections) < 5:
        fail(f"need >= 5 '## / ### ' sections, got {len(sections)}: {sections}")

    low = text.lower()

    # 字段层：项目 ID
    if "merchant-portal-v7" not in low and "merchant portal v7" not in low:
        fail("missing project id 'merchant-portal-v7'")

    # 字段层：同时引用 v6 和 v7
    if "v6" not in low:
        fail("missing reference to 'v6' baseline")
    if "v7" not in low:
        fail("missing reference to 'v7' candidate")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
