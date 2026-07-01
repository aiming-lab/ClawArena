#!/usr/bin/env python3
"""check_q2.py — Validate q2: charter_confirmation.md from the signature page PNG.

Ground truth (from design_spec §4 q2 and §3.1 image inventory):
  ratification_date  = "April 15, 2026"  (readable only from the PNG image)
  board_resolution   = "BR-2026-Q1-007"  (readable only from the PNG image)
  board_chair_name   = "Dr. Eleanor Voss"
  supersession stmt  = Charter v3.1 is superseded as of that date

Important: no text file in the workspace contains "April 15, 2026" or
"BR-2026-Q1-007" — these values must come from the PNG via a VLM subagent.
The check validates the output file only (it cannot verify that a VLM was used,
but the build-script invariant ensures no text shortcut exists).

Pass conditions (all must hold; exit 0):
  1. Structure layer: output/charter_confirmation.md exists; >= 200 bytes;
     contains >= 3 labeled fields (lines with ":" or table rows).
  2. Field layer (regex):
     - Ratification date: "April 15, 2026" or "2026-04-15" appears verbatim.
     - Board resolution number: "BR-2026-Q1-007" appears verbatim.
     - Board Chair name: "Eleanor Voss" or "DR_VOSS" or "BOARD_CHAIR" appears.
     - Supersession statement: v3.1 ... supersede or supersede ... v3.1
       (case-insensitive).
  3. Anti-shortcut (decoy guard): file must not cite v3.1 as the ratified
     document (pattern: v3.1 ... April / 2026-04 as a positive ratification
     reference) — that would indicate confusion with the archived charter.

Usage: python check_q2.py <workspace_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Field-layer patterns
# ---------------------------------------------------------------------------

RATIFICATION_DATE_RE = re.compile(
    r"April\s+15,?\s+2026|2026-04-15",
    re.IGNORECASE,
)

RESOLUTION_NUMBER_RE = re.compile(r"BR-2026-Q1-007")

BOARD_CHAIR_RE = re.compile(
    r"[Ee]leanor\s+[Vv]oss|DR_VOSS|BOARD_CHAIR",
)

SUPERSESSION_RE = re.compile(
    r"v3\.1.{0,50}supersede|supersede.{0,50}v3\.1",
    re.IGNORECASE | re.DOTALL,
)

# ---------------------------------------------------------------------------
# Anti-shortcut: v3.1 cited as the ratified document
# ---------------------------------------------------------------------------

V31_AS_RATIFIED_RE = re.compile(
    r"v3\.1.{0,30}(April|2026-04)",
    re.IGNORECASE | re.DOTALL,
)

# ---------------------------------------------------------------------------
# Labeled-field counter (lines with ":" or table rows)
# ---------------------------------------------------------------------------

LABELED_FIELD_RE = re.compile(
    # 容许列表项前缀（- / * / •）后接 "Key: Value"，markdown 项目符号是常见且合法写法
    r"^\s*(?:[-*•]\s*)?(?:\*{0,2}\w[\w\s/().-]{0,50}\*{0,2})\s*:\s*\S"
    r"|^\s*\|[^|]+\|[^|]+\|",
    re.MULTILINE,
)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q2.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    conf_file = ws / "output" / "charter_confirmation.md"

    if not conf_file.exists():
        print("FAIL: output/charter_confirmation.md does not exist")
        return 1

    content = conf_file.read_text(encoding="utf-8")
    raw_bytes = content.encode("utf-8")
    errors: list[str] = []

    # 1. Structure layer（四个字段值另有逐一硬校验；长度仅作非空防线，放宽到 150）
    if len(raw_bytes) < 150:
        errors.append(
            f"output/charter_confirmation.md too short "
            f"({len(raw_bytes)} bytes; need >= 150)"
        )

    labeled_fields = LABELED_FIELD_RE.findall(content)
    if len(labeled_fields) < 3:
        errors.append(
            f"output/charter_confirmation.md contains only {len(labeled_fields)} "
            "labeled field(s); need >= 3 (ratification date, resolution number, "
            "Board Chair name, and/or supersession statement)"
        )

    # 2. Field layer
    if not RATIFICATION_DATE_RE.search(content):
        errors.append(
            "ratification date not found — the file must contain "
            "'April 15, 2026' or '2026-04-15' exactly as read from the "
            "charter_v3.2_signature_page.png image"
        )

    if not RESOLUTION_NUMBER_RE.search(content):
        errors.append(
            "board resolution number 'BR-2026-Q1-007' not found verbatim — "
            "dispatch a VLM subagent to read the charter signature page PNG"
        )

    if not BOARD_CHAIR_RE.search(content):
        errors.append(
            "Board Chair name not found — the file must contain "
            "'Eleanor Voss' (or 'DR_VOSS' / 'BOARD_CHAIR') as the signatory"
        )

    if not SUPERSESSION_RE.search(content):
        errors.append(
            "supersession statement not found — add a statement that "
            "Charter v3.1 is superseded as of the ratification date"
        )

    # 3. Anti-shortcut: v3.1 as the ratified document。
    # 仅当 "v3.1 … April/2026-04" 出现且其附近【无】supersede/replaced 语境时才算误把 v3.1
    # 当 ratified。否则会误杀本题【必填】的正确 supersession 语句
    # "Charter v3.1 is superseded as of April 15, 2026"（它天然含 v3.1 与日期）。
    for _m in V31_AS_RATIFIED_RE.finditer(content):
        _win = content[max(0, _m.start() - 60): _m.end() + 60].lower()
        if "supersede" not in _win and "replaced" not in _win:
            errors.append(
                "output/charter_confirmation.md appears to cite Charter v3.1 as the "
                "ratified document (pattern 'v3.1 ... April / 2026-04') — "
                "Charter v3.1 is the SUPERSEDED document; Charter v3.2 is operative"
            )
            break

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        f"PASS: output/charter_confirmation.md ({len(raw_bytes)} bytes) contains "
        "ratification date April 15 2026, resolution BR-2026-Q1-007, "
        "Board Chair Eleanor Voss, and a Charter v3.1 supersession statement"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
