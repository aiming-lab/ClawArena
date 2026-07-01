"""check_q1.py — Wave3 s_oss_supply_chain_audit q1 checker.

Verifies output/audit_plan.md:
1. File exists
2. ≥ 5 section headings (## or #)
3. Mentions Mercator (Robotics / org name)
4. Mentions OSS (release context)
5. Mentions SBOM
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

    # 1. ≥ 5 section headings
    headings = re.findall(r"^#{1,3}\s+.+", text, re.MULTILINE)
    if len(headings) < 5:
        print(
            f"FAIL: only {len(headings)} section headings found in audit_plan.md "
            "(need ≥ 5). Expected sections: SBOM, CVE triage, typosquatting, "
            "build reproducibility/CI, license compliance."
        )
        return 1

    # 2. Mentions Mercator
    if not re.search(r"Mercator", text, re.IGNORECASE):
        print("FAIL: 'Mercator' (project org) not found in audit_plan.md")
        return 1

    # 3. Mentions OSS (release context)
    if not re.search(r"\bOSS\b|open.source\s+release", text, re.IGNORECASE):
        print("FAIL: OSS release context not mentioned in audit_plan.md")
        return 1

    # 4. Mentions SBOM
    if not re.search(r"\bSBOM\b", text, re.IGNORECASE):
        print("FAIL: 'SBOM' not mentioned in audit_plan.md")
        return 1

    print(
        f"PASS: audit_plan.md has {len(headings)} sections + Mercator + OSS + SBOM"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
