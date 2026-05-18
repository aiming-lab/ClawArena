#!/usr/bin/env python3
"""
check_q3.py -- Verify docs/contradiction_map.json.

Usage:
    python check_q3.py <workspace_path>
"""
import sys
import json
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    json_path = workspace / "docs" / "contradiction_map.json"
    if not json_path.exists():
        print(f"FAILED: {json_path} not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: cannot parse docs/contradiction_map.json: {e}")
        sys.exit(1)

    # Check top-level structure
    if "contradictions" not in data:
        errors.append("FAILED: docs/contradiction_map.json missing 'contradictions' key")
    else:
        contradictions = data["contradictions"]
        if not isinstance(contradictions, list) or len(contradictions) < 3:
            errors.append(
                f"FAILED: 'contradictions' must be a list with >= 3 entries, "
                f"got {len(contradictions) if isinstance(contradictions, list) else type(contradictions)}"
            )
        else:
            required_fields = ["id", "title", "source_a", "evidence_a", "source_b", "evidence_b", "resolved"]
            for i, entry in enumerate(contradictions):
                missing = [f for f in required_fields if f not in entry]
                if missing:
                    errors.append(f"FAILED: contradictions[{i}] missing fields: {missing}")
                if "resolved" in entry and entry["resolved"] is not False:
                    errors.append(
                        f"FAILED: contradictions[{i}] has resolved={entry['resolved']!r}, "
                        "expected false (all contradictions unresolved at Phase 0)"
                    )

            # Check C1 covers GPU SKU mismatch
            all_text = json.dumps(contradictions)
            if not re.search(r'GPU-A100-80G|A100', all_text):
                errors.append("FAILED: no contradiction references GPU-A100-80G or A100 (C1 missing)")
            if not re.search(r'GPU-A40-48G|A40', all_text):
                errors.append("FAILED: no contradiction references GPU-A40-48G or A40 (C1 missing)")

            # Check that actual filenames are cited
            has_filename = (
                re.search(r'order-history-618\.md', all_text) or
                re.search(r'package-tracking-log\.md', all_text) or
                re.search(r'product-listing-screenshot\.md', all_text) or
                re.search(r'payment-records\.md', all_text)
            )
            if not has_filename:
                errors.append(
                    "FAILED: no source filenames found in contradictions. "
                    "source_a/source_b fields must cite actual workspace file names."
                )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
