"""check_q1.py — Wave3 s_security_incident_triage q1 checker.

Verifies output/triage_timeline.md:
- File exists
- ≥ 5 section headings (accept #, **, or numbered N.)
- Mentions incident ID INC-2026-0514-A
- Mentions EU (timezone context) or 04:00 UTC
- Covers ≥ 3 of: IOC / log / EDR / network / notification / containment / triage / siem / pcap / forensic
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def main(workspace: Path) -> int:
    out = workspace / "output" / "triage_timeline.md"
    if not out.exists():
        print("FAIL: output/triage_timeline.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. ≥ 5 section headings
    headings = re.findall(
        r"(?m)^(?:#{1,4}\s+.+|(?:\*{1,2}|\d+[\.\)])\s+\S.{3,})",
        text,
    )
    if len(headings) < 5:
        print(f"FAIL: found {len(headings)} section headings, need ≥ 5")
        return 1

    # 2. Mentions incident ID INC-2026-0514-A (or close variant)
    if not re.search(r"INC[-\s]?2026[-\s]?0514[-\s]?A", text, re.IGNORECASE):
        print("FAIL: incident ID INC-2026-0514-A not mentioned")
        return 1

    # 3. EU timezone context or 04:00 UTC
    if not re.search(r"(?:EU|04:00|04\.00\s*UTC|four.{0,10}UTC)", text, re.IGNORECASE):
        print("FAIL: EU timezone or 04:00 UTC reference not found")
        return 1

    # 4. ≥ 3 investigation topic keywords
    topics = [
        "ioc", "log", "edr", "network", "notification", "containment",
        "triage", "siem", "pcap", "forensic", "attacker", "lateral",
        "credential", "alert", "exfil",
    ]
    hits = [t for t in topics if re.search(t, text, re.IGNORECASE)]
    if len(hits) < 3:
        print(f"FAIL: only {len(hits)} investigation topics covered (need ≥ 3): {hits}")
        return 1

    print(
        f"PASS: triage_timeline.md has {len(headings)} headings, "
        f"INC-2026-0514-A, EU/04:00 UTC, topics: {hits[:5]}"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
