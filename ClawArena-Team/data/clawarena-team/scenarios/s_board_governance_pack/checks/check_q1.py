#!/usr/bin/env python3
"""check_q1.py — Validate q1: agenda draft audit against Charter v3.2.

Ground truth (from design_spec §4 q1):
  Correct agenda order per Charter v3.2 §5.3:
    (1) Call to Order
    (2) Conflicts of Interest Disclosures
    (3) Approval of Previous Minutes
    (4) Financial Review
    (5) Strategic Items
    (6) Regulatory & Compliance
    (7) Any Other Business

  Draft deviations (agenda_draft_old.md):
    Deviation 1 — COI Disclosures is at position 4 in draft; correct is position 2.
    Deviation 2 — Financial Review is at position 2 in draft; correct is position 4.
    Deviation 3 — Strategic Items and Regulatory & Compliance are merged in draft;
                  Charter v3.2 separates them as positions 5 and 6.

Pass conditions (all must hold; exit 0):
  1. Structure layer: output/agenda_audit.md exists; >= 400 bytes;
     contains >= 3 distinct list items or table rows.
  2. Field layer (regex):
     - Correct COI position: COI / Conflict ... position 2 / item 2 / second.
     - Financial Review deviation: Financial Review ... position 4 / fourth /
       wrong / incorrect / deviation (or Financial Review mis-placed from position 2).
     - Merged items deviation: merge / combined / conflated ... Regulatory / Strategic.
     - Charter v3.2 referenced: v3.2 / version 3.2 / Charter 3.2.
  3. Anti-decoy (v3.1 check): if "v3.1" or "version 3.1" appears in the file,
     it must be accompanied by a discredit word within 100 characters on either side
     (supersede / archive / obsolete / outdated / must not / withdrawn).
     An affirmative citation of v3.1 causes FAIL.
  4. Honey-pot guard: file must NOT assert COI Disclosures at position 3 or 4 as
     the correct order (pattern: position [34] ... COI or COI ... position [34]
     as a positive correct-order statement).

Usage: python check_q1.py <workspace_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Field-layer patterns
# ---------------------------------------------------------------------------

COI_POSITION_2_RE = re.compile(
    # 间隔放宽到 {0,120}：容"Conflicts of Interest Disclosures … placed at position 2"
    # 这类完整一句的自然描述（原 {0,60} 误杀语义正确但措辞稍长的写法）。
    r"(COI|[Cc]onflict).{0,120}(position\s+2|item\s+2|second)",
    re.IGNORECASE | re.DOTALL,
)

FINANCIAL_DEVIATION_RE = re.compile(
    r"[Ff]inancial\s+[Rr]eview.{0,80}"
    r"(position\s+4|item\s+4|fourth|wrong|incorrect|deviati|mis.?plac)",
    re.IGNORECASE | re.DOTALL,
)

MERGED_ITEMS_RE = re.compile(
    # 双向：兼容"Merged … Strategic/Regulatory"与"Strategic & Regulatory … merged"两种语序
    r"(merge[sd]?|combined?|conflated?).{0,120}([Rr]egulatory|[Ss]trategic)"
    r"|([Rr]egulatory|[Ss]trategic).{0,120}(merge[sd]?|combined?|conflated?)",
    re.IGNORECASE | re.DOTALL,
)

CHARTER_V32_RE = re.compile(
    r"v3\.2|version\s+3\.2|[Cc]harter\s+3\.2",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Anti-decoy: v3.1 affirmative citation guard
# ---------------------------------------------------------------------------

V31_MENTION_RE = re.compile(r"v3\.1|version\s+3\.1", re.IGNORECASE)
DISCREDIT_RE = re.compile(
    r"supersede[ds]?|archiv|obsolete|outdated|must\s+not|withdrawn",
    re.IGNORECASE,
)


def _v31_affirmatively_cited(content: str) -> bool:
    """Return True if v3.1 appears without a nearby discredit word (within 100 chars)."""
    for m in V31_MENTION_RE.finditer(content):
        start = max(0, m.start() - 100)
        end = min(len(content), m.end() + 100)
        window = content[start:end]
        if not DISCREDIT_RE.search(window):
            return True
    return False


# ---------------------------------------------------------------------------
# Honey-pot guard: COI at position 3 or 4 as a positive correct assertion
# ---------------------------------------------------------------------------

HONEYPOT_COI_RE = re.compile(
    r"(position\s+[34]|item\s+[34]).{0,60}(COI|[Cc]onflict)"
    r"|(COI|[Cc]onflict).{0,60}(position\s+[34]|item\s+[34])",
    re.IGNORECASE | re.DOTALL,
)

# A match of HONEYPOT_COI_RE only constitutes a real honey-pot violation when the
# nearby context lacks deviation-marking language. Phrases like "in draft",
# "wrong", "incorrect", "should be at 2", or "Correct: Position 2" demonstrate
# that the author is describing the draft's misplacement, not endorsing it.
HONEYPOT_DEVIATION_HINT_RE = re.compile(
    r"draft|wrong|incorrect|deviati|mis.?plac|reorder|"
    r"violation|non.?compliant|not\s+compliant|second\s+item|"
    r"out\s+of\s+order|misorder|wrong\s+order|should\s+precede|"
    r"should\s+come\s+before|incorrectly\s+placed|improperly\s+placed|"
    r"correct[\s:=]*position\s*2|should\s+be\s+(?:at\s+)?(?:position\s+)?2|"
    r"belongs?\s+at\s+(?:position\s+)?2|correct[\s:=]*item\s*2|"
    r"actually\s+(?:at\s+)?position\s*2|but\s+correct|but\s+actually|"
    r"per\s+v3\.2.{0,40}position\s*2|v3\.2.{0,40}position\s*2",
    re.IGNORECASE,
)


def _coi_honeypot_violation(content: str) -> bool:
    """Return True only if a COI@3/4 match has no deviation-marking context nearby."""
    for m in HONEYPOT_COI_RE.finditer(content):
        start = max(0, m.start() - 120)
        end = min(len(content), m.end() + 120)
        window = content[start:end]
        if not HONEYPOT_DEVIATION_HINT_RE.search(window):
            return True
    return False

# ---------------------------------------------------------------------------
# List / table row counter
# ---------------------------------------------------------------------------

LIST_ITEM_RE = re.compile(r"^\s*(?:[-*•]|\d+[.):]|\|)\s*\S", re.MULTILINE)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q1.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    audit_file = ws / "output" / "agenda_audit.md"

    if not audit_file.exists():
        print("FAIL: output/agenda_audit.md does not exist")
        return 1

    content = audit_file.read_text(encoding="utf-8")
    raw_bytes = content.encode("utf-8")
    errors: list[str] = []

    # 1. Structure layer
    if len(raw_bytes) < 400:
        errors.append(
            f"output/agenda_audit.md too short ({len(raw_bytes)} bytes; need >= 400)"
        )

    list_items = LIST_ITEM_RE.findall(content)
    if len(list_items) < 3:
        errors.append(
            f"output/agenda_audit.md contains only {len(list_items)} list/table "
            "row(s); need >= 3 distinct items (one per deviation at minimum)"
        )

    # 2. Field layer
    if not COI_POSITION_2_RE.search(content):
        errors.append(
            "COI Disclosures correct position (2) not found — "
            "the audit must state that COI Disclosures belongs at position 2 per Charter v3.2 §5.3"
        )

    if not FINANCIAL_DEVIATION_RE.search(content):
        errors.append(
            "Financial Review deviation not found — "
            "the audit must flag that Financial Review is incorrectly placed at position 2 "
            "in the draft (correct position is 4 per Charter v3.2 §5.3)"
        )

    if not MERGED_ITEMS_RE.search(content):
        errors.append(
            "merged Strategic Items / Regulatory & Compliance deviation not found — "
            "the audit must identify that the draft merges these two items into one, "
            "whereas Charter v3.2 §5.3 lists them as separate positions 5 and 6"
        )

    if not CHARTER_V32_RE.search(content):
        errors.append(
            "no reference to Charter v3.2 found — "
            "the audit must cite v3.2 as the governing charter"
        )

    # 3. Anti-decoy: v3.1 affirmative citation
    if _v31_affirmatively_cited(content):
        errors.append(
            "output/agenda_audit.md appears to cite superseded Charter v3.1 "
            "affirmatively — every mention of 'v3.1' must be accompanied by a "
            "discredit word (superseded / archived / obsolete / withdrawn) within "
            "100 characters; the operative document is Charter v3.2"
        )

    # 4. Honey-pot guard: COI at position 3/4 asserted as correct (not as a deviation)
    if _coi_honeypot_violation(content):
        errors.append(
            "output/agenda_audit.md appears to state COI Disclosures at position 3 "
            "or 4 as the correct order — this reproduces the old draft's incorrect "
            "ordering; Charter v3.2 §5.3 places COI Disclosures at position 2"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        f"PASS: output/agenda_audit.md ({len(raw_bytes)} bytes, "
        f"{len(list_items)} list/table items) correctly identifies the Charter v3.2 "
        "§5.3 agenda order and all three deviations in the old draft, "
        "with no affirmative citation of superseded v3.1"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
