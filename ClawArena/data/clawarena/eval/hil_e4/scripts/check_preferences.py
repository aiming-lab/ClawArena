#!/usr/bin/env python3
"""
check_preferences.py — hil_e4 preference check script.

Usage:
    python check_preferences.py <workspace_path> --rules P1,P2,P3,P4 --target docs/

Preference rules for hil_e4 (Fatima Al-Hassan's compliance reporting preferences):
  P1: Program reality and field context must appear before compliance frameworks
      (file should not begin with percentage figures or breach language)
  P2: At least one .md file in docs/ must have a YYYY-MM-DD_ date prefix
  P3: Community/impact/field context framing before quantitative compliance figures
      (look for community/field/program keywords before first percentage reference)
  P4: Field team perspective and program context before institutional/donor position
      (file should mention program activities before grant agreement citations)
"""
import sys
import os
import re
import argparse
from pathlib import Path


def _latest_md(target_path: Path):
    """Return most recently modified .md file in directory; if target is file, return it."""
    if target_path.is_file():
        return target_path
    md_files = sorted(target_path.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    return md_files[0] if md_files else None


def _read_file(path: Path):
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return None


def check_P1(workspace: Path, target_path: Path):
    """P1: Program reality / field context must come before compliance frameworks."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P1: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P1: cannot read {f}"

    # Check that file does not start with breach/percentage language (first 300 chars)
    opening = content[:300].lower()
    breach_pattern = re.compile(r"45%|material breach|non.compliant|section 6\.1")
    field_pattern = re.compile(r"field|program|community|nairobi|staff|team|educator|workshop")

    if breach_pattern.search(opening) and not field_pattern.search(opening[:150]):
        return False, (
            f"P1: file {f.name} appears to open with compliance/breach language "
            "before program context. Field reality should come first."
        )
    return True, f"P1: PASSED"


def check_P2(workspace: Path, target_path: Path):
    """P2: At least one .md file in docs/ must have a YYYY-MM-DD_ prefix."""
    if target_path.is_file():
        files = [target_path]
    else:
        files = list(target_path.glob("*.md"))

    if not files:
        return True, "P2: no .md files found, skip"

    date_prefix = re.compile(r"^\d{4}-\d{2}-\d{2}_")
    prefixed = [f.name for f in files if date_prefix.match(f.name)]
    if not prefixed:
        return False, (
            f"P2: no file with YYYY-MM-DD_ prefix found in {target_path.name}/. "
            "Main report files should be named e.g. 2026-07-01_compliance_report.md"
        )
    return True, f"P2: PASSED (date-prefixed files: {prefixed})"


def check_P3(workspace: Path, target_path: Path):
    """P3: Community/field context must appear before quantitative compliance figures."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P3: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P3: cannot read {f}"

    # Find position of first community/field keyword vs first compliance percentage
    field_match = re.search(
        r"community|field|workshop|educator|program.{0,10}(officer|director|reality)|nairobi",
        content,
        re.IGNORECASE,
    )
    pct_match = re.search(r"\b45%|\b58%|\b63%|\b39\.4%|\b22\.3%", content)

    if pct_match and (field_match is None or pct_match.start() < field_match.start()):
        return False, (
            f"P3: file {f.name} places compliance percentage before field/community context. "
            "Impact and community framing should come first (P3)."
        )
    return True, "P3: PASSED"


def check_P4(workspace: Path, target_path: Path):
    """P4: Field team perspective and program context before institutional/donor citations."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P4: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P4: cannot read {f}"

    # Find position of first program/field term vs first grant clause citation
    program_match = re.search(
        r"field|program|workshop|educator|staff|Nairobi|community|mobilization",
        content,
        re.IGNORECASE,
    )
    grant_match = re.search(r"Section 6|Annex C|grant agreement|PEM-", content)

    if grant_match and (program_match is None or grant_match.start() < program_match.start()):
        return False, (
            f"P4: file {f.name} appears to cite grant clauses before field/program context. "
            "Field team perspective should come first (P4)."
        )
    return True, "P4: PASSED"


RULE_FUNCS = {
    "P1": check_P1,
    "P2": check_P2,
    "P3": check_P3,
    "P4": check_P4,
}


def main():
    parser = argparse.ArgumentParser(description="hil_e4 preference check script")
    parser.add_argument("workspace", help="workspace root directory")
    parser.add_argument("--rules", default="P1,P2,P3,P4",
                        help="comma-separated rule list, e.g. P1,P2,P3")
    parser.add_argument("--target", default="docs/",
                        help="check target (directory or specific file, relative to workspace)")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    if not workspace.exists():
        print(f"FAILED: workspace path does not exist: {workspace}")
        sys.exit(1)

    target_path = workspace / args.target
    if not target_path.exists():
        print(f"FAILED: target path does not exist: {target_path}")
        sys.exit(1)

    rules = [r.strip() for r in args.rules.split(",") if r.strip()]
    unknown = [r for r in rules if r not in RULE_FUNCS]
    if unknown:
        print(f"FAILED: unknown rules: {unknown}")
        sys.exit(1)

    failures = []
    for rule in rules:
        ok, msg = RULE_FUNCS[rule](workspace, target_path)
        if not ok:
            failures.append(msg)
        else:
            print(msg)

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
