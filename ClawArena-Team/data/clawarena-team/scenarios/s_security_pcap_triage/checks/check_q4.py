"""q4: findings/slack_evidence.md contains verbatim key phrase from Slack screenshot.

Pass conditions (all required):
  1. findings/slack_evidence.md exists.
  2. Contains the phrase 'unauthorized SSH attempt' (case-insensitive, exact words).

C9 modality decoy: the phrase is visible only in the image — no text file in slack/
transcribes it. A subagent that skips the image cannot produce the correct phrase.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root

# Ground-truth phrase from the Slack screenshot image
REQUIRED_PHRASE_RE = re.compile(
    r"unauthorized\s+SSH\s+attempt",
    re.IGNORECASE,
)


def main() -> int:
    ws = workspace_root()
    evidence = ws / "findings" / "slack_evidence.md"
    if not evidence.exists():
        fail("missing findings/slack_evidence.md")

    text = evidence.read_text(encoding="utf-8", errors="ignore")

    if not REQUIRED_PHRASE_RE.search(text):
        fail(
            "findings/slack_evidence.md does not contain the required phrase "
            "'unauthorized SSH attempt'. The subagent must read the Slack screenshot "
            "image (slack/soc_channel_screenshot.png) — the phrase is only in the image."
        )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
