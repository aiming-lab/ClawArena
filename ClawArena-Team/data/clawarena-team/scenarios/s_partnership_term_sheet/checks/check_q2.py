"""check_q2.py — Wave3 s_partnership_term_sheet q2 checker.

Verifies output/ts_diff.md (Markdown table — anti-q4-overfitting):
1. v3 economic split: 55/45 or 55% Mercator / 45% Helios
2. v2 economic split: 60/40
3. Chinese draft: 股权分配：55% or 55% Mercator (Chinese confirmation)
4. Board: 3 Mercator + 2 Helios (v3/Chinese)

Discredit guard (D dimension):
- If "60/40" appears in the output as confirmed v3/current split without
  a discredit word in the surrounding 240-char window → FAIL.
  (60/40 from v2 is acceptable IF clearly labelled as v2 or discredited.)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_WINDOW = 240

_DISCREDIT_WORDS = re.compile(
    r"\b(?:v2|version\s*2|旧版|old|supersede[sd]?|replaced|inaccurate|incorrect|"
    r"false|wrong|ai\s*summary|auto.generated|unverified|not\s*current|"
    r"prior|earlier|draft|incorrect|错误|已废弃|不正确)\b",
    re.IGNORECASE,
)


def _is_safely_labelled(text: str, pattern: str) -> bool:
    """Return True if every match of pattern is within a discredit/label window."""
    for m in re.finditer(re.escape(pattern), text, re.IGNORECASE):
        start = max(0, m.start() - _WINDOW)
        end = min(len(text), m.end() + _WINDOW)
        ctx = text[start:end]
        if not _DISCREDIT_WORDS.search(ctx):
            return False
    return True


def main(workspace: Path) -> int:
    out = workspace / "output" / "ts_diff.md"
    if not out.exists():
        print("FAIL: output/ts_diff.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. v3 split = 55/45 (accept various formats)
    if not re.search(
        r"55\s*/\s*45|55\s*%\s*(?:/\s*)?(?:Mercator|Helios|45)|Mercator\s*55|55\s*Mercator",
        text, re.IGNORECASE
    ):
        print("FAIL: v3 economic split 55/45 not found in ts_diff.md")
        return 1

    # 2. v2 split = 60/40 (must appear; 60/40 is expected for v2)
    if not re.search(r"60\s*/\s*40|60\s*%", text):
        print("FAIL: v2 economic split 60/40 not found in ts_diff.md")
        return 1

    # 3. Chinese draft confirms 55% Mercator / 45% Helios
    cn_ok = re.search(
        r"股权分配[：:]\s*55|55\s*%\s*Mercator|Mercator\s*55\s*%|"
        r"jv_agreement_cn|中文|chinese.*55|55.*chinese",
        text, re.IGNORECASE
    )
    if not cn_ok:
        print(
            "FAIL: Chinese draft (jv_agreement_cn.docx) 55% / 股权分配 55% not confirmed "
            "in ts_diff.md. The Chinese draft must be explicitly compared."
        )
        return 1

    # 4. Board: 3 Mercator + 2 Helios
    if not re.search(r"3\s*(?:Mercator|seats?)\s*\+?\s*2\s*(?:Helios|seats?)|"
                     r"3\s+Mercator.*2\s+Helios|Mercator.*3.*Helios.*2", text, re.IGNORECASE):
        print("FAIL: board composition '3 Mercator + 2 Helios' not found in ts_diff.md")
        return 1

    # Discredit guard: if 60/40 appears in a context suggesting it is the CURRENT v3 split
    # (without a discredit/label word in vicinity) → FAIL
    # Only fail if 60/40 is near v3/current/confirmed without discredit
    for m in re.finditer(r"60\s*/\s*40|60/40", text, re.IGNORECASE):
        start = max(0, m.start() - _WINDOW)
        end = min(len(text), m.end() + _WINDOW)
        ctx = text[start:end]
        # Check if it's labelled as v3 / current / confirmed (without discredit)
        if re.search(r"\bv3\b|current|confirmed|wave3|latest", ctx, re.IGNORECASE):
            if not _DISCREDIT_WORDS.search(ctx):
                print(
                    "FAIL (D-dimension discredit guard): 60/40 appears near v3/current "
                    "context without a discredit word. The v3 split is 55/45; "
                    "60/40 belongs to v2 only."
                )
                return 1

    print(
        "PASS: ts_diff.md has v3=55/45, v2=60/40, Chinese=55%, "
        "board=3+2, discredit guard OK"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
