#!/usr/bin/env python3
"""check_cryptographic_proof.py — Validates analysis/cryptographic_proof.md for q18."""
import sys
import re
from pathlib import Path


def main():
    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "cryptographic_proof.md"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    lower = content.lower()
    errors = []

    # Must contain the hash value
    if "a3f7b2c8e9d1" not in content:
        errors.append("cryptographic_proof.md must contain hash 'a3f7b2c8e9d1'")

    # Must contain "SHA-256"
    if "SHA-256" not in content and "sha-256" not in lower and "sha256" not in lower:
        errors.append("cryptographic_proof.md must contain 'SHA-256'")

    # Must contain "identical" or "byte" (proof of byte-level identity)
    if "identical" not in lower and "byte" not in lower:
        errors.append(
            "cryptographic_proof.md must contain 'identical' or 'byte' "
            "(describing byte-level file identity)"
        )

    # Must contain collision probability or uniqueness statement
    uniqueness_patterns = [
        r"collision",
        r"2\^128",
        r"unique",
        r"negligibl",
        r"probabil",
        r"cryptograph",
    ]
    found_uniqueness = any(re.search(pat, lower) for pat in uniqueness_patterns)
    if not found_uniqueness:
        errors.append(
            "cryptographic_proof.md must contain a statement about collision probability "
            "or cryptographic uniqueness of SHA-256"
        )

    # Must have >= 2 ## headings
    headings = re.findall(r'^## .+', content, re.MULTILINE)
    if len(headings) < 2:
        errors.append(
            f"cryptographic_proof.md must have >= 2 '## ' headings, found {len(headings)}"
        )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
