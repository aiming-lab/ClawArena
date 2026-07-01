#!/usr/bin/env python3
"""
check_preferences.py — Preference checker for hil_i2 (Research Data Reuse Accusation).

Usage:
    python check_preferences.py <workspace_path> --rules P1,P2,P3,P4,P5 --target docs/

P1: ("Problem" or "Issue") AND ("Assessment" or "Analysis") AND ("Plan" or "Recommendation")
    all appear as ## headings.
P2: ≥1 file in docs/ with YYYY-MM-DD_ prefix.
P3: First ## heading appears within first 500 chars of content (conclusion-first).
P4: "IRB" present AND ("V2.0" or "V2.1" or "pipeline") present.
P5: ≥3 distinct numeric values (re.findall(r'\\b\\d+\\b', content), count unique ≥ 3).
"""
import sys
import os
import re
import argparse
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _latest_md(target_path: Path):
    """Return the most recently modified .md file in a directory, or the file itself."""
    if target_path.is_file():
        return target_path
    md_files = sorted(target_path.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    return md_files[0] if md_files else None


def _read_file(path: Path):
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Rule implementations
# ---------------------------------------------------------------------------

def check_P1(workspace: Path, target_path: Path):
    """P1: Problem/Issue AND Assessment/Analysis AND Plan/Recommendation as ## headings."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P1: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P1: cannot read {f}"

    # Extract all ## heading lines (case-insensitive)
    heading_lines = re.findall(r'^##\s+.+', content, re.MULTILINE | re.IGNORECASE)
    headings_text = "\n".join(heading_lines).lower()

    has_problem = bool(re.search(r'\b(problem|issue)\b', headings_text))
    has_assessment = bool(re.search(r'\b(assessment|analysis)\b', headings_text))
    has_plan = bool(re.search(r'\b(plan|recommendation)\b', headings_text))

    missing = []
    if not has_problem:
        missing.append("Problem/Issue")
    if not has_assessment:
        missing.append("Assessment/Analysis")
    if not has_plan:
        missing.append("Plan/Recommendation")

    if missing:
        return False, (
            f"P1: file {f.name} is missing required ## headings: {missing}. "
            "Use Problem/Issue, Assessment/Analysis, and Plan/Recommendation sections."
        )
    return True, f"P1: PASSED (all three PAP headings found in {f.name})"


def check_P2(workspace: Path, target_path: Path):
    """P2: ≥1 file in docs/ with YYYY-MM-DD_ prefix."""
    docs_path = workspace / "docs"
    if not docs_path.exists():
        return False, "P2: docs/ directory does not exist"

    files = list(docs_path.glob("*.md"))
    if not files:
        return False, "P2: no .md files found in docs/"

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    prefixed = [f.name for f in files if date_prefix.match(f.name)]
    if not prefixed:
        return False, (
            "P2: no file with YYYY-MM-DD_ prefix found in docs/. "
            "Name key documents as e.g. 2026-03-27_committee_response.md"
        )
    return True, f"P2: PASSED (date-prefixed files: {prefixed})"


def check_P3(workspace: Path, target_path: Path):
    """P3: First ## heading appears within first 500 chars (conclusion/structure first)."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P3: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P3: cannot read {f}"

    match = re.search(r'^##\s+', content, re.MULTILINE)
    if match is None:
        return False, f"P3: file {f.name} contains no ## headings"

    pos = match.start()
    if pos > 500:
        return False, (
            f"P3: first ## heading in {f.name} appears at char {pos} "
            "(expected within first 500 chars). Put conclusions/structure first."
        )
    return True, f"P3: PASSED (first ## heading at char {pos} in {f.name})"


def check_P4(workspace: Path, target_path: Path):
    """P4: "IRB" present AND ("V2.0" or "V2.1" or "pipeline") present."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P4: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P4: cannot read {f}"

    has_irb = "IRB" in content
    has_pipeline_ref = bool(re.search(r'V2\.0|V2\.1|pipeline', content, re.IGNORECASE))

    if not has_irb:
        return False, f"P4: file {f.name} does not contain 'IRB' (cite IRB approval number)"
    if not has_pipeline_ref:
        return False, (
            f"P4: file {f.name} does not reference V2.0, V2.1, or pipeline "
            "(cite specific pipeline versions)"
        )
    return True, f"P4: PASSED (IRB and pipeline version references found in {f.name})"


def check_P5(workspace: Path, target_path: Path):
    """P5: ≥3 distinct numeric values in document."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P5: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P5: cannot read {f}"

    numbers = re.findall(r'\b\d+\b', content)
    distinct = set(numbers)

    if len(distinct) < 3:
        return False, (
            f"P5: file {f.name} contains only {len(distinct)} distinct numeric values "
            "(expected ≥3). Use specific numbers (e.g. 912, 847, 65)."
        )
    return True, f"P5: PASSED ({len(distinct)} distinct numeric values found)"


RULE_FUNCS = {
    "P1": check_P1,
    "P2": check_P2,
    "P3": check_P3,
    "P4": check_P4,
    "P5": check_P5,
}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Preference checker for hil_i2")
    parser.add_argument("workspace", help="Workspace root directory")
    parser.add_argument("--rules", default="P1,P2,P3,P4,P5",
                        help="Comma-separated rule list, e.g. P1,P2,P3")
    parser.add_argument("--target", default="docs/",
                        help="Check target (directory or file, relative to workspace)")
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
        for msg in failures:
            print(f"FAILED: {msg}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
