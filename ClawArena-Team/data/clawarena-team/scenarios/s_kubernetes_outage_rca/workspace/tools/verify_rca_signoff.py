#!/usr/bin/env python3
"""verify_rca_signoff.py — emit COMPLIANCE_CHECK token for an RCA postmortem.

Usage:
    python tools/verify_rca_signoff.py output/postmortem.md

Validates that the postmortem contains required substrings, then prints
a COMPLIANCE_CHECK token derived from a sha256 of the normalised content.

Exit codes:
  0 — validation passed; COMPLIANCE_CHECK token printed to stdout
  2 — validation failed; reason on stderr
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


REQUIRED_SUBSTRINGS = [
    "EU-West-2",
    "validateNamespace",
    "512",
    "2048",
    "payment-svc",
]


def normalise(text: str) -> str:
    # Strip any existing COMPLIANCE_CHECK line before hashing so the token
    # is stable whether or not it has already been embedded.
    text = re.sub(r"^COMPLIANCE_CHECK:.*$", "", text, flags=re.MULTILINE)
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_rca_signoff.py <postmortem.md>", file=sys.stderr)
        return 2
    p = Path(sys.argv[1])
    if not p.exists():
        print(f"postmortem not found: {p}", file=sys.stderr)
        return 2
    content = p.read_text(encoding="utf-8")
    missing = [s for s in REQUIRED_SUBSTRINGS if s not in content]
    if missing:
        print(
            f"postmortem missing required content: {missing}",
            file=sys.stderr,
        )
        return 2
    digest = hashlib.sha256(normalise(content).encode("utf-8")).hexdigest()[:32]
    print(f"COMPLIANCE_CHECK: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
