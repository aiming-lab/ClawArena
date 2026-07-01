"""q1: output/audit_plan.md 存在 + >= 5 section + 引用 W-12 + v5/clim-sim-v5-2026q2。

通过条件（全部满足，exit 0）：
  1. output/audit_plan.md 存在
  2. 含 >= 5 个 '## ' 二级标题
  3. 含字符串 'W-12'
  4. 含 'v5' 或 'clim-sim-v5'（大小写不敏感）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root


def main() -> int:
    ws = workspace_root()
    plan = ws / "output" / "audit_plan.md"
    if not plan.exists():
        fail("missing output/audit_plan.md")

    text = plan.read_text(encoding="utf-8", errors="ignore")

    sections = re.findall(r"^##\s+\S.*$", text, flags=re.MULTILINE)
    if len(sections) < 5:
        fail(f"need >= 5 '## ' sections, got {len(sections)}: {sections}")

    if "W-12" not in text:
        fail("missing required basin id 'W-12'")

    low = text.lower()
    if "v5" not in low and "clim-sim" not in low:
        fail("missing simulation reference: 'v5' or 'clim-sim-v5'")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
