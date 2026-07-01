"""check_q2.py — Staff roster consolidation with HR schema reconciliation.

Ground truth:
  - Hospital A Tier-1 cardiac headcount: 47
  - Hospital B Tier-1 cardiac headcount: 44
  - Unified FTE (Tier-1 only): 84.5
  - Unified tenure column name: unified_tenure
  - Schema trap: tenure_years (A) and years_of_service (B) must NOT both appear
    as separate header columns in the consolidated CSV.

Pass conditions:
  output/consolidated_roster.csv
    1. Exists; >= 5000 bytes; has a header row; >= 80 data rows.
    2. Header contains 'unified_tenure'.
    3. Header does NOT contain both 'tenure_years' AND 'years_of_service'.
    4. Has a column distinguishing source hospital (source_hospital / site / hospital / origin).

  output/roster_summary.md
    1. Exists; >= 300 bytes; >= 3 list items or labeled fields.
    2. Hospital A Tier-1 count 47 near St. Alban's / Hospital A context.
    3. Hospital B Tier-1 count 44 near Riverside / Hospital B context.
    4. Unified FTE 84.5 present.
    5. Schema mismatch acknowledgment present.
    6. No archive contamination: '2024' near a staffing count >= 30 is a hard fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Regex anchors.
FTE_RE = re.compile(r"\b84\.5\b|\b84\s+\.?\s*5\b")
SCHEMA_ACK_RE = re.compile(
    r"tenure_years|years_of_service|unified_tenure|schema|column.*differ|differ.*column",
    re.IGNORECASE,
)
HOSP_A_CONTEXT = re.compile(r"St\.?\s*Alban|Hospital\s+A|hosp_a", re.IGNORECASE)
HOSP_B_CONTEXT = re.compile(r"Riverside|Hospital\s+B|hosp_b", re.IGNORECASE)
SOURCE_COL_RE = re.compile(
    r"source_hospital|source|site|hospital|origin", re.IGNORECASE
)
ARCHIVE_YEAR_RE = re.compile(r"\b2024\b")
STAFFING_COUNT_RE = re.compile(r"\b[3-9]\d\b|\b[1-2]\d{2}\b")


def _check_roster_csv(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing: {path}"]

    raw = path.read_bytes()
    if len(raw) < 5000:
        errors.append(
            f"consolidated_roster.csv too small ({len(raw)} bytes); must be >= 5000 bytes"
        )

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")

    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines:
        errors.append("consolidated_roster.csv appears empty")
        return errors

    header = lines[0].lower()
    data_rows = lines[1:]

    # Minimum row count.
    if len(data_rows) < 80:
        errors.append(
            f"consolidated_roster.csv has only {len(data_rows)} data rows; "
            "expected >= 80 (Tier-1 staff from both hospitals)"
        )

    # unified_tenure present.
    if "unified_tenure" not in header:
        errors.append(
            "consolidated_roster.csv header is missing 'unified_tenure' column; "
            "the two tenure columns must be unified into a single column"
        )

    # Schema trap: both raw columns present.
    has_tenure_years = "tenure_years" in header
    has_years_of_service = "years_of_service" in header
    if has_tenure_years and has_years_of_service:
        errors.append(
            "consolidated_roster.csv header contains both 'tenure_years' AND "
            "'years_of_service' — schema was not unified; "
            "only 'unified_tenure' should appear in the merged output"
        )

    # Source hospital column.
    if not SOURCE_COL_RE.search(header):
        errors.append(
            "consolidated_roster.csv has no column identifying the source hospital "
            "(expected 'source_hospital', 'site', 'hospital', or similar)"
        )

    return errors


def _find_count_near_context(text: str, count: int, context_re: re.Pattern) -> bool:
    """Return True if `count` appears within 300 chars of a context match."""
    count_str = str(count)
    count_pat = re.compile(r"\b" + re.escape(count_str) + r"\b")
    for cm in context_re.finditer(text):
        window_start = max(0, cm.start() - 300)
        window_end = min(len(text), cm.end() + 300)
        window = text[window_start:window_end]
        if count_pat.search(window):
            return True
    return False


def _check_roster_summary(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing: {path}"]

    text = path.read_text(encoding="utf-8")

    if len(text.encode("utf-8")) < 300:
        errors.append(
            f"roster_summary.md too short ({len(text.encode())} bytes); must be >= 300 bytes"
        )

    # Section / list structure.
    headers = re.findall(r"^#{1,4}\s+\S", text, re.MULTILINE)
    list_items = re.findall(r"^[ \t]*[-*\d]\S*\s+\S", text, re.MULTILINE)
    if len(headers) + len(list_items) < 3:
        errors.append(
            "roster_summary.md has fewer than 3 section headers or list items"
        )

    # Hospital A count 47 near Hospital A context.
    if not _find_count_near_context(text, 47, HOSP_A_CONTEXT):
        errors.append(
            "roster_summary.md does not show Hospital A Tier-1 count of 47 "
            "near a Hospital A / St. Alban's reference"
        )

    # Hospital B count 44 near Hospital B context.
    if not _find_count_near_context(text, 44, HOSP_B_CONTEXT):
        errors.append(
            "roster_summary.md does not show Hospital B Tier-1 count of 44 "
            "near a Hospital B / Riverside General reference"
        )

    # Unified FTE 84.5.
    if not FTE_RE.search(text):
        errors.append(
            "roster_summary.md does not contain unified FTE figure of 84.5"
        )

    # Schema mismatch acknowledgment.
    if not SCHEMA_ACK_RE.search(text):
        errors.append(
            "roster_summary.md does not acknowledge the HR schema mismatch "
            "(tenure_years vs years_of_service, or unified_tenure, or column difference)"
        )

    # Archive contamination: 2024 near a staffing count.
    for m in ARCHIVE_YEAR_RE.finditer(text):
        window_start = max(0, m.start() - 200)
        window_end = min(len(text), m.end() + 200)
        window = text[window_start:window_end]
        if STAFFING_COUNT_RE.search(window):
            errors.append(
                "roster_summary.md appears to cite 2024 archive roster figures "
                "in a staffing-count context — use only the 2026 HR CSV exports"
            )
            break

    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q2.py <workspace>", file=sys.stderr)
        return 1
    ws = Path(sys.argv[1])
    errors: list[str] = []

    errors.extend(_check_roster_csv(ws / "output" / "consolidated_roster.csv"))
    errors.extend(_check_roster_summary(ws / "output" / "roster_summary.md"))

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        "PASS: consolidated_roster.csv uses unified_tenure column, "
        "roster_summary.md correctly reports 47 + 44 Tier-1 staff, "
        "84.5 FTE, and acknowledges the schema mismatch"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
