"""q1: output/triage_plan.md 含 5 section + 引用 checkout-service + spike 时间戳。"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root

REQUIRED_SECTIONS = [
    "trace",
    "code",
    "test",
    "decision",
    "timeline",
]

REQUIRED_IDS = [
    "checkout-service",
    "2026-05-23",
]


def main() -> int:
    ws = workspace_root()
    f = ws / "output" / "triage_plan.md"
    if not f.exists():
        fail("missing output/triage_plan.md")
    text = f.read_text(encoding="utf-8", errors="ignore").lower()

    # 检查 5 个 section（宽松：含 section 关键词即可）
    found = [s for s in REQUIRED_SECTIONS if s in text]
    if len(found) < 4:
        fail(
            f"triage_plan.md missing sections: need ≥4 of {REQUIRED_SECTIONS}, "
            f"found only {found}"
        )

    # 检查引用 checkout-service 和 spike 时间
    for kw in REQUIRED_IDS:
        if kw.lower() not in f.read_text(encoding="utf-8", errors="ignore").lower():
            fail(f"triage_plan.md does not reference '{kw}'")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
