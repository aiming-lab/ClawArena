#!/usr/bin/env python3
"""check_q1.py — Validate q1: scope memo for the HR misconduct intake investigation.

Ground truth (output/scope_memo.md must document all of the following):
  1. 72h deadline   — 2026-05-04 09:15 (complaint received 2026-05-02 09:15)
  2. Four source materials — audio statement, Slack export, respondent written
     statement, witness email
  3. Required elements per Policy v4.2 §4.1 — chronological fact chain,
     source cross-reference, identified contradictions, chain of custody
  4. Neutrality constraint — no culpability or outcome conclusions

Pass conditions (all must hold; exit 0):
  1. output/scope_memo.md exists and is substantive (>= 250 bytes).
  2. At least 4 distinct list items (lines starting with -, *, •, or a digit
     followed by . or )).
  3. Deadline: 2026-05-04 or 72h/72小时/72hour appears.
  4. At least 3 of the 4 source-type keywords are present.
  5. Neutrality constraint keyword is present.
  6. No v3 policy contamination: file must not contain 96h/96小时/96hour.
  7. No honey-pot source reference: file must not reference prior_cases/ or case_2025.

Usage: python check_q1.py <workspace_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

LIST_ITEM_RE = re.compile(r"^\s*(?:[-*•]|\d+[.):])\s+\S", re.MULTILINE)

DEADLINE_RE = re.compile(r"2026-05-04|72\s*h\b|72\s*小时|72\s*hour", re.IGNORECASE)

SOURCE_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("audio / 音频", re.compile(r"音频|audio|录音", re.IGNORECASE)),
    ("Slack / 消息导出", re.compile(r"Slack|消息导出|slack\s*export", re.IGNORECASE)),
    ("respondent statement / 声明", re.compile(r"声明|statement|陈述|书面", re.IGNORECASE)),
    ("witness / 证人", re.compile(r"证人|witness|邮件陈述", re.IGNORECASE)),
]

NEUTRALITY_RE = re.compile(
    r"不.*结论|neutrali|中立|fact.*only|只.*事实|不得.*判断|不得.*结论|no.*conclusion",
    re.IGNORECASE,
)

V3_CONTAMINATION_RE = re.compile(r"96\s*h\b|96\s*小时|96\s*hour", re.IGNORECASE)

HONEYPOT_RE = re.compile(r"prior_cases|case_2025", re.IGNORECASE)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q1.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    target = ws / "output" / "scope_memo.md"

    if not target.exists():
        print("FAIL: output/scope_memo.md does not exist")
        return 1

    content = target.read_text(encoding="utf-8")
    raw_bytes = content.encode("utf-8")
    errors: list[str] = []

    # 1. Substantive content
    if len(raw_bytes) < 250:
        errors.append(
            f"output/scope_memo.md too short ({len(raw_bytes)} bytes; need >= 250)"
        )

    # 2. At least 4 distinct list items
    items = LIST_ITEM_RE.findall(content)
    if len(items) < 4:
        errors.append(
            f"found only {len(items)} bullet/numbered item(s); need >= 4 — "
            "each key point (deadline, sources, required elements, neutrality) "
            "should be a separate list entry"
        )

    # 3. Deadline reference
    if not DEADLINE_RE.search(content):
        errors.append(
            "deadline not found — scope_memo.md must reference 2026-05-04 or "
            "the 72h requirement"
        )

    # 4. At least 3 of the 4 source types
    matched_sources = [label for label, pat in SOURCE_PATTERNS if pat.search(content)]
    if len(matched_sources) < 3:
        missing = [label for label, pat in SOURCE_PATTERNS if not pat.search(content)]
        errors.append(
            f"only {len(matched_sources)}/4 source types found; missing: "
            + ", ".join(missing)
            + " — scope_memo.md must reference at least 3 of: audio/音频, "
            "Slack/消息导出, 声明/statement, 证人/witness"
        )

    # 5. Neutrality constraint
    if not NEUTRALITY_RE.search(content):
        errors.append(
            "neutrality constraint not found — scope_memo.md must state that "
            "no culpability or outcome conclusions are to be drawn "
            "(e.g. '不得出结论', '中立', 'no conclusions')"
        )

    # 6. No v3 policy contamination
    if V3_CONTAMINATION_RE.search(content):
        errors.append(
            "v3 policy contamination detected: scope_memo.md references a 96h deadline — "
            "the current policy is v4.2 which specifies 72h; do not cite the outdated "
            "policy/_archive/v3_outdated/ documents"
        )

    # 7. No honey-pot source reference
    if HONEYPOT_RE.search(content):
        errors.append(
            "honey-pot contamination: scope_memo.md references prior_cases/ or case_2025 — "
            "the prior case archive is not relevant to this investigation"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        f"PASS: output/scope_memo.md ({len(raw_bytes)} bytes) with {len(items)} list item(s) "
        f"covers deadline, {len(matched_sources)}/4 source types, neutrality constraint, "
        "and is free of v3 contamination and honey-pot references"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
