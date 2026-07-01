"""check_q1.py — output/review_plan.md 含 5 section + area-7 + 两时相日期。

通过条件（全部满足，exit 0）：
  1. output/review_plan.md 存在且 >= 200 字符。
  2. 含 >= 5 个真正的分节标题（H1-H4 / 编号 / 加粗），且标题文字覆盖 5 个主题：
     imagery / metadata / survey / cross_reference / decision。
     散文正文不再作为兜底（题面要求真正的 5-section plan）。
  3. 引用 area-7（大小写不限）。
  4. 引用 2024-08-12 与 2026-04-23（或等价的 Aug 2024 / Apr 2026 等）。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root

_SECTION_THEMES = [
    r"imager",         # imagery
    r"metadat",        # metadata
    r"survey",         # survey
    r"cross[_\s\-]?ref",  # cross_reference
    r"decis",          # decision
]

_DATE_T1_RE = re.compile(r"2024[-/\s]?08[-/\s]?12|Aug(?:ust)?\s+2024|2024.+T1", re.IGNORECASE)
_DATE_T2_RE = re.compile(r"2026[-/\s]?04[-/\s]?23|Apr(?:il)?\s+2026|2026.+T2", re.IGNORECASE)


def main() -> int:
    ws = workspace_root()
    target = ws / "output" / "review_plan.md"

    # 1. 存在性 + 最小长度
    if not target.exists():
        fail("missing output/review_plan.md")
    content = target.read_text(encoding="utf-8", errors="ignore")
    if len(content.strip()) < 200:
        fail("output/review_plan.md too short (< 200 chars)")

    # 2. 5 个真正的 section 标题，覆盖 5 个主题。
    # 题面明确要求 '5-section analysis plan'：散文正文不算 section，必须是标题行。
    # 接受 H1-H4（#~####）/ 编号（'1.' '1)'）/ 加粗（'**Foo**'）形式的标题。
    headers = re.findall(
        r"(?m)^\s*(?:#{1,4}\s*(\S.*)|(?:\*{1,2})\s*(\S.*?)\**\s*|(?:\d+[.\)])\s*(\S.*))$",
        content,
    )
    header_lines = [h for grp in headers for h in grp if h]
    if len(header_lines) < 5:
        fail(f"review_plan.md needs >= 5 section headings, got {len(header_lines)}: {header_lines}")
    headers_text = " ".join(header_lines).lower()
    missed = [theme for theme in _SECTION_THEMES if not re.search(theme, headers_text)]
    if missed:
        fail(f"review_plan.md missing section-heading themes (prose body does not count): {missed}")

    # 3. area-7 引用
    if not re.search(r"area[-_\s]?7", content, re.IGNORECASE):
        fail("review_plan.md does not reference area-7")

    # 4. 两时相日期
    if not _DATE_T1_RE.search(content):
        fail("review_plan.md does not reference T1 date 2024-08-12")
    if not _DATE_T2_RE.search(content):
        fail("review_plan.md does not reference T2 date 2026-04-23")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
