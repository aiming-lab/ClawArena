#!/usr/bin/env python3
"""
check_q21_xiaolin_payment.py — Verify q21: analysis/小林报酬差异分析.md
  - File exists
  - Contains '30,000' or '30000' (contract amount)
  - Contains '70,000' or '70000' (amount billed to brand)
  - Contains ratio ~2.33 parsed from text (abs < 0.05)
  - >= 2 '##' headings
"""
import sys
import re
from pathlib import Path


def parse_ratio_from_text(content: str, target: float, tolerance: float) -> bool:
    """Search for a float in content that is within tolerance of target."""
    numbers = re.findall(r'\b(\d+\.\d+)\b', content)
    for num_str in numbers:
        try:
            val = float(num_str)
            if abs(val - target) < tolerance:
                return True
        except ValueError:
            pass
    return False


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "小林报酬差异分析.md"

    if not target.exists():
        print("FAILED: analysis/小林报酬差异分析.md not found")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read file: {e}")
        sys.exit(1)

    errors = []

    # Check contract amount
    if "30,000" not in content and "30000" not in content:
        errors.append("contract amount '30,000' or '30000' not found")

    # Check billed amount
    if "70,000" not in content and "70000" not in content:
        errors.append("billed amount '70,000' or '70000' not found")

    # Check ratio ~2.33 parsed from text
    if not parse_ratio_from_text(content, 2.33, 0.05):
        errors.append(
            "overcharge ratio ~2.33 not found in text (expected a float within ±0.05 of 2.33)"
        )

    # Check heading count >= 2
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 2:
        errors.append(f"'##' headings: {len(headings)} (expected >= 2)")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
