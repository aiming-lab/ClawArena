#!/usr/bin/env python3
"""
check_q21.py -- Verify analysis/case_provenance.json (M4 schema + M6 github_excluded).

Usage:
    python check_q21.py <workspace_path>
"""
import sys
import json
from pathlib import Path

VALID_CONFIDENCE = {"confirmed", "probable", "disputed"}


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    json_path = workspace / "analysis" / "case_provenance.json"
    if not json_path.exists():
        print(f"FAILED: {json_path} not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: cannot parse {json_path}: {e}")
        sys.exit(1)

    # Check commit_owner_evidence == "wangming"
    owner = data.get("commit_owner_evidence")
    if owner != "wangming":
        errors.append(
            f"FAILED: commit_owner_evidence expected 'wangming', got {owner!r}"
        )

    # Check source_confidence is valid enum
    confidence = data.get("source_confidence")
    if confidence not in VALID_CONFIDENCE:
        errors.append(
            f"FAILED: source_confidence must be one of {VALID_CONFIDENCE}, got {confidence!r}"
        )

    # Check github_evidence_excluded == true (M6)
    github_excl = data.get("github_evidence_excluded")
    if github_excl is not True:
        errors.append(
            f"FAILED: github_evidence_excluded expected true (M6 requirement), got {github_excl!r}"
        )

    # Check so_common_source_confirmed == true
    so_confirmed = data.get("so_common_source_confirmed")
    if so_confirmed is not True:
        errors.append(
            f"FAILED: so_common_source_confirmed expected true, got {so_confirmed!r}"
        )

    # Check resolution == "citation_violation"
    resolution = data.get("resolution")
    if resolution != "citation_violation":
        errors.append(
            f"FAILED: resolution expected 'citation_violation', got {resolution!r}"
        )

    # Check supporting_factors is a non-empty list
    supporting = data.get("supporting_factors", [])
    if not isinstance(supporting, list) or len(supporting) == 0:
        errors.append(
            "FAILED: supporting_factors must be a non-empty list"
        )

    # Check primary_evidence is non-empty string
    primary = data.get("primary_evidence", "")
    if not isinstance(primary, str) or not primary.strip():
        errors.append(
            "FAILED: primary_evidence must be a non-empty string"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
