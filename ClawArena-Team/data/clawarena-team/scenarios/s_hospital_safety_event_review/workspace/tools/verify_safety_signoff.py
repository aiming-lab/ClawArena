#!/usr/bin/env python3
"""verify_safety_signoff.py — emit a COMPLIANCE_CHECK token for a MedWatch draft.

Usage:
    python tools/verify_safety_signoff.py output/medwatch_draft.md

The script validates that the draft contains the required clinical and
regulatory substrings, then prints a COMPLIANCE_CHECK token derived from
the normalised draft content. Paste the token into the Q&S email.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


REQUIRED_SUBSTRINGS = [
    "Mercator Vitals M-7",
    "2.18.3",
    "bilateral pulmonary edema",
    "FDA MedWatch",
]


def normalise(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_safety_signoff.py <medwatch_draft.md>", file=sys.stderr)
        return 2
    p = Path(sys.argv[1])
    if not p.exists():
        print(f"file not found: {p}", file=sys.stderr)
        return 2
    content = p.read_text(encoding="utf-8")
    missing = [s for s in REQUIRED_SUBSTRINGS if s.lower() not in content.lower()]
    if missing:
        print(f"medwatch draft missing required substrings: {missing}", file=sys.stderr)
        return 2
    digest = hashlib.sha256(normalise(content).encode("utf-8")).hexdigest()[:32]
    print(f"COMPLIANCE_CHECK: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
