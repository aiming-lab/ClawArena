"""check_q5.py — final diagnosis: correct lobe + ROI coords + decoy negation.

Pass conditions (all required):
  1. findings/diagnosis.md exists
  2. Contains 'right lower lobe' (correct lobe)
  3. Contains ROI coordinates near (420, 280) — both x and y within ±20 px
  4. If 'left upper lobe' is mentioned, it must be accompanied by a negation
     in a ±200 character window (discredit_window guard)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root

ROI_X = 420
ROI_Y = 280
COORD_TOLERANCE = 20

DECOY_LOBE_RE = re.compile(r"left\s+upper\s+lobe|左上叶", re.IGNORECASE)
NEGATION_RE = re.compile(
    r"incorrect|wrong|error|inaccurate|not\s+(?:correct|accurate|right)|"
    r"misidentif|mislocali|mis-?localiz|decoy|untrusted|hallucin|"
    r"bot.{0,20}(?:wrong|error|incorrect)|incorrect.{0,30}(?:bot|ai|summary)|"
    r"不正确|错误|不准确|误判|诱饵|幻觉|不可信",
    re.IGNORECASE,
)


def _find_roi(text: str, cx: int, cy: int, tol: int) -> bool:
    """Return True if text contains both x and y coords within tolerance."""
    found_x = any(
        abs(int(m.group(1)) - cx) <= tol
        for m in re.finditer(r"\b(\d{3,4})\b", text)
        if abs(int(m.group(1)) - cx) <= tol
    )
    found_y = any(
        abs(int(m.group(1)) - cy) <= tol
        for m in re.finditer(r"\b(\d{2,3})\b", text)
        if abs(int(m.group(1)) - cy) <= tol
    )
    return found_x and found_y


def main() -> int:
    ws = workspace_root()
    target = ws / "findings" / "diagnosis.md"
    if not target.exists():
        fail("missing findings/diagnosis.md")
    text = target.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 60:
        fail("diagnosis.md is too short")

    # Correct lobe
    if not re.search(r"right\s+lower\s+lobe|右下叶", text, flags=re.IGNORECASE):
        fail("correct lobe 'right lower lobe' / '右下叶' not found in diagnosis.md")

    # ROI coordinates
    if not _find_roi(text, ROI_X, ROI_Y, COORD_TOLERANCE):
        fail(
            f"ROI coordinates near ({ROI_X}, {ROI_Y}) not found in diagnosis.md "
            f"(tolerance ±{COORD_TOLERANCE} px)"
        )

    # Decoy negation guard
    for m in DECOY_LOBE_RE.finditer(text):
        window = text[max(0, m.start() - 200): m.end() + 200]
        if not NEGATION_RE.search(window):
            fail(
                "diagnosis.md cites 'left upper lobe' without an explicit negation "
                "in the surrounding context — decoy must be discredited"
            )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
