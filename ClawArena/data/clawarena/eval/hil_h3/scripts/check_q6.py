#!/usr/bin/env python3
"""
check_q6.py -- Verify analysis/repo_comparison.json.

Usage:
    python check_q6.py <workspace_path>
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

    json_path = workspace / "analysis" / "repo_comparison.json"
    if not json_path.exists():
        print(f"FAILED: {json_path} not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: cannot parse {json_path}: {e}")
        sys.exit(1)

    # Check wangming_commits_before_chenwei_first == true
    flag = data.get("wangming_commits_before_chenwei_first")
    if flag is not True:
        errors.append(
            f"FAILED: wangming_commits_before_chenwei_first expected true, got {flag!r}"
        )

    # Check time_diff approximately 30 hours (±5 tolerance)
    diff = data.get("time_diff_wangming_first_to_chenwei_first_hours")
    if diff is None:
        errors.append(
            "FAILED: missing field 'time_diff_wangming_first_to_chenwei_first_hours'"
        )
    else:
        try:
            diff_val = float(diff)
            if abs(diff_val - 30) > 5:
                errors.append(
                    f"FAILED: time_diff expected approximately 30 hours (±5), got {diff_val}"
                )
        except (TypeError, ValueError):
            errors.append(
                f"FAILED: time_diff_wangming_first_to_chenwei_first_hours must be numeric, got {diff!r}"
            )

    # Check wangming_gitlab.total_commits == 5
    wm = data.get("wangming_gitlab", {})
    wm_commits = wm.get("total_commits")
    if wm_commits != 5:
        errors.append(
            f"FAILED: wangming_gitlab.total_commits expected 5, got {wm_commits!r}"
        )

    # Check chenwei_gitlab.total_commits == 3
    cw = data.get("chenwei_gitlab", {})
    cw_commits = cw.get("total_commits")
    if cw_commits != 3:
        errors.append(
            f"FAILED: chenwei_gitlab.total_commits expected 3, got {cw_commits!r}"
        )

    # Check wangming_gitlab.platform == "GitLab"
    if wm.get("platform", "").lower() not in ("gitlab", "gitLab"):
        errors.append(
            f"FAILED: wangming_gitlab.platform expected 'GitLab', got {wm.get('platform')!r}"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
