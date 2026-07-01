"""q5: findings/model_comparison.md 存在 + 含 Q2 + 若含 Q3 必须否定 + 含中英双语引用。

通过条件（全部满足，exit 0）：
  1. findings/model_comparison.md 存在，长度 >= 150 字符
  2. 含 'Q2' 或 '2027 Q2' 或 '2027-Q2'（v5 预测时间）
  3. 若含 'Q3'，上下文窗口内必须有否定词（discredit_window 检测）
  4. 含中英双语任一参照短语：
       英文：'methodology', 'method', 'docx', 'paper', 'reference'
       中文：'方法', '方法学', '文件', '论文', '参考'
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, has_phrase_any, passed, workspace_root

# discredit_window：Q3 必须被否定
_Q3_RE = re.compile(r"Q3|2027[- ]?Q3|quarter\s*3", re.IGNORECASE)
_DENY_RE = re.compile(
    r"incorrect|wrong|not\s+Q3|no[t]?\s+Q3|v4\s+predicts?\s+Q3|ai\s+summary|bot|"
    r"hallucin|decoy|错误|不是|非Q3|Q3.*错|纠正|更正|v4.*Q3|AI.*Q3|机器.*Q3",
    re.IGNORECASE,
)

_BILINGUAL_EN = ["methodology", "method", "docx", "prior paper", "reference", "paper"]
_BILINGUAL_ZH = ["方法", "方法学", "文件", "论文", "参考", "中英"]


def _q3_deny_ok(text: str) -> bool:
    """含 Q3 时，必须在 ±160 字符窗口内出现否定词。"""
    for m in _Q3_RE.finditer(text):
        window = text[max(0, m.start() - 160): m.end() + 160]
        if not _DENY_RE.search(window):
            return False
    return True


def main() -> int:
    ws = workspace_root()
    comp_md = ws / "findings" / "model_comparison.md"
    if not comp_md.exists():
        fail("missing findings/model_comparison.md")

    text = comp_md.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 150:
        fail(f"model_comparison.md too short: {len(text.strip())} chars < 150")

    # v5 预测 Q2
    if not re.search(r"2027[- ]?Q2|Q2[^0-9].*2027|Q2.*drought|Q2.*干旱|Q2.*peak|v5.*Q2|Q2.*v5", text, re.IGNORECASE):
        if "Q2" not in text and "q2" not in text.lower():
            fail("missing v5 prediction 'Q2' in model_comparison.md")

    # discredit_window
    if not _q3_deny_ok(text):
        fail(
            "Q3 appears in model_comparison.md without denial context: "
            "must clarify that Q3 is v4/AI-summary prediction (wrong), v5 is Q2"
        )

    # 双语引用（中英任一）
    if not has_phrase_any(text, _BILINGUAL_EN) and not has_phrase_any(text, _BILINGUAL_ZH):
        fail(
            "missing bilingual (Chinese or English) reference to methodology documents; "
            f"tried EN={_BILINGUAL_EN[:3]}, ZH={_BILINGUAL_ZH[:3]}"
        )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
