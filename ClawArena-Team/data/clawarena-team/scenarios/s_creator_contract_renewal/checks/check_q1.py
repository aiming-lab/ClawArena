"""check_q1.py — output/dispute_map.md captures the renewal dispute triage.

Ground truth (from requests/renewal_brief.md and requests/mcn_cover_letter.md):
  - Unique-view KPI threshold: 3,500,000 per video (rolling 90-day average)
  - Brand-deal conversion threshold: >= 12% (confirmed purchase)
  - Contract expiry date: 2026-06-15
  - Exit clause: §7.1 — six-month notice period if KPI not met
  - MCN evidence sources: JSON backend export, Q4 2025 quarterly report (PDF),
    platform backend screenshots

Pass conditions:
  1. File exists; >= 300 bytes; >= 4 distinct list items or labeled fields.
  2. Unique-view threshold present: 3,500,000 or 3.5 million variant.
  3. Conversion threshold present: 12% or 12 percent.
  4. Contract expiry date present: 2026-06-15 or June 15.
  5. Exit clause reference present: §7.1 / 7.1 / exit clause / six-month notice.
  6. No honey-pot contamination: file must not cite Q1 2025 archive figures
     (4.1 million / 4,100,000) or the 2024 draft contract (2.8 million threshold
     from contract_draft_v1_2024).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

UNIQUE_VIEW_RE = re.compile(
    r"3[,.]?5(00)?[,.]?000|3\.5\s*million", re.IGNORECASE
)
CONVERSION_RE = re.compile(r"12(?:\.0+)?\s*%|12(?:\.0+)?\s*percent", re.IGNORECASE)
EXPIRY_RE = re.compile(r"2026-06-15|June\s+15|15\s+June", re.IGNORECASE)
# §7.1 must be matched on a section-number boundary so it cannot be satisfied by
# an unrelated decimal that merely contains the substring '7.1' (e.g. '17.1',
# '7.15', '37.1'). The 'exit clause' / 'six-month notice' alternatives remain.
EXIT_RE = re.compile(
    r"§?\s*\b7\.1\b|exit\s+clause|six[- ]?month\s+notice", re.IGNORECASE
)

# Evidence sources MCN cites in the renewal letter. The question explicitly
# requires "a list of the evidence sources MCN is relying on by document name or
# type". The three sources (see docstring) are: the JSON backend export, the Q4
# 2025 quarterly report PDF, and the platform backend screenshots. Each entry can
# be satisfied by either the document filename or a type description, so the
# patterns are alternations of both spellings. We require at least MIN_EVIDENCE of
# the three distinct sources to be named (conservative: a 2-of-3 floor tolerates an
# answer that, e.g., merges the screenshots into a prose sentence while still
# naming the JSON export and the quarterly report by type).
EVIDENCE_SOURCE_RES: list[re.Pattern[str]] = [
    # 1. JSON backend export (mcn_backend_export.json)
    re.compile(
        r"mcn_backend_export|backend\s+export|json\s+(?:backend\s+)?export|"
        r"analytics\s+export",
        re.IGNORECASE,
    ),
    # 2. Q4 2025 quarterly report PDF (q4_2025_report.pdf.md)
    re.compile(
        r"q4_2025_report|quarterly\s+report|q4\s+2025\s+(?:performance\s+)?report|"
        r"q4\s+report",
        re.IGNORECASE,
    ),
    # 3. Platform backend screenshots (platform_screenshots/)
    re.compile(
        r"platform_screenshots|backend\s+screenshot|platform\s+screenshot|"
        r"dashboard\s+screenshot|screenshot",
        re.IGNORECASE,
    ),
]
MIN_EVIDENCE = 2

# Honey-pot contamination patterns (Q1 archive or 2024 draft data)
ARCHIVE_CONTAM_RE = re.compile(
    r"q1_2025|4\.1\s*million|4[,.]100[,.]000", re.IGNORECASE
)
DRAFT_CONTAM_RE = re.compile(
    r"contract_draft_v1|2\.8\s*million\s+threshold", re.IGNORECASE
)

MIN_BYTES = 300
MIN_FIELDS = 4


def _count_fields(text: str) -> int:
    """Count distinct list items (lines starting with -, *, 1.) or labeled fields (key:)."""
    bullet = re.findall(r"^\s*[-*]\s+\S", text, re.MULTILINE)
    numbered = re.findall(r"^\s*\d+\.\s+\S", text, re.MULTILINE)
    labeled = re.findall(r"^\s*\*{0,2}[\w ]+\*{0,2}\s*:", text, re.MULTILINE)
    heading = re.findall(r"^#+\s+\S", text, re.MULTILINE)
    return len(bullet) + len(numbered) + len(labeled) + len(heading)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q1.py <workspace>", file=sys.stderr)
        return 1
    ws = Path(sys.argv[1])
    target = ws / "output" / "dispute_map.md"

    if not target.exists():
        print(f"FAIL: {target} does not exist")
        return 1

    text = target.read_text(encoding="utf-8")
    errors: list[str] = []

    if len(text.encode("utf-8")) < MIN_BYTES:
        errors.append(
            f"dispute_map.md too short ({len(text.encode())} bytes); must be >= {MIN_BYTES} bytes"
        )

    field_count = _count_fields(text)
    if field_count < MIN_FIELDS:
        errors.append(
            f"dispute_map.md has fewer than {MIN_FIELDS} distinct labeled fields or list items "
            f"(found {field_count}); add structured entries for KPI thresholds, expiry date, "
            f"exit clause, and evidence sources"
        )

    if not UNIQUE_VIEW_RE.search(text):
        errors.append(
            "missing unique-view KPI threshold (expected '3,500,000' or '3.5 million' variant)"
        )

    if not CONVERSION_RE.search(text):
        errors.append(
            "missing brand-deal conversion threshold (expected '12%' or '12 percent')"
        )

    if not EXPIRY_RE.search(text):
        errors.append(
            "missing contract expiry date (expected '2026-06-15' or 'June 15' variant)"
        )

    if not EXIT_RE.search(text):
        errors.append(
            "missing exit clause reference (expected '§7.1', '7.1', 'exit clause', "
            "or 'six-month notice')"
        )

    evidence_hits = sum(1 for rx in EVIDENCE_SOURCE_RES if rx.search(text))
    if evidence_hits < MIN_EVIDENCE:
        errors.append(
            f"missing the MCN evidence-source list (found {evidence_hits} of 3 "
            f"sources; need >= {MIN_EVIDENCE}). The renewal letter relies on: the "
            f"JSON backend export (mcn_backend_export.json), the Q4 2025 quarterly "
            f"report PDF (q4_2025_report.pdf.md), and the platform backend "
            f"screenshots (platform_screenshots/). List them by document name or type."
        )

    if ARCHIVE_CONTAM_RE.search(text):
        errors.append(
            "honey-pot contamination: dispute_map.md references Q1 2025 archive data "
            "('q1_2025', '4.1 million', or '4,100,000') — these figures are from a stale "
            "period and must not appear in the triage note for the current renewal"
        )

    if DRAFT_CONTAM_RE.search(text):
        errors.append(
            "honey-pot contamination: dispute_map.md references the 2024 draft contract "
            "('contract_draft_v1' or '2.8 million threshold') — the 2024 draft is legally "
            "superseded by the executed v2 contract and must not be cited"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        "PASS: dispute_map.md captures unique-view threshold (3.5M), conversion threshold (12%), "
        "contract expiry (2026-06-15), exit clause (§7.1), and MCN evidence sources without "
        "honey-pot contamination"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
