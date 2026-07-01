"""check_q3.py — symptom correlation: bilingual chief complaint.

Pass conditions (all required, fatal):
  1. notes/symptom_correlation.md exists and is non-trivial
  2. Contains 'cough 3 weeks' (or equivalent: 'three weeks', '3 weeks', '3-week cough')
  3. Contains '咳嗽' (Chinese cough keyword)

Session reuse (same subagent session reused from q2) is a FATAL gate, keyed on
the real continuation signal: the harness only continues a session when the SAME
``session_id`` is threaded back into RunSubagent (``new_session = session_id is
None or session_id not in harnesses``). Passing a ``subagent_id`` without a
``session_id`` spawns a fresh session every round, so we require some non-empty
``session_id`` to appear >= 2 times. All content checks above remain fatal too.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, has_phrase_any, passed, run_subagent_session_id_counts, workspace_root


def main() -> int:
    ws = workspace_root()
    target = ws / "notes" / "symptom_correlation.md"
    if not target.exists():
        fail("missing notes/symptom_correlation.md")
    text = target.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 60:
        fail("symptom_correlation.md is too short")

    # English chief complaint
    if not re.search(r"cough.{0,20}(?:3|three)\s*weeks?|(?:3|three)[- ]week.{0,10}cough", text, flags=re.IGNORECASE):
        fail("chief complaint 'cough 3 weeks' (or '3-week cough') not found in symptom_correlation.md")

    # Chinese cough keyword
    if "咳嗽" not in text:
        fail("Chinese keyword '咳嗽' not found in symptom_correlation.md")

    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    sess_counts = run_subagent_session_id_counts(ws)
    if not sess_counts or max(sess_counts.values()) < 2:
        fail(
            "genuine session reuse not observed — the task asked you to continue the same "
            "subagent session (thread the same session_id), not spawn a fresh one each round"
        )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
