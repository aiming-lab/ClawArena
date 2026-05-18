#!/usr/bin/env python3
"""
check_version_table.py — Validates analysis/version_difference_table.md.

Checks:
  1. File exists at analysis/version_difference_table.md
  2. "V2.0" and "V2.1" both present (exact strings)
  3. 王逸生 or "Wang Yisheng" present (V2.0 author — exact name)
  4. 林依 or "Lin Yi" present (V2.1 author — exact name)
  5. V2.0 date "2025-09-20" present (exact date string)
  6. V2.1 date "2025-10-15" present (exact date string)
  7. "23" present as word-boundary number (ID-only differences)
  8. [NUMERIC] V2.0 author + date co-verified in same document
  9. [NUMERIC] V2.1 author + date co-verified in same document
  10. [NUMERIC] Clinical differences = 0 stated explicitly
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_version_table.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "version_difference_table.md"

    if not target.exists():
        print(f"FAILED: {target} does not exist")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # Pipeline versions (exact strings)
    if "V2.0" not in content:
        failures.append("FAILED: 'V2.0' not found")
    if "V2.1" not in content:
        failures.append("FAILED: 'V2.1' not found")

    # V2.0 author: 王逸生 (exact Unicode) or Wang Yisheng
    if not re.search(r'王逸生|Wang\s+Yisheng|\bWang\b', content):
        failures.append("FAILED: '王逸生' / 'Wang Yisheng' (V2.0 author) not found")

    # V2.1 author: 林依 (exact Unicode) or Lin Yi
    if not re.search(r'林依|Lin\s+Yi|\bLin\b', content):
        failures.append("FAILED: '林依' / 'Lin Yi' (V2.1 author) not found")

    # V2.0 date — exact string required
    if "2025-09-20" not in content:
        failures.append("FAILED: V2.0 date '2025-09-20' (exact string) not found")

    # V2.1 date — exact string required
    if "2025-10-15" not in content:
        failures.append("FAILED: V2.1 date '2025-10-15' (exact string) not found")

    # 23 ID-only differences (word boundary)
    if not re.search(r'\b23\b', content):
        failures.append("FAILED: '23' (ID-only differences) not found as standalone number")

    # Clinical differences = 0 (must be explicit, not just a bare '0' token)
    if not re.search(
        r'(clinical.{0,80}(0|zero|none|no\s+diff)'
        r'|(0|zero|none).{0,80}clinical)',
        content, re.IGNORECASE
    ):
        failures.append(
            "FAILED: zero clinical differences not explicitly stated "
            "(expected 'clinical differences: 0' or equivalent)"
        )

    if failures:
        for f in failures:
            print(f)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
