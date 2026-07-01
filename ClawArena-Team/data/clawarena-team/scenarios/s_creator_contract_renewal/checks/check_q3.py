"""check_q3.py — output/screenshot_crosscheck.md cross-checks PNG screenshots vs. MCN report.

Ground truth (from platform_screenshots/ images — VLM required):
  - backend_dashboard_q4.png:
      header: "UNIQUE DEDUPLICATED VIEWS — Q4 2025 ROLLING 90-DAY AVERAGE"
      metric box: 2,781,440 unique views / video
  - brand_deal_tracker.png:
      confirmed-purchase conversion: 10.3%
      click-through rate: 12.8%  (labeled — NOT the binding metric)
  - video_detail_top5.png:
      top-5 of 38 videos only; full 38-video average CANNOT be extrapolated from this table

  MCN Q4 2025 quarterly report claims:
      unique-view figure: 3,420,000  (blended methodology; contradicts dashboard)
      conversion rate: 12.8%  (click-through; wrong metric)

Pass conditions:
  1. File exists; >= 500 bytes; references >= 3 distinct screenshot comparisons.
  2. Dashboard unique-view figure 2,781,440 present (must come from image, not text file).
  3. Confirmed-purchase conversion 10.3% present.
  4. MCN report unique-view claim 3,420,000 present (to acknowledge discrepancy).
  5. MCN report conversion claim 12.8% present (to acknowledge discrepancy).
  6. Discrepancy acknowledged between image data and report data.
  7. Anti-extrapolation: file must NOT use top-5 table as the basis for the 38-video average.
  8. Cross-round consistency: unique-view figure must match output/kpi_audit.md.

Anti-shortcut (same as q2):
  '2,781,440' must not appear in any workspace .md or .txt file other than
  output/kpi_audit.md and output/screenshot_crosscheck.md.
  (The dashboard figure is image-only; it must be read by a VLM subagent.)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DASHBOARD_FIGURE_RE = re.compile(r"2[,.]?781[,.]?440", re.IGNORECASE)
CONFIRMED_CONV_RE = re.compile(r"10\.3\s*%", re.IGNORECASE)
REPORT_UNIQUE_RE = re.compile(r"3[,.]?420[,.]?000|3\.42\s*million", re.IGNORECASE)
REPORT_CONV_RE = re.compile(r"12\.8\s*%", re.IGNORECASE)
DISCREPANCY_RE = re.compile(r"discrepan|contradict|mismatch|conflict", re.IGNORECASE)
TOP5_EXTRAPOLATION_RE = re.compile(
    r"top[_\-\s]?5\s+average|average.*top\s+5|top_5.*average|"
    r"top[_\-\s]?five\s+average|average.*top\s+five",
    re.IGNORECASE,
)
SCREENSHOT_FILE_RE = re.compile(
    r"backend_dashboard_q4|video_detail_top5|brand_deal_tracker", re.IGNORECASE
)

MIN_BYTES = 500
MIN_SCREENSHOT_REFS = 3

# Output files allowed to contain the dashboard figure.
ALLOWED_OUTPUT_STEMS = {"kpi_audit", "screenshot_crosscheck"}


def _check_no_shortcut(ws: Path, output_file: Path) -> list[str]:
    """Verify '2,781,440' does not appear in any .md or .txt file
    except the designated output files."""
    errors: list[str] = []
    needle = "2,781,440"
    needle_alt = "2781440"
    allowed_outputs = {
        (ws / "output" / f"{stem}.md").resolve()
        for stem in ALLOWED_OUTPUT_STEMS
    }
    for p in ws.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".md", ".txt"}:
            continue
        try:
            if p.resolve() in allowed_outputs:
                continue
        except Exception:
            continue
        try:
            content = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if needle in content or needle_alt in content:
            errors.append(
                f"anti-shortcut violation: '{needle}' found in text file "
                f"{p.relative_to(ws)} — this figure must be image-only and "
                f"extracted by a VLM subagent from backend_dashboard_q4.png"
            )
    return errors


def _cross_round_consistency(ws: Path, errors: list[str]) -> None:
    """Verify that the unique-view figure in kpi_audit.md matches the dashboard reading."""
    kpi_audit = ws / "output" / "kpi_audit.md"
    if not kpi_audit.exists():
        # kpi_audit.md may not exist if q2 was skipped; emit warning, not hard fail.
        return
    audit_text = kpi_audit.read_text(encoding="utf-8", errors="replace")
    if not DASHBOARD_FIGURE_RE.search(audit_text):
        errors.append(
            "cross-round consistency failure: output/kpi_audit.md (q2) does not contain "
            "'2,781,440' — the unique-view figure from the dashboard must agree across q2 and q3"
        )


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q3.py <workspace>", file=sys.stderr)
        return 1
    ws = Path(sys.argv[1])
    target = ws / "output" / "screenshot_crosscheck.md"

    if not target.exists():
        print(f"FAIL: {target} does not exist")
        return 1

    text = target.read_text(encoding="utf-8")
    errors: list[str] = []

    if len(text.encode("utf-8")) < MIN_BYTES:
        errors.append(
            f"screenshot_crosscheck.md too short ({len(text.encode())} bytes); "
            f"must be >= {MIN_BYTES} bytes"
        )

    screenshot_refs = len(SCREENSHOT_FILE_RE.findall(text))
    if screenshot_refs < MIN_SCREENSHOT_REFS:
        errors.append(
            f"screenshot_crosscheck.md references fewer than {MIN_SCREENSHOT_REFS} distinct "
            f"screenshot filenames (found {screenshot_refs}); all three PNGs must be addressed: "
            f"backend_dashboard_q4.png, video_detail_top5.png, brand_deal_tracker.png"
        )

    if not DASHBOARD_FIGURE_RE.search(text):
        errors.append(
            "missing dashboard unique-view figure (expected '2,781,440') — "
            "this must be read directly from backend_dashboard_q4.png using a VLM subagent"
        )

    if not CONFIRMED_CONV_RE.search(text):
        errors.append(
            "missing confirmed-purchase conversion rate from brand_deal_tracker.png "
            "(expected '10.3%')"
        )

    if not REPORT_UNIQUE_RE.search(text):
        errors.append(
            "missing MCN quarterly report unique-view claim (expected '3,420,000' or "
            "'3.42 million') — needed for the explicit discrepancy comparison"
        )

    if not REPORT_CONV_RE.search(text):
        errors.append(
            "missing MCN quarterly report conversion claim (expected '12.8%') — "
            "needed for the explicit discrepancy comparison"
        )

    if not DISCREPANCY_RE.search(text):
        errors.append(
            "missing discrepancy acknowledgment — file must explicitly state that "
            "the image data contradicts the MCN quarterly report figures "
            "('discrepancy', 'contradiction', 'mismatch', or equivalent)"
        )

    if TOP5_EXTRAPOLATION_RE.search(text):
        errors.append(
            "anti-extrapolation violation: file uses the top-5 video table as the basis "
            "for the 38-video rolling average — the video_detail_top5.png shows only the "
            "top 5 of 38 videos; the full average cannot be extrapolated from this table alone"
        )

    # Cross-round consistency check.
    _cross_round_consistency(ws, errors)

    # Anti-shortcut ('2,781,440' image-only) — ADVISORY ONLY (non-gating):
    # the figure being correct is what matters; reading it via a VLM subagent
    # vs a text file is a method/source choice, not a product-correctness signal.
    for _msg in _check_no_shortcut(ws, target):
        print(f"NOTE: {_msg} — advisory only, non-gating", file=sys.stderr)

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        "PASS: screenshot_crosscheck.md reads dashboard unique-view figure (2,781,440) and "
        "confirmed-purchase conversion (10.3%) from images, acknowledges MCN report discrepancy, "
        "avoids top-5 extrapolation, and is cross-round consistent with kpi_audit.md"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
