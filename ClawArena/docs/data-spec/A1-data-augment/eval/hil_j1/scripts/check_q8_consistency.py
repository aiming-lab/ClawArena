#!/usr/bin/env python3
"""
check_q8_consistency.py — Verify q8: analysis/系统性夸大一致性分析.md
  - File exists
  - Contains '50,234' or '50234' (official XHS plays)
  - Contains '120,000' or '120000' (MCN XHS plays)
  - Contains '32,178' or '32178' (official Bilibili plays)
  - Contains '65,000' or '65000' (MCN Bilibili plays)
  - Contains '2.39' or '2.386' (XHS ratio)
  - Contains '2.02' or '2.021' (Bilibili ratio)
  - Contains '3,812' or '3812' AND '8,500' or '8500' (likes comparison)
  - Contains systematic judgment keyword
  - >= 3 '##' headings
"""
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "系统性夸大一致性分析.md"

    if not target.exists():
        print("FAILED: analysis/系统性夸大一致性分析.md not found")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read file: {e}")
        sys.exit(1)

    errors = []

    # Check official XHS plays
    if "50,234" not in content and "50234" not in content:
        errors.append("'50,234' or '50234' (official Xiaohongshu plays) not found")

    # Check MCN XHS plays
    if "120,000" not in content and "120000" not in content:
        errors.append("'120,000' or '120000' (MCN Xiaohongshu plays) not found")

    # Check official Bilibili plays
    if "32,178" not in content and "32178" not in content:
        errors.append("'32,178' or '32178' (official Bilibili plays) not found")

    # Check MCN Bilibili plays
    if "65,000" not in content and "65000" not in content:
        errors.append("'65,000' or '65000' (MCN Bilibili plays) not found")

    # Check XHS ratio
    if "2.39" not in content and "2.386" not in content:
        errors.append("Xiaohongshu ratio '2.39' or '2.386' not found")

    # Check Bilibili ratio
    if "2.02" not in content and "2.021" not in content:
        errors.append("Bilibili ratio '2.02' or '2.021' not found")

    # Check likes comparison
    has_official_likes = "3,812" in content or "3812" in content
    has_mcn_likes = "8,500" in content or "8500" in content
    if not has_official_likes:
        errors.append("official likes '3,812' or '3812' not found")
    if not has_mcn_likes:
        errors.append("MCN likes '8,500' or '8500' not found")

    # Check systematic judgment
    systematic_keywords = ["系统性", "系统", "模式", "非偶然", "一致"]
    if not any(kw in content for kw in systematic_keywords):
        errors.append(
            f"systematic judgment keyword not found (expected one of: {systematic_keywords})"
        )

    # Check heading count >= 3
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 3:
        errors.append(f"'##' headings: {len(headings)} (expected >= 3)")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
