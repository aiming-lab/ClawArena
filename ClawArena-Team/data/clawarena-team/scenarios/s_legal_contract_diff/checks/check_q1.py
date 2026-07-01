#!/usr/bin/env python3
"""check_q1.py (wave3) — verify the partner work plan.

Wave3 升级点：除 wave2 的 5 section + 双方 + MSA + Q3 要求外，
还需至少 1 处提及解压（zip / unzip / extract / decompress）
或 encrypted docx / bilingual（G 维度意识）。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ws = Path(sys.argv[1])
target = ws / "output" / "work_plan.md"

if not target.exists():
    print(f"FAIL: {target} does not exist")
    sys.exit(1)

content = target.read_text(encoding="utf-8")
text = content.lower()

# ---- 结构层：≥ 5 section marker ----
section_markers = []
for ln in content.splitlines():
    stripped = ln.strip()
    if re.match(r"^#{1,4}\s+\S", stripped):
        section_markers.append(stripped[:80])
    elif re.match(r"^\d+\.\s+\S", stripped):
        section_markers.append(stripped[:80])
    elif re.match(r"^[-*•]\s+\*\*[^*]+\*\*", stripped):
        section_markers.append(stripped[:80])
    elif re.match(r"^\*\*[^*]+\*\*\s*$", stripped):
        section_markers.append(stripped[:80])

if len(section_markers) < 5:
    print(
        f"FAIL: need ≥5 section markers (heading / bold-numbered / ordered-list); "
        f"found {len(section_markers)}: {section_markers}"
    )
    sys.exit(1)

# ---- 长度下限 ----
if len(content.strip()) < 400:
    print(f"FAIL: work plan too short ({len(content)} chars)")
    sys.exit(1)

# ---- 真值层：5 工作主题各自的关键词 ----
topics = [
    [r"contract", r"v3", r"v4", r"diff", r"docx", r"zip"],
    [r"matrix", r"xlsx", r"errata", r"clause", r"spread"],
    [r"signature", r"sign[- ]?off", r"signed", r"pdf"],
    [r"voice\s*memo", r"voicemail", r"external\s+counsel", r"audio", r"wav",
     r"encrypt", r"bilingual", r"annex", r"decry"],
    [r"partner\s+email", r"email\s+to\s+karen", r"deliverable", r"final\s+email",
     r"yaml", r"report", r"audit"],
]
missing_topics = []
for i, kws in enumerate(topics, start=1):
    if not any(re.search(p, text) for p in kws):
        missing_topics.append((i, kws[:3]))
if missing_topics:
    print(f"FAIL: work plan missing topic markers for areas: {missing_topics}")
    sys.exit(1)

# ---- 必须 mention 双方 + MSA + Q3 ----
parties = re.search(r"goldenleaf", text) and re.search(r"mercator", text)
deal = re.search(r"msa\b|master\s+services", text)
q3 = re.search(r"\bq3\b", text)
if not (parties and deal and q3):
    print(
        f"FAIL: must mention both parties, MSA, and Q3 "
        f"(parties={bool(parties)}, deal={bool(deal)}, q3={bool(q3)})"
    )
    sys.exit(1)

# ---- wave3 新增：zip / encrypted docx 意识 ----
zip_aware = re.search(
    r"unzip|extract|decompress|zip|encrypt|bilingual|wilkins2026|contracts_bundle",
    text
)
if not zip_aware:
    print(
        "FAIL: work plan must mention unzipping the contract bundle or decrypting "
        "the bilingual annex (zip / unzip / extract / encrypted / bilingual / wilkins2026)"
    )
    sys.exit(1)

print("PASS")
sys.exit(0)
