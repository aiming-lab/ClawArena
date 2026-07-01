#!/usr/bin/env python3
"""check_denial_timeline_v2.py — Validates analysis/denial_vs_evidence_timeline.md for q24."""
import sys
import re
from pathlib import Path


def main():
    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "denial_vs_evidence_timeline.md"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    lower = content.lower()
    errors = []

    # Must contain the delta value: "2487" or "41 min"
    if "2487" not in content and "41 min" not in lower:
        errors.append(
            "denial_vs_evidence_timeline.md must contain '2487' or '41 min' "
            "(the Δt between download and email)"
        )

    # Must contain the hash
    if "a3f7b2c8e9d1" not in content:
        errors.append(
            "denial_vs_evidence_timeline.md must contain 'a3f7b2c8e9d1' "
            "(SHA-256 hash for event 4 — hash confirmation)"
        )

    # Must contain admission language
    admission_keywords = ["误操作", "我承认", "完整版薪资表", "承认", "完整版"]
    if not any(kw in content for kw in admission_keywords):
        errors.append(
            "denial_vs_evidence_timeline.md must contain the admission language "
            "(e.g., '误操作', '我承认', '完整版')"
        )

    # Must have >= 4 ## headings
    headings = re.findall(r'^## .+', content, re.MULTILINE)
    if len(headings) < 4:
        errors.append(
            f"denial_vs_evidence_timeline.md must have >= 4 '## ' headings, found {len(headings)}"
        )

    # Events must appear in chronological order: "14:22" before "15:03"
    pos_1422 = content.find("14:22")
    pos_1503 = content.find("15:03")
    if pos_1422 == -1:
        errors.append(
            "denial_vs_evidence_timeline.md must reference '14:22' (download time)"
        )
    if pos_1503 == -1:
        errors.append(
            "denial_vs_evidence_timeline.md must reference '15:03' (email send time)"
        )
    if pos_1422 != -1 and pos_1503 != -1 and pos_1422 >= pos_1503:
        errors.append(
            "Chronological order error: '14:22' (download) must appear before '15:03' (email send)"
        )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
