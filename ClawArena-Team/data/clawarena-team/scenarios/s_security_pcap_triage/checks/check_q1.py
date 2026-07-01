"""q1: output/triage_plan.md exists + >=4 sections + references SEC-2026-0419.

Pass conditions (all required):
  1. output/triage_plan.md exists.
  2. Contains >= 4 '## ' level-2 sections.
  3. Contains the incident ID 'SEC-2026-0419'.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root


def main() -> int:
    ws = workspace_root()
    plan = ws / "output" / "triage_plan.md"
    if not plan.exists():
        fail("missing output/triage_plan.md")

    text = plan.read_text(encoding="utf-8", errors="ignore")

    # Section count
    sections = re.findall(r"^##\s+\S.*$", text, flags=re.MULTILINE)
    if len(sections) < 4:
        fail(f"need >= 4 '## ' sections, got {len(sections)}: {sections}")

    # Incident ID reference
    if "SEC-2026-0419" not in text:
        fail("missing required incident ID reference: SEC-2026-0419")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
