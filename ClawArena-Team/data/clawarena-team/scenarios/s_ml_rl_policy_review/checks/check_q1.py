"""q1: review_plan.md exists + 5 section + 引用 v3/v4/rotpen-rdd."""
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
    # 题面只说 '5-section'，未限定标题层级/格式。放宽为接受常见分节形式：
    # H1-H4（#~####，允许无空格 '##Foo'）/ 编号（'1.' '1)'）/ 加粗（'**Foo**'）。
    sections = re.findall(
        r"(?m)^\s*(?:#{1,4}\s*\S.*|(?:\*{1,2}|\d+[.\)])\s*\S.{2,})$",
        text,
    )
    if len(sections) < 5:
        fail(f"need >= 5 sections, got {len(sections)}: {sections}")
    low = text.lower()
    for needle in ("v3", "v4", "rotpen-rdd"):
        if needle.lower() not in low:
            fail(f"missing required reference: {needle}")
    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
