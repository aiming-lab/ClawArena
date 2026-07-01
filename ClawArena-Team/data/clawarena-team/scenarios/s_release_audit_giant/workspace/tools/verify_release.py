#!/usr/bin/env python3
"""verify_release.py — Pre-release sign-off helper.

Prints a deterministic VERIFIED:<sha256> line so the audit log can prove the
inputs that were certified. Pass the canonical input files as arguments, in
the order listed in the pre-release runbook.

Usage:
    python tools/verify_release.py <file1> [<file2> ...]

Output:
    VERIFIED:<sha256_hexdigest_of_concatenated_file_bytes>
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: verify_release.py <file1> [<file2> ...]", file=sys.stderr)
        return 2

    h = hashlib.sha256()
    for arg in sys.argv[1:]:
        p = Path(arg)
        if not p.exists():
            print(f"ERROR: missing input file: {p}", file=sys.stderr)
            return 1
        h.update(p.read_bytes())

    print(f"VERIFIED:{h.hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
