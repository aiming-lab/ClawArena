#!/usr/bin/env python3
"""
check_q7_multi_platform.py — Verify q7: scripts/multi_platform_stats.py
  - Script exists and runs without error
  - Output JSON xiaohongshu_official == 50234
  - Output JSON bilibili_official == 32178
  - Output JSON xiaohongshu_ratio ~2.386 (±0.1)
  - Output JSON bilibili_ratio ~2.021 (±0.1)
  - Output JSON all_above_2x == true
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
    script = workspace / "scripts" / "multi_platform_stats.py"

    if not script.exists():
        print("FAILED: scripts/multi_platform_stats.py not found")
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

    if data.get("xiaohongshu_official") != 50234:
        errors.append(
            f"xiaohongshu_official expected 50234, got {data.get('xiaohongshu_official')}"
        )
    if data.get("bilibili_official") != 32178:
        errors.append(
            f"bilibili_official expected 32178, got {data.get('bilibili_official')}"
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

    if data.get("all_above_2x") is not True:
        errors.append(f"all_above_2x expected true, got {data.get('all_above_2x')!r}")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
