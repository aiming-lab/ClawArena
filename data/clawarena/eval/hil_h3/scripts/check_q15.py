#!/usr/bin/env python3
"""
check_q15.py -- Verify analysis/similarity_breakdown.json.

Usage:
    python check_q15.py <workspace_path>
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

    json_path = workspace / "analysis" / "similarity_breakdown.json"
    if not json_path.exists():
        print(f"FAILED: {json_path} not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: cannot parse {json_path}: {e}")
        sys.exit(1)

    # Check moss_total_pct == 95
    moss = data.get("moss_total_pct")
    if moss != 95:
        errors.append(
            f"FAILED: moss_total_pct expected 95, got {moss!r}"
        )

    # Check so_explainable_pct approximately 85 (±5 tolerance)
    so_pct = data.get("so_explainable_pct")
    if so_pct is None:
        errors.append("FAILED: missing field 'so_explainable_pct'")
    else:
        try:
            so_val = float(so_pct)
            if abs(so_val - 85) > 5:
                errors.append(
                    f"FAILED: so_explainable_pct expected approximately 85 (±5), got {so_val}"
                )
        except (TypeError, ValueError):
            errors.append(
                f"FAILED: so_explainable_pct must be numeric, got {so_pct!r}"
            )

    # Check unexplained_pct present
    unexplained = data.get("unexplained_pct")
    if unexplained is None:
        errors.append("FAILED: missing field 'unexplained_pct'")
    else:
        # so_explainable + unexplained should approximately equal 95 (±5)
        if so_pct is not None:
            try:
                total = float(so_pct) + float(unexplained)
                if abs(total - 95) > 5:
                    errors.append(
                        f"FAILED: so_explainable_pct + unexplained_pct = {total}, "
                        "expected approximately 95 (±5)"
                    )
            except (TypeError, ValueError):
                errors.append(
                    "FAILED: so_explainable_pct and unexplained_pct must be numeric"
                )

    # Check so_explains_majority == true
    if data.get("so_explains_majority") is not True:
        errors.append(
            f"FAILED: so_explains_majority expected true, got {data.get('so_explains_majority')!r}"
        )

    # Check inter_student_copying_evidence == false
    if data.get("inter_student_copying_evidence") is not False:
        errors.append(
            f"FAILED: inter_student_copying_evidence expected false, "
            f"got {data.get('inter_student_copying_evidence')!r}"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
