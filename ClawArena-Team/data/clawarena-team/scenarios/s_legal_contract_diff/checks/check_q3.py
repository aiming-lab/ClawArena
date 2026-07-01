#!/usr/bin/env python3
"""check_q3.py (wave3) — verify audio + encrypted docx review.

锚点：
- sla_true: 99.9%（wav 真值，verbal amendment）
- liability_cap: 150%（encrypted docx 中英对照，均可命中）
- multilingual guard: 中文"终止条款"或英文"Termination"均接受
- C9 guard: 99.5% 出现即 fail（v3 decoy）
- 99.7% 作为 v4 draft 值也不应被当作最终 SLA

产出文件：output/audio_and_encrypted_review.md
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ws = Path(sys.argv[1])
target = ws / "output" / "audio_and_encrypted_review.md"

if not target.exists():
    print(f"FAIL: {target} does not exist")
    sys.exit(1)

content = target.read_text(encoding="utf-8")
text = content.lower()

# ---- 1. wav 真值 99.9%（音频修订）----
sla_true = re.search(r"\b99\.9(?:0+)?\s*%?", content, re.IGNORECASE)
if not sla_true:
    print("FAIL: audio_and_encrypted_review.md must contain 99.9% (the verbal SLA amendment from the wav)")
    sys.exit(1)

# ---- 2. encrypted docx 赔偿封顶 150%（中英双语均可命中）----
cap_150_en = re.search(r"150\s*%|one\s+hundred\s+and\s+fifty\s*(?:per\s*cent|%)?", text)
cap_150_zh = re.search(r"150\s*%|百分之一百五十|合同总价的\s*150", content)
if not (cap_150_en or cap_150_zh):
    print(
        "FAIL: must contain the liability cap 150% from the encrypted docx "
        "(either English '150%' or Chinese '合同总价的 150%' / '百分之一百五十')"
    )
    sys.exit(1)

# ---- 3. multilingual guard：需提及 Termination 或 终止条款 ----
termination_mentioned = (
    re.search(r"\btermination\b", text)
    or re.search(r"终止条款|终止", content)
)
if not termination_mentioned:
    print("FAIL: must reference 'Termination' (English) or '终止条款' (Chinese) from the annex")
    sys.exit(1)

# ---- 4. C9 honey-pot guard：99.5% 出现即 fail（v3 decoy，不是 verbal value）----
c9_decoy = re.search(r"\b99\.5(?:0+)?\s*%?", content, re.IGNORECASE)
if c9_decoy:
    # 检查 99.5 附近 300 字内是否有否定词（如明确标注为 decoy / wrong / incorrect）
    m = c9_decoy
    start = max(0, m.start() - 300)
    end = m.end() + 300
    window = text[start:end]
    negate = re.search(
        r"wrong|incorrect|decoy|not\s+the|error|false|inaccur|refute|discard|"
        r"v3\s+draft|old\s+value|transcript\s+error|transcript\s+decoy",
        window,
    )
    if not negate:
        print(
            "FAIL: 99.5% appears in the output without being explicitly identified as "
            "incorrect/a decoy. 99.5% is the v3 draft value (and possible transcript "
            "transcription error), NOT the verbally agreed SLA. The wav true value is 99.9%."
        )
        sys.exit(1)

# ---- 5. 产出必须有 wav 来源和 encrypted docx 来源的清晰分区 ----
has_wav_reference = re.search(r"wav|voice\s*memo|counsel|audio|verbal|spoken", text)
has_encrypted_reference = re.search(
    r"encrypt|decrypt|wilkins|bilingual|annex|中英|双语|password", text
)
if not has_wav_reference:
    print("FAIL: output must reference the wav / voice memo as source for SLA value")
    sys.exit(1)
if not has_encrypted_reference:
    print(
        "FAIL: output must reference the encrypted docx / bilingual annex as source "
        "for the liability cap"
    )
    sys.exit(1)

print("PASS")
sys.exit(0)
