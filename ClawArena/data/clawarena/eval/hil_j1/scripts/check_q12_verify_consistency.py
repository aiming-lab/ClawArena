#!/usr/bin/env python3
"""
check_q12_verify_consistency.py — Verify q12: scripts/verify_ratio_consistency.py
  - Script exists and runs without error
  - Output JSON all_above_2x == true
  - Output JSON explanation_api_consistent == false
  - Output JSON xiaohongshu_ratio ~2.386 (±0.1)
  - Output JSON bilibili_ratio ~2.021 (±0.1)
  - Output JSON likes_ratio ~2.23 (±0.1)
"""
import sys
import json
import subprocess
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    script = workspace / "scripts" / "verify_ratio_consistency.py"

    if not script.exists():
        print("FAILED: scripts/verify_ratio_consistency.py not found")
        sys.exit(1)

    try:
        result = subprocess.run(
            ["python3", str(script)],
            capture_output=True,
            text=True,
            timeout=55,
            cwd=str(workspace),
        )
    except subprocess.TimeoutExpired:
        print("FAILED: script timed out after 55 seconds")
        sys.exit(1)
    except Exception as e:
        print(f"FAILED: error running script: {e}")
        sys.exit(1)

    if result.returncode != 0:
        print(f"FAILED: script exited with code {result.returncode}")
        if result.stderr:
            print(f"FAILED: stderr: {result.stderr[:500]}")
        sys.exit(1)

    try:
        data = json.loads(result.stdout)
    except Exception as e:
        print(f"FAILED: script stdout is not valid JSON: {e}")
        print(f"FAILED: stdout was: {result.stdout[:300]}")
        sys.exit(1)

    errors = []

    if data.get("all_above_2x") is not True:
        errors.append(f"all_above_2x expected true, got {data.get('all_above_2x')!r}")

    if data.get("explanation_api_consistent") is not False:
        errors.append(
            f"explanation_api_consistent expected false, got {data.get('explanation_api_consistent')!r}"
        )

    xh_ratio = data.get("xiaohongshu_ratio")
    if xh_ratio is None:
        errors.append("JSON missing field 'xiaohongshu_ratio'")
    elif abs(xh_ratio - 2.386) > 0.1:
        errors.append(f"xiaohongshu_ratio expected ~2.386 (±0.1), got {xh_ratio}")

    bili_ratio = data.get("bilibili_ratio")
    if bili_ratio is None:
        errors.append("JSON missing field 'bilibili_ratio'")
    elif abs(bili_ratio - 2.021) > 0.1:
        errors.append(f"bilibili_ratio expected ~2.021 (±0.1), got {bili_ratio}")

    likes_ratio = data.get("likes_ratio")
    if likes_ratio is None:
        errors.append("JSON missing field 'likes_ratio'")
    elif abs(likes_ratio - 2.23) > 0.1:
        errors.append(f"likes_ratio expected ~2.23 (±0.1), got {likes_ratio}")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
