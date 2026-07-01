"""check_q2.py — wave3 s_ecommerce_chargeback_dispute q2 checker.

Verifies output/customer_intent.md (G + I 维度开端，反 q4 过拟合):
1. File exists
2. Chinese replacement token present: 补发 or 替换 or 免费发送
3. English replacement token: "replacement unit" OR "in lieu of refund" OR "replacement"
4. C9 modality_decoy guard: "full refund" present without discredit → FAIL
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_DISCREDIT_WORDS = re.compile(
    r"\b(?:hallucinate[sd]?|fabricate[sd]?|incorrect|inaccurate|false|wrong|"
    r"error|erroneous|decoy|auto.generated|auto.summary|conflict|contradict|"
    r"not.*authoritative|do\s+not\s+rely|unreliable|misstate|overstated|"
    r"ignore|disregard|refute[sd]?|invalid|bogus|note(?:d)?|caution|warning|"
    # 否定/纠正退款误读的词。注意：不得含 'replacement'/'lieu'/'rather'/'instead'
    # —— 题面强制文档必含 'replacement' 等换货表述，这些词在任意 'full refund'
    # 的 ±240 窗口内必然出现，会让错误锚定 'full refund' 被无条件放过。
    r"declined|denied|rejected|not\s+a\s+full)\b",
    re.IGNORECASE,
)
_WINDOW = 240


def _is_safely_quoted(text: str, pattern: str) -> bool:
    """Return True iff every occurrence of pattern is within a discredit window."""
    for m in re.finditer(pattern, text, re.IGNORECASE):
        start = max(0, m.start() - _WINDOW)
        end   = min(len(text), m.end() + _WINDOW)
        ctx   = text[start:end]
        if not _DISCREDIT_WORDS.search(ctx):
            return False
    return True


def main(workspace: Path) -> int:
    out = workspace / "output" / "customer_intent.md"
    if not out.exists():
        print("FAIL: output/customer_intent.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. Chinese replacement token（G 维度）
    # Accept: 补发 / 补发一件 / 免费补发 / 替换 / 替换商品 / 免费发送
    if not re.search(r"补发|替换|免费.*(?:发|送)", text):
        print(
            "FAIL: Chinese replacement token ('补发' / '替换' / '免费补发') not found "
            "in customer_intent.md. Must extract from cn_support_chat.txt."
        )
        return 1

    # 2. English replacement token（wav 权威源 or en_support_chat）
    if not re.search(
        r"replacement\s+unit|in\s+lieu\s+of\s+refund|replacement.*free|"
        r"free.*replacement|ship.*replacement|replacement.*(?:agreed|accepted|confirm)",
        text,
        re.IGNORECASE,
    ):
        print(
            "FAIL: English replacement confirmation not found in customer_intent.md. "
            "Must confirm from voice_memos/customer_voicemail.wav or en_support_chat.txt."
        )
        return 1

    # 3. C9 modality_decoy guard: "full refund" without discredit → FAIL
    if re.search(r"full\s+refund", text, re.IGNORECASE):
        if not _is_safely_quoted(text, r"full\s+refund"):
            print(
                "FAIL (C9 modality_decoy): customer_intent.md contains 'full refund' "
                "without being discredited. This phrase comes from the auto-generated "
                "internal_summary_auto.txt decoy — it conflicts with the authoritative "
                "wav recording and Chinese chat log which confirm replacement. "
                "Do not use the auto-summary as the authoritative source."
            )
            return 1

    print(
        "PASS: Chinese replacement token + English replacement confirmation + "
        "no uncredited 'full refund'"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
