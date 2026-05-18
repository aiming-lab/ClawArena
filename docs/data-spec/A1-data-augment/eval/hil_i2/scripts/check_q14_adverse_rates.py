#!/usr/bin/env python3
"""
check_q14_adverse_rates.py — Validates q14 output:
  (a) analysis/adverse_outcome_comparison.md
  (b) analysis/adverse_outcome_rates.json

MD checks:
  - '65' and '847' present
  - rates described as consistent / not significantly different
  - selective exclusion hypothesis refuted

JSON checks:
  - excluded_n == 65 (int)
  - published_n == 847 (int)
  - rates_significantly_different == false (bool)
  - conclusion == "no_selective_exclusion" (str, exact)
"""
import sys
import json
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q14_adverse_rates.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    # --- File 1: adverse_outcome_comparison.md ---
    md_path = workspace / "analysis" / "adverse_outcome_comparison.md"
    if not md_path.exists():
        print("FAILED: analysis/adverse_outcome_comparison.md not found")
        sys.exit(1)

    md_content = md_path.read_text(encoding="utf-8")

    for num in ("65", "847"):
        if not re.search(rf'\b{num}\b', md_content):
            errors.append(f"adverse_outcome_comparison.md: '{num}' not found")

    # Rates consistent language
    if not re.search(
        r'consistent|similar|not significantly different|no significant|comparable|no difference',
        md_content,
        re.IGNORECASE
    ):
        errors.append(
            "adverse_outcome_comparison.md: no 'consistent' / 'similar' / 'not significantly "
            "different' language found for rate comparison"
        )

    # Selective exclusion refuted
    if not re.search(
        r'refut|not support|contradict|no evidence|disprove|rules out|selective.{0,50}(not|no)',
        md_content,
        re.IGNORECASE
    ):
        errors.append(
            "adverse_outcome_comparison.md: selective exclusion hypothesis not explicitly refuted"
        )

    # Minimum 2 ## headings
    headings = re.findall(r'^##\s+', md_content, re.MULTILINE)
    if len(headings) < 2:
        errors.append(
            f"adverse_outcome_comparison.md: only {len(headings)} ## headings (expected ≥2)"
        )

    # --- File 2: adverse_outcome_rates.json ---
    json_path = workspace / "analysis" / "adverse_outcome_rates.json"
    if not json_path.exists():
        print("FAILED: analysis/adverse_outcome_rates.json not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: adverse_outcome_rates.json is not valid JSON: {e}")
        sys.exit(1)

    if data.get("excluded_n") != 65:
        errors.append(f"excluded_n expected 65, got {data.get('excluded_n')!r}")

    if data.get("published_n") != 847:
        errors.append(f"published_n expected 847, got {data.get('published_n')!r}")

    if data.get("rates_significantly_different") is not False:
        errors.append(
            f"rates_significantly_different expected false, "
            f"got {data.get('rates_significantly_different')!r}"
        )

    if data.get("conclusion") != "no_selective_exclusion":
        errors.append(
            f"conclusion expected 'no_selective_exclusion', got {data.get('conclusion')!r}"
        )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
