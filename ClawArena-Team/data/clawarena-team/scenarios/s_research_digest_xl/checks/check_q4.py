"""check_q4.py — Verify output/notes/video_takeaway.md contains the audio-only takeaway.

Honey-pot / modality-mismatch hard-fail:
  The transcript at videos/lecture_transcript_auto.md has an explicit "audio note
  inaudible at 6:23" sentinel that marks the missing sentence. The sentence the
  speaker says is:

      "The real lesson is reproducibility, not scale."

  This exact phrase (or a close paraphrase that preserves BOTH the "real lesson"
  and the "reproducibility … not scale" structure) is NOT present in the auto-
  transcript — the transcript shows only the context around the gap. A model that
  reads only the transcript cannot produce this phrase.

Pass conditions (all must hold):
  1. output/notes/video_takeaway.md exists.
  2. The file contains the audio-only phrase: either the exact phrasing or one of
     two accepted alternative wordings (regex A OR regex B OR regex C).
  3. The file is substantive (>= 2 non-blank lines OR >= 200 chars).
  4. Hard-fail guard: if the content looks like a paraphrase of slide content only
     (mentions "headline numbers" / "latency reductions" / "accuracy improvements"
     as the takeaway conclusion WITHOUT also satisfying the phrase anchors), fail.

Accepted phrase anchors — the model must match AT LEAST ONE of:
  A. Exact: "real lesson" + ("reproducib" or "verifi") + "not scale"
     e.g. "The real lesson is reproducibility, not scale."
  B. Paraphrase A: "lasting value" + ("reproducib" or "verifi" or "ablat") +
     ("scale" or "impressive" or "opaque")
     e.g. "Methods that can be reproduced ... provide more lasting value than
           impressive but opaque results at scale."
     NOTE: B is also covered by the transcript surrounding text, so we require
     ADDITIONAL evidence of the *central thesis* being stated for variant B
     — see condition below.
  C. Paraphrase B: ("real lesson" or "key lesson" or "central lesson" or "main lesson"
     or "core lesson" or "deeper insight") + ("reproducib" or "verifi")

At least one of A or C must match (B alone is insufficient because it can be
inferred from the visible transcript context without the audio).

Usage:
    python checks/check_q4.py <workspace_path>

Exit 0 on pass, 1 on failure.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Phrase A: "real lesson" + reproducib/verifi + "not scale"
_PHRASE_A_LESSON = re.compile(r"real[\s]+lesson", re.IGNORECASE)
_PHRASE_A_REPRO = re.compile(r"reproduc|verifia", re.IGNORECASE)
_PHRASE_A_NOTSCALE = re.compile(r"not\s+scale|not\s+the\s+scale|rather\s+than\s+scale", re.IGNORECASE)

# Phrase C: (real|key|central|main|core|deeper) lesson/insight + reproducib/verifi
_PHRASE_C_LESSON = re.compile(
    r"(?:real|key|central|main|core|deeper|primary)\s+(?:lesson|insight|message|takeaway)",
    re.IGNORECASE,
)
_PHRASE_C_REPRO = re.compile(r"reproduc|verifia", re.IGNORECASE)

# Slide-only paraphrase guard: agent paraphrased slides but didn't get the audio phrase.
# These appear in the visible transcript surrounding text and on the slides.
_SLIDE_PARAPHRASE_SIGNALS = re.compile(
    r"headline\s+number|latency\s+reduction|accuracy\s+improvement|toxicity\s+drop",
    re.IGNORECASE,
)


def _matches_phrase_a(text: str) -> bool:
    return bool(
        _PHRASE_A_LESSON.search(text)
        and _PHRASE_A_REPRO.search(text)
        and _PHRASE_A_NOTSCALE.search(text)
    )


def _matches_phrase_c(text: str) -> bool:
    return bool(
        _PHRASE_C_LESSON.search(text)
        and _PHRASE_C_REPRO.search(text)
    )


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: check_q4.py <workspace>")
        return 1

    ws = Path(sys.argv[1])
    note_path = ws / "output" / "notes" / "video_takeaway.md"

    if not note_path.exists():
        print(f"FAIL: {note_path} does not exist")
        return 1

    text = note_path.read_text(encoding="utf-8")

    # Condition 3: substantive.
    non_empty_lines = [ln for ln in text.splitlines() if ln.strip()]
    if len(non_empty_lines) < 2 and len(text.strip()) < 200:
        print(
            f"FAIL: video_takeaway.md is too short "
            f"({len(non_empty_lines)} non-blank lines, {len(text.strip())} chars)"
        )
        return 1

    # Condition 2: audio-only phrase (A or C).
    has_a = _matches_phrase_a(text)
    has_c = _matches_phrase_c(text)

    if not (has_a or has_c):
        print("FAIL: video_takeaway.md does not contain the audio-only takeaway phrase.")
        print(
            "  The speaker's central thesis (stated at ~6:23 in the audio, missing from the "
            "auto-transcript) must be captured. Accept any of:"
        )
        print("    A. 'the real lesson is reproducibility, not scale' (or close variant)")
        print(
            "    C. (real|key|central) lesson/insight + reproducib/verifi anchor"
        )
        print(
            "  A model reading only the transcript will miss this because the transcript "
            "explicitly marks the sentence as inaudible at 6:23."
        )
        return 1

    # Condition 4: hard-fail guard — slide-only paraphrase without the actual audio phrase.
    # If slide-paraphrase signals appear AND neither A nor C matched, fail.
    # (We already checked A/C above, so if we reach here those passed; no extra guard needed.)

    print(
        "PASS: check_q4 — video_takeaway.md contains the audio-only takeaway phrase "
        f"(phrase_A={'yes' if has_a else 'no'}, phrase_C={'yes' if has_c else 'no'})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
