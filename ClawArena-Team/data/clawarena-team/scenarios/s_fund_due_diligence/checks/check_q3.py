#!/usr/bin/env python3
"""check_q3.py — Validate output/live_sharpe.md for the fund DD q3 round.

Ground truth:
  - Net-of-fees annualised Sharpe (2024 live period): 1.62
    Source: live_reports/live_performance_summary_2024.md FOOTER blockquote.
    Exact label in source: "Annualised net-of-fees Sharpe: 1.62"
  - Gross-of-fees annualised Sharpe (body): 2.03
  - Net figures location: page footer blockquote (six-point font in original PDF)

Pass conditions (all must hold):
  1. File exists at output/live_sharpe.md; >= 400 bytes.
  2. At least 3 distinct labeled fields or list items.
  3. Net Sharpe in [1.60, 1.64]: regex r"\\b1\\.6[0-4]\\b" must appear.
  4. Gross Sharpe in [2.01, 2.05]: regex r"\\b2\\.0[1-5]\\b" must appear.
  5. Footer location identified: r"footer|foot.?note|page.?foot|small.?font|
       six.?point|blockquote" (case-insensitive) must appear.
  6. True value (C10): net Sharpe must be syntactically labelled as net-of-fees:
       regex r"net.{0,60}1\\.6[0-4]|1\\.6[0-4].{0,60}net" (case-insensitive).
  7. Anti-shortcut: if file cites _index.md as the source of the net figure
       WITHOUT also citing the footer, emit WARNING (not FAIL) that the agent
       may have read the misleading index rather than the report footers.
  8. No archive contamination: must not contain r"0\\.83|1\\.45|apex.*fund.?I\\b"
       (would indicate agent read the decoy prior-fund DD or pre-pivot backtest).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

MIN_BYTES = 400
LIST_ITEM_RE = re.compile(r"^\s*[-*•]|\d+[.)]\s|##? ", re.MULTILINE)

# Value regexes
NET_SHARPE_RE = re.compile(r"\b1\.6[0-4]\b")
GROSS_SHARPE_RE = re.compile(r"\b2\.0[1-5]\b")

# Location of net figures
FOOTER_RE = re.compile(
    r"footer|foot.?note|page.?foot|small.?font|six.?point|blockquote",
    re.IGNORECASE,
)

# True-value labelled citation
NET_LABEL_RE = re.compile(
    r"net.{0,60}1\.6[0-4]|1\.6[0-4].{0,60}net",
    re.IGNORECASE,
)

# Anti-shortcut: index.md misuse without footer citation
INDEX_MD_RE = re.compile(r"_index\.md.{0,200}net|index.{0,200}net.{0,200}figure", re.IGNORECASE)

# Archive contamination
ARCHIVE_RE = re.compile(r"0\.83|1\.45|apex.{0,5}fund.?I\b", re.IGNORECASE)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q3.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    output_file = ws / "output" / "live_sharpe.md"

    if not output_file.exists():
        print(f"FAIL: missing {output_file}", file=sys.stderr)
        return 1

    raw_bytes = output_file.read_bytes()
    text = raw_bytes.decode("utf-8")
    errors: list[str] = []

    # 1. Byte length
    if len(raw_bytes) < MIN_BYTES:
        errors.append(
            f"live_sharpe.md too short ({len(raw_bytes)} bytes); "
            f"must be >= {MIN_BYTES} bytes"
        )

    # 2. At least 3 labeled fields / list items
    items = LIST_ITEM_RE.findall(text)
    if len(items) < 3:
        errors.append(
            f"live_sharpe.md has only {len(items)} labeled sections or list items; "
            "need >= 3 distinct labeled fields"
        )

    # 3. Net Sharpe in [1.60, 1.64]
    if not NET_SHARPE_RE.search(text):
        errors.append(
            "live_sharpe.md missing the net-of-fees annualised Sharpe; "
            "expected a float in [1.60, 1.64] — the authoritative value (1.62) "
            "appears only in the page footer of live_performance_summary_2024.md"
        )

    # 4. Gross Sharpe in [2.01, 2.05]
    if not GROSS_SHARPE_RE.search(text):
        errors.append(
            "live_sharpe.md missing the gross-of-fees annualised Sharpe; "
            "expected a float in [2.01, 2.05] — the gross Sharpe (2.03) appears "
            "in the body section of live_performance_summary_2024.md"
        )

    # 5. Footer location identified
    if not FOOTER_RE.search(text):
        errors.append(
            "live_sharpe.md does not identify where the net-of-fees figures appear; "
            "must reference the footer / footnote / page-footer / blockquote location "
            "of the document structure"
        )

    # 6. True value: net Sharpe must be syntactically labelled as net
    if not NET_LABEL_RE.search(text):
        errors.append(
            "live_sharpe.md does not label the net Sharpe as net-of-fees; "
            "the float 1.6x must appear adjacent to 'net' to confirm the agent "
            "identified the correct (post-cost) figure and not just any Sharpe value"
        )

    # 7. Anti-shortcut warning (not a FAIL — emitted as a stderr warn, counted separately)
    if INDEX_MD_RE.search(text) and not FOOTER_RE.search(text):
        print(
            "[warn] live_sharpe.md appears to cite _index.md as the net-figure source "
            "without also referencing the footer section; the index contains a misleading "
            "claim ('all figures net-of-fees') that is incorrect — the authoritative "
            "net Sharpe is in the report footer blockquotes only",
            file=sys.stderr,
        )

    # 8. Archive contamination
    if ARCHIVE_RE.search(text):
        errors.append(
            "live_sharpe.md references archive contamination (0.83, 1.45, or Fund I); "
            "these values come from decoy files and are not applicable to Fund II live analysis"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
