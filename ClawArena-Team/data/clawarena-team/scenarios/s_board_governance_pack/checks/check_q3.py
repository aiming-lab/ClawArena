#!/usr/bin/env python3
"""check_q3.py — Validate q3: COI disclosure reconciliation table.

Ground truth (from design_spec §4 q3 and §3.2):
  DIRECTOR_CHEN  — classifies Nexus Fintech Partners LP as "non-material"
                   (rationale: holding < 0.5% of fund NAV)
  DIRECTOR_ALBA  — classifies same investment as "potential material conflict
                   requiring full board vote"
                   (rationale: LP holds warrants in Meridian Capital subsidiary)
  Governing rule — DIRECTOR_ALBA's more conservative classification governs
                   until resolved by board vote (per COI policy extract)
  Verbatim policy sentence (丑):
    "Where two or more directors submit conflicting classifications of the same
     interest, the more conservative classification shall govern for all agenda
     and disclosure purposes until the board resolves the matter by majority vote."
  Required next step — board vote at Q2 meeting
  Agenda implication — COI Disclosures item (position 2) must include Nexus
                       Fintech Partners LP as a sub-item for board resolution

Pass conditions (all must hold; exit 0):
  1. Structure layer: output/coi_reconciliation.md exists; >= 500 bytes;
     contains a table (pipe-delimited rows) or >= 4 distinct labeled sections.
  2. Field layer (regex):
     - DIRECTOR_CHEN non-material: Chen ... non-material or non-material ... Chen.
     - DIRECTOR_ALBA material: Alba ... material or material ... Alba.
     - Governing classification: Alba ... govern or more conservative ... govern
       or govern ... conservative.
     - Nexus Fintech reference: "Nexus Fintech" appears.
     - Board vote required: board vote / majority vote / vote required.
  3. Verbatim citation (丑):
     The sentence "Where two or more directors submit conflicting classifications
     of the same interest, the more conservative classification shall govern"
     must appear as a quoted extract (approximate match via regex).
  4. Agenda implication: position 2 / item 2 / COI Disclosures linked to
     Nexus / sub-item / flagged / vote — within 150 characters.
  5. Anti-decoy: file must not cite "board_minutes_2026_q1" as the source of
     classification guidance (that is the _archive/ Q1 minutes red herring).

Usage: python check_q3.py <workspace_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Field-layer patterns
# ---------------------------------------------------------------------------

CHEN_NONMATERIAL_RE = re.compile(
    r"[Cc]hen.{0,100}non.?material|non.?material.{0,100}[Cc]hen",
    re.IGNORECASE | re.DOTALL,
)

ALBA_MATERIAL_RE = re.compile(
    r"[Aa]lba.{0,100}material|material.{0,100}[Aa]lba",
    re.IGNORECASE | re.DOTALL,
)

GOVERNING_CLASS_RE = re.compile(
    r"[Aa]lba.{0,100}govern"
    r"|more\s+conservative.{0,50}govern"
    r"|govern.{0,100}conservative",
    re.IGNORECASE | re.DOTALL,
)

NEXUS_FINTECH_RE = re.compile(r"Nexus\s+Fintech", re.IGNORECASE)

BOARD_VOTE_RE = re.compile(
    r"board\s+vote|majority\s+vote|vote\s+required|vote\s+to\s+resolve",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Verbatim citation (丑) — policy sentence
# ---------------------------------------------------------------------------

VERBATIM_POLICY_RE = re.compile(
    r"[Ww]here\s+two\s+or\s+more\s+directors\s+submit\s+conflicting\s+"
    r"classifications.{0,30}more\s+conservative\s+classification\s+shall\s+govern",
    re.DOTALL,
)

# ---------------------------------------------------------------------------
# Agenda implication: COI position 2 linked to Nexus / sub-item / flagged
# ---------------------------------------------------------------------------

AGENDA_IMPLICATION_RE = re.compile(
    r"(position\s+2|item\s+2|COI\s+[Dd]isclosures).{0,150}"
    r"(Nexus|sub.?item|flagged|vote|board\s+vote)",
    re.IGNORECASE | re.DOTALL,
)

# ---------------------------------------------------------------------------
# Anti-decoy: board_minutes_2026_q1 cited as source of classification guidance
# ---------------------------------------------------------------------------

ARCHIVE_MINUTES_RE = re.compile(r"board_minutes_2026_q1", re.IGNORECASE)

# Discredit window (parallel to q1's v3.1 guard): a mention of the archived Q1
# minutes is acceptable ONLY when it is explicitly named-and-excluded — i.e. a
# discredit word appears within 100 characters on either side. A correct answer
# may legitimately point at the decoy to dismiss it (e.g. "did NOT use the
# outdated _archive/board_minutes_2026_q1.md"); only an affirmative citation
# (decoy named as the source of guidance, with no nearby exclusion language)
# constitutes a violation.
ARCHIVE_DISCREDIT_RE = re.compile(
    r"not\s+use[d]?|did\s+not|do\s+not|excluded?|exclud|disregard|ignore[d]?"
    r"|supersede[ds]?|archiv|obsolete|outdated|stale|withdrawn|red\s*herring"
    r"|must\s+not|rather\s+than|instead\s+of|not\s+the\s+authoritative|not\s+authoritative",
    re.IGNORECASE,
)


def _archive_minutes_affirmatively_cited(content: str) -> bool:
    """Return True only if board_minutes_2026_q1 is cited WITHOUT a nearby
    discredit/exclusion word (within 100 chars on either side). Naming the decoy
    in order to explicitly exclude it is allowed (parallel to q1 v3.1 guard)."""
    for m in ARCHIVE_MINUTES_RE.finditer(content):
        start = max(0, m.start() - 100)
        end = min(len(content), m.end() + 100)
        window = content[start:end]
        if not ARCHIVE_DISCREDIT_RE.search(window):
            return True
    return False

# ---------------------------------------------------------------------------
# Structure: table rows or labeled sections
# ---------------------------------------------------------------------------

TABLE_ROW_RE = re.compile(r"^\s*\|[^|\n]+\|", re.MULTILINE)
LABELED_SECTION_RE = re.compile(
    r"^\s*#{1,4}\s+\S|^\s*\*{1,2}[A-Z][^*\n]{3,}\*{1,2}\s*$"
    r"|^\s*\w[\w\s/()-]{3,}\s*:\s*\S",
    re.MULTILINE,
)


def _has_structure(content: str) -> bool:
    """Return True if file has a table OR >= 4 distinct labeled sections."""
    table_rows = TABLE_ROW_RE.findall(content)
    if len(table_rows) >= 3:
        return True
    sections = LABELED_SECTION_RE.findall(content)
    return len(sections) >= 4


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q3.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    recon_file = ws / "output" / "coi_reconciliation.md"

    if not recon_file.exists():
        print("FAIL: output/coi_reconciliation.md does not exist")
        return 1

    content = recon_file.read_text(encoding="utf-8")
    raw_bytes = content.encode("utf-8")
    errors: list[str] = []

    # 1. Structure layer
    if len(raw_bytes) < 500:
        errors.append(
            f"output/coi_reconciliation.md too short "
            f"({len(raw_bytes)} bytes; need >= 500)"
        )

    if not _has_structure(content):
        errors.append(
            "output/coi_reconciliation.md must contain a table (pipe-delimited) "
            "or >= 4 distinct labeled sections to satisfy the reconciliation format requirement"
        )

    # 2. Field layer
    if not CHEN_NONMATERIAL_RE.search(content):
        errors.append(
            "DIRECTOR_CHEN's classification 'non-material' not found — "
            "the file must state Chen's classification explicitly"
        )

    if not ALBA_MATERIAL_RE.search(content):
        errors.append(
            "DIRECTOR_ALBA's classification 'material' not found — "
            "the file must state Alba's classification explicitly"
        )

    if not GOVERNING_CLASS_RE.search(content):
        errors.append(
            "governing classification not identified — "
            "the file must state that DIRECTOR_ALBA's more conservative classification "
            "governs per the COI policy"
        )

    if not NEXUS_FINTECH_RE.search(content):
        errors.append(
            "'Nexus Fintech' not found — "
            "the file must name the shared outside investment explicitly"
        )

    if not BOARD_VOTE_RE.search(content):
        errors.append(
            "board vote requirement not found — "
            "the file must state that a board vote is required to resolve the "
            "conflicting classifications"
        )

    # 3. Verbatim citation (丑)
    if not VERBATIM_POLICY_RE.search(content):
        errors.append(
            "verbatim COI policy sentence not found — "
            "the file must quote the exact policy sentence: "
            "\"Where two or more directors submit conflicting classifications of the "
            "same interest, the more conservative classification shall govern\" "
            "(from director_disclosures/coi_policy_extract.md)"
        )

    # 4. Agenda implication
    if not AGENDA_IMPLICATION_RE.search(content):
        errors.append(
            "agenda implication not found — "
            "the file must link the COI finding to position 2 (COI Disclosures item) "
            "and flag Nexus Fintech Partners LP as requiring a board vote sub-item"
        )

    # 5. Anti-decoy: board_minutes_2026_q1 cited as guidance source.
    #    Discredit-window exception: naming the decoy to explicitly exclude it
    #    is allowed (mirrors q1/q2/q4/q5); only an affirmative citation fails.
    if _archive_minutes_affirmatively_cited(content):
        errors.append(
            "output/coi_reconciliation.md cites 'board_minutes_2026_q1' as a source "
            "of classification guidance — this file (_archive/board_minutes_2026_q1.md) "
            "contains outdated COI references and must not be used; "
            "the authoritative source is director_disclosures/coi_policy_extract.md"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        f"PASS: output/coi_reconciliation.md ({len(raw_bytes)} bytes) identifies "
        "both directors' Nexus Fintech classifications, states that DIRECTOR_ALBA's "
        "more conservative classification governs, includes the verbatim policy sentence, "
        "flags board vote requirement, and links the finding to agenda position 2"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
