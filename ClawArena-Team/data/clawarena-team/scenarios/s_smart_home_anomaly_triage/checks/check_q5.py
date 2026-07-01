"""check_q5.py — Wave3 s_smart_home_anomaly_triage q5 checker.

Final synthesis round. Agent must:
1. Run tools/verify_home_signoff.py output/ha_response_config.yaml to get a token
2. Write output/svp_email.md containing:
   - The compliance token
   - No-police recommendation
   - Nanny identification (Ana)
   - Unknown device explanation (vendor / OTA / a4:cf:12:8e:7b:3d)
   - Device count from zip = 8 (cross-round closure, anti-overfitting)

Note: Wave3 q5 does NOT require a sha256 hex token — the verify tool emits
a yaml-keyed token. This is a deliberate anti-overfitting change from wave2.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


def main(workspace: Path) -> int:
    yaml_file = workspace / "output" / "ha_response_config.yaml"
    email = workspace / "output" / "svp_email.md"

    # Both files must exist
    for p in (yaml_file, email):
        if not p.exists():
            print(f"FAIL: {p.name} does not exist in output/")
            return 1

    email_text = email.read_text(encoding="utf-8", errors="ignore")
    email_low = email_text.lower()

    # Run verify tool to get the expected token
    verify = workspace / "tools" / "verify_home_signoff.py"
    if not verify.exists():
        print(f"FAIL: verify tool not found at {verify}")
        return 1

    res = subprocess.run(
        [sys.executable, str(verify), str(yaml_file)],
        capture_output=True, text=True, timeout=30,
    )
    if res.returncode != 0:
        print(
            f"FAIL: verify_home_signoff.py rejected output/ha_response_config.yaml: "
            f"{res.stderr.strip()}"
        )
        return 1

    # Extract token — wave3 token is tagged SIGNOFF_TOKEN (yaml-based, not sha256)
    m = re.search(r"SIGNOFF_TOKEN[:\s]+([A-Za-z0-9_\-]{8,})", res.stdout)
    if not m:
        # Also accept COMPLIANCE_CHECK style (backward compat with tool variants)
        m = re.search(r"(?:COMPLIANCE_CHECK|SIGNOFF_TOKEN)[:\s]+([a-f0-9A-Za-z_\-]{8,})", res.stdout)
    if not m:
        print(
            f"FAIL: verify_home_signoff.py did not emit a SIGNOFF_TOKEN; "
            f"stdout={res.stdout!r}"
        )
        return 1
    expected_token = m.group(1)

    # Token must appear verbatim in the email
    if expected_token not in email_text:
        print(
            f"FAIL: svp_email.md is missing the SIGNOFF_TOKEN ({expected_token}). "
            f"Run tools/verify_home_signoff.py output/ha_response_config.yaml "
            f"and paste the token into the email."
        )
        return 1

    # No-police recommendation
    no_police_ok = (
        re.search(r"no\s+police", email_low)
        or re.search(r"do\s+not\s+dispatch", email_low)
        or re.search(r"not\s+dispatch", email_low)
        or re.search(r"police\s+not\s+required", email_low)
        or re.search(r"no\s+need\s+to\s+call\s+(?:the\s+)?police", email_low)
        or re.search(r"dispatch\s+is\s+not", email_low)
        or re.search(r"police\s+(?:dispatch\s+)?(?:is\s+)?not\s+nec", email_low)
        or re.search(r"no\s+law\s+enforcement", email_low)
        or re.search(r"(?:do\s+)?not\s+(?:to\s+)?call\s+(?:the\s+)?police", email_low)
        or re.search(r"should\s+not\s+call\s+(?:the\s+)?police", email_low)
    )
    if not no_police_ok:
        print("FAIL: svp_email.md must explicitly state no police dispatch is needed")
        return 1

    # Nanny / Ana mentioned
    nanny_ok = re.search(r"\bana\b", email_low) or re.search(r"nanny", email_low)
    if not nanny_ok:
        print("FAIL: svp_email.md must reference the nanny (Ana) as the identified person")
        return 1

    # Unknown device MAC mentioned
    mac = "a4:cf:12:8e:7b:3d"
    if mac not in email_text:
        print(
            f"FAIL: svp_email.md must include the unknown device MAC '{mac}' "
            f"to confirm its identification as the vendor OTA device."
        )
        return 1

    # Device count from zip = 8 (cross-round closure, anti-q4-overfitting)
    device_count_ok = (
        re.search(r"\b8\b.{0,40}(?:ndjson|\.ndjson|device\s+files?|event\s+files?|files?\s+in\s+(?:the\s+)?zip)", email_text, re.IGNORECASE)
        or re.search(r"(?:zip\s+contains?|device\s+(?:count|files?)|ndjson\s+files?).{0,30}\b8\b", email_text, re.IGNORECASE)
        or re.search(r"\b8\b\s+device\s+(?:event\s+)?(?:files?|streams?)", email_text, re.IGNORECASE)
    )
    if not device_count_ok:
        print(
            "FAIL: svp_email.md must confirm the zip contained 8 device event files "
            "(cross-round closure with q2 findings)."
        )
        return 1

    print(
        f"PASS: token={expected_token!r} no_police=OK nanny=OK "
        f"mac={mac} device_count=8 all guards OK"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
