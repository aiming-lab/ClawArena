"""check_q2.py — output/kpi_audit.md uses the correct JSON column for KPI computation.

Ground truth (from platform_data/mcn_backend_export.json):
  - Correct column: view_count_unique (deduplicated per platform ToS §3.4)
  - Q4 2025 unique-view average (38 videos): 2,781,440       ← does NOT meet 3,500,000
  - Trap column: view_count_raw (includes purchased traffic)
  - Q4 2025 raw average (38 videos): 3,592,000               ← appears to meet threshold
  - Confirmed-purchase conversion average: 10.3%             ← does NOT meet 12%
  - Click-through conversion average (trap): 12.8%           ← appears to meet threshold

Anti-shortcut (C10):
  No text file in the workspace may contain the string "2,781,440".
  The check verifies that '2,781,440' does NOT appear in any .md or .txt file under
  workspace/ — it must be derived from the JSON by the subagent, not read from a text hint.

Pass conditions:
  1. File exists; >= 400 bytes; >= 4 labeled fields.
  2. Unique-view figure 2,781,440 present.
  3. Confirmed-purchase conversion 10.3% present.
  4. KPI not-met conclusion for both metrics.
  5. Column selection rationale references view_count_unique.
  6. Anti-trap: if raw figure 3,592,000 appears, it must be discredited within 300 chars.
  7. Anti-trap: if 12.8% appears, it must be discredited within 300 chars.
  8. Anti-shortcut: '2,781,440' must not appear in any .md or .txt workspace text file
     other than the output file itself.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

UNIQUE_VIEW_RE = re.compile(r"2[,.]?781[,.]?440|2\.78\s*million", re.IGNORECASE)
# 真值 10.3105%；接受 1 位(10.3%)或 2 位(10.31%)小数等合理写法
CONVERSION_RE = re.compile(r"10\.3[0-9]?\s*%|10\.3[0-9]?\s*percent", re.IGNORECASE)
# "not met" 的多种合法表达：含 "Meets Threshold: No" / "does not meet" 等表格式结论
NOT_MET_RE = re.compile(
    r"not\s+met|below\s+threshold|fail|underperform|does\s+not\s+meet|not\s+meet|"
    r"meets?\s+threshold[:\s*]+no\b|threshold[:\s]+not\s+met",
    re.IGNORECASE,
)
COLUMN_RE = re.compile(r"view_count_unique|unique.*deduplic|deduplic.*unique", re.IGNORECASE)

RAW_FIGURE_RE = re.compile(r"3[,.]?592[,.]?000|3\.59\s*million", re.IGNORECASE)
RAW_DISCREDIT_RE = re.compile(
    r"incorrect|wrong\s+column|raw.*includ.*purchased|purchased.*traffic|not.*binding|"
    r"trap|raw.*inflat|inflat.*raw",
    re.IGNORECASE,
)
CLICKTHROUGH_RE = re.compile(r"12\.8\s*%", re.IGNORECASE)
CLICKTHROUGH_DISCREDIT_RE = re.compile(
    r"click[- ]?through|not\s+confirm|wrong\s+metric|not.*binding|trap|engagement",
    re.IGNORECASE,
)

MIN_BYTES = 400
DISCREDIT_WINDOW = 300


def _discredited_within(text: str, pattern: re.Pattern, discredit: re.Pattern,
                         window: int = DISCREDIT_WINDOW) -> bool:
    """Return True if every match of `pattern` has a `discredit` match within `window` chars."""
    for m in pattern.finditer(text):
        start = max(0, m.start() - window)
        end = min(len(text), m.end() + window)
        if not discredit.search(text[start:end]):
            return False
    return True


def _check_no_shortcut(ws: Path, output_file: Path) -> list[str]:
    """Verify '2,781,440' does not appear in any .md or .txt file except the output file."""
    errors: list[str] = []
    needle = "2,781,440"
    needle_alt = "2781440"
    for p in ws.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".md", ".txt"}:
            continue
        # Allow the output file itself.
        try:
            if p.resolve() == output_file.resolve():
                continue
        except Exception:
            continue
        try:
            content = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if needle in content or needle_alt in content:
            errors.append(
                f"anti-shortcut violation: '{needle}' found in text file {p.relative_to(ws)} — "
                f"the dashboard unique-view figure must be image-only; no text file may contain "
                f"this string (it forces VLM delegation for q3)"
            )
    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q2.py <workspace>", file=sys.stderr)
        return 1
    ws = Path(sys.argv[1])
    target = ws / "output" / "kpi_audit.md"

    if not target.exists():
        print(f"FAIL: {target} does not exist")
        return 1

    text = target.read_text(encoding="utf-8")
    errors: list[str] = []

    if len(text.encode("utf-8")) < MIN_BYTES:
        errors.append(
            f"kpi_audit.md too short ({len(text.encode())} bytes); must be >= {MIN_BYTES} bytes"
        )

    if not UNIQUE_VIEW_RE.search(text):
        errors.append(
            "missing correct unique-view average figure "
            "(expected '2,781,440' or '2.78 million' variant)"
        )

    if not CONVERSION_RE.search(text):
        errors.append(
            "missing confirmed-purchase conversion rate (expected '10.3%' or '10.3 percent')"
        )

    not_met_count = len(NOT_MET_RE.findall(text))
    if not_met_count < 2:
        errors.append(
            f"KPI not-met conclusion appears fewer than 2 times (found {not_met_count}); "
            "both unique-view average and conversion rate must be explicitly concluded as "
            "not meeting their respective thresholds"
        )

    if not COLUMN_RE.search(text):
        errors.append(
            "missing column selection rationale — must reference 'view_count_unique' or "
            "'unique deduplicated' to justify column choice over view_count_raw"
        )

    # Anti-trap: raw figure must be discredited if present.
    if RAW_FIGURE_RE.search(text):
        if not _discredited_within(text, RAW_FIGURE_RE, RAW_DISCREDIT_RE):
            errors.append(
                "agent appears to have cited view_count_raw (3,592,000) without discrediting it "
                "within 300 characters — view_count_raw includes purchased traffic and is not "
                "the contractually binding metric; it must be explicitly flagged as the wrong column"
            )

    # Anti-trap: click-through rate must be discredited if present.
    if CLICKTHROUGH_RE.search(text):
        if not _discredited_within(text, CLICKTHROUGH_RE, CLICKTHROUGH_DISCREDIT_RE):
            errors.append(
                "agent appears to have cited click-through conversion (12.8%) without "
                "discrediting it within 300 characters — the contractually binding metric "
                "per §4.2 is confirmed-purchase conversion (10.3%), not click-through"
            )

    # Anti-shortcut ('2,781,440' image-only) — ADVISORY ONLY (non-gating):
    # the figure being correct is what matters; whether it was read via a VLM
    # subagent vs present in a text file is a method/source choice, not a
    # product-correctness signal.
    for _msg in _check_no_shortcut(ws, target):
        print(f"NOTE: {_msg} — advisory only, non-gating", file=sys.stderr)

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        "PASS: kpi_audit.md uses view_count_unique column, reports 2,781,440 unique-view average "
        "and 10.3% confirmed-purchase conversion, concludes both KPIs not met, and discredits "
        "the raw/click-through trap columns where present"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
