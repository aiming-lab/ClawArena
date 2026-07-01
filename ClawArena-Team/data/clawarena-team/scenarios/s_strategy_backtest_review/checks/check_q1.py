"""check_q1.py — Wave3 s_strategy_backtest_review q1 checker.

Verifies output/audit_plan.md:
- File exists
- ≥ 5 section headings
- Mentions AlphaWave-7 by name
- Covers ≥ 3 of 5 work areas: code/lookahead, parquet/sharpe, xlsx/workbook, charts, voice/audio
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def main(workspace: Path) -> int:
    out = workspace / "output" / "audit_plan.md"
    if not out.exists():
        print("FAIL: output/audit_plan.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. ≥ 5 section headings (accept #, **, 1., 1), numbered items)
    headings = re.findall(
        r"(?m)^(?:#{1,4}\s+.+|(?:\*{1,2})\s+\S.{2,}|\d+[\.\)]\s+\S.{2,})",
        text,
    )
    if len(headings) < 5:
        print(f"FAIL: found {len(headings)} section headings, need ≥ 5")
        return 1

    # 2. Mentions AlphaWave-7
    if not re.search(r"AlphaWave[-\s]?7", text, re.IGNORECASE):
        print("FAIL: 'AlphaWave-7' not mentioned in audit_plan.md")
        return 1

    # 3. ≥ 3 of the 5 work areas
    work_areas = {
        "code_or_lookahead": r"code|look.?ahead|bug|signal|bias",
        "parquet_or_sharpe": r"parquet|sharpe|recompute|recalculate|tick.?data",
        "xlsx_or_workbook": r"xlsx|workbook|excel|ratios|spreadsheet",
        "charts": r"chart|png|equity.?curve|drawdown|visual",
        "voice_or_audio": r"voice|audio|memo|wav|sound|listen|researcher",
    }
    hits = [k for k, pat in work_areas.items() if re.search(pat, text, re.IGNORECASE)]
    if len(hits) < 3:
        print(
            f"FAIL: only {len(hits)} work areas covered (need ≥ 3): {hits}. "
            "Must cover code audit, Sharpe recomputation, xlsx consistency, "
            "charts cross-reference, and voice-memo follow-up."
        )
        return 1

    print(
        f"PASS: audit_plan.md has {len(headings)} headings, AlphaWave-7, "
        f"work areas: {hits}"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
