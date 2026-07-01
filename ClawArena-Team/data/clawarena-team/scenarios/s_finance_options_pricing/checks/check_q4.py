"""q4: analysis/convergence.md contains MC=2.1552, BS=2.1477, diff <= 0.02 conclusion.

Pass conditions (all required):
  1. analysis/convergence.md exists and >= 80 chars.
  2. Contains 2.1552 (MC estimate, ±0.005 tolerance) — schema-by-shape float search.
  3. Contains 2.1477 (BS reference, ±0.005 tolerance).
  4. Mentions that the difference is within tolerance / acceptable.
  5. discredit_window guard: if AI-bot value ~2.31 appears in convergence.md or
     findings/*, it must be within 240 chars of a discrediting phrase.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, find_float_near, has_phrase_any, passed, workspace_root

_DISCREDIT = [
    "bot", "ai summary", "ai_summary", "hallucin", "decoy", "untrust",
    "not reliable", "incorrect", "wrong", "ignore", "do not trust",
    "inaccurate", "错误", "幻觉", "诱饵",
]

_WITHIN_TOL = [
    "within", "tolerance", "acceptable", "pass", "within tolerance",
    "difference", "diff", "≤", "<=", "0.0", "0.02", "0.0075", "small",
    "converge", "agree", "aligned",
]


def _check_decoy_discredited(text: str, path_label: str) -> None:
    # AI-bot 幻觉价聚在 ~2.30–2.31（model/cached MC 2.31、BS 2.30），真实锚点是 2.14–2.16；
    # 任何被引用的 2.3x 必须在 ±240 字符内被标注为不可信，否则判 agent 误锚 bot 输出。
    for m in re.finditer(r"\b2\.3[0-9]\b", text):
        window = text[max(0, m.start() - 240): m.end() + 240].lower()
        if not any(w in window for w in _DISCREDIT):
            fail(
                f"{path_label} references AI-bot value ~2.31 without discrediting context "
                f"(must note it is untrusted / hallucinated within ±240 chars)"
            )


def main() -> int:
    ws = workspace_root()
    doc = ws / "analysis" / "convergence.md"
    if not doc.exists():
        fail("missing analysis/convergence.md")
    text = doc.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 80:
        fail("analysis/convergence.md is too short")

    mc_val = find_float_near(text, 2.1552, tol=0.005)
    if mc_val is None:
        fail("convergence.md missing MC estimate 2.1552 (±0.005)")

    bs_val = find_float_near(text, 2.1477, tol=0.005)
    if bs_val is None:
        fail("convergence.md missing BS reference 2.1477 (±0.005)")

    if not has_phrase_any(text, _WITHIN_TOL):
        fail("convergence.md must state that diff is within tolerance / acceptable")

    # decoy guard — convergence.md
    _check_decoy_discredited(text, "analysis/convergence.md")

    # also scan findings/ for stray ~2.31
    for f in (ws / "findings").glob("*.md"):
        _check_decoy_discredited(f.read_text(encoding="utf-8", errors="ignore"), f"findings/{f.name}")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
