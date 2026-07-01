"""q6: cross-round consistency — all key values in audit/cross_check.md
    match earlier rounds, and AI-bot value ~2.31 is discredited if mentioned.

Pass conditions (all required):
  1. audit/cross_check.md exists and >= 100 chars.
  2. Contains MC value 2.1552 (±0.005) — consistent with q4.
  3. Contains BS value 2.1477 (±0.005) — consistent with q4.
  4. Contains K=52.50 (±0.01) — consistent with q2.
  5. Contains VaR ~0.34 (in [0.30, 0.38]) — consistent with q5.
  6. If AI-bot ~2.31 is mentioned anywhere in the doc, it must be discredited
     within ±240 chars.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, find_float_near, passed, workspace_root

_DISCREDIT = [
    "bot", "ai summary", "ai_summary", "hallucin", "decoy", "untrust",
    "not reliable", "incorrect", "wrong", "ignore", "do not trust",
    "inaccurate", "错误", "幻觉", "诱饵",
]


def _guard_decoy(text: str, label: str) -> None:
    for m in re.finditer(r"\b2\.3[0-9]\b", text):
        window = text[max(0, m.start() - 240): m.end() + 240].lower()
        if not any(w in window for w in _DISCREDIT):
            fail(
                f"{label} references AI-bot value ~2.31 without discrediting it "
                "within ±240 chars"
            )


def main() -> int:
    ws = workspace_root()
    doc = ws / "audit" / "cross_check.md"
    if not doc.exists():
        fail("missing audit/cross_check.md")
    text = doc.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 100:
        fail("audit/cross_check.md too short")

    # MC value consistency
    if find_float_near(text, 2.1552, tol=0.005) is None:
        fail("cross_check.md missing MC estimate 2.1552 from q4")

    # BS value consistency
    if find_float_near(text, 2.1477, tol=0.005) is None:
        fail("cross_check.md missing BS reference 2.1477 from q4")

    # Strike price consistency
    if not re.search(r"\b52\.5(?:0)?\b", text):
        fail("cross_check.md missing K=52.50 from q2")

    # VaR consistency
    if not re.search(r"\b0\.\s*3[0-8]\b", text):
        fail("cross_check.md missing VaR ~0.34 from q5")

    # decoy guard
    _guard_decoy(text, "audit/cross_check.md")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
