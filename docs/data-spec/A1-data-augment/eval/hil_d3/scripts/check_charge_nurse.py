#!/usr/bin/env python3
"""check_charge_nurse.py — (legacy stub, logic merged into check_cross_validation.py for v2).

In v2, q11 merges cross_source_validation and charge_nurse_asymmetry.
This file retained for backward compatibility — delegates to check_cross_validation.py.
"""
import sys
import subprocess
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_charge_nurse.py <workspace>")
        sys.exit(1)

    script_dir = Path(__file__).parent
    result = subprocess.run(
        [sys.executable, str(script_dir / "check_cross_validation.py"), sys.argv[1]],
        capture_output=False
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
