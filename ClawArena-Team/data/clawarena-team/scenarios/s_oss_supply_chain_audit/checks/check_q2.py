"""check_q2.py — Wave3 s_oss_supply_chain_audit q2 checker.

Verifies output/cve_findings.md (B dimension: vendor_snapshot.tar.gz must be extracted):
1. lib-tinypath@1.4.2 (vulnerable package full name)
2. CVE-2026-21847 (CVE ID)
3. 8.7 HIGH (severity — both score and label)
4. colorz (typosquat package name)

The vulnerable package version 1.4.2 and typosquat colorz also appear in the
vendor_snapshot.tar.gz (Cargo.lock and package-lock.json), so a subagent that
decompresses the tarball can confirm these independently.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def main(workspace: Path) -> int:
    out = workspace / "output" / "cve_findings.md"
    if not out.exists():
        print("FAIL: output/cve_findings.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. Vulnerable package full name: lib-tinypath@1.4.2
    if not re.search(r"lib-tinypath@1\.4\.2|lib-tinypath\s+1\.4\.2", text, re.IGNORECASE):
        print(
            "FAIL: 'lib-tinypath@1.4.2' (or 'lib-tinypath 1.4.2') not found in "
            "cve_findings.md. Check sbom/ and vendor_snapshot.tar.gz Cargo.lock."
        )
        return 1

    # 2. CVE ID
    if not re.search(r"CVE-2026-21847", text):
        print("FAIL: 'CVE-2026-21847' not found in cve_findings.md")
        return 1

    # 3. Severity: 8.7 and HIGH (both required)
    if not re.search(r"8\.7", text):
        print("FAIL: severity score '8.7' not found in cve_findings.md")
        return 1
    if not re.search(r"\bHIGH\b", text, re.IGNORECASE):
        print("FAIL: severity label 'HIGH' not found in cve_findings.md")
        return 1

    # 4. Typosquat package
    if not re.search(r"\bcolorz\b", text, re.IGNORECASE):
        print(
            "FAIL: typosquat package 'colorz' not found in cve_findings.md. "
            "Check vendor_snapshot.tar.gz package-lock.json and sbom/."
        )
        return 1

    print(
        "PASS: cve_findings.md contains lib-tinypath@1.4.2 + CVE-2026-21847 + "
        "8.7 HIGH + colorz typosquat"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
