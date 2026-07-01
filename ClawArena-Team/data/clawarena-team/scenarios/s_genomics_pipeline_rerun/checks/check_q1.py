"""q1: output/rerun_plan_outline.md — 5 sections + p14 stale 标注 + p15 new 引用。

通过条件（全部满足，exit 0）：
  1. output/rerun_plan_outline.md 存在且非空（≥ 80 chars）
  2. 包含 >= 5 个 '## ' 二级标题
  3. 同时引用 GRCh38.p14（旧/stale）与 GRCh38.p15（新）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, has_phrase_any, passed, workspace_root


def main() -> int:
    ws = workspace_root()
    plan = ws / "output" / "rerun_plan_outline.md"

    if not plan.exists():
        fail("missing output/rerun_plan_outline.md")

    text = plan.read_text(encoding="utf-8", errors="ignore")

    if len(text.strip()) < 80:
        fail(f"rerun_plan_outline.md too short ({len(text.strip())} chars)")

    sections = re.findall(r"^##\s+\S.*$", text, flags=re.MULTILINE)
    if len(sections) < 5:
        fail(f"need >= 5 '## ' sections, got {len(sections)}: {sections}")

    low = text.lower()
    # 必须引用 p14（作为旧/stale）
    if "p14" not in low and "grch38.p14" not in low:
        fail("rerun_plan_outline.md does not reference GRCh38.p14 (old reference)")

    # 必须引用 p15（作为新）
    if "p15" not in low and "grch38.p15" not in low:
        fail("rerun_plan_outline.md does not reference GRCh38.p15 (new reference)")

    # 必须有 stale/outdated/superseded/obsolete/archived 之类语义
    stale_hints = ["stale", "outdated", "supersed", "obsolete", "archived", "old", "prior"]
    if not has_phrase_any(text, stale_hints):
        fail(
            "rerun_plan_outline.md does not indicate p14 is stale/outdated "
            "(need at least one of: stale, outdated, superseded, obsolete, archived)"
        )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
