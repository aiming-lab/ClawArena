#!/usr/bin/env python3
"""
check_dedup_verification.py — Validates analysis/deduplication_verification.md
                               AND analysis/deduplication_verification.json (if present).

MD checks:
  1. File exists at analysis/deduplication_verification.md
  2. N=912, N=847, 65 present as word-boundary numbers
  3. "HIS" AND "migration" present
  4. ("tiebreaker" OR "V2.0") AND "V2.1" present
  5. "23" present (ID-only differences)

JSON checks (analysis/deduplication_verification.json — if present):
  6. total_raw == 912
  7. excluded_count == 65
  8. clinical_data_differences_in_excluded == 0
  9. irb_before_extraction == true (if field present)
"""
import sys
import re
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_dedup_verification.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "deduplication_verification.md"

    if not target.exists():
        print(f"FAILED: {target} does not exist")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # Key numeric values (word-boundary)
    for num in ("912", "847", "65", "23"):
        if not re.search(rf'\b{num}\b', content):
            failures.append(f"FAILED: '{num}' not found as standalone number in {target.name}")

    # HIS migration
    if "HIS" not in content:
        failures.append("FAILED: 'HIS' not found (HIS migration source must be mentioned)")
    if not re.search(r'\bmigration\b', content, re.IGNORECASE):
        failures.append("FAILED: 'migration' not found")

    # Pipeline version references
    has_tiebreaker = bool(re.search(r'\btiebreaker\b', content, re.IGNORECASE))
    has_v20 = "V2.0" in content
    has_v21 = "V2.1" in content

    if not (has_tiebreaker or has_v20):
        failures.append("FAILED: 'tiebreaker' or 'V2.0' not found")
    if not has_v21:
        failures.append("FAILED: 'V2.1' not found")

    # IRB number in MD
    if 'BFH-2025-IRB-0342' not in content:
        failures.append("FAILED: IRB number #BFH-2025-IRB-0342 not found in MD")

    # Zero clinical differences stated
    if not re.search(
        r'(clinical.{0,60}(0|zero|none|no\s+diff)'
        r'|(0|zero|none).{0,60}clinical.{0,60}diff)',
        content, re.IGNORECASE
    ):
        failures.append(
            "FAILED: clinical_data_differences == 0 not stated "
            "(document must confirm zero clinical differences among excluded records)"
        )

    # --- JSON VALIDATION (if present) ---
    json_target = workspace / "analysis" / "deduplication_verification.json"
    if json_target.exists():
        try:
            data = json.loads(json_target.read_text(encoding="utf-8"))
            if data.get('total_raw') != 912:
                failures.append(
                    f"FAILED: JSON total_raw expected 912, got {data.get('total_raw')}"
                )
            if data.get('excluded_count') != 65:
                failures.append(
                    f"FAILED: JSON excluded_count expected 65, got {data.get('excluded_count')}"
                )
            if data.get('clinical_data_differences_in_excluded') != 0:
                failures.append(
                    "FAILED: JSON clinical_data_differences_in_excluded expected 0, "
                    f"got {data.get('clinical_data_differences_in_excluded')}"
                )
            if 'irb_before_extraction' in data and data.get('irb_before_extraction') is not True:
                failures.append("FAILED: JSON irb_before_extraction must be true")
        except json.JSONDecodeError as exc:
            failures.append(f"FAILED: deduplication_verification.json is not valid JSON: {exc}")

    if failures:
        for f in failures:
            print(f)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
