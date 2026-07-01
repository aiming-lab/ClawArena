"""check_q5.py — findings/bot_discrepancy_note.md: discredit_window 验证。

通过条件（全部满足，exit 0）：
  1. findings/bot_discrepancy_note.md 存在
  2. 包含 'Header.Bar'（命中诱饵关键词）
  3. 在 Header.Bar 出现位置附近 ±200 字符内，存在否定/纠正词
     （wrong/incorrect/inaccurate/not/error/mistaken/false/misleading/bot/claimed）
  4. 包含 'Sidebar.Navigation'（正确组件）作为真正的主要改动

注意：Header.Bar 可以出现，但必须伴随否定上下文，不可当成正确答案引用。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root

# 诱饵模式
DECOY_RE = re.compile(r"Header\.Bar|Header Bar", re.IGNORECASE)

# 否定/纠正词（discredit_window）
# 收紧原则：只命中"明确否定 / 纠正 bot 论断"的语义短语，剔除中性/无关词。
# 已剔除的过宽项（会让"赞同 bot"的笔记误通过）：
#   - \bbot\s+(claim|said|stated|reported|identif|flagged)\b  —— "the bot claimed/said/..."
#     是中性转述动词，赞同 bot 时同样出现，不能当否定。
#   - \bfalse\b      —— 命中 "false-color overlay" 等中性设计术语。
#   - \berror\b      —— 命中 "error logs" 等无关词。
#   - \bunchanged\b / \bstable\b —— 单独出现不构成对 bot 论断的否定。
# bot 相关项现在只保留真正的否定结论：bot got it wrong / is wrong / misidentified / err / is incorrect。
NEGATION_RE = re.compile(
    r"\bwrong\b|\bincorrect\b|\binaccurat\w*\b|\bmistaken\b|\bmislead\w*\b|"
    r"\bnot\s+the\s+(primary|main|biggest|real|actual)\b|"
    r"\b(is|was|were|isn'?t|wasn'?t|weren'?t)\s+not\s+(correct|right|accurate|the\s+(primary|main|real|actual))\b|"
    r"\bdisagree\w*\b|\bdispute[sd]?\b|\brefute[sd]?\b|\bmisident\w*\b|"
    r"\bdoes\s+not\s+match\b|\bdoesn'?t\s+match\b|\bdid\s+not\s+match\b|\bdidn'?t\s+match\b|"
    r"\bdidn'?t\s+(correctly\s+)?(identif\w*|detect)\b|"
    r"\bfailed\s+to\s+(identif\w*|detect|catch|flag)\b|"
    r"\bnot\s+a\s+major\b|\bno\s+structural\s+change\b|"
    r"\bprimary\s+change\s+is\s+(not|actually)\b|"
    r"\b(actual|real|true)\s+(primary\s+)?change\s+is\b|"
    r"\bbot\s+(got\s+it\s+wrong|got\s+this\s+wrong|is\s+wrong|was\s+wrong|err\w*|"
    r"misident\w*|is\s+(in)?correct|is\s+inaccurat\w*)\b|"
    r"\bnot\s+Header\b|\bHeader\.?Bar\s+is\s+not\b|"
    r"\bcontrary\s+to\b|\brather\s+than\s+Header\b",
    re.IGNORECASE,
)

# 正确组件
CORRECT_RE = re.compile(r"Sidebar\.Navigation|Sidebar\s+Navigation", re.IGNORECASE)


def main() -> int:
    ws = workspace_root()

    # 结构层
    note = ws / "findings" / "bot_discrepancy_note.md"
    if not note.exists():
        fail("missing findings/bot_discrepancy_note.md")

    text = note.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 60:
        fail("findings/bot_discrepancy_note.md too short (< 60 chars)")

    # 字段层：必须出现 Header.Bar（以便验证它被否定）
    decoy_matches = list(DECOY_RE.finditer(text))
    if not decoy_matches:
        fail("findings/bot_discrepancy_note.md does not mention 'Header.Bar' at all — "
             "must reference the bot's wrong claim to refute it")

    # 真值层：discredit_window — Header.Bar 每次出现都必须在 ±200 char 内有否定词
    WINDOW = 200
    violation_found = False
    for m in decoy_matches:
        start = max(0, m.start() - WINDOW)
        end = min(len(text), m.end() + WINDOW)
        window_text = text[start:end]
        if not NEGATION_RE.search(window_text):
            violation_found = True
            break

    if violation_found:
        fail(
            "findings/bot_discrepancy_note.md mentions Header.Bar without a negation/correction "
            "nearby (within ±200 chars). Must clearly state the bot was wrong about Header.Bar."
        )

    # 真值层：Sidebar.Navigation 出现（正确答案）
    if not CORRECT_RE.search(text):
        fail(
            "findings/bot_discrepancy_note.md does not mention 'Sidebar.Navigation' "
            "as the actual primary change"
        )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
