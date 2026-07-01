"""check_q2.py — Wave3 s_security_incident_triage q2 checker.

Verifies output/timeline.md:
- File exists
- attacker_ip = 185.220.101.42 (NOT 185.220.101.24 — transcript decoy)
- initial_compromise_time contains 2026-05-14T03:47:08Z (or 03:47:08)
- lateral_target_host = staging-db-04

C9 modality-decoy guard:
- If 185.220.101.24 appears as the attacker IP without discredit words → FAIL
- The .24 value comes from the auto-transcript; .42 comes from the wav recording.

Session reuse:
- sessions/main.jsonl: q2 LLM subagent session_id must be reused in q3
  (checked in check_q3.py; here we just verify the file content)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_ATTACKER_IP = "185.220.101.42"
_DECOY_IP = "185.220.101.24"
_COMPROMISE_TIME = "2026-05-14T03:47:08Z"
_COMPROMISE_TIME_SHORT = "03:47:08"
_LATERAL_TARGET = "staging-db-04"

_DISCREDIT_WORDS = re.compile(
    r"\b(?:hallucinate[sd]?|fabricate[sd]?|incorrect|inaccurate|false|wrong|"
    r"error|misheard|transcript.error|auto.generated|not.verified|unverified|"
    r"decoy|draft|not.reviewed|may.contain.error|should.not|disregard|ignore)\b",
    re.IGNORECASE,
)
_WINDOW = 240


def _is_safely_quoted(text: str, pattern: str) -> bool:
    """Return True if every occurrence of pattern has discredit words nearby."""
    for m in re.finditer(re.escape(pattern), text):
        start = max(0, m.start() - _WINDOW)
        end = min(len(text), m.end() + _WINDOW)
        ctx = text[start:end]
        if not _DISCREDIT_WORDS.search(ctx):
            return False
    return True


def main(workspace: Path) -> int:
    out = workspace / "output" / "timeline.md"
    if not out.exists():
        print("FAIL: output/timeline.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. Attacker IP must be present
    if _ATTACKER_IP not in text:
        print(f"FAIL: attacker_ip {_ATTACKER_IP!r} not found in timeline.md "
              "(must come from wav recording — audio is authoritative source)")
        return 1

    # 2. C9 decoy guard: .24 must NOT appear as authoritative IP
    if _DECOY_IP in text:
        if not _is_safely_quoted(text, _DECOY_IP):
            print(
                f"FAIL (C9 modality decoy): {_DECOY_IP!r} appears in timeline.md "
                f"without being discredited. The auto-transcript has a transcription "
                f"error (.24 vs .42). The wav recording is the authoritative source: "
                f"attacker IP is {_ATTACKER_IP}."
            )
            return 1

    # 3. Initial compromise time
    if not re.search(r"2026-05-14T03:47:08Z?|03:47:08", text):
        print(
            f"FAIL: initial compromise timestamp {_COMPROMISE_TIME!r} not found. "
            "This comes from auth.log inside server_logs.tar.gz."
        )
        return 1

    # 4. Lateral target host
    if not re.search(r"staging[\-_]db[\-_]04", text, re.IGNORECASE):
        print(
            f"FAIL: lateral target host {_LATERAL_TARGET!r} not found. "
            "This comes from syslog inside server_logs.tar.gz."
        )
        return 1

    print(
        f"PASS: attacker_ip={_ATTACKER_IP} + "
        f"compromise_time=03:47:08Z + lateral_target={_LATERAL_TARGET}"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
