#!/usr/bin/env python3
"""check_q2.py — Validate output/terms_crosstab.md for q2 (three-grantor terms cross-tabulation).

Key traps:
  - Nordic §9 "Non-Binding Programmatic Clarification" (NOK 5,000 equipment threshold)
    must be explicitly discredited if cited; binding cap is NOK 15,000 per §5.5.
  - Grantor C equipment cap is USD 500 per item (§3.4).
  - Grantor B indirect costs: NOT eligible (§6.2 explicit exclusion).
  - FY2024 archive agreements must not be referenced.

Pass conditions (all must hold):
  1. File exists; >= 600 bytes; contains a table or >= 6 list items covering travel,
     indirect costs, and equipment.
  2. Nordic indirect costs exclusion stated (Nordic + indirect exclusion co-occur within 900 chars).
  3. Grantor C equipment cap USD 500 present.
  4. Nordic binding equipment cap NOK 15,000 present.
  5. §9 discredit window: if NOK 5,000 threshold cited as equipment eligibility rule,
     non-binding / not enforceable / guidance only / §9 must appear within 500 chars.
  6. Anti-decoy: no reference to FY2024 / halcyon_2024 / fy2024_audit.

Usage: python check_q2.py <workspace_abs_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BYTE_MIN = 600
TABLE_OR_LIST_RE = re.compile(
    r"(\|.+\|)|^[-*]\s+.{20,}",
    re.MULTILINE,
)
REQUIRED_TOPICS = re.compile(
    r"travel|indirect|equipment",
    re.IGNORECASE,
)

NORDIC_RE = re.compile(r"Nordic|Grantor\s*B", re.IGNORECASE)
INDIRECT_EXCL_RE = re.compile(
    r"indirect.*exclu|exclu.*indirect|overhead.*not\s+elig|not\s+elig.*overhead|§6\.2",
    re.IGNORECASE,
)
GRANTOR_C_CAP_RE = re.compile(
    r"USD\s*500|500\s*USD|500.*per.?item|\$\s*500",
    re.IGNORECASE,
)
NORDIC_BINDING_CAP_RE = re.compile(
    r"NOK\s*15[,.]?000|15[,.]?000\s*NOK|15000",
    re.IGNORECASE,
)
NOK_5000_RE = re.compile(
    r"NOK\s*5[,.]?000|5[,.]?000\s*NOK|5000\s*NOK",
    re.IGNORECASE,
)
NONBINDING_DISCREDIT_RE = re.compile(
    r"non.?binding|not\s+enforc|guidance\s+only|§9|not\s+a\s+contractual|programmatic\s+clarification",
    re.IGNORECASE,
)
ARCHIVE_RE = re.compile(
    r"FY2024|halcyon_2024|fy2024_audit|grant_2024",
    re.IGNORECASE,
)


def _co_occur_within(text: str, re_a: re.Pattern, re_b: re.Pattern, window: int) -> bool:
    """Return True if any match of re_a and any match of re_b appear within `window` chars."""
    for m_a in re_a.finditer(text):
        start = max(0, m_a.start() - window)
        end = min(len(text), m_a.end() + window)
        if re_b.search(text[start:end]):
            return True
    return False


def _nok5000_safely_discredited(text: str) -> bool:
    """
    If NOK 5,000 appears in an equipment-eligibility context, NONBINDING_DISCREDIT_RE
    must appear within 500 chars of each occurrence.
    """
    for m in NOK_5000_RE.finditer(text):
        start = max(0, m.start() - 500)
        end = min(len(text), m.end() + 500)
        window = text[start:end]
        if not NONBINDING_DISCREDIT_RE.search(window):
            return False
    return True


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q2.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    target = ws / "output" / "terms_crosstab.md"

    if not target.exists():
        print(f"FAIL: missing {target}", file=sys.stderr)
        return 1

    text = target.read_text(encoding="utf-8")
    errors: list[str] = []

    # 1. Byte length
    byte_len = len(text.encode("utf-8"))
    if byte_len < BYTE_MIN:
        errors.append(
            f"terms_crosstab.md too short ({byte_len} bytes); expected >= {BYTE_MIN} bytes "
            "with a comparative table or at least 6 list items covering all three grantors"
        )

    # 1b. Structural check: table rows or list items, and required topics
    table_hits = len(TABLE_OR_LIST_RE.findall(text))
    topic_hits = len(REQUIRED_TOPICS.findall(text))
    if table_hits < 3 and topic_hits < 3:
        errors.append(
            "terms_crosstab.md lacks a comparative table or a list of >= 6 items "
            "covering travel, indirect costs, and equipment for all three grantors"
        )

    # 2. Nordic indirect costs exclusion (Nordic + indirect exclusion co-occur)
    # 窗口放宽到 900：合法的转置 Markdown 表里列头(grantor 名)与单元格("Not Eligible §6.2")
    # 可相距数百字符仍属同一行语义；400 会误杀正确的表格表达。
    if not _co_occur_within(text, NORDIC_RE, INDIRECT_EXCL_RE, 900):
        errors.append(
            "Nordic indirect costs exclusion not clearly stated: "
            "Nordic Development Cooperative (or Grantor B) and indirect-cost-exclusion "
            "language (§6.2 / 'excluded' / 'not eligible') must co-occur within 400 chars"
        )

    # 3. Grantor C equipment cap USD 500
    if not GRANTOR_C_CAP_RE.search(text):
        errors.append(
            "Grantor C (Opal City) equipment per-item cap of USD 500 not found; "
            "expected pattern: 'USD 500' / '500 USD' / '500 per item' / '$500'"
        )

    # 4. Nordic binding equipment cap NOK 15,000
    if not NORDIC_BINDING_CAP_RE.search(text):
        errors.append(
            "Nordic binding equipment cap of NOK 15,000 (§5.5) not found; "
            "the binding cap — not the non-binding §9 threshold — must be stated"
        )

    # 5. §9 discredit window: if NOK 5,000 cited, must be discredited
    if NOK_5000_RE.search(text) and not _nok5000_safely_discredited(text):
        errors.append(
            "NOK 5,000 equipment threshold cited without discredit language within 500 chars; "
            "agent appears to have treated the non-binding §9 clarification as a binding "
            "constraint. Must add: 'non-binding' / 'not enforceable' / 'guidance only' / §9 "
            "label near every mention of the 5,000 threshold."
        )

    # 6. Anti-decoy: FY2024 archive reference
    if ARCHIVE_RE.search(text):
        errors.append(
            "terms_crosstab.md references FY2024 or archive agreements "
            "(FY2024 / halcyon_2024 / fy2024_audit / grant_2024); "
            "agent appears to have read decoy content from _archive/"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
