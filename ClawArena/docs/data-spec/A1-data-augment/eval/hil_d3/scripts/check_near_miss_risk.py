#!/usr/bin/env python3
"""check_near_miss_risk.py — (legacy stub, logic merged into check_reporting_culture.py for v2).

In v2, q14 merges reporting_culture_analysis.md and near_miss_risk_model.md.
This file retained for backward compatibility — delegates to check_reporting_culture.py.
"""
import sys
import subprocess
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_near_miss_risk.py <workspace>")
        sys.exit(1)

    script_dir = Path(__file__).parent
    result = subprocess.run(
        [sys.executable, str(script_dir / "check_reporting_culture.py"), sys.argv[1]],
        capture_output=False
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
