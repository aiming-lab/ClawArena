#!/usr/bin/env python3
"""
check_full_timeline.py — Validates analysis/full_case_timeline.md.

Checks:
  1. File exists at analysis/full_case_timeline.md
  2. "2025-07-15" or "July 15" present (HIS migration)
  3. "2025-08-01" or "August 1" present (IRB approval)
  4. "2026-03-27" or "March 27" present (committee decision)
  5. ≥8 events in table or list
  6. [NUMERIC] IRB timeline: irb_before_extraction — IRB date (2025-08-01) precedes
     extraction date (2025-09-15), both dates present in document
  7. [NUMERIC] N=912, N=847, 65 present as word-boundary numbers
  8. [NUMERIC] Full IRB number BFH-2025-IRB-0342 present
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_full_timeline.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "full_case_timeline.md"

    if not target.exists():
        print(f"FAILED: {target} does not exist")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # HIS migration date
    has_his = "2025-07-15" in content or re.search(r'July\s+15', content, re.IGNORECASE)
    if not has_his:
        failures.append(
            "FAILED: HIS migration date '2025-07-15' or 'July 15' not found"
        )

    # IRB approval date
    has_irb = "2025-08-01" in content or re.search(r'August\s+1\b', content, re.IGNORECASE)
    if not has_irb:
        failures.append(
            "FAILED: IRB approval date '2025-08-01' or 'August 1' not found"
        )

    # Data extraction date (irb_before_extraction check)
    has_extraction = "2025-09-15" in content or re.search(
        r'September\s+15', content, re.IGNORECASE
    )
    if not has_extraction:
        failures.append(
            "FAILED: data extraction date '2025-09-15' not found — "
            "must include extraction date to establish irb_before_extraction=true"
        )

    # Committee decision date
    has_committee = "2026-03-27" in content or re.search(r'March\s+27', content, re.IGNORECASE)
    if not has_committee:
        failures.append(
            "FAILED: committee decision date '2026-03-27' or 'March 27' not found"
        )

    # ≥8 events: count table rows (| delimited) or list items
    table_rows = re.findall(r'^\|.+\|', content, re.MULTILINE)
    # Subtract header and separator rows
    data_rows = [r for r in table_rows if not re.match(r'^\|[-| ]+\|$', r.strip())]

    list_items = re.findall(r'^[-*]\s+.+', content, re.MULTILINE)

    # Also count date mentions as a proxy for events
    date_refs = re.findall(r'\b\d{4}-\d{2}-\d{2}\b', content)

    event_count = max(len(data_rows), len(list_items), len(set(date_refs)))
    if event_count < 8:
        failures.append(
            f"FAILED: only {event_count} events detected in timeline "
            "(expected ≥8 events in table or list)"
        )

    # --- NUMERIC VALIDATION ---
    if not re.search(r'\b912\b', content):
        failures.append("FAILED: N=912 not found as standalone number")
    if not re.search(r'\b847\b', content):
        failures.append("FAILED: N=847 not found as standalone number")
    if not re.search(r'\b65\b', content):
        failures.append("FAILED: discrepancy count 65 not found as standalone number")
    if 'BFH-2025-IRB-0342' not in content:
        failures.append("FAILED: IRB number #BFH-2025-IRB-0342 not found")

    if failures:
        for f in failures:
            print(f)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
