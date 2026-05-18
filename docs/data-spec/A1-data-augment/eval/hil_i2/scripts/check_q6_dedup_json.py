#!/usr/bin/env python3
"""
check_q6_dedup_json.py — Validates analysis/deduplication_verification.json strict schema.

Required fields and exact values:
  total_raw: 912 (int)
  total_published: 847 (int)
  excluded_count: 65 (int)
  exclusion_cause: "HIS_migration_duplicates" (str)
  clinical_data_differences_in_excluded: 0 (int)
  pipeline_version: "V2.0" (str)
  pipeline_author: "王逸生" (str)
  pipeline_date: "2025-09-20" (str)
  adverse_outcome_rate_excluded: float
  adverse_outcome_rate_published: float
  rates_differ_significantly: false (bool)
"""
import sys
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q6_dedup_json.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "deduplication_verification.json"

    if not target.exists():
        print("FAILED: analysis/deduplication_verification.json not found")
        sys.exit(1)

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: invalid JSON: {e}")
        sys.exit(1)

    errors = []

    if data.get("total_raw") != 912:
        errors.append(f"total_raw expected 912 (int), got {data.get('total_raw')!r}")

    if data.get("total_published") != 847:
        errors.append(f"total_published expected 847 (int), got {data.get('total_published')!r}")

    if data.get("excluded_count") != 65:
        errors.append(f"excluded_count expected 65 (int), got {data.get('excluded_count')!r}")

    if data.get("exclusion_cause") != "HIS_migration_duplicates":
        errors.append(
            f"exclusion_cause expected 'HIS_migration_duplicates', "
            f"got {data.get('exclusion_cause')!r}"
        )

    if data.get("clinical_data_differences_in_excluded") != 0:
        errors.append(
            f"clinical_data_differences_in_excluded expected 0, "
            f"got {data.get('clinical_data_differences_in_excluded')!r}"
        )

    if data.get("pipeline_version") != "V2.0":
        errors.append(
            f"pipeline_version expected 'V2.0', got {data.get('pipeline_version')!r}"
        )

    if data.get("pipeline_author") != "王逸生":
        errors.append(
            f"pipeline_author expected '王逸生', got {data.get('pipeline_author')!r}"
        )

    if data.get("pipeline_date") != "2025-09-20":
        errors.append(
            f"pipeline_date expected '2025-09-20', got {data.get('pipeline_date')!r}"
        )

    # adverse_outcome_rate_excluded must be a float (or int coercible to float)
    aor_excl = data.get("adverse_outcome_rate_excluded")
    if not isinstance(aor_excl, (int, float)):
        errors.append(
            f"adverse_outcome_rate_excluded expected float, got {type(aor_excl).__name__!r}"
        )

    # adverse_outcome_rate_published must be a float
    aor_pub = data.get("adverse_outcome_rate_published")
    if not isinstance(aor_pub, (int, float)):
        errors.append(
            f"adverse_outcome_rate_published expected float, got {type(aor_pub).__name__!r}"
        )

    if data.get("rates_differ_significantly") is not False:
        errors.append(
            f"rates_differ_significantly expected false, "
            f"got {data.get('rates_differ_significantly')!r}"
        )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
