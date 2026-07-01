#!/usr/bin/env python3
"""verify_incident_signoff.py — Validate containment_rules.yaml and sign off incident.

Usage:
    python tools/verify_incident_signoff.py output/containment_rules.yaml

Returns exit 0 + verification line if all required actions are present.
"""
from __future__ import annotations
import hashlib
import sys
from pathlib import Path

REQUIRED_ACTIONS = ["block_ip", "revoke_token", "rotate_creds"]
REQUIRED_IPS = ["185.220.101.42", "91.219.236.85", "194.87.139.55"]
INCIDENT_ID = "INC-2026-0514-A"

def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python tools/verify_incident_signoff.py <path_to_yaml>")
        return 1

    yaml_path = Path(sys.argv[1])
    if not yaml_path.exists():
        print(f"ERROR: {yaml_path} does not exist")
        return 1

    content = yaml_path.read_text(encoding="utf-8")
    content_lower = content.lower()

    errors = []

    # Check all required action keys are present
    for action in REQUIRED_ACTIONS:
        if action not in content_lower:
            errors.append(f"  MISSING: action '{action}' not found in yaml")

    # Check attacker IP is blocked
    if "185.220.101.42" not in content:
        errors.append(f"  MISSING: attacker IP 185.220.101.42 not in block rules")

    # Check OIDC token revocation mentioned
    if "oidc" not in content_lower:
        errors.append("  MISSING: OIDC token revocation not specified")

    # Check db-04 rotation
    if "db-04" not in content_lower and "staging-db-04" not in content_lower:
        errors.append("  MISSING: staging-db-04 credential rotation not specified")

    if errors:
        print(f"VERIFICATION FAILED — Incident {INCIDENT_ID}")
        for e in errors:
            print(e)
        print("Containment rules are incomplete. Do not notify CSO until corrected.")
        return 1

    # Compute deterministic token from yaml content
    digest = hashlib.sha256(content.encode()).hexdigest()[:16]
    print(f"VERIFICATION PASSED — Incident {INCIDENT_ID}")
    print(f"Containment rules validated: block_ip + revoke_token + rotate_creds all present.")
    print(f"Attacker IP 185.220.101.42 confirmed in block rules.")
    print(f"OIDC token revocation confirmed.")
    print(f"staging-db-04 credential rotation confirmed.")
    print(f"SIGNOFF TOKEN: {digest}")
    print(f"Status: READY FOR CSO NOTIFICATION")
    return 0

if __name__ == "__main__":
    sys.exit(main())
