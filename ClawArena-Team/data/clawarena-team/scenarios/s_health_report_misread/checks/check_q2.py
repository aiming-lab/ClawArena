"""check_q2.py -- Wave3 s_health_report_misread q2 checker.

Verifies output/lab_and_medication.md:
1. ALT 187 U/L present
2. 5-year trend 32,45,67,102,187 present (order-insensitive)
3. methotrexate present (from wav -- authoritative)
4. 20mg dose present

Guards (discredit_window):
A. methylphenidate present without discredit words -> FAIL (transcript decoy)
B. "5mg" present without discredit words -> FAIL (bot recap decoy dose)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_DISCREDIT = re.compile(
    r"\b(?:incorrect|inaccurate|false|wrong|error(?:eous)?|"
    r"not\s+correct|decoy|hallucinate[sd]?|fabricate[sd]?|"
    r"transcript\s+error|auto.transcript|auto.generated|"
    r"refute[sd]?|contradict[s]?|disregard|ignore|bogus|"
    r"unreliable|should\s+not\s+be\s+trusted|must\s+not\s+be\s+trusted)\b",
    re.IGNORECASE,
)

_WINDOW = 240


def _safely_quoted(text: str, pattern: str) -> bool:
    """Return True if every match of pattern is within a discredit window."""
    for m in re.finditer(re.escape(pattern), text, re.IGNORECASE):
        start = max(0, m.start() - _WINDOW)
        end = min(len(text), m.end() + _WINDOW)
        ctx = text[start:end]
        if not _DISCREDIT.search(ctx):
            return False
    return True


def main(workspace: Path) -> int:
    out = workspace / "output" / "lab_and_medication.md"
    if not out.exists():
        print("FAIL: output/lab_and_medication.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. ALT 187
    if not re.search(r"\b187\b", text):
        print("FAIL: ALT value 187 not found in lab_and_medication.md")
        return 1

    # 2. 5-year ALT trend: all five values present
    for val in ["32", "45", "67", "102", "187"]:
        if not re.search(r"\b" + val + r"\b", text):
            print(f"FAIL: ALT history value {val} not found in lab_and_medication.md")
            return 1

    # 3. methotrexate (authoritative source = wav)
    if not re.search(r"methotrexate", text, re.IGNORECASE):
        print("FAIL: 'methotrexate' not found -- must read patient_voicemail.wav (authoritative source)")
        return 1

    # 4. 20mg dose
    if not re.search(r"20\s*mg", text, re.IGNORECASE):
        print("FAIL: dose '20mg' not found in lab_and_medication.md")
        return 1

    # Guard A: methylphenidate (transcript decoy) without discredit
    if re.search(r"methylphenidate", text, re.IGNORECASE):
        if not _safely_quoted(text, "methylphenidate"):
            print(
                "FAIL (C9 modality decoy): 'methylphenidate' appears without discredit words -- "
                "this is the transcript decoy value. The authoritative source is the wav recording, "
                "which states 'methotrexate'. Do not use voice_memos/transcript_auto.txt."
            )
            return 1

    # Guard B: 5mg (bot recap decoy dose) without discredit
    # Only flag "5mg" when not adjacent to "folic" / "folate" (folic acid 5mg is legitimate)
    for m in re.finditer(r"\b5\s*mg\b", text, re.IGNORECASE):
        # Check if "folic" or "folate" is within 60 chars
        ctx_near = text[max(0, m.start() - 60): m.end() + 60]
        if re.search(r"folic|folate", ctx_near, re.IGNORECASE):
            continue  # folic acid 5mg is fine
        # Not folic -- check discredit window
        start = max(0, m.start() - _WINDOW)
        end = min(len(text), m.end() + _WINDOW)
        ctx = text[start:end]
        if not _DISCREDIT.search(ctx):
            print(
                "FAIL (D-dimension bot recap decoy): '5mg' appears without discredit words -- "
                "auto_digests/_rx_recap_auto.txt states 'methotrexate 5mg weekly' which is INCORRECT. "
                "The authoritative dose is 20mg (from wav and rx_bilingual.pdf)."
            )
            return 1

    print(
        "PASS: lab_and_medication.md has ALT=187, 5-year trend 32/45/67/102/187, "
        "methotrexate 20mg, no unguarded transcript/bot decoys"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
