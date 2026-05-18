#!/usr/bin/env python3
"""
check_q8_pipeline_authorship.py — Validates analysis/pipeline_authorship_analysis.md.

Checks:
  1. 'V2.0' and '王逸生' present (within proximity check)
  2. 'V2.1' present
  3. '林依' present
  4. 'field rename' or 'minor' present (characterizing V2.1 as minor update)
  5. ≥3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q8_pipeline_authorship.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "pipeline_authorship_analysis.md"

    if not target.exists():
        print("FAILED: analysis/pipeline_authorship_analysis.md not found")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    errors = []

    # V2.0 present
    if "V2.0" not in content:
        errors.append("'V2.0' not found")

    # 王逸生 present
    if "王逸生" not in content:
        errors.append("'王逸生' not found")

    # V2.1 present
    if "V2.1" not in content:
        errors.append("'V2.1' not found")

    # 林依 present
    if "林依" not in content:
        errors.append("'林依' not found")

    # V2.1 characterized as minor / field rename
    if not re.search(r'field rename|minor|tiebreaker', content, re.IGNORECASE):
        errors.append("V2.1 not characterized as 'field rename', 'minor', or tiebreaker change")

    # V2.0 and 王逸生 in same paragraph context (within 300 chars)
    v20_idx = content.find("V2.0")
    wang_idx = content.find("王逸生")
    if v20_idx >= 0 and wang_idx >= 0:
        if abs(v20_idx - wang_idx) > 400:
            errors.append(
                f"'V2.0' and '王逸生' are too far apart ({abs(v20_idx - wang_idx)} chars) — "
                "they should appear in the same section"
            )
    elif v20_idx < 0 or wang_idx < 0:
        pass  # Already reported above

    # Minimum 3 ## headings
    headings = re.findall(r'^##\s+', content, re.MULTILINE)
    if len(headings) < 3:
        errors.append(f"only {len(headings)} ## headings found (expected ≥3)")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
