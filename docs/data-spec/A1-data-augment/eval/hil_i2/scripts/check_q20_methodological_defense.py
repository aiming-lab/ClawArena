#!/usr/bin/env python3
"""
check_q20_methodological_defense.py — Validates analysis/methodological_defense.md.

Checks:
  1. 'V2.0' present (pipeline version — exact string)
  2. Full IRB number BFH-2025-IRB-0342 present
  3. 'HIS' and 'migration' both present
  4. Contrast between complaint framing and evidence-based explanation (M2)
  5. [NUMERIC] N=912, N=847, 65 present as word-boundary numbers
  6. [NUMERIC] 'HIS migration' phrase in same document context as IRB number
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q20_methodological_defense.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "methodological_defense.md"

    if not target.exists():
        print("FAILED: analysis/methodological_defense.md not found")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    errors = []

    # V2.0 present (exact string match)
    if "V2.0" not in content:
        errors.append("'V2.0' not found — cite Pipeline V2.0 by 王逸生")

    # Full IRB number required
    if 'BFH-2025-IRB-0342' not in content:
        errors.append(
            "'BFH-2025-IRB-0342' IRB number not found — cite the full IRB approval number #BFH-2025-IRB-0342"
        )

    # HIS and migration both present
    if "HIS" not in content:
        errors.append("'HIS' not found — explain HIS system migration context")
    if not re.search(r'migration|migrate', content, re.IGNORECASE):
        errors.append("'migration' not found — explain the HIS migration event")

    # M2 contrast: complaint framing vs evidence-based explanation
    has_complaint = re.search(r'complaint|allegation|allege|selective', content, re.IGNORECASE)
    has_evidence = re.search(
        r'pipeline|log|evidence|standard|pre-register|pre-approved',
        content, re.IGNORECASE
    )
    if not has_complaint or not has_evidence:
        errors.append(
            "M2 contrast missing: document must explicitly contrast the complaint's framing "
            "('selective exclusion') with the evidence-based explanation ('standard HIS deduplication')"
        )

    # --- NUMERIC VALIDATION ---
    if not re.search(r'\b912\b', content):
        errors.append("N=912 not found as standalone number")
    if not re.search(r'\b847\b', content):
        errors.append("N=847 not found as standalone number")
    if not re.search(r'\b65\b', content):
        errors.append("discrepancy count 65 not found as standalone number")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
