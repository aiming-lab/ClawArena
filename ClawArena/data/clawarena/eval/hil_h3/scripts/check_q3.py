#!/usr/bin/env python3
"""
check_q3.py -- Verify docs/evidence_classification.json.

Usage:
    python check_q3.py <workspace_path>
"""
import sys
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    json_path = workspace / "docs" / "evidence_classification.json"
    if not json_path.exists():
        print(f"FAILED: {json_path} not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: cannot parse {json_path}: {e}")
        sys.exit(1)

    # Check top-level keys
    if "objective_evidence" not in data:
        errors.append("FAILED: missing key 'objective_evidence'")
    if "subjective_evidence" not in data:
        errors.append("FAILED: missing key 'subjective_evidence'")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    obj = data.get("objective_evidence", [])
    subj = data.get("subjective_evidence", [])

    # Objective: at least 3 entries
    if not isinstance(obj, list) or len(obj) < 3:
        errors.append(
            f"FAILED: objective_evidence must have >= 3 entries, got {len(obj)}"
        )
    else:
        for i, entry in enumerate(obj):
            if not isinstance(entry, dict):
                errors.append(f"FAILED: objective_evidence[{i}] must be a dict")
                continue
            if not entry.get("source"):
                errors.append(f"FAILED: objective_evidence[{i}] missing 'source'")
            if not entry.get("finding"):
                errors.append(f"FAILED: objective_evidence[{i}] missing 'finding'")
            if entry.get("verifiable") is not True:
                errors.append(
                    f"FAILED: objective_evidence[{i}] 'verifiable' must be true"
                )

    # Subjective: at least 2 entries
    if not isinstance(subj, list) or len(subj) < 2:
        errors.append(
            f"FAILED: subjective_evidence must have >= 2 entries, got {len(subj)}"
        )
    else:
        for i, entry in enumerate(subj):
            if not isinstance(entry, dict):
                errors.append(f"FAILED: subjective_evidence[{i}] must be a dict")
                continue
            if not entry.get("source"):
                errors.append(f"FAILED: subjective_evidence[{i}] missing 'source'")
            if not entry.get("claim"):
                errors.append(f"FAILED: subjective_evidence[{i}] missing 'claim'")
            if entry.get("verifiable") is not False:
                errors.append(
                    f"FAILED: subjective_evidence[{i}] 'verifiable' must be false"
                )

    # Check that git histories appear in objective evidence
    obj_sources = " ".join(
        str(e.get("source", "")) + " " + str(e.get("finding", ""))
        for e in obj
        if isinstance(e, dict)
    ).lower()
    if "git" not in obj_sources and "commit" not in obj_sources:
        errors.append(
            "FAILED: objective_evidence should include git commit history entries"
        )

    # Check that MOSS report appears in objective evidence
    if "moss" not in obj_sources and "plagiarism" not in obj_sources and "similarity" not in obj_sources:
        errors.append(
            "FAILED: objective_evidence should include MOSS report / plagiarism detection report"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
