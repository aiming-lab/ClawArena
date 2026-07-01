"""check_q1.py — output/review_plan.md 存在，含 ≥ 5 个 section 标题，引用 trial_id 与 compound。

通过条件（全部满足，exit 0）：
  1. output/review_plan.md 存在且非空
  2. 含 ≥ 5 个 ## 级标题（或等价结构）
  3. 含 "TR-2026-PHII-091"（trial_id）
  4. 含 "compound-X42" 或 "compound X42"（compound）
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
    if len(text.strip()) < 100:
        fail("output/review_plan.md is too short (< 100 chars)")

    # 计数 section 标题（## 或 ###，或数字列表 1. ... 5. 等）
    heading_count = len(re.findall(r"^#{1,3}\s+\S", text, re.MULTILINE))
    numbered_count = len(re.findall(r"^\d+\.\s+\S", text, re.MULTILINE))
    total_sections = max(heading_count, numbered_count)
    if total_sections < 5:
        fail(f"review_plan.md has only {total_sections} sections/headings (need ≥ 5)")

    if "TR-2026-PHII-091" not in text:
        fail("trial ID 'TR-2026-PHII-091' not found in review_plan.md")

    if not re.search(r"compound[- ]?[Xx]42", text, re.IGNORECASE):
        fail("compound name 'compound-X42' (or compound X42) not found in review_plan.md")

    passed("OK: output/review_plan.md has ≥ 5 sections and references trial ID + compound")
    return 0


if __name__ == "__main__":
    sys.exit(main())
