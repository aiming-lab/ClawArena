#!/usr/bin/env python3
"""
check_complete_chain.py — Validate analysis/complete_evidence_chain.md.

Checks:
  - File exists
  - At least 4 evidence layers mentioned (cloud log, email audit, IT scope gap, hash match)
  - All 4 contradiction IDs (C1, C2, C3, C4) referenced
  - Has >= 4 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_complete_chain.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "complete_evidence_chain.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    content_lower = content.lower()

    # Check evidence layers
    evidence_layers = [
        ("cloud log", ["cloud storage", "cloud log", "cloud-storage", "access log"]),
        ("email audit", ["email audit", "email-attachment", "email attachment", "email"]),
        ("IT scope gap", ["it scope", "it report", "it security", "inv-042", "scope gap", "scope limitation"]),
        ("hash match", ["hash", "sha-256", "sha256", "checksum", "a3f7b2c8e9d1"]),
    ]

    missing_layers = []
    for layer_name, keywords in evidence_layers:
        if not any(kw in content_lower for kw in keywords):
            missing_layers.append(layer_name)

    if missing_layers:
        print(f"FAILED: evidence layers not mentioned: {missing_layers}")
        sys.exit(1)

    # Check C1–C4 references
    for cid in ["C1", "C2", "C3", "C4"]:
        if cid not in content:
            print(f"FAILED: contradiction '{cid}' not referenced in complete_evidence_chain.md")
            sys.exit(1)

    heading_pattern = re.compile(r'^## .+', re.MULTILINE)
    headings = heading_pattern.findall(content)
    if len(headings) < 4:
        print(f"FAILED: expected >= 4 ## headings, found {len(headings)}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
