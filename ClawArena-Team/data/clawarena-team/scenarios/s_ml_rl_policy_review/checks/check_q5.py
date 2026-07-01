"""q5: findings/test_failures.md 含真实 pytest 失败的测试名 + 行号 42。"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root


def main() -> int:
    ws = workspace_root()
    f = ws / "findings" / "test_failures.md"
    if not f.exists():
        fail("missing findings/test_failures.md")
    text = f.read_text(encoding="utf-8", errors="ignore")
    if "test_v4_swingup_max_attempts" not in text:
        fail("missing failing test name 'test_v4_swingup_max_attempts'")
    # 行号 42（±0；严格）
    if not re.search(r"\bline\s*42\b|:42\b|line\s*=\s*42", text, flags=re.IGNORECASE):
        fail("missing assertion line number 42")
    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
