"""check_q1.py — output/notes/q1_launch_profile.md captures the launch fundamentals.

Ground truth (from briefs/launch_brief.md):
  - Launch date: 2026-06-17
  - Code-name: Helix-7
  - Target segment: mid-market SaaS observability
  - Headline positioning: 'first 24-hour anomaly detection dashboard for mid-market SaaS'
    (or equivalent verbatim anchor)

Pass conditions:
  1. File exists, length >= 100 chars.
  2. Exact launch date '2026-06-17' present.
  3. Exact code-name 'Helix-7' present (case-sensitive, hyphenated).
  4. Exact segment string 'mid-market SaaS observability' present (case-insensitive).
  5. Headline positioning: both anchors identifiable (题面允许 quoted or
     paraphrased closely)：
       - time-window anchor: '24-hour' / '24 hour' / '24h'
       - detection-capability anchor: 'anomaly detection' (近义可分开出现)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Exact anchors required — must match precisely what the brief states.
DATE_EXACT = re.compile(r"2026-06-17")
CODENAME_EXACT = re.compile(r"\bHelix-7\b")
SEGMENT_EXACT = re.compile(r"mid[- ]market\s+SaaS\s+observability", re.IGNORECASE)
# 题面允许近似改写：只要 time-window 与 detection-capability 两个 anchor 均可识别即可，
# 不再强制 '24-hour anomaly detection' 三词严格相邻。
POSITION_TIMEWINDOW = re.compile(r"24[\s-]?hour|24\s*h\b", re.IGNORECASE)
POSITION_DETECTION = re.compile(r"anomaly\s+detection|anomaly[- ]detection", re.IGNORECASE)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q1.py <workspace>", file=sys.stderr)
        return 1
    ws = Path(sys.argv[1])
    note = ws / "output" / "notes" / "q1_launch_profile.md"
    if not note.exists():
        print(f"FAIL: {note} does not exist")
        return 1
    text = note.read_text(encoding="utf-8")
    errors: list[str] = []
    if len(text.strip()) < 100:
        errors.append("q1_launch_profile.md too short (< 100 chars)")
    if not DATE_EXACT.search(text):
        errors.append("missing exact launch date anchor '2026-06-17'")
    if not CODENAME_EXACT.search(text):
        errors.append("missing exact product code-name 'Helix-7' (case-sensitive, hyphenated)")
    if not SEGMENT_EXACT.search(text):
        errors.append("missing exact target segment 'mid-market SaaS observability'")
    if not POSITION_TIMEWINDOW.search(text):
        errors.append("missing headline time-window anchor (e.g. '24-hour')")
    if not POSITION_DETECTION.search(text):
        errors.append("missing headline detection-capability anchor (e.g. 'anomaly detection')")
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1
    print("PASS: q1_launch_profile.md carries exact launch date, Helix-7 code-name, mid-market SaaS observability segment, and 24-hour anomaly detection positioning")
    return 0


if __name__ == "__main__":
    sys.exit(main())
