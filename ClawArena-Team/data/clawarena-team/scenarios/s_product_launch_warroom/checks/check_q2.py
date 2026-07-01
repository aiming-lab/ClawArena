"""check_q2.py — output/notes/q2_specs_digest.md covers all 10 specs.

Ground truth (from specs/_index.md):
  spec_01_overview.md      — Helix-7 Platform Overview
  spec_02_correlation_engine.md — Real-Time Correlation Engine
  spec_03_anomaly_dashboard.md  — 24-Hour Anomaly Dashboard
  spec_04_data_ingest.md        — Data Ingest and Schema Mapping
  spec_05_alerts_routing.md     — Alert Routing and Escalation
  spec_06_historical_context.md — Historical Context (18-Month Rolling Window)
  spec_07_integrations.md       — Third-Party Integrations Matrix
  spec_08_compliance.md         — Compliance and Audit Trail
  spec_09_pricing_tiers.md      — Pricing Tiers and Seat Math
  spec_10_rollout.md            — Phased Rollout Plan

Pass conditions:
  1. File exists, length >= 400 chars.
  2. All 10 spec filenames (spec_01 through spec_10) are mentioned by filename
     stem OR their central-feature keyword is present.
  3. Each of the 10 spec keywords must appear at least once across the full text.
  4. At least 6 of the 10 entries must be >= 30 chars on the line(s) near the
     spec reference (the digest must have non-trivial descriptions).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# (filename_re, central_feature_re, display_name)
SPEC_CHECKS: list[tuple[str, str, str]] = [
    (r"spec_01", r"platform\s+overview|helix[- ]7\s+platform", "spec_01 / Platform Overview"),
    (r"spec_02", r"correlation\s+engine|real[- ]time\s+correlation", "spec_02 / Real-Time Correlation Engine"),
    (r"spec_03", r"anomaly\s+dashboard|24[- ]hour\s+anomaly", "spec_03 / 24-Hour Anomaly Dashboard"),
    (r"spec_04", r"data\s+ingest|schema\s+mapping", "spec_04 / Data Ingest and Schema Mapping"),
    (r"spec_05", r"alert[s]?\s+routing|escalation", "spec_05 / Alert Routing and Escalation"),
    (r"spec_06", r"historical\s+context|18[- ]month|rolling\s+window", "spec_06 / Historical Context"),
    (r"spec_07", r"integrations?\s+matrix|third[- ]party\s+integrations?", "spec_07 / Third-Party Integrations Matrix"),
    (r"spec_08", r"compliance|audit\s+trail", "spec_08 / Compliance and Audit Trail"),
    (r"spec_09", r"pricing\s+tiers|seat\s+math", "spec_09 / Pricing Tiers and Seat Math"),
    (r"spec_10", r"rollout|phased\s+rollout", "spec_10 / Phased Rollout Plan"),
]


def _entry_length_ok(text: str, spec_file_re: str, feature_re: str) -> bool:
    """Check that the line(s) referencing this spec are >= 30 chars."""
    combined = re.compile(f"({spec_file_re}|{feature_re})", re.IGNORECASE)
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if combined.search(line):
            # Accept if the line itself is long enough, or the following line adds context.
            if len(line.strip()) >= 30:
                return True
    return False


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q2.py <workspace>", file=sys.stderr)
        return 1
    ws = Path(sys.argv[1])
    note = ws / "output" / "notes" / "q2_specs_digest.md"
    if not note.exists():
        print(f"FAIL: {note} does not exist")
        return 1
    text = note.read_text(encoding="utf-8")
    errors: list[str] = []

    if len(text.strip()) < 400:
        errors.append("q2_specs_digest.md too short for 10 substantive entries (< 400 chars)")

    missing_keyword: list[str] = []
    short_entries: list[str] = []
    for file_re, feat_re, label in SPEC_CHECKS:
        combined_re = re.compile(f"({file_re}|{feat_re})", re.IGNORECASE)
        if not combined_re.search(text):
            missing_keyword.append(label)
        elif not _entry_length_ok(text, file_re, feat_re):
            short_entries.append(label)

    if missing_keyword:
        errors.append(f"missing spec entries: {missing_keyword}")
    if short_entries:
        errors.append(f"spec entries too short (< 30 chars on reference line): {short_entries}")

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1
    print("PASS: q2_specs_digest.md covers all 10 specs with substantive per-spec descriptions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
