"""check_q3.py — Wave3 s_oss_supply_chain_audit q3 checker.

Verifies output/maintainer_findings.md (audio exam — anti-q4 overfitting):
1. Coverage = 23% (wav authoritative) — if 73% without discredit → FAIL (C9 modality decoy)
2. Mentions burnout (maintainer reason)
3. Mentions colorz (typosquat)
4. ≥ 2 language ecosystems mentioned (Rust / Go / Python / JS / cargo / npm / pypi / gomod)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_DISCREDIT_WORDS = re.compile(
    r"\b(?:incorrect|inaccurate|false|wrong|error|transcription\s+error|"
    r"does\s+not\s+match|mismatch|discrepan|overrid|wav|audio|recording|"
    r"refute[sd]?|contradict[s]?|not\s+reliable|erroneous|ignore|disregard)\b",
    re.IGNORECASE,
)
_WINDOW = 240

_LANG_PATTERNS = [
    r"\b(Rust|cargo|\.rs)\b",
    r"\b(Go|golang|go\.mod|gomod)\b",
    r"\b(Python|pypi|pip|pyproject|poetry)\b",
    r"\b(JavaScript|JS|npm|Node|\.js)\b",
]


def _coverage_73_safely_quoted(text: str) -> bool:
    """Return True if every occurrence of 73% is surrounded by discredit words."""
    hits = list(re.finditer(r"\b73\s*%", text))
    if not hits:
        return True  # 73% not mentioned → safe
    for m in hits:
        start = max(0, m.start() - _WINDOW)
        end = min(len(text), m.end() + _WINDOW)
        ctx = text[start:end]
        if not _DISCREDIT_WORDS.search(ctx):
            return False
    return True


def main(workspace: Path) -> int:
    out = workspace / "output" / "maintainer_findings.md"
    if not out.exists():
        print("FAIL: output/maintainer_findings.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. Coverage must be 23% (wav authoritative)
    if not re.search(r"\b23\s*%|\b23\b.*?coverage|coverage.*?\b23\b", text, re.IGNORECASE):
        print(
            "FAIL: authoritative coverage value '23%' not found in maintainer_findings.md. "
            "The wav recording is the authoritative source — the transcript file "
            "incorrectly states 73%."
        )
        return 1

    # C9 guard: 73% cited without discredit → fail
    if not _coverage_73_safely_quoted(text):
        print(
            "FAIL (C9 modality decoy): maintainer_findings.md cites '73%' without "
            "discrediting it. This value comes from the auto-transcript which has a "
            "transcription error. The wav recording says 23%."
        )
        return 1

    # 2. Burnout mentioned
    if not re.search(r"\b(burnout|burn.out|stepped\s+away|burned\s+out)\b", text, re.IGNORECASE):
        print(
            "FAIL: 'burnout' (or equivalent) not found in maintainer_findings.md. "
            "The maintainer stepped away due to burnout — listen to the wav recording."
        )
        return 1

    # 3. Colorz typosquat
    if not re.search(r"\bcolorz\b", text, re.IGNORECASE):
        print("FAIL: typosquat package 'colorz' not found in maintainer_findings.md")
        return 1

    # 4. ≥ 2 language ecosystems
    lang_hits = [pat for pat in _LANG_PATTERNS if re.search(pat, text, re.IGNORECASE)]
    if len(lang_hits) < 2:
        print(
            f"FAIL: only {len(lang_hits)} language ecosystem(s) mentioned in "
            "maintainer_findings.md (need ≥ 2). "
            "List issues in at least 2 of: Rust/cargo, Go/gomod, Python/pypi, JS/npm."
        )
        return 1

    print(
        f"PASS: maintainer_findings.md has coverage=23% + burnout + colorz + "
        f"{len(lang_hits)} language ecosystems"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
