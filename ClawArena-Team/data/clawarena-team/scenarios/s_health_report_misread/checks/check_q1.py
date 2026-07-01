"""check_q1.py -- Wave3 s_health_report_misread q1 checker.

Verifies output/triage_plan.md:
- File exists
- >= 5 section headings
- Mentions patient code P-20260517
- Mentions "encrypt" (recognizes encrypted PDF needs decryption)
- Mentions mp4 or video or frame (recognizes video frame extraction needed)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def main(workspace: Path) -> int:
    out = workspace / "output" / "triage_plan.md"
    if not out.exists():
        print("FAIL: output/triage_plan.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. >= 5 section headings
    headings = re.findall(
        r"(?m)^(?:#{1,4}\s+.+|(?:\*{1,2}|\d+[\.\)])\s+\S.{3,})",
        text,
    )
    if len(headings) < 5:
        print(f"FAIL: found {len(headings)} section headings, need >= 5")
        return 1

    # 2. Patient code P-20260517
    if not re.search(r"P-20260517", text):
        print("FAIL: patient code P-20260517 not mentioned in triage_plan.md")
        return 1

    # 3. Mentions encryption (encrypted_report.pdf needs decryption)
    if not re.search(r"encrypt", text, re.IGNORECASE):
        print("FAIL: 'encrypt' not mentioned -- plan must note encrypted_report.pdf needs decryption")
        return 1

    # 4. Mentions mp4 or video or frame (liver_scan_replay.mp4 frame extraction)
    if not re.search(r"mp4|video|frame|replay", text, re.IGNORECASE):
        print("FAIL: 'mp4' or 'video' or 'frame' not mentioned -- plan must note video frame extraction")
        return 1

    # 5. Mentions liver / ALT / hepatic concern
    if not re.search(r"liver|ALT|hepatic|transaminase", text, re.IGNORECASE):
        print("FAIL: liver function concern (liver/ALT/hepatic) not mentioned")
        return 1

    print(
        f"PASS: triage_plan.md has {len(headings)} headings, P-20260517, "
        f"encrypt, video/frame references, liver concern"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
