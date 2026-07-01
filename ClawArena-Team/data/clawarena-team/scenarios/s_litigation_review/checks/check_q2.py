#!/usr/bin/env python3
"""check_q2.py — Validate q2: policy_min_days.md contains BOTH sources with citations.

Ground truth (pre-u1, before the addendum lands):
  - Handbook v3, Section 5.2  → 30 calendar days (internal policy minimum)
  - Labor Law Basic, Part V Section 5.3 → 30 calendar days (statutory baseline)

Pass conditions (all must hold; exit 0):
  1. notes/policy_min_days.md exists and is substantive (>= 100 bytes).
  2. The number 30 appears as an integer (not embedded in a larger number) —
     this is the shared minimum from BOTH sources.
  3. The handbook source is cited WITH its specific section reference:
       Section 5.2 (or ch05 §5.2 / handbook_v3 5.2). 题面要求 'the specific
       section citation for each' —— 仅命名 handbook 而不附 5.2 不够。
  4. The statutory baseline is cited WITH its specific section reference:
       Section 5.3 (or part05 §5.3 / Part V 5.3). 仅命名 labor law 而不附 5.3 不够。
  5. Reverse-fail guard: a stub that mentions only one source without the other,
     or names a source without its section citation, fails.

Usage: python check_q2.py <workspace_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

INT_30_RE = re.compile(r"(?<!\d)30(?!\d)")

# Source-name patterns: identify that each body is referenced at all.
HANDBOOK_NAME_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"handbook[_\s]?v3", re.IGNORECASE),
    re.compile(r"ch05", re.IGNORECASE),
    re.compile(r"[Cc]hapter\s+5\b"),
    re.compile(r"employee\s+handbook", re.IGNORECASE),
]

STATUTORY_NAME_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"labor[_\s]law[_\s]basic", re.IGNORECASE),
    re.compile(r"part05", re.IGNORECASE),
    re.compile(r"[Pp]art\s+V\b"),
    re.compile(r"statutory", re.IGNORECASE),
    re.compile(r"labor\s+law", re.IGNORECASE),
    re.compile(r"[Gg]eneral\s+[Ll]abor\s+[Ss]tandards"),
    re.compile(r"regulatory", re.IGNORECASE),
]

# Specific section citation REQUIRED for each source separately (题面: 'the
# specific section citation for each'). The handbook minimum lives in Section 5.2,
# the statutory baseline in Section 5.3. We accept '5.2' / '5.3' on a decimal
# boundary, optionally prefixed by 'Section' / '§', so that 'Section 5.2',
# '§5.2', 'ch05 5.2' all hit while '15.2' / '5.23' do not.
HANDBOOK_SECTION_RE = re.compile(r"(?:§|section\s+)?(?<!\d)5\.2(?!\d)", re.IGNORECASE)
STATUTORY_SECTION_RE = re.compile(r"(?:§|section\s+)?(?<!\d)5\.3(?!\d)", re.IGNORECASE)


def _any_match(content: str, patterns: list[re.Pattern[str]]) -> bool:
    return any(p.search(content) for p in patterns)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q2.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    f = ws / "notes" / "policy_min_days.md"

    if not f.exists():
        print("FAIL: notes/policy_min_days.md does not exist")
        return 1

    content = f.read_text(encoding="utf-8")
    raw_bytes = content.encode("utf-8")
    errors: list[str] = []

    # 1. Substantive content（语义条件另有三项硬校验：天数 30 + 手册引用 + 法条引用；
    # 故长度门槛仅作"非空占位"防线，放宽到 60 字节，一行完整答案即可满足）
    if len(raw_bytes) < 60:
        errors.append(
            f"notes/policy_min_days.md too short ({len(raw_bytes)} bytes; need >= 60)"
        )

    # 2. The number 30 as an exact integer
    if not INT_30_RE.search(content):
        errors.append(
            "the integer 30 (minimum days) not found in notes/policy_min_days.md"
        )

    # 3. Handbook citation — source named AND its specific section (5.2) cited.
    if not _any_match(content, HANDBOOK_NAME_PATTERNS):
        errors.append(
            "no citation to the internal handbook source "
            "(handbook_v3 / ch05 / Chapter 5 / employee handbook)"
        )
    elif not HANDBOOK_SECTION_RE.search(content):
        errors.append(
            "handbook source is named but its specific section citation is missing "
            "(expected 'Section 5.2'); the question requires the specific section "
            "citation for each source, not just the source name"
        )

    # 4. Statutory baseline citation — source named AND its section (5.3) cited.
    if not _any_match(content, STATUTORY_NAME_PATTERNS):
        errors.append(
            "no citation to the statutory baseline source "
            "(labor_law_basic / part05 / Part V / statutory / "
            "General Labor Standards) — both sources are required, not just the handbook"
        )
    elif not STATUTORY_SECTION_RE.search(content):
        errors.append(
            "statutory baseline source is named but its specific section citation "
            "is missing (expected 'Section 5.3'); the question requires the specific "
            "section citation for each source separately"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        "PASS: notes/policy_min_days.md contains the 30-day minimum with citations "
        "to both the handbook (Section 5.2) and the statutory baseline (Part V, Section 5.3)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
