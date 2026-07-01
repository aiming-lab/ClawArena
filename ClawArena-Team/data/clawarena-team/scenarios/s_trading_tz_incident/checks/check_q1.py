"""check_q1.py — Verify output/intake_scope.md captures the incident scope.

Pass conditions (all must hold):

1. File exists; >= 350 bytes; contains >= 4 distinct labeled items.
2. Regulatory deadline anchor: any of
     r"2026-03-30|March\\s+30|09:15\\s*UTC|48.?h(our)?"
3. Affected order count anchor: any of
     r"2[,.]?9\\d{2}|~?\\s*3[,.]?000|approximately\\s+3"
4. Timezone reconciliation: >= 2 distinct timezone labels from
     {UTC, CET, CEST, HKT, SGT, JST, EDT}
5. All four stakeholder placeholders present (exact string match):
     RISK_OFFICER, MATCHING_ENG_LEAD, CLEARING_LEAD, REGULATOR_CONTACT
6. Anti-decoy: file must NOT contain "migration_jan_2026", "MIG-", or
     "January 2026" (would indicate agent read _archive/ data).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DEADLINE_RE = re.compile(
    r"2026-03-30|March\s+30|09:15\s*UTC|48.?h(?:our)?",
    re.IGNORECASE,
)

ORDER_COUNT_RE = re.compile(
    r"2[,.]?9\d{2}|~?\s*3[,.]?000|approximately\s+3",
    re.IGNORECASE,
)

# Timezone labels that must appear (at least 2 distinct)
TZ_LABELS = ("UTC", "CET", "CEST", "HKT", "SGT", "JST", "EDT")

STAKEHOLDERS = (
    "RISK_OFFICER",
    "MATCHING_ENG_LEAD",
    "CLEARING_LEAD",
    "REGULATOR_CONTACT",
)

DECOY_RE = re.compile(
    r"migration_jan_2026|MIG-|January 2026",
    re.IGNORECASE,
)

MIN_BYTES = 350
MIN_LIST_ITEMS = 4


def _count_list_items(text: str) -> int:
    """Count lines that start with -, *, a digit+., or contain a colon-separated label."""
    count = 0
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"^[-*]\s+\S", stripped):
            count += 1
        elif re.match(r"^\d+\.\s+\S", stripped):
            count += 1
        elif re.match(r"^#{1,4}\s+\S", stripped):
            count += 1
        elif ":" in stripped and len(stripped) > 5:
            count += 1
    return count


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q1.py <workspace>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    note = ws / "output" / "intake_scope.md"
    if not note.exists():
        print(f"FAIL: {note} does not exist")
        return 1

    text = note.read_text(encoding="utf-8")
    raw_bytes = len(note.read_bytes())
    errors: list[str] = []

    # 1. Size and structure
    if raw_bytes < MIN_BYTES:
        errors.append(
            f"intake_scope.md is too short ({raw_bytes} bytes; minimum {MIN_BYTES})"
        )

    items = _count_list_items(text)
    if items < MIN_LIST_ITEMS:
        errors.append(
            f"intake_scope.md has only {items} labeled item(s); need >= {MIN_LIST_ITEMS} "
            "distinct list items or labeled fields"
        )

    # 2. Regulatory deadline
    if not DEADLINE_RE.search(text):
        errors.append(
            "no regulatory deadline anchor found — expected '2026-03-30', "
            "'March 30', '09:15 UTC', or '48h' to mark the 48-hour reporting deadline"
        )

    # 3. Affected order count
    if not ORDER_COUNT_RE.search(text):
        errors.append(
            "no affected order count anchor found — expected '2,947', '~3,000', "
            "or 'approximately 3,000' to indicate the scale of the incident"
        )

    # 4. Timezone labels (>= 2 distinct)
    tz_hits = [tz for tz in TZ_LABELS if re.search(r"\b" + re.escape(tz) + r"\b", text, re.IGNORECASE)]
    if len(tz_hits) < 2:
        errors.append(
            f"fewer than 2 distinct timezone labels found (found: {tz_hits or 'none'}); "
            "the intake scope must name at least 2 of: UTC, CET, CEST, HKT, SGT, JST, EDT "
            "to document the multi-timezone reconciliation challenge"
        )

    # 5. All four stakeholder placeholders
    for placeholder in STAKEHOLDERS:
        if placeholder not in text:
            errors.append(
                f"missing stakeholder placeholder '{placeholder}' — all four must appear "
                "verbatim: RISK_OFFICER, MATCHING_ENG_LEAD, CLEARING_LEAD, REGULATOR_CONTACT"
            )

    # 6. Anti-decoy
    m = DECOY_RE.search(text)
    if m:
        errors.append(
            f"decoy content detected ('{m.group()}') — the file references _archive/ "
            "migration data which is unrelated to the March 2026 timezone incident"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        "PASS: intake_scope.md captures the regulatory deadline, affected order count, "
        ">= 2 timezone labels, and all four stakeholder placeholders"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
