#!/usr/bin/env python3
"""
check_q4_script_ratios.py — Verify q4: scripts/compute_data_ratios.py
  - Script exists and runs without error
  - Output JSON contains xiaohongshu_ratio (~2.386 ±0.1)
  - Output JSON contains bilibili_ratio (~2.021 ±0.1)
  - Output JSON systematic_inflation == true
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
    script = workspace / "scripts" / "compute_data_ratios.py"

    if not script.exists():
        print("FAILED: scripts/compute_data_ratios.py not found")
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

    xh_ratio = data.get("xiaohongshu_ratio", None)
    if xh_ratio is None:
        errors.append("JSON missing field 'xiaohongshu_ratio'")
    elif abs(xh_ratio - 2.386) > 0.1:
        errors.append(f"xiaohongshu_ratio expected ~2.386 (±0.1), got {xh_ratio}")

    bili_ratio = data.get("bilibili_ratio", None)
    if bili_ratio is None:
        errors.append("JSON missing field 'bilibili_ratio'")
    elif abs(bili_ratio - 2.021) > 0.1:
        errors.append(f"bilibili_ratio expected ~2.021 (±0.1), got {bili_ratio}")

    systematic = data.get("systematic_inflation")
    if systematic is not True:
        errors.append(f"systematic_inflation expected true, got {systematic!r}")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
