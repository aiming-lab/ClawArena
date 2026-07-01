"""check_q4.py — findings/recruitment_numbers.md 含正确招募数字 240/120/80/40，且明确否定 200。

通过条件（全部满足，exit 0）：
  1. findings/recruitment_numbers.md 存在且非空
  2. 含 "240"（总计）
  3. 含 "120"（CN）
  4. 含 "80"（DE）
  5. 含 "40"（US）
  6. 若含 "200"，则其上下文（±120 chars）必须同时含否定词
     （如 "incorrect / wrong / hallucinated / not use / bot / 错误 / 不准确 / AI"）
     — 否则视为采纳了 AI 摘要的幻觉数字，判 FAIL
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root

# 否定/否决关键词。ASCII 词必须用 \b 锚定为完整词，避免子串误命中普通英文：
#   裸 'AI' 会命中 available / maintain / remain / again 等(把反幻觉守卫击穿)；
#   裸 'bot' 会命中 robot / bottle / abort；'error' 收紧为 \berror\w*\b 仍容许复数。
# CJK token 无词边界问题，保持原样直接子串匹配。
_NEGATION_RE = re.compile(
    r"\bincorrect\b|\bwrong\b|\bnot\s+use\b|\bdo\s+not\b|\bdon't\b|"
    r"\bhallucinat\w*\b|\bbot\b|\berror\w*\b|\binaccurate\b|"
    r"\bignore\b|\bdiscard\b|\bdeprecated\b|\breject\w*\b|\bnot\b\s+200|"
    r"\bAI\b|"
    r"错误|不准确|不正确|不可用|摘要|幻觉|拒绝|忽略|丢弃|废弃",
    re.IGNORECASE,
)


def _check_200_if_present(text: str) -> bool:
    """若 text 中出现 '200' 作为独立整数，检查其 ±120 chars 窗口内是否有否定词。
    若存在 '200' 但无否定词，返回 False（应 FAIL）；否则返回 True（OK）。
    """
    for m in re.finditer(r"\b200\b", text):
        window = text[max(0, m.start() - 120): m.end() + 120]
        if not _NEGATION_RE.search(window):
            return False
    return True


def main() -> int:
    ws = workspace_root()
    rnum = ws / "findings" / "recruitment_numbers.md"
    if not rnum.exists():
        fail("missing findings/recruitment_numbers.md")

    text = rnum.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 30:
        fail("findings/recruitment_numbers.md is too short")

    if not re.search(r"\b240\b", text):
        fail("total recruitment 240 not found in recruitment_numbers.md")
    if not re.search(r"\b120\b", text):
        fail("CN count 120 not found in recruitment_numbers.md")
    if not re.search(r"\b80\b", text):
        fail("DE count 80 not found in recruitment_numbers.md")
    if not re.search(r"\b40\b", text):
        fail("US count 40 not found in recruitment_numbers.md")

    if not _check_200_if_present(text):
        fail(
            "recruitment_numbers.md contains '200' without a nearby negation — "
            "this suggests the AI bot's hallucinated figure was accepted without being discredited"
        )

    passed("OK: recruitment_numbers.md has 240/120/80/40 with correct bot-discard logic")
    return 0


if __name__ == "__main__":
    sys.exit(main())
