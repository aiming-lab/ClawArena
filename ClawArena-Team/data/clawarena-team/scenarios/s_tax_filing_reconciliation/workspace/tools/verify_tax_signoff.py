#!/usr/bin/env python3
"""verify_tax_signoff.py — emit a COMPLIANCE_CHECK token for the client letter.

Usage:
    python tools/verify_tax_signoff.py output/client_letter.md

The token is an MD5-based compliance token derived from the letter's
normalised content (COMPLIANCE_CHECK line stripped out for stability).

Exit codes:
    0 — token printed to stdout as: COMPLIANCE_CHECK: <32-hex-chars>
    2 — usage error or letter missing required content
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


def normalise(text: str) -> str:
    lines = [l for l in text.splitlines()
             if not l.strip().startswith("COMPLIANCE_CHECK:")]
    return re.sub(r"\s+", " ", " ".join(lines)).strip()


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_tax_signoff.py <client_letter.md>", file=sys.stderr)
        return 2

    p = Path(sys.argv[1])
    if not p.exists():
        print(f"client letter not found: {p}", file=sys.stderr)
        return 2

    content = p.read_text(encoding="utf-8")

    required = ["PFIC", "18,420", "1.0913", "Liu Wei"]
    missing = [s for s in required if s not in content]
    if missing:
        print(f"client letter missing required content: {missing}", file=sys.stderr)
        return 2

    digest = hashlib.md5(normalise(content).encode("utf-8")).hexdigest()
    print(f"COMPLIANCE_CHECK: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
