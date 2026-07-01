"""check_q2.py — Wave3 s_devops_runbook_sync q2 checker.

Verifies output/event_timeline.md:
1. V0234__add_idempotency_keys.sql present (failing migration — must come from log + sqlite)
2. "phase 3" present (failure phase)
3. rollback duration: 7 (hours)
4. LOCK TIMEOUT + ETL combination (wav root cause — from dba_lead_voicemail.wav)
5. RDS parameter group pg-prod-billing-v3 (from tfstate_archive.tar.gz, B-dimension)

Decoy guards (discredit_window 240 chars):
D1. "network partition" without negation → FAIL (C9 transcript decoy)
D2. "V0299" without negation → FAIL (AI hallucination decoy from _runbook_bot_summary.md)

Session reuse: check_q3 handles the session reuse guard for q2→q3.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


_DISCREDIT_WORDS = re.compile(
    r"\b(?:hallucinate[sd]?|fabricate[sd]?|incorrect|inaccurate|false|wrong|"
    r"not\s+correct|does\s+not\s+exist|nonexistent|ignore|disregard|refute[sd]?|"
    r"contradict[s]?|erroneous|invalid|bogus|AI.generated|auto.generated|decoy|"
    r"misidentif|error|mistaken)\b",
    re.IGNORECASE,
)

_WINDOW = 240


def _safely_absent_or_discredited(text: str, pattern: str) -> bool:
    """Return True if pattern is absent OR every occurrence is within discredit window."""
    for m in re.finditer(pattern, text, re.IGNORECASE):
        start = max(0, m.start() - _WINDOW)
        end = min(len(text), m.end() + _WINDOW)
        ctx = text[start:end]
        if not _DISCREDIT_WORDS.search(ctx):
            return False
    return True


def main(workspace: Path) -> int:
    out = workspace / "output" / "event_timeline.md"
    if not out.exists():
        print("FAIL: output/event_timeline.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. Failing migration ID
    if not re.search(r"V0234", text):
        print("FAIL: 'V0234' (failing migration ID) not found in event_timeline.md")
        return 1
    if not re.search(r"add_idempotency_keys", text, re.IGNORECASE):
        print("FAIL: 'add_idempotency_keys' not found in event_timeline.md")
        return 1

    # 2. Failure phase
    if not re.search(r"phase\s*3", text, re.IGNORECASE):
        print("FAIL: 'phase 3' not found in event_timeline.md")
        return 1

    # 3. Rollback duration 7 hours
    if not re.search(r"\b7\b", text):
        print("FAIL: rollback duration '7' (hours) not found in event_timeline.md")
        return 1

    # 4. Wav root cause: LOCK TIMEOUT + ETL
    if not re.search(r"LOCK.TIMEOUT", text, re.IGNORECASE):
        print("FAIL: 'LOCK TIMEOUT' not found — root cause from dba_lead_voicemail.wav must be cited")
        return 1
    if not re.search(r"\bETL\b", text, re.IGNORECASE):
        print("FAIL: 'ETL' not found — wav root cause (ETL job blocking) must be cited")
        return 1

    # 5. RDS parameter group (from tfstate_archive.tar.gz — B dimension)
    if not re.search(r"pg-prod-billing-v3", text, re.IGNORECASE):
        print("FAIL: RDS parameter group 'pg-prod-billing-v3' not found — must extract from tfstate_archive.tar.gz")
        return 1

    # Decoy guard D1: network partition (transcript decoy)
    if not _safely_absent_or_discredited(text, r"network\s+partition"):
        print(
            "FAIL (C9 modality decoy): 'network partition' appears in event_timeline.md without "
            "being discredited. This is the auto-transcript error — the wav audio clearly states "
            "the root cause was LOCK TIMEOUT + ETL, not a network partition."
        )
        return 1

    # Decoy guard D2: V0299 (AI hallucination from _runbook_bot_summary.md)
    if not _safely_absent_or_discredited(text, r"V0299"):
        print(
            "FAIL (D-dimension AI hallucination): 'V0299' appears in event_timeline.md without "
            "being discredited. V0299__fake_index.sql does not exist — it was fabricated by "
            "the runbook bot summary (_runbook_bot_summary.md). The correct failing migration is V0234."
        )
        return 1

    print(
        "PASS: event_timeline.md has V0234 + phase-3 + 7h + LOCK_TIMEOUT + ETL + "
        "pg-prod-billing-v3; network-partition and V0299 guards OK"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
