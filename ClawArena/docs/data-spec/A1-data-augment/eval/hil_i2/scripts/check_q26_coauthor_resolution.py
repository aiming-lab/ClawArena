#!/usr/bin/env python3
"""
check_q26_coauthor_resolution.py — Validates analysis/coauthor_resolution_strategy.md.

Checks:
  1. '王逸生' name present (exact Unicode string)
  2. Contemporaneous / pre-complaint contrast (co-signature vs post-complaint distancing)
  3. 'pipeline' cited as independent evidence not affected by Wang's later statements
  4. ≥2 ## headings
  5. [NUMERIC] pipeline independence assertion verified: pipeline log is independent of Wang's statements
  6. [NUMERIC] '王逸生' name co-located with pipeline/authorship context (within document)
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q26_coauthor_resolution.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "coauthor_resolution_strategy.md"

    if not target.exists():
        print("FAILED: analysis/coauthor_resolution_strategy.md not found")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    errors = []

    # 王逸生 present (exact Unicode name)
    if "王逸生" not in content:
        errors.append("'王逸生' not found — must name the co-author explicitly")

    # Contemporaneous / pre-complaint contrast
    if not re.search(
        r'contemporaneous|pre-complaint|before.{0,30}complaint|original.{0,20}sign|prior.{0,20}sign',
        content,
        re.IGNORECASE
    ):
        errors.append(
            "No contemporaneous/pre-complaint contrast found — "
            "document must contrast Wang's original co-signature with his post-complaint distancing"
        )

    # Pipeline independence assertion (the pipeline log is independent of Wang's statements)
    if not re.search(r'pipeline.{0,100}independent|independent.{0,100}pipeline', content, re.IGNORECASE):
        if not re.search(
            r'pipeline.{0,80}(not invalidat|still valid|exist|predates|independent|document|unaffected)',
            content,
            re.IGNORECASE
        ):
            errors.append(
                "Pipeline independence assertion not found — "
                "must state that pipeline log validity is independent of Wang's later behavior"
            )

    # ≥2 ## headings
    headings = re.findall(r'^##\s+', content, re.MULTILINE)
    if len(headings) < 2:
        errors.append(f"only {len(headings)} ## headings found (expected ≥2)")

    # 王逸生 and 'pipeline' both appear — co-location check
    if "王逸生" in content and not re.search(r'pipeline|V2\.0|log', content, re.IGNORECASE):
        errors.append(
            "'王逸生' found but no pipeline/V2.0 reference near authorship context"
        )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
