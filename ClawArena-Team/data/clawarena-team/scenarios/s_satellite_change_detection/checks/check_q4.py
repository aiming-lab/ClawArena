"""check_q4.py — findings/cross_reference.md 含差异 0.3 ha + within tolerance 判定。

通过条件（全部满足，exit 0）：
  1. findings/cross_reference.md 存在且 >= 150 字符。
  2. 含差异数字 0.3（±0.05 容差），且上下文含 ha / hect 单位词。
  3. 含"within tolerance"或等价中英文表述（within / 容差内 / 符合容差 / meets tolerance 等）。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root, find_number_near

_WITHIN_TOLERANCE_RE = re.compile(
    r"within\s+(?:\w+\s+){0,3}tolerance"  # within X tolerance (X = "the allowed", "acceptable", "the ±0.5 ha", etc.)
    r"|meets?\s+(?:the\s+)?tolerance"
    r"|below\s+(?:the\s+)?tolerance"
    r"|under\s+(?:the\s+)?tolerance"
    r"|inside\s+(?:the\s+)?tolerance"
    r"|tolerance(?:\s+is)?\s+(?:not\s+)?exceeded"
    r"|符合容差|在容差(?:范围)?内|满足精度|精度满足|差异在容差|未超容差",
    re.IGNORECASE,
)


def main() -> int:
    ws = workspace_root()
    target = ws / "findings" / "cross_reference.md"

    # 1. 存在 + 最小长度
    if not target.exists():
        fail("missing findings/cross_reference.md")
    content = target.read_text(encoding="utf-8", errors="ignore")
    if len(content.strip()) < 150:
        fail("findings/cross_reference.md too short (< 150 chars)")

    # 2. 差异数字 0.3 ha（±0.05）
    diff = find_number_near(content, 0.3, tolerance=0.05)
    if diff is None:
        fail("cross_reference.md does not contain discrepancy value ~0.3 (ha)")
    # 确认有单位词在文件中（宽松：全文有 ha 或 hect 即可）
    if not re.search(r"\bha\b|\bhect(?:are)?", content, re.IGNORECASE):
        fail("cross_reference.md is missing unit (ha / hectares)")

    # 3. within tolerance 判定
    if not _WITHIN_TOLERANCE_RE.search(content):
        fail(
            "cross_reference.md does not contain 'within tolerance' conclusion "
            "(or equivalent phrase)"
        )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
