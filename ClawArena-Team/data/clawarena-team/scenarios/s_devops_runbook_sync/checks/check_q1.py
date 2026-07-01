"""check_q1.py — Wave3 s_devops_runbook_sync q1 checker.

Verifies output/postmortem_plan.md:
1. File exists with ≥ 5 sections (## headings)
2. Mentions V0234 (failing migration ID)
3. Mentions "phase 3" (failure phase)
4. Mentions "sqlite" (sqlite query awareness — wave3 B-dimension)
5. Mentions "tar.gz" OR "tar -xzf" (binary archive awareness — wave3 B-dimension)
6. Covers both affected services (payment + billing)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def main(workspace: Path) -> int:
    out = workspace / "output" / "postmortem_plan.md"
    if not out.exists():
        print("FAIL: output/postmortem_plan.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. At least 5 section headings (## or ###)
    sections = re.findall(r"^#{1,3} .+", text, re.MULTILINE)
    if len(sections) < 5:
        print(f"FAIL: only {len(sections)} section headings found (need ≥ 5)")
        return 1

    # 2. Failing migration ID
    if not re.search(r"V0234", text):
        print("FAIL: failing migration ID 'V0234' not found in postmortem_plan.md")
        return 1

    # 3. Failure phase
    if not re.search(r"phase\s*3", text, re.IGNORECASE):
        print("FAIL: 'phase 3' not found in postmortem_plan.md")
        return 1

    # 4. sqlite awareness (B-dimension)
    if not re.search(r"sqlite", text, re.IGNORECASE):
        print("FAIL: 'sqlite' not found in postmortem_plan.md — plan must acknowledge ops_db.sqlite query step")
        return 1

    # 5. tar.gz / binary archive awareness (B-dimension)
    if not re.search(r"tar[.\-]gz|tar\s+-[xz]|tfstate.*archive", text, re.IGNORECASE):
        print("FAIL: 'tar.gz' or extraction step not found — plan must acknowledge tfstate_archive.tar.gz decompression step")
        return 1

    # 6. Both affected services
    if not re.search(r"payment", text, re.IGNORECASE):
        print("FAIL: 'payment' service not mentioned")
        return 1
    if not re.search(r"billing", text, re.IGNORECASE):
        print("FAIL: 'billing' service not mentioned")
        return 1

    print(
        f"PASS: postmortem_plan.md has {len(sections)} sections + V0234 + phase-3 + sqlite + tar.gz + services"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
