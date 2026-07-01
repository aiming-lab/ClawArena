#!/usr/bin/env python3
"""check_q2.py (wave3) — verify v3-to-v4 diff + xlsx errata.

锚点：
- v4 true values: 9 months MRR, 99.7%, §7.4(c), 45 days
- FINAL row errata: termination cap wrong=6, correct=9, change_log reference
- binary_archive guard: output must reference unpacking the zip (implicit: model
  got values from docx inside zip, not from filename guessing)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ws = Path(sys.argv[1])
target = ws / "output" / "v3_v4_diff.md"

if not target.exists():
    print(f"FAIL: {target} does not exist")
    sys.exit(1)

content = target.read_text(encoding="utf-8")

# ---- v4 真值（必须全部命中）----
V4_RULES = {
    "termination cap (9 months MRR)": re.compile(r"\b9(?:\.0+)?\s*months?", re.IGNORECASE),
    "SLA 99.7%": re.compile(r"\b99\.7(?:0+)?\s*%", re.IGNORECASE),
    "DPA clause §7.4(c)": re.compile(r"§?\s*7\.4\s*\(\s*c\s*\)", re.IGNORECASE),
    "notice period 45 days": re.compile(r"\b45(?:\.0+)?\s*(?:day|d)s?\b", re.IGNORECASE),
}

missing_v4 = [name for name, rx in V4_RULES.items() if not rx.search(content)]
if missing_v4:
    print(f"FAIL: missing v4 anchors in diff: {missing_v4}")
    sys.exit(1)

# ---- v3 基线引用（至少 2 个锚点）----
v3_anchors = [
    re.compile(r"\b99\.5(?:0+)?\s*%", re.IGNORECASE),
    re.compile(r"\b6(?:\.0+)?\s*months?", re.IGNORECASE),
    re.compile(r"\b30(?:\.0+)?\s*(?:day|d)s?\b", re.IGNORECASE),
    re.compile(r"§?\s*7\.2\s*\(?\s*b?\s*\)?", re.IGNORECASE),
]
v3_hits = sum(1 for rx in v3_anchors if rx.search(content))
if v3_hits < 2:
    print(
        f"FAIL: v3 baseline not referenced enough (matched {v3_hits}/4 anchors); "
        "include v3 values for the four fields."
    )
    sys.exit(1)

# ---- FINAL row errata（xlsx 审计）----
errata_patterns = [
    # FINAL 行
    re.compile(r"\bfinal\b", re.IGNORECASE),
    # 错误值 6（context: wrong / errata / error / v3 / copied / stale）
    re.compile(r"\b6(?:\.0+)?\b", re.IGNORECASE),
    # 正确值 9（context: correct / should be / v4）
    re.compile(r"\b9(?:\.0+)?\b", re.IGNORECASE),
    # change_log 引用
    re.compile(r"change[\s_-]?log|corrected\s+in\s+v4", re.IGNORECASE),
]
missing_errata = []
for pat in errata_patterns:
    if not pat.search(content):
        missing_errata.append(pat.pattern)
if missing_errata:
    print(f"FAIL: xlsx errata section missing patterns: {missing_errata}")
    sys.exit(1)

# ---- 6 必须在 wrong/error/errata 上下文内，9 必须在 correct/v4 上下文内 ----
def _near(pat: str, anchors: list[str], window: int = 150) -> bool:
    text_lower = content.lower()
    for m in re.finditer(pat, text_lower):
        start = max(0, m.start() - window)
        end = m.end() + window
        win = text_lower[start:end]
        if any(a in win for a in anchors):
            return True
    return False

if not _near(r"\b6(?:\.0+)?\b", ["wrong", "errata", "incorrect", "v3", "copied", "error"]):
    print("FAIL: must reference the wrong FINAL-row value (6) in an error context")
    sys.exit(1)
if not _near(r"\b9(?:\.0+)?\b", ["correct", "should be", "v4", "right", "actual", "fix"]):
    print("FAIL: must reference the correct FINAL-row value (9) in a correction context")
    sys.exit(1)

print("PASS")
sys.exit(0)
