#!/usr/bin/env python3
"""check_presenteeism.py — (legacy stub, logic merged into check_near_miss_log.py for v2).

In v2, q15 merges near_miss_event_log.json and presenteeism_vs_absenteeism.md.
This file retained for backward compatibility — delegates to check_near_miss_log.py.
"""
import sys
import subprocess
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_presenteeism.py <workspace>")
        sys.exit(1)

    script_dir = Path(__file__).parent
    result = subprocess.run(
        [sys.executable, str(script_dir / "check_near_miss_log.py"), sys.argv[1]],
        capture_output=False
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
