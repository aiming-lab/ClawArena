"""check_q2.py — wave3 s_hospital_safety_event_review q2 checker.

Verifies output/event_evidence.md:
  1. File exists
  2. Contains wav-authoritative root cause phrase (not transcript decoy)
     - Must mention: "dose preset" and "mg/h" and "mcg/h" proximity
       OR verbatim: "dose preset menu defaulted to mg/h"
  3. Firmware version 2.18.3 present
  4. X-ray finding: bilateral pulmonary edema (from imaging_archive)
  5. Dose error value 12.0 present

C9 modality-decoy guard:
  - If 'nurse misprogramming' appears and NOT discredited in 240-char window → FAIL
    (model used transcript_auto.txt decoy instead of wav)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# NOTE: the bare token `error` was intentionally removed. The check below
# mandates the literal dose value "12.0", and natural phrasing such as
# "dose error value 12.0" placed the standalone word `error` inside the
# 240-char discredit window of the `nurse misprogramming` decoy, causing the
# C9 guard to treat the decoy as discredited and PASS a wrong-root-cause
# answer. The remaining discredit tokens (transcription.error, erroneous,
# incorrect, inaccurate, …) still match a genuine refutation that targets the
# decoy, but the standalone `error` no longer leaks through the dose value.
_DISCREDIT = re.compile(
    r"\b(?:incorrect|inaccurate|false|wrong|not accurate|transcription.error|"
    r"disregard|ignore|decoy|mislabelled|misidentified|auto.generated|"
    r"contradicts|refutes?|erroneous|inaccurate|not.authoritative)\b",
    re.IGNORECASE,
)
_WINDOW = 240


def main(workspace: Path) -> int:
    out = workspace / "output" / "event_evidence.md"
    if not out.exists():
        print("FAIL: output/event_evidence.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. Wav-authoritative root cause phrase
    # Accept: "dose preset menu defaulted to mg/h" or "mg/h instead of mcg/h"
    # or "defaulted to mg/h" or "preset.*mg/h" combinations
    wav_cause_patterns = [
        r"dose\s+preset\s+menu\s+defaulted",
        r"dose\s+preset.*mg/h",
        r"defaulted\s+to\s+mg/h",
        r"mg/h\s+instead\s+of\s+mcg/h",
        r"unit.mode.+mg/h.+firmware",
        r"firmware.+unit.mode.*mg/h",
    ]
    wav_found = any(re.search(p, text, re.IGNORECASE) for p in wav_cause_patterns)
    if not wav_found:
        print(
            "FAIL: wav-authoritative root cause phrase not found in event_evidence.md. "
            "Expected: 'dose preset menu defaulted to mg/h' or equivalent. "
            "Use the Q&S briefing WAV — not the auto-transcript."
        )
        return 1

    # 2. Firmware version 2.18.3
    if not re.search(r"2\.18\.3", text):
        print("FAIL: firmware version 2.18.3 not found in event_evidence.md")
        return 1

    # 3. X-ray finding: bilateral pulmonary edema
    if not re.search(r"bilateral\s+pulmonary\s+edema", text, re.IGNORECASE):
        print(
            "FAIL: 'bilateral pulmonary edema' not found in event_evidence.md. "
            "This comes from xray_report_annotated.png in imaging_archive.tar.gz "
            "(must decompress archive first, then use VLM subagent)."
        )
        return 1

    # 4. Dose error value 12.0
    if not re.search(r"12\.0", text):
        print("FAIL: dose error value '12.0' not found in event_evidence.md")
        return 1

    # C9 modality-decoy guard
    for m in re.finditer(r"nurse\s+misprogramming", text, re.IGNORECASE):
        start = max(0, m.start() - _WINDOW)
        end = min(len(text), m.end() + _WINDOW)
        ctx = text[start:end]
        if not _DISCREDIT.search(ctx):
            print(
                "FAIL (C9 modality-decoy): 'nurse misprogramming' appears as root cause "
                "without being discredited. This is the transcript_auto.txt DECOY — "
                "the WAV recording is authoritative: root cause is firmware unit-mode bug."
            )
            return 1

    print(
        "PASS: event_evidence.md has wav root cause + firmware 2.18.3 + "
        "bilateral pulmonary edema + dose 12.0; C9 guard OK"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
