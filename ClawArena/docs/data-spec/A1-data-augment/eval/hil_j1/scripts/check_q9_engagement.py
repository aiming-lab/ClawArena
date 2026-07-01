#!/usr/bin/env python3
"""
check_q9_engagement.py — Verify q9: analysis/互动数据比率分析.md
  - File exists
  - Contains '3,812' or '3812' (official likes)
  - Contains '8,500' or '8500' (MCN likes)
  - Contains ratio text approximately 2.23x (regex parse, abs < 0.05)
  - >= 2 '##' headings
"""
import sys
import re
from pathlib import Path


def parse_ratio_from_text(content: str, target: float, tolerance: float) -> bool:
    """Search for a float in content that is within tolerance of target."""
    # Extract all decimal numbers from content
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
    target = workspace / "analysis" / "互动数据比率分析.md"

    if not target.exists():
        print("FAILED: analysis/互动数据比率分析.md not found")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read file: {e}")
        sys.exit(1)

    errors = []

    # Check official likes
    if "3,812" not in content and "3812" not in content:
        errors.append("official likes '3,812' or '3812' not found")

    # Check MCN likes
    if "8,500" not in content and "8500" not in content:
        errors.append("MCN likes '8,500' or '8500' not found")

    # Check ratio ~2.23x
    if not parse_ratio_from_text(content, 2.23, 0.05):
        errors.append(
            "likes ratio ~2.23 not found in text (expected a float within ±0.05 of 2.23)"
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
