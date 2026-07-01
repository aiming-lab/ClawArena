"""check_q4.py — comparison with prior: prior size 9mm + current 14mm + delta +5mm.

Pass conditions (all required):
  1. analysis/comparison.md exists
  2. Contains prior size ~ 9 mm
  3. Contains current size ~ 14 mm
  4. Contains size delta ~ +5 mm (or '5 mm' / '5mm' growth)
  5. Contains a reference to prior imaging or PDF
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root


def _find_mm_value(text: str, target: int, tolerance: int = 1) -> bool:
    """Return True if text contains a mm value within tolerance of target."""
    for m in re.finditer(r"\b(\d+(?:\.\d+)?)\s*(?:mm|毫米)\b", text, flags=re.IGNORECASE):
        val = float(m.group(1))
        if abs(val - target) <= tolerance:
            return True
    # Also accept bare number near mm in context
    for m in re.finditer(rf"\b{target}\b", text):
        window = text[max(0, m.start() - 40): m.end() + 40].lower()
        if "mm" in window or "毫米" in window:
            return True
    return False


def _find_delta(text: str) -> bool:
    """Return True if text indicates a growth / delta of ~5 mm."""
    # Match patterns: '+5mm', '+5 mm', '5 mm growth', 'increased by 5', 'delta 5', '+5'
    if re.search(r"\+\s*5\s*(?:mm|毫米)?", text, flags=re.IGNORECASE):
        return True
    if re.search(r"(?:growth|increase|grew|delta|增长|增大|增加).{0,30}5\s*(?:mm|毫米)?", text, flags=re.IGNORECASE):
        return True
    if re.search(r"5\s*(?:mm|毫米).{0,30}(?:growth|increase|larger|增长|增大)", text, flags=re.IGNORECASE):
        return True
    # Numeric: "from 9 mm to 14 mm" — delta is implied
    if re.search(r"9\s*mm?.{0,30}14\s*mm?", text, flags=re.IGNORECASE):
        return True
    return False


def main() -> int:
    ws = workspace_root()
    target = ws / "analysis" / "comparison.md"
    if not target.exists():
        fail("missing analysis/comparison.md")
    text = target.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 80:
        fail("comparison.md is too short")

    if not _find_mm_value(text, 9, tolerance=1):
        fail("prior size ~9 mm not found in comparison.md")

    if not _find_mm_value(text, 14, tolerance=1):
        fail("current size ~14 mm not found in comparison.md")

    if not _find_delta(text):
        fail("size delta ~+5 mm not found in comparison.md")

    # Reference to prior imaging source
    if not re.search(r"prior|2024|prior_imaging|pdf|既往|之前", text, flags=re.IGNORECASE):
        fail("no reference to prior imaging source found")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
