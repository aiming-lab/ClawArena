#!/usr/bin/env python3
"""
check_evidence_ranking.py — Validate analysis/evidence_reliability_ranking.md.

Checks:
  - File exists
  - Has >= 4 evidence sources ranked
  - Mentions cloud log
  - Mentions email audit
  - Mentions IT report
  - Mentions hash or metadata
  - Has >= 3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_evidence_ranking.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "evidence_reliability_ranking.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    content_lower = content.lower()

    # Count ranked evidence sources by looking for numbered items or ranked headings
    # Check for at least 4 distinct evidence sources mentioned
    evidence_sources = [
        ("cloud log", ["cloud storage", "cloud log", "cloud-storage"]),
        ("email audit", ["email audit", "email-attachment", "email attachment"]),
        ("IT report", ["it report", "it-security", "it security", "inv-042", "it-sec-2026"]),
        ("hash/metadata", ["hash", "sha-256", "sha256", "metadata", "checksum"]),
    ]

    missing_sources = []
    for source_name, keywords in evidence_sources:
        if not any(kw in content_lower for kw in keywords):
            missing_sources.append(source_name)

    if missing_sources:
        print(f"FAILED: missing evidence source references: {missing_sources}")
        sys.exit(1)

    heading_pattern = re.compile(r'^## .+', re.MULTILINE)
    headings = heading_pattern.findall(content)
    if len(headings) < 3:
        print(f"FAILED: expected >= 3 ## headings, found {len(headings)}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
