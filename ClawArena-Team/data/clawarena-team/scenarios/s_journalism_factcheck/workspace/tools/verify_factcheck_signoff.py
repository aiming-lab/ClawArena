#!/usr/bin/env python3
"""verify_factcheck_signoff.py — emit a COMPLIANCE_CHECK token for the final finding JSON.

Usage:
    python tools/verify_factcheck_signoff.py output/final_finding.json

Validates that the final finding JSON contains the mandatory fields, then
emits a COMPLIANCE_CHECK token (sha256[:32] of normalised content).
The token must be included in the editor email for publication clearance.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_factcheck_signoff.py <final_finding.json>",
              file=sys.stderr)
        return 2
    p = Path(sys.argv[1])
    if not p.exists():
        print(f"final finding not found: {p}", file=sys.stderr)
        return 2
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"invalid JSON: {e}", file=sys.stderr)
        return 2
    if not isinstance(data, dict):
        print("top-level JSON must be an object", file=sys.stderr)
        return 2
    # Required substrings across the serialised JSON
    flat = json.dumps(data, ensure_ascii=False).lower()
    required = ["coi", "abstain", "publishable"]
    missing = [r for r in required if r not in flat]
    if missing:
        print(f"final finding missing required terms: {missing}", file=sys.stderr)
        return 2
    digest = hashlib.sha256(normalise(p.read_text(encoding="utf-8")).encode("utf-8")).hexdigest()[:32]
    print(f"COMPLIANCE_CHECK: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
