"""q1: output/review_plan.md exists + 5 sections + references gbm-v2-2026q2.

Pass conditions (all required):
  1. File output/review_plan.md exists and is >= 100 chars.
  2. Contains >= 5 '## ' level-2 headings.
  3. References the model name 'gbm-v2-2026q2' (case-insensitive).
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
        fail("review_plan.md is too short (< 100 chars)")
    sections = re.findall(r"^##\s+\S.*$", text, flags=re.MULTILINE)
    if len(sections) < 5:
        fail(f"need >= 5 '## ' sections, got {len(sections)}: {sections}")
    if "gbm-v2-2026q2" not in text.lower():
        fail("missing required model reference: gbm-v2-2026q2")
    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
