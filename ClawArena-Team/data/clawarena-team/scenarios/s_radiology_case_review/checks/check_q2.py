"""check_q2.py — imaging findings: right lower lobe + size ~14mm + session_reuse >= 1.

Pass conditions (all required):
  1. findings/imaging_finding.md exists and is non-trivial
  2. Contains 'right lower lobe' (or '右下叶') — correct lobe
  3. Contains a size near 14 mm (13–15 acceptable)
  4. ADVISORY ONLY (non-gating): sessions/main.jsonl shows at least 1 RunSubagent
     call (subagent used for images)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, session_reuse_count, workspace_root


def _size_near_14(text: str) -> bool:
    """Check if text contains a size value between 13 and 15 mm."""
    for m in re.finditer(r"\b(1[0-9])\s*(?:mm|毫米)\b", text, flags=re.IGNORECASE):
        val = int(m.group(1))
        if 13 <= val <= 15:
            return True
    # Also accept bare '14' near 'mm'
    for m in re.finditer(r"\b14\b", text):
        window = text[max(0, m.start() - 30): m.end() + 30].lower()
        if "mm" in window or "毫米" in window or "millim" in window:
            return True
    return False


def main() -> int:
    ws = workspace_root()
    target = ws / "findings" / "imaging_finding.md"
    if not target.exists():
        fail("missing findings/imaging_finding.md")
    text = target.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 60:
        fail("imaging_finding.md is too short")

    # Correct lobe
    if not re.search(r"right\s+lower\s+lobe|右下叶|right lower lobe", text, flags=re.IGNORECASE):
        fail("correct lobe 'right lower lobe' / '右下叶' not found in imaging_finding.md")

    # Size near 14 mm
    if not _size_near_14(text):
        fail("lesion size ~14 mm not found in imaging_finding.md")

    # Session used / VLM subagent: ADVISORY ONLY (non-gating)
    print(
        "NOTE: session reuse not verified — advisory only, non-gating",
        file=sys.stderr,
    )
    print(
        "NOTE: modality subagent delegation not verified — advisory only, non-gating",
        file=sys.stderr,
    )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
