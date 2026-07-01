"""q1: output/review_plan.md 存在 + 5 个 ## section + 引用 EXP-2421。

通过条件（全部满足，exit 0）：
  1. output/review_plan.md 存在且非空
  2. 含 >= 5 个 '## ' 二级标题
  3. 文本中包含 'EXP-2421'
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
    if len(text.strip()) < 50:
        fail("output/review_plan.md is too short (< 50 chars)")
    # 5 个二级标题（## ）
    sections = re.findall(r"^##\s+\S.*$", text, flags=re.MULTILINE)
    if len(sections) < 5:
        fail(f"need >= 5 '## ' sections, got {len(sections)}: {sections}")
    # 必须引用 EXP-2421
    if "EXP-2421" not in text:
        fail("missing required reference: EXP-2421")
    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
