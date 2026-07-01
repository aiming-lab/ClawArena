"""check_q4.py — Equipment deduplication and union disposal arbitration.

Ground truth (from 2026 equipment CSVs + union_docs/memo_2026_equipment_disposal.md via u1):
  - Total serial-number duplicates: 23
  - Disposal method: RMEA auction within 30 days of merger effective date
  - Merger effective date: 2026-06-01 => 30-day deadline: 2026-07-01
  - Internal transfer: PROHIBITED without RMEA waiver

Pass conditions:
  output/equipment_dedup.csv
    1. Exists; >= 2000 bytes; header row present; exactly 23 data rows.
    2. Header contains serial number column, device category column,
       and at least one of: disposal_method / disposition / action.
    3. If row count == 19, fail with archive-contamination message.

  output/equipment_disposition_memo.md
    1. Exists; >= 600 bytes; >= 3 sections or list items.
    2. '23' appears in context of duplicates/devices.
    3. RMEA / Regional Medical Equipment Authority present.
    4. Auction + 30-day deadline combination present.
    5. Internal transfer prohibition explicit.
    6. '19' must NOT appear as a duplicate device count.
    7. Cross-round dependency: output/roster_summary.md (q2) must exist.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RMEA_RE = re.compile(r"RMEA|Regional\s+Medical\s+Equipment\s+Authority", re.IGNORECASE)
AUCTION_30_RE = re.compile(
    r"auction.*30\s*day|30\s*day.*auction|RMEA.*auction|auction.*merger.*effective",
    re.IGNORECASE,
)
INTERNAL_PROHIBIT_RE = re.compile(
    r"internal\s+transfer.*prohibit|prohibit.*internal\s+transfer"
    r"|NOT.*internal\s+transfer|internal.*NOT|no\s+internal\s+transfer"
    r"|internal.*not\s+permit|not\s+permit.*internal",
    re.IGNORECASE,
)

SERIAL_COL_RE = re.compile(r"serial", re.IGNORECASE)
CATEGORY_COL_RE = re.compile(r"category|type|device_type|device_category", re.IGNORECASE)
DISPOSITION_COL_RE = re.compile(r"disposal_method|disposition|action|method", re.IGNORECASE)

# Near-context check: '23' within 300 chars of 'duplicate' or 'device'.
DUPLICATE_CONTEXT_RE = re.compile(r"duplicat|device|serial", re.IGNORECASE)


def _find_num_near_context(text: str, num: int, context_re: re.Pattern) -> bool:
    pat = re.compile(r"\b" + str(num) + r"\b")
    for cm in context_re.finditer(text):
        window = text[max(0, cm.start() - 300):min(len(text), cm.end() + 300)]
        if pat.search(window):
            return True
    return False


def _check_dedup_csv(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing: {path}"]

    raw = path.read_bytes()
    if len(raw) < 2000:
        errors.append(
            f"equipment_dedup.csv too small ({len(raw)} bytes); must be >= 2000 bytes"
        )

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")

    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines:
        errors.append("equipment_dedup.csv appears empty")
        return errors

    header_raw = lines[0]
    header = header_raw.lower()
    data_rows = lines[1:]
    data_count = len(data_rows)

    # Archive contamination: 19 rows => 2024 archive.
    if data_count == 19:
        errors.append(
            "equipment_dedup.csv has exactly 19 data rows — this matches the 2024 archive "
            "equipment list (19 duplicates); the correct 2026 duplicate count is 23; "
            "use the 2026 equipment CSVs, not _archive/abandoned_merger_2024/equipment_list_2024.csv"
        )
    elif data_count != 23:
        errors.append(
            f"equipment_dedup.csv has {data_count} data rows; expected exactly 23 "
            f"(one per serial-number duplicate pair); "
            f"{'too few — check if 2024 archive was used' if data_count < 23 else 'too many — review dedup logic'}"
        )

    # Required columns.
    if not SERIAL_COL_RE.search(header):
        errors.append(
            "equipment_dedup.csv header is missing a serial number column"
        )
    if not CATEGORY_COL_RE.search(header):
        errors.append(
            "equipment_dedup.csv header is missing a device category column"
        )
    if not DISPOSITION_COL_RE.search(header):
        errors.append(
            "equipment_dedup.csv header is missing a disposal method column "
            "(disposal_method / disposition / action)"
        )

    return errors


def _check_disposition_memo(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing: {path}"]

    text = path.read_text(encoding="utf-8")

    if len(text.encode("utf-8")) < 600:
        errors.append(
            f"equipment_disposition_memo.md too short ({len(text.encode())} bytes); "
            "must be >= 600 bytes"
        )

    # Section structure.
    headers = len(re.findall(r"^#{1,4}\s+\S", text, re.MULTILINE))
    list_items = len(re.findall(r"^[ \t]*[-*\d]\S*\s+\S", text, re.MULTILINE))
    if headers + list_items < 3:
        errors.append(
            "equipment_disposition_memo.md has fewer than 3 section headers or list items"
        )

    # '23' near duplicate/device context.
    if not _find_num_near_context(text, 23, DUPLICATE_CONTEXT_RE):
        errors.append(
            "equipment_disposition_memo.md does not state the duplicate count of 23 "
            "in a device/duplicate context"
        )

    # RMEA.
    if not RMEA_RE.search(text):
        errors.append(
            "equipment_disposition_memo.md does not reference RMEA "
            "(Regional Medical Equipment Authority) as the disposal authority"
        )

    # Auction + 30-day.
    if not AUCTION_30_RE.search(text):
        errors.append(
            "equipment_disposition_memo.md does not establish the RMEA auction "
            "within 30 days of merger effective date requirement"
        )

    # Internal transfer prohibition.
    if not INTERNAL_PROHIBIT_RE.search(text):
        errors.append(
            "equipment_disposition_memo.md does not explicitly state that "
            "internal transfer of duplicate devices is prohibited"
        )

    # Anti-archive: '19' as a duplicate count.
    if re.search(r"\b19\b", text):
        for m in re.finditer(r"\b19\b", text):
            window = text[max(0, m.start() - 200):min(len(text), m.end() + 200)]
            if re.search(r"duplicat|device|serial", window, re.IGNORECASE):
                errors.append(
                    "equipment_disposition_memo.md contains '19' as a duplicate count "
                    "— this is the 2024 archive figure; the correct 2026 count is 23"
                )
                break

    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q4.py <workspace>", file=sys.stderr)
        return 1
    ws = Path(sys.argv[1])
    errors: list[str] = []

    # Cross-round dependency: q2 roster_summary.md must exist.
    roster_summary = ws / "output" / "roster_summary.md"
    if not roster_summary.exists():
        errors.append(
            "output/roster_summary.md (q2 output) is missing — "
            "cross-round dependency not satisfied; complete round 2 first"
        )

    errors.extend(_check_dedup_csv(ws / "output" / "equipment_dedup.csv"))
    errors.extend(_check_disposition_memo(ws / "output" / "equipment_disposition_memo.md"))

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        "PASS: equipment_dedup.csv has exactly 23 serial-number duplicate rows, "
        "disposition memo cites RMEA auction within 30 days "
        "and explicitly prohibits internal transfer"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
