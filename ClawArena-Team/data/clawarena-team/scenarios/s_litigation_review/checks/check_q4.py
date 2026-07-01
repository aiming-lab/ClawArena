#!/usr/bin/env python3
"""check_q4.py — Validate q4: audio_vs_transcript.md discrepancy report.

C9 model-mismatch trap: the auto-transcript (meetings/transcript_2026-03-22.md)
states dates that the audio (audio/hearing_2026-03-22.wav) contradicts.

Ground truth (from narration_script.md / manifest_gen.json):
  PIP start date:   transcript says "March 22, 2026"  |  audio says "March 15, 2026"
  Earliest eval:    transcript says "April 21, 2026"   |  audio says "April 14, 2026"

Pass conditions (all must hold; exit 0):
  1. notes/audio_vs_transcript.md exists.
  2. Both the WRONG (transcript) value AND the CORRECT (audio) value are present
     for the PIP start date discrepancy:
       - transcript value "March 22" / "2026-03-22"
       - audio value "March 15" / "2026-03-15"
  3. A discrepancy-word anchor is present (discrepan / mismatch / conflict /
     differ / incorrect / inaccura / contradict / error).
  4. The audio is explicitly identified as the authoritative source — one of:
       "audio … authoritative", "authoritative … audio",
       "audio … correct", "recording … authoritative",
       "authoritative … recording", "transcript … incorrect",
       "transcript … error", "transcript … inaccura", "auto-generated", "ASR".
  5. Hard-fail guard: if the note mentions ONLY the transcript's wrong value
     for the start date (March 22 / 2026-03-22) WITHOUT also mentioning the
     correct audio value (March 15 / 2026-03-15), the check fails even if a
     discrepancy word is present.  This catches modality-mismatch — the agent
     read the transcript only and never consulted the audio.

Usage: python check_q4.py <workspace_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


# --- Transcript (WRONG) values ---
TRANSCRIPT_DATE_RE = re.compile(
    r"March\s+22|2026-03-22|2026/03/22|03[/-]22[/-]2026",
    re.IGNORECASE,
)

# --- Audio (CORRECT) values ---
AUDIO_DATE_RE = re.compile(
    r"March\s+15|2026-03-15|2026/03/15|03[/-]15[/-]2026",
    re.IGNORECASE,
)

# --- Discrepancy vocabulary ---
DISCREPANCY_RE = re.compile(
    r"discrepan|mismatch|conflict|differ|incorrect|inaccura|contradict|error",
    re.IGNORECASE,
)

# --- Authority statements (audio is authoritative) ---
AUTHORITY_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"audio.{0,60}authoritative|authoritative.{0,60}audio", re.IGNORECASE | re.DOTALL),
    re.compile(r"audio.{0,60}correct|correct.{0,60}audio", re.IGNORECASE | re.DOTALL),
    re.compile(r"recording.{0,60}authoritative|authoritative.{0,60}recording", re.IGNORECASE | re.DOTALL),
    re.compile(r"transcript.{0,60}incorrect|incorrect.{0,60}transcript", re.IGNORECASE | re.DOTALL),
    re.compile(r"transcript.{0,60}error|error.{0,60}transcript", re.IGNORECASE | re.DOTALL),
    re.compile(r"transcript.{0,60}inaccura|inaccura.{0,60}transcript", re.IGNORECASE | re.DOTALL),
    re.compile(r"auto[\s-]?generated", re.IGNORECASE),
    re.compile(r"\bASR\b"),
    re.compile(r"trust.{0,30}audio|trust.{0,30}recording", re.IGNORECASE | re.DOTALL),
]


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q4.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    f = ws / "notes" / "audio_vs_transcript.md"

    if not f.exists():
        print("FAIL: notes/audio_vs_transcript.md does not exist")
        return 1

    content = f.read_text(encoding="utf-8")
    errors: list[str] = []

    has_transcript_date = TRANSCRIPT_DATE_RE.search(content) is not None
    has_audio_date = AUDIO_DATE_RE.search(content) is not None

    # 2. Both wrong and correct values present
    if not has_audio_date:
        errors.append(
            "the correct PIP start date from the audio (March 15 / 2026-03-15) "
            "is not mentioned — the note must state both the transcript's wrong value "
            "AND the audio's correct value for each discrepancy"
        )

    # 5. Hard-fail: only transcript value, no audio value  →  modality-mismatch trap
    if has_transcript_date and not has_audio_date:
        errors.append(
            "HARD-FAIL (modality mismatch): the note cites the transcript's start date "
            "(March 22) but never mentions the audio's correct date (March 15) — "
            "this indicates the audio was never consulted; the audio is the authoritative source"
        )

    # 3. Discrepancy vocabulary
    if not DISCREPANCY_RE.search(content):
        errors.append(
            "no discrepancy-word anchor found "
            "(discrepancy / mismatch / conflict / differ / incorrect / inaccurate / "
            "contradict / error)"
        )

    # 4. Audio explicitly identified as authoritative
    if not any(p.search(content) for p in AUTHORITY_PATTERNS):
        errors.append(
            "the audio is not explicitly identified as the authoritative source — "
            "add a statement such as 'the audio is authoritative', "
            "'the transcript is incorrect', or 'auto-generated transcript'"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        "PASS: audio_vs_transcript.md states both the transcript's wrong date and the "
        "audio's correct date (March 15 / 2026-03-15), with a discrepancy description "
        "and explicit identification of the audio as authoritative"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
