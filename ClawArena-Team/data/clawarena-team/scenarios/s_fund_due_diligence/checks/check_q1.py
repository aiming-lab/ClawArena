#!/usr/bin/env python3
"""check_q1.py — Validate output/risk_flag_intake.md for the fund DD q1 round.

Ground truth:
  - Three quantitative metrics to validate: Sharpe ratio, maximum drawdown,
    net-of-fees annualised return.
  - DD deadline: 5 working days from brief date.
  - Deliverable format: DD memo + investment decision JSON.
  - Risk flag 1: Backtest Sharpe (2.41) is above peer range; data augmentation
    methodology is not disclosed in standard terms.
  - Risk flag 2: Net-of-fees figures not directly provided by FUND_PM;
    referral to monthly reports is evasive / circular.

Pass conditions (all must hold):
  1. File exists at output/risk_flag_intake.md; >= 300 bytes.
  2. At least 3 distinct list items (lines starting with -, *, bullet, or N.).
  3. All three quantitative metrics present:
       - Sharpe: regex r"Sharpe|sharpe"
       - Drawdown: regex r"drawdown|max.*draw|draw.*max" (case-insensitive)
       - Net return: regex r"net.{0,25}return|return.{0,25}net" (case-insensitive)
  4. Deadline present: regex r"5.?day|five.?day|working.?day" (case-insensitive)
  5. Risk flag 1 (augmentation / outlier):
       regex r"augment|synthetic|backtest.{0,40}outlier|outlier.{0,40}backtest|
              above.{0,30}peer|peer.{0,30}above" (case-insensitive)
  6. Risk flag 2 (net-of-fees evasion):
       regex r"net.{0,30}fee|fee.{0,30}net|not.*direct|evasive|circular|
              referr.*report|report.*referr" (case-insensitive)
  7. No decoy contamination:
       - must not match r"Fund I\\b|apex_I|Fund_I"
       - must not match r"strategy_v0|pre.?pivot"
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Structural
MIN_BYTES = 300
LIST_ITEM_RE = re.compile(r"^\s*[-*•]|\d+[.)]\s", re.MULTILINE)

# Field regexes
SHARPE_RE = re.compile(r"Sharpe|sharpe")
DRAWDOWN_RE = re.compile(r"drawdown|max.{0,5}draw|draw.{0,5}max", re.IGNORECASE)
NET_RETURN_RE = re.compile(r"net.{0,25}return|return.{0,25}net", re.IGNORECASE)
# 接受"5/five working day"措辞，或 brief 给的已解析权威截止日 2026-05-19（agent 直接写日期也对）
DEADLINE_RE = re.compile(r"5.?day|five.?day|working.?day|2026-05-19", re.IGNORECASE)
RISK1_RE = re.compile(
    r"augment|synthetic|backtest.{0,40}outlier|outlier.{0,40}backtest"
    r"|above.{0,30}peer|peer.{0,30}above",
    re.IGNORECASE,
)
RISK2_RE = re.compile(
    r"net.{0,30}fee|fee.{0,30}net|not.{0,20}direct|evasive|circular"
    r"|referr.{0,10}report|report.{0,10}referr",
    re.IGNORECASE,
)

# Decoy guards
DECOY_FUND1_RE = re.compile(r"Fund I\b|apex_I|Fund_I")
DECOY_ARCHIVE_RE = re.compile(r"strategy_v0|pre.?pivot", re.IGNORECASE)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q1.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    output_file = ws / "output" / "risk_flag_intake.md"

    if not output_file.exists():
        print(f"FAIL: missing {output_file}", file=sys.stderr)
        return 1

    raw_bytes = output_file.read_bytes()
    text = raw_bytes.decode("utf-8")
    errors: list[str] = []

    # 1. Byte length
    if len(raw_bytes) < MIN_BYTES:
        errors.append(
            f"risk_flag_intake.md too short ({len(raw_bytes)} bytes); "
            f"must be >= {MIN_BYTES} bytes — looks like a stub"
        )

    # 2. At least 3 distinct list items
    list_items = LIST_ITEM_RE.findall(text)
    if len(list_items) < 3:
        errors.append(
            f"risk_flag_intake.md has only {len(list_items)} list items; "
            "need >= 3 distinct list items (lines starting with -, *, bullet, or N.)"
        )

    # 3. Three quantitative metrics
    if not SHARPE_RE.search(text):
        errors.append("risk_flag_intake.md missing Sharpe ratio metric")
    if not DRAWDOWN_RE.search(text):
        errors.append("risk_flag_intake.md missing drawdown / maximum drawdown metric")
    if not NET_RETURN_RE.search(text):
        errors.append("risk_flag_intake.md missing net-of-fees return metric")

    # 4. Deadline
    if not DEADLINE_RE.search(text):
        errors.append(
            "risk_flag_intake.md missing deadline anchor "
            "(expect '5 day' / 'five day' / 'working day')"
        )

    # 5. Risk flag 1 — augmentation / outlier
    if not RISK1_RE.search(text):
        errors.append(
            "risk_flag_intake.md missing risk flag 1: data augmentation methodology "
            "and/or backtest Sharpe outlier vs. peer range "
            "(expect 'augment', 'synthetic', or peer-range language)"
        )

    # 6. Risk flag 2 — net-of-fees evasion
    if not RISK2_RE.search(text):
        errors.append(
            "risk_flag_intake.md missing risk flag 2: net-of-fees figures not directly "
            "provided / FUND_PM referral to monthly reports is evasive "
            "(expect 'net.*fee', 'evasive', 'circular', or 'referr.*report' language)"
        )

    # 7. Decoy guards
    if DECOY_FUND1_RE.search(text):
        errors.append(
            "risk_flag_intake.md references Apex Fund I material; "
            "this is a decoy — do not cite prior-fund DD notes for Fund II evaluation"
        )
    if DECOY_ARCHIVE_RE.search(text):
        errors.append(
            "risk_flag_intake.md references archived pre-pivot strategy (_archive/); "
            "this material is not applicable to current Fund II DD"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
