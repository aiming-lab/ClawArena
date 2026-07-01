"""check_q3.py -- Wave3 s_health_report_misread q3 checker.

Verifies output/imaging_summary.md:
1. "Grade II" present (from mp4 frames 12-16s -- unique source)
2. "mild hepatic steatosis without focal lesion" present (or close variant)

Guard:
C. "Grade I" present without discredit words -> FAIL (imaging/transcript_auto.txt decoy)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_DISCREDIT = re.compile(
    r"\b(?:incorrect|inaccurate|false|wrong|error(?:eous)?|"
    r"not\s+correct|decoy|hallucinate[sd]?|fabricate[sd]?|"
    r"refute[sd]?|contradict[s]?|disregard|ignore|bogus|"
    r"auto.transcript|transcript\s+error|auto.generated|"
    r"should\s+not\s+be\s+trusted|must\s+not\s+be\s+trusted)\b",
    re.IGNORECASE,
)

_WINDOW = 240


def main(workspace: Path) -> int:
    out = workspace / "output" / "imaging_summary.md"
    if not out.exists():
        print("FAIL: output/imaging_summary.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. Grade II (from mp4 grading frames at 12-16s)
    if not re.search(r"Grade\s*II", text, re.IGNORECASE):
        print(
            "FAIL: 'Grade II' not found in imaging_summary.md -- "
            "this value only appears in liver_scan_replay.mp4 frames at 12-16 seconds. "
            "Use a vision-capable subagent to read those frames."
        )
        return 1

    # 2. Mild hepatic steatosis without focal lesion
    if not re.search(r"mild\s+hepatic\s+steatosis", text, re.IGNORECASE):
        print(
            "FAIL: 'mild hepatic steatosis' not found in imaging_summary.md -- "
            "this phrase appears in ultrasound_snapshot_*.png and encrypted_report.pdf."
        )
        return 1

    if not re.search(r"without\s+focal\s+lesion|no\s+focal\s+lesion", text, re.IGNORECASE):
        print(
            "FAIL: 'without focal lesion' (or equivalent) not found in imaging_summary.md"
        )
        return 1

    # Guard C: Grade I (imaging transcript decoy) without discredit
    for m in re.finditer(r"Grade\s*I\b(?!\s*I)", text, re.IGNORECASE):
        start = max(0, m.start() - _WINDOW)
        end = min(len(text), m.end() + _WINDOW)
        ctx = text[start:end]
        if not _DISCREDIT.search(ctx):
            print(
                "FAIL (C9 imaging transcript decoy): 'Grade I' appears without discredit words -- "
                "imaging/transcript_auto.txt incorrectly states 'Grade I (灰阶评分 1 分)'. "
                "The authoritative grading (Grade II) is only in the mp4 video frames at 12-16s."
            )
            return 1

    print(
        "PASS: imaging_summary.md has Grade II, mild hepatic steatosis without focal lesion, "
        "no unguarded Grade I decoy"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
