"""check_q4.py — output/commitment_gap.md recovers MCN_AM's oral commitment from vlog audio.

Ground truth (from vlog_archive/lin_vlog_20251108_mcn_meeting.mp4, 0:28–0:35):
  MCN_AM says verbatim:
    "...if the platform pushes an algorithm change that cuts traffic by more than
    fifteen percent across the board, we will adjust your unique-view threshold
    down to 3.2 million per video — you have my word on that."

  Transcript trap (C9 / modal mismatch):
    vlog_archive/lin_vlog_20251108_transcript.md marks the critical window as:
    "[inaudible — recording interference]"
    — any agent reading only the transcript finds no commitment.
    — the agent must use an omni subagent on the mp4 to hear the verbatim sentence.

  Gap facts:
    - contract_docs/creator_contract_v2_current.md §4.2: threshold fixed at 3.5M;
      no algorithm-adjustment clause exists.
    - quarterly_reports/q4_2025_report.pdf.md: does not reference the commitment.
    - correspondence/wechat_export_meiqi_bowen.md (2025-11-09):
        MCN_AM writes "Great meeting yesterday, I'll make sure the algorithm
        adjustment gets into the formal addendum" — addendum was never created.

Pass conditions:
  1. File exists; >= 400 bytes; >= 3 distinct labeled sections.
  2. Verbatim commitment — 3.2 million threshold present:
       regex: r"3\\.2\\s*million.*per\\s*video|3\\.2\\s*million.*threshold|threshold.*3\\.2\\s*million"
  3. Verbatim commitment — fifteen-percent traffic trigger present:
       regex: r"fifteen\\s*percent|15\\s*%.*traffic|traffic.*15\\s*%"
  4. Gap identification: commitment is not in the current contract:
       regex: r"not\\s+in\\s+contract|absent.*contract|contract.*no.*mention|oral.*not.*written|unwritten"
  5. WeChat corroboration present:
       regex: r"wechat|addendum.*never|never.*addendum|meiqi.*adden|adden.*meiqi"
  6. Transcript trap guard (C9): if file contains only the "inaudible" note without
       the 3.2M threshold quote, FAIL — agent read only the incomplete transcript.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

THRESHOLD_32M_RE = re.compile(
    r"3\.2\s*million.*per\s*video|3\.2\s*million.*threshold|threshold.*3\.2\s*million|"
    r"3[,.]200[,.]?000",
    re.IGNORECASE,
)
FIFTEEN_PCT_RE = re.compile(
    r"fifteen\s*percent|15(?:\.0+)?\s*%.*traffic|traffic.*15(?:\.0+)?\s*%|"
    r"fifteen.*percent.*traffic|traffic.*fifteen.*percent",
    re.IGNORECASE,
)
GAP_RE = re.compile(
    r"not\s+in\s+contract|absent.*contract|contract.*no.*mention|"
    r"oral.*not.*written|unwritten|not\s+reflected|no\s+written|"
    r"contract.*does\s+not|missing.*contract",
    re.IGNORECASE,
)
WECHAT_RE = re.compile(
    r"wechat|addendum.*never|never.*addendum|meiqi.*adden|adden.*meiqi|"
    r"follow[- ]?up.*message|message.*follow[- ]?up|written.*follow",
    re.IGNORECASE,
)

# Transcript trap guard: agent read only the transcript and found nothing.
INAUDIBLE_ONLY_RE = re.compile(
    r"inaudible|no.*commitment.*found|commitment.*not.*found|no.*oral.*commitment",
    re.IGNORECASE,
)

SECTION_RE = re.compile(r"^#+\s+\S|^\*{2}.+\*{2}\s*$|^---", re.MULTILINE)
MIN_BYTES = 400
MIN_SECTIONS = 3


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q4.py <workspace>", file=sys.stderr)
        return 1
    ws = Path(sys.argv[1])
    target = ws / "output" / "commitment_gap.md"

    if not target.exists():
        print(f"FAIL: {target} does not exist")
        return 1

    text = target.read_text(encoding="utf-8")
    errors: list[str] = []

    if len(text.encode("utf-8")) < MIN_BYTES:
        errors.append(
            f"commitment_gap.md too short ({len(text.encode())} bytes); "
            f"must be >= {MIN_BYTES} bytes"
        )

    section_count = len(SECTION_RE.findall(text))
    if section_count < MIN_SECTIONS:
        errors.append(
            f"commitment_gap.md has fewer than {MIN_SECTIONS} distinct labeled sections "
            f"(found {section_count}); add sections for: (1) oral commitment quote, "
            f"(2) contract gap, (3) WeChat / written evidence"
        )

    # C9 transcript trap guard — must check BEFORE testing for commitment content.
    if INAUDIBLE_ONLY_RE.search(text) and not THRESHOLD_32M_RE.search(text):
        errors.append(
            "C9 transcript trap: commitment_gap.md references 'inaudible' or 'no commitment "
            "found' without quoting the 3.2 million threshold — the transcript has a deliberate "
            "gap at 0:28–0:35; the agent must use an omni subagent on the mp4 to hear MCN_AM's "
            "verbatim commitment; reading only the transcript is insufficient"
        )

    if not THRESHOLD_32M_RE.search(text):
        errors.append(
            "missing MCN_AM's oral commitment — '3.2 million per video' threshold not found; "
            "this must be recovered from the vlog audio (mp4) using an omni subagent; "
            "the transcript marks the critical window as [inaudible]"
        )

    if not FIFTEEN_PCT_RE.search(text):
        errors.append(
            "missing fifteen-percent traffic trigger from MCN_AM's oral commitment "
            "('fifteen percent', '15%', or equivalent); "
            "the full commitment: 'if the platform pushes an algorithm change that cuts "
            "traffic by more than fifteen percent across the board...'"
        )

    if not GAP_RE.search(text):
        errors.append(
            "missing gap identification — file must state that the oral commitment is "
            "not reflected in the current contract §4.2 "
            "('not in contract', 'absent from contract', 'oral commitment not written', etc.)"
        )

    if not WECHAT_RE.search(text):
        errors.append(
            "missing WeChat corroboration — file must reference the WeChat message "
            "from MCN_AM (2025-11-09) about getting the algorithm adjustment into the "
            "formal addendum, which was never created "
            "('WeChat', 'addendum never', 'Meiqi addendum', etc.)"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        "PASS: commitment_gap.md recovers MCN_AM's oral commitment (3.2M threshold, 15% traffic "
        "trigger) from vlog audio, identifies the contract gap, and references the WeChat "
        "follow-up message"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
