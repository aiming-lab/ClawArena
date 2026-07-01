#!/usr/bin/env python3
"""check_q1.py — Validate output/audit_intake.md for q1 (audit brief comprehension).

Pass conditions (all must hold):
  1. File exists at output/audit_intake.md; >= 400 bytes.
  2. Contains >= 3 distinct sections or list items.
  3. All three grantor names appear (regex matches >= 3 times across Halcyon/Nordic/Opal).
  4. Each of the three grantors is identifiable separately (per-grantor regex).
  5. At least one deliverable type is mentioned (compliance report / non-compliance / NC-[ABC]).
  6. Anti-decoy: no reference to FY2024 archive material.

Usage: python check_q1.py <workspace_abs_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

GRANTOR_HITS_RE = re.compile(r"Halcyon|Nordic|Opal", re.IGNORECASE)
GRANTOR_A_RE = re.compile(r"Halcyon|Grantor\s*A", re.IGNORECASE)
GRANTOR_B_RE = re.compile(r"Nordic|Grantor\s*B", re.IGNORECASE)
GRANTOR_C_RE = re.compile(r"Opal\s*City|Grantor\s*C", re.IGNORECASE)
DELIVERABLE_RE = re.compile(r"compliance\s*report|non.?compli|NC.?[ABC]", re.IGNORECASE)
SECTION_OR_ITEM_RE = re.compile(r"^(#{1,4}\s+\S|[-*]\s+\S|\d+\.\s+\S)", re.MULTILINE)
ARCHIVE_RE = re.compile(r"FY2024|fy2024|grant_2024|2024_closed", re.IGNORECASE)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q1.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    target = ws / "output" / "audit_intake.md"

    if not target.exists():
        print(f"FAIL: missing {target}", file=sys.stderr)
        return 1

    text = target.read_text(encoding="utf-8")
    errors: list[str] = []

    # 1. Byte length
    byte_len = len(text.encode("utf-8"))
    if byte_len < 400:
        errors.append(
            f"audit_intake.md too short ({byte_len} bytes); expected >= 400 bytes "
            "covering all three grantors with open questions per grantor"
        )

    # 2. Structural depth: >= 3 sections or list items
    structural_hits = len(SECTION_OR_ITEM_RE.findall(text))
    if structural_hits < 3:
        errors.append(
            f"audit_intake.md has only {structural_hits} structural item(s); "
            "expected >= 3 (headers or list bullets), one per grantor at minimum"
        )

    # 3. Grantor name coverage: >= 3 total hits across all three names
    grantor_total = len(GRANTOR_HITS_RE.findall(text))
    if grantor_total < 3:
        errors.append(
            f"grantor names appear only {grantor_total} time(s); expected >= 3 "
            "(each of Halcyon, Nordic, Opal City should be named)"
        )

    # 4. Per-grantor presence
    if not GRANTOR_A_RE.search(text):
        errors.append("Grantor A (Halcyon Foundation) not identified in audit_intake.md")
    if not GRANTOR_B_RE.search(text):
        errors.append("Grantor B (Nordic Development Cooperative) not identified")
    if not GRANTOR_C_RE.search(text):
        errors.append("Grantor C (Opal City Community Fund) not identified")

    # 5. Deliverable type mentioned
    if not DELIVERABLE_RE.search(text):
        errors.append(
            "no deliverable type mentioned; expected reference to compliance report, "
            "non-compliance items, or NC-A/NC-B/NC-C coding system"
        )

    # 6. Anti-decoy: FY2024 archive contamination
    if ARCHIVE_RE.search(text):
        errors.append(
            "audit_intake.md references FY2024 or archive material "
            "(FY2024 / grant_2024 / 2024_closed); agent appears to have read "
            "decoy content from _archive/grant_2024_closed/"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
