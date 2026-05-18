#!/usr/bin/env python3
"""
check_q22_pipeline_audit.py — Validates analysis/pipeline_audit_trail.md.

Checks:
  1. 'V2.0' and exact date '2025-09-20' both present
  2. 'V2.1' and exact date '2025-10-15' both present
  3. 'field rename' characterization for V2.1 (or 'minor')
  4. 'post-hoc' refuted OR 'pre-submission' stated (pipeline predates complaint)
  5. [NUMERIC] V2.0 date 2025-09-20 verified as exact string
  6. [NUMERIC] V2.1 date 2025-10-15 verified as exact string
  7. [NUMERIC] 'field rename' for V2.1 verified via re.search
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q22_pipeline_audit.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "pipeline_audit_trail.md"

    if not target.exists():
        print("FAILED: analysis/pipeline_audit_trail.md not found")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    errors = []

    # V2.0 and exact date 2025-09-20
    if "V2.0" not in content:
        errors.append("'V2.0' not found")
    if "2025-09-20" not in content:
        errors.append("'2025-09-20' (V2.0 run date — exact string required) not found")

    # V2.1 and exact date 2025-10-15
    if "V2.1" not in content:
        errors.append("'V2.1' not found")
    if "2025-10-15" not in content:
        errors.append("'2025-10-15' (V2.1 run date — exact string required) not found")

    # V2.1 characterized as field rename or minor
    if not re.search(
        r'field\s+rename|minor|tiebreaker only|no.{0,20}case removal|no.{0,20}exclusion logic',
        content, re.IGNORECASE
    ):
        errors.append(
            "V2.1 not characterized as minor/field-rename update — "
            "expected 'field rename', 'minor', or equivalent"
        )

    # Pre-submission / not post-hoc
    if not re.search(
        r'pre-submission|pre submission|not post.hoc|predates|before.{0,30}submission|before.{0,30}complaint',
        content,
        re.IGNORECASE
    ):
        errors.append(
            "no 'pre-submission' or 'not post-hoc' language found — "
            "document must establish that deduplication predates the complaint"
        )

    # 王逸生 authorship for V2.0
    if not re.search(r'王逸生|Wang\s+Yisheng|\bWang\b', content):
        errors.append("'王逸生' / 'Wang Yisheng' (V2.0 author) not found")

    # 林依 authorship for V2.1
    if not re.search(r'林依|Lin\s+Yi|\bLin\b', content):
        errors.append("'林依' / 'Lin Yi' (V2.1 author) not found")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
