#!/usr/bin/env python3
"""
check_q16_zhang_guidance.py — Validates analysis/zhang_zhuren_guidance_analysis.md.

Checks:
  1. '张主任' or 'zhangzhuren' (case-insensitive) present
  2. 'standard' or 'pre-registered' present
  3. Contrast between complaint characterization and Zhang's guidance present
  4. ≥3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q16_zhang_guidance.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "zhang_zhuren_guidance_analysis.md"

    if not target.exists():
        print("FAILED: analysis/zhang_zhuren_guidance_analysis.md not found")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    errors = []

    # 张主任 or zhangzhuren
    if not re.search(r'张主任|zhangzhuren|zhang.{0,5}zhuren|director zhang', content, re.IGNORECASE):
        errors.append(
            "'张主任' or 'zhangzhuren' not found — cite Director Zhang as the guidance source"
        )

    # Standard or pre-registered
    if not re.search(r'standard|pre-register|preregister|registered', content, re.IGNORECASE):
        errors.append(
            "'standard' or 'pre-registered' not found — "
            "document must characterize HIS deduplication as standard/pre-registered procedure"
        )

    # Contrast: complaint characterization vs guidance
    has_complaint_ref = re.search(r'complaint|allegation|allege', content, re.IGNORECASE)
    has_guidance_ref = re.search(
        r'guidance|clarif|explain|standard|pre-register', content, re.IGNORECASE
    )
    if not has_complaint_ref or not has_guidance_ref:
        errors.append(
            "no contrast between complaint characterization and Zhang's expert guidance found — "
            "document must compare the two interpretations"
        )

    # ≥3 ## headings
    headings = re.findall(r'^##\s+', content, re.MULTILINE)
    if len(headings) < 3:
        errors.append(f"only {len(headings)} ## headings found (expected ≥3)")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
