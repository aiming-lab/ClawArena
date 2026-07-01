"""check_q1.py — triage plan exists with required anchors.

通过条件（全部满足，exit 0）：
  1. output/triage_plan.md 存在
  2. 至少 5 个 ## 级别 section
  3. 同时包含 robot-arm-04、E-0211、2026-05-23 (alarm date) 三个锚点
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root


def main() -> int:
    ws = workspace_root()
    plan = ws / "output" / "triage_plan.md"
    if not plan.exists():
        fail("missing output/triage_plan.md")
    text = plan.read_text(encoding="utf-8", errors="ignore")
    sections = re.findall(r"^##\s+\S.*$", text, flags=re.MULTILINE)
    if len(sections) < 5:
        fail(f"need >= 5 '## ' sections, got {len(sections)}: {sections}")
    low = text.lower()
    for needle in ("robot-arm-04", "e-0211", "2026-05-23"):
        if needle.lower() not in low:
            fail(f"missing required anchor: {needle!r}")
    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
