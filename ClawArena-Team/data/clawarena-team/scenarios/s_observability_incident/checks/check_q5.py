"""q5: findings/test_fail.md 含真实 pytest 失败的测试名 + 行号 51。

验证模型实际运行了 pytest（代码真跑），而非仅靠静态分析猜测行号。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root

# BRIEF 锚点：test_checkout_under_pool_pressure.py:51
FAILING_TEST_NAME = "test_checkout_latency_under_pool_pressure"
EXPECTED_LINE = 51


def main() -> int:
    ws = workspace_root()
    f = ws / "findings" / "test_fail.md"
    if not f.exists():
        fail("missing findings/test_fail.md")
    text = f.read_text(encoding="utf-8", errors="ignore")

    # 必须包含失败测试名
    if FAILING_TEST_NAME not in text:
        fail(f"findings/test_fail.md missing failing test name '{FAILING_TEST_NAME}'")

    # 行号 51（严格，±0）
    if not re.search(r"\bline\s*51\b|:51\b|line\s*=\s*51", text, flags=re.IGNORECASE):
        fail(f"findings/test_fail.md missing assertion line number {EXPECTED_LINE}")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
