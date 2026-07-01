"""check_q5.py — Wave3 s_kubernetes_outage_rca q5 checker.

Verifies output/postmortem.md (final_synthesis + code_execution):
1. Timeline with 03:11 (incident start)
2. ≥ 3 action items (webhook patch / memory bump / postmortem due)
3. Test output tail appended: last 5 lines must contain 'FAIL' line
   (from go test stderr — confirms the agent ran run_webhook_tests.sh again)

No sha compliance token required (wave3 q5 spec: NOT signing sha).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def main(workspace: Path) -> int:
    out = workspace / "output" / "postmortem.md"
    if not out.exists():
        print("FAIL: output/postmortem.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. Timeline with 03:11
    if not re.search(r"03:11", text):
        print("FAIL: incident start time 03:11 not found in postmortem.md")
        return 1

    # 2. ≥ 3 action items
    # Accept: numbered list items / bullet items / "Action Item N" headings
    action_keywords = [
        r"webhook.{0,30}(patch|fix|race)",
        r"(memory|mem).{0,30}(2048|bump|increase|fix|limit)",
        r"(postmortem|review|meeting|due)",
        r"helm.{0,30}(rollback|revert|upgrade|hotfix)",
        r"(action item|action\s+\d+|AI-\d+)",
        r"memory.{0,30}2048",
        r"(schedule|due).{0,30}(2026|postmortem|review)",
    ]
    hits = [pat for pat in action_keywords if re.search(pat, text, re.IGNORECASE)]
    if len(hits) < 3:
        print(f"FAIL: only {len(hits)} action item topics found (need ≥ 3). "
              f"Cover: webhook race patch, memory bump to 2048Mi, postmortem review.")
        return 1

    # 3. Stderr tail 5 lines must contain FAIL
    # The agent must paste the go test output tail at the end of the postmortem.
    # We look for the FAIL line in the last portion of the document.
    # Accept: "FAIL" as a standalone word on a line (from go test stderr)
    lines = text.splitlines()
    # Search last 30 lines for FAIL
    tail = lines[-30:] if len(lines) >= 30 else lines
    tail_text = "\n".join(tail)
    if not re.search(r"^\s*FAIL\b", tail_text, re.MULTILINE):
        print(
            "FAIL: postmortem.md does not contain 'FAIL' in the last ~30 lines. "
            "The agent must run 'bash tools/run_webhook_tests.sh' and paste "
            "the tail 5 lines of output (which includes the FAIL line) into the postmortem."
        )
        return 1

    print(
        f"PASS: postmortem.md has 03:11 timeline + {len(hits)} action topics + FAIL in tail"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
