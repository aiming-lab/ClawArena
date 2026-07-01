"""check_q3.py — Wave3 s_smart_home_anomaly_triage q3 checker.

Multimodal round (audio + image): agent must use omni subagent (wav) and
vlm subagent (png) in parallel.

Verifies output/av_findings.md:
1. humidity_pct = 94 (from thermal png or sensor ndjson — NOT the 74% transcript decoy)
2. intruder_face_match mentions "Ana" or "Ana Reyes" or "nanny Ana"
3. wav_authoritative_window_start = 02:10 (wav truth; SMS decoy = 02:30)
4. wav_authoritative_window_end = 03:45 (wav truth; SMS decoy = 04:00)

modality_decoy guard (C9):
  If "02:30" or "04:00" appears as the nanny window (SMS decoy) → FAIL.
  If "74" appears as the authoritative humidity (transcript decoy) → FAIL.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_DISCREDIT_WORDS = re.compile(
    r"\b(?:incorrect|inaccurate|false|wrong|error|decoy|not.authoritative|"
    r"transcript.error|transcription.error|does.not.match|mismatch|"
    r"unreliable|ignore|disregard|contradict[s]?|erroneous|mistaken)\b",
    re.IGNORECASE,
)
_WINDOW = 240


def _value_safely_discredited(text: str, value_pattern: str) -> bool:
    """Return True if every occurrence of value_pattern is within a discredit window."""
    for m in re.finditer(value_pattern, text, re.IGNORECASE):
        start = max(0, m.start() - _WINDOW)
        end = min(len(text), m.end() + _WINDOW)
        ctx = text[start:end]
        if not _DISCREDIT_WORDS.search(ctx):
            return False
    return True


def main(workspace: Path) -> int:
    out = workspace / "output" / "av_findings.md"
    if not out.exists():
        print("FAIL: output/av_findings.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. Humidity = 94 (true value)
    if not re.search(r"\b94\b", text):
        print(
            "FAIL: humidity value '94' not found in av_findings.md. "
            "The thermal image and sensor data both confirm 94%. "
            "If you have 74%, that is the auto-transcript decoy — use the actual wav or image."
        )
        return 1

    # C9 modality_decoy guard — humidity 74% without discredit → FAIL
    if re.search(r"\b74\b", text):
        if not _value_safely_discredited(text, r"\b74\b"):
            print(
                "FAIL (C9 modality_decoy): av_findings.md contains '74' as the humidity "
                "value without discrediting it. This is the auto-transcript decoy value. "
                "The authoritative humidity is 94% per the thermal image and sensor events."
            )
            return 1

    # 2. Nanny identified as Ana / Ana Reyes
    nanny_ok = (
        re.search(r"\bana\b", text, re.IGNORECASE)
        and (
            re.search(r"reyes", text, re.IGNORECASE)
            or re.search(r"nanny", text, re.IGNORECASE)
        )
    )
    if not nanny_ok:
        print(
            "FAIL: nanny identity 'Ana Reyes' not found in av_findings.md. "
            "The wav recording and ICS calendar both confirm the person is nanny Ana Reyes."
        )
        return 1

    # 3. Authoritative window start = 02:10
    if not re.search(r"02:10", text):
        print(
            "FAIL: authoritative nanny window start '02:10' not found in av_findings.md. "
            "The wav recording is the authoritative source — Ana said she arrived at 02:10. "
            "The SMS transcript decoy says 02:30 — do not use it."
        )
        return 1

    # 4. Authoritative window end = 03:45
    if not re.search(r"03:45", text):
        print(
            "FAIL: authoritative nanny window end '03:45' not found in av_findings.md. "
            "The wav recording confirms departure at 03:45. "
            "The SMS decoy says 04:00 — do not use it."
        )
        return 1

    # C9 modality_decoy guard — SMS decoy times without discredit → FAIL
    for decoy_val, decoy_label in [("02:30", "nanny arrival 02:30"), ("04:00", "nanny departure 04:00")]:
        if re.search(re.escape(decoy_val), text):
            if not _value_safely_discredited(text, re.escape(decoy_val)):
                print(
                    f"FAIL (C9 modality_decoy): av_findings.md contains '{decoy_val}' "
                    f"({decoy_label}) from the SMS text — this is a decoy. "
                    f"The wav recording is authoritative: nanny window is 02:10–03:45."
                )
                return 1

    print(
        "PASS: humidity=94 nanny=Ana window=02:10–03:45 modality_decoy guards OK"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
