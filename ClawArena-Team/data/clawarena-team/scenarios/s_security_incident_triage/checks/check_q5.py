"""check_q5.py — Wave3 s_security_incident_triage q5 checker.

Verifies output/incident_email.md (final_synthesis + code_execution):
1. Incident ID INC-2026-0514-A present
2. Attacker IP 185.220.101.42 mentioned
3. ≥ 2 of: revoke / block / rotate (containment action verbs)
4. Verification tool stdout present — must contain "SIGNOFF TOKEN" or
   "VERIFICATION PASSED" (agent ran verify_incident_signoff.py)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_INCIDENT_ID = "INC-2026-0514-A"
_ATTACKER_IP = "185.220.101.42"


def main(workspace: Path) -> int:
    out = workspace / "output" / "incident_email.md"
    if not out.exists():
        print("FAIL: output/incident_email.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. Incident ID
    if not re.search(r"INC[-\s]?2026[-\s]?0514[-\s]?A", text, re.IGNORECASE):
        print(f"FAIL: incident ID {_INCIDENT_ID!r} not found in incident_email.md")
        return 1

    # 2. Attacker IP
    if _ATTACKER_IP not in text:
        print(f"FAIL: attacker IP {_ATTACKER_IP!r} not found in incident_email.md")
        return 1

    # 3. ≥ 2 containment action verbs
    action_patterns = [
        r"\brevoke\b",
        r"\bblock\b",
        r"\brotate\b",
        r"\bcontain\b",
        r"\bremove\b.*blocklist|blocklist.*\bremove\b",
    ]
    hit_actions = [p for p in action_patterns if re.search(p, text, re.IGNORECASE)]
    if len(hit_actions) < 2:
        print(
            f"FAIL: only {len(hit_actions)} containment action verbs found "
            f"(need ≥ 2 of: revoke, block, rotate). "
            f"The email must describe the containment actions taken."
        )
        return 1

    # 4. Verification tool stdout — must contain SIGNOFF TOKEN or VERIFICATION PASSED
    if not re.search(
        r"SIGNOFF\s+TOKEN|VERIFICATION\s+PASSED|verify.*passed|signoff.*token",
        text,
        re.IGNORECASE,
    ):
        print(
            "FAIL: verification tool output not found in incident_email.md. "
            "The agent must run `python tools/verify_incident_signoff.py "
            "output/containment_rules.yaml` and paste the complete stdout "
            "(including 'SIGNOFF TOKEN' line) into the email."
        )
        return 1

    print(
        f"PASS: incident_email.md has {_INCIDENT_ID}, {_ATTACKER_IP}, "
        f"{len(hit_actions)} action verbs, and verification tool stdout."
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
