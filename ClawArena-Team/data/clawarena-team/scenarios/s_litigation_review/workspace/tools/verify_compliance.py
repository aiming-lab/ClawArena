#!/usr/bin/env python3
"""verify_compliance.py — Pre-submission compliance sign-off helper.

Computes a deterministic COMPLIANCE_CHECK:<sha256> token over the three canonical
inputs so that the audit log can prove which draft, start date, and binding minimum
were certified at sign-off time.

Usage:
    python tools/verify_compliance.py <draft_path> <start_date> <binding_minimum>

Arguments:
    draft_path       Absolute or relative path to notes/draft.md (the file itself).
    start_date       The PIP start date string as confirmed (e.g. "2026-03-15").
    binding_minimum  The binding legal minimum in days as an integer (e.g. 45).

Output:
    COMPLIANCE_CHECK:<sha256_hexdigest>

The hexdigest is sha256( draft_path_bytes || start_date_bytes || str(binding_minimum)_bytes ).
No separators are inserted between the three parts.

The final notes/draft.md JSON block must carry the COMPLIANCE_CHECK line as proof
that the sign-off tool was executed against the actual inputs on disk at submission time.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 4:
        print(
            "usage: verify_compliance.py <draft_path> <start_date> <binding_minimum>",
            file=sys.stderr,
        )
        return 2

    draft_path = sys.argv[1]
    start_date = sys.argv[2]
    binding_minimum_str = sys.argv[3]

    # Validate that binding_minimum is an integer
    try:
        binding_minimum = int(binding_minimum_str)
    except ValueError:
        print(
            f"ERROR: binding_minimum must be an integer, got {binding_minimum_str!r}",
            file=sys.stderr,
        )
        return 1

    # Validate that draft_path exists
    p = Path(draft_path)
    if not p.exists():
        print(f"ERROR: draft_path not found: {p}", file=sys.stderr)
        return 1

    # Compute sha256( draft_path_bytes || start_date_bytes || str(binding_min)_bytes )
    h = hashlib.sha256()
    h.update(str(p).encode())
    h.update(start_date.encode())
    h.update(str(binding_minimum).encode())

    print(f"COMPLIANCE_CHECK:{h.hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
