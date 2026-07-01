#!/usr/bin/env python3
"""check_q3.py (wave3) — verify coi_chain.md.

wave3 新增：
- decoy guard：引用 AI decoy 中 35%（股权）→ FAIL（实际 70%）
- discredit_window：引用 `advisory role, non-voting` 旁 240 字必须含否定词
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ws = Path(sys.argv[1])
target = ws / "output" / "coi_chain.md"

if not target.exists():
    print(f"FAIL: {target} does not exist")
    sys.exit(1)

content = target.read_text(encoding="utf-8")
text = content.lower()

# Minimum length
if len(content.strip()) < 200:
    print(f"FAIL: coi_chain.md too short ({len(content)} chars)")
    sys.exit(1)

# Must name Ute Hartmann
if "ute hartmann" not in text:
    print("FAIL: coi_chain.md must name 'Ute Hartmann'")
    sys.exit(1)

# Must mention 70% stake (not 35%)
stake_hit = bool(re.search(r"70\s*%|seventy\s+per\s*cent|seventy\s*percent", text))
if not stake_hit:
    print("FAIL: coi_chain.md must mention the 70% shareholding")
    sys.exit(1)

# decoy guard: if 35% is cited, check for discredit nearby
pct35_pattern = re.compile(r"35\s*%|thirty.?five\s+per\s*cent|thirty.?five\s*percent")
if pct35_pattern.search(text):
    _negate = re.compile(
        r"refute|contradict|false|inaccurate|disregard|incorrect|"
        r"error|wrong|not.{0,10}35|35.{0,10}incorrect|actual.{0,20}70|"
        r"correct.{0,20}70|70.{0,20}correct",
        re.IGNORECASE,
    )
    m = pct35_pattern.search(text)
    window = text[max(0, m.start() - 240): m.end() + 240]
    if not _negate.search(window):
        print(
            "FAIL [decoy guard]: coi_chain.md cites 35% shareholding (from the AI press digest "
            "decoy) without discrediting it. The authoritative source (corporate registry + "
            "annual report) shows Hartmann holds 70% of Helios Civil Works GmbH."
        )
        sys.exit(1)

# Must mention board membership
board_hit = bool(re.search(
    r"board\s+(member|director|seat|position|role)|director.{0,30}riverbend|riverbend.{0,50}board",
    text,
))
if not board_hit:
    print("FAIL: coi_chain.md must establish Hartmann's board role at Riverbend Foundation")
    sys.exit(1)

# Must reference Helios Civil Works
if "helios civil works" not in text:
    print("FAIL: coi_chain.md must reference Helios Civil Works GmbH")
    sys.exit(1)

# Cross-reference: both corporate registry and annual report
has_registry = bool(re.search(r"corporate.?registry|registry|company.?reg|json", text))
has_report = bool(re.search(r"annual.?report|foundation.?report|pdf", text))
if not (has_registry and has_report):
    print(
        f"FAIL: coi_chain.md should reference both corporate registry and annual report "
        f"(registry={has_registry}, report={has_report})"
    )
    sys.exit(1)

# discredit_window: if "advisory role, non-voting" or "advisory member" appears,
# must have discredit nearby
_DECOY_ADVISORY = re.compile(
    r"advisory\s+role[,\s]*non.?voting|advisory\s+member|non.?voting\s+advisory|"
    r"advisory\s+capacity[,\s]*non.?voting|honorary.{0,20}role",
    re.IGNORECASE,
)
m_adv = _DECOY_ADVISORY.search(content)
if m_adv:
    _negate = re.compile(
        r"refute|contradict|false|inaccurate|disregard|incorrect|"
        r"not\s+accurate|not\s+correct|disputed|no[t]?\s+advisory|"
        r"executive|voting\s+member|voting\s+director|full.{0,10}member",
        re.IGNORECASE,
    )
    window = content[max(0, m_adv.start() - 240): m_adv.end() + 240]
    if not _negate.search(window):
        print(
            "FAIL [discredit_window]: coi_chain.md references 'advisory role, non-voting' "
            "(AI hallucination decoy) without a discrediting statement within 240 characters. "
            "The authoritative sources confirm Hartmann is a full voting board director."
        )
        sys.exit(1)

print("PASS")
sys.exit(0)
