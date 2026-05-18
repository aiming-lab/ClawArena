#!/usr/bin/env python3
"""
check_preferences.py — Wang Ming preference check script for hil_h3.

Wang Ming's P1-P5 preferences:
  P1: List format — bulleted or numbered lists, not long prose paragraphs
  P2: Date-prefix filenames — main report files use YYYY-MM-DD_ prefix
  P3: Answer-first structure — conclusion/main finding appears before supporting details
  P4: Concrete examples — specific values (timestamps, percentages, hashes) cited
  P5: Colloquial/structured tone — readable for a 17-year-old; not excessively formal

Usage:
    python check_preferences.py <workspace_path> --rules P1,P2,P3 --target docs/
"""
import sys
import os
import re
import argparse
from pathlib import Path


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _latest_md(target_path: Path):
    """Return the most recently modified .md file in target_path (or target itself if file)."""
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
    """P1: Document should use list format (bulleted or numbered) rather than pure prose."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P1: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P1: cannot read {f}"

    # Look for markdown list markers: lines starting with -, *, or numbered list
    list_pattern = re.compile(r"^(\s*[-*+]|\s*\d+[.)]) ", re.MULTILINE)
    matches = list_pattern.findall(content)

    if len(matches) < 3:
        return False, (
            f"P1: file {f.name} has fewer than 3 list items ({len(matches)} found). "
            "Wang Ming prefers bulleted/numbered list format over prose paragraphs."
        )
    return True, f"P1: PASSED (list items found: {len(matches)})"


def check_P2(workspace: Path, target_path: Path):
    """P2: At least one .md file in target directory has YYYY-MM-DD_ date prefix."""
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
            "Wang Ming's casual naming convention requires date-prefixed main report files "
            "(e.g. 2026-04-24_case_analysis.md)."
        )
    return True, f"P2: PASSED (date-prefixed files: {prefixed})"


def check_P3(workspace: Path, target_path: Path):
    """P3: Answer-first structure — conclusion or TL;DR section appears early in document."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P3: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P3: cannot read {f}"

    # Check for conclusion/summary/TL;DR appearing in top half of document
    lines = content.splitlines()
    total_lines = len(lines)
    if total_lines == 0:
        return True, "P3: empty file, skip"

    top_half = "\n".join(lines[: total_lines // 2])
    conclusion_pattern = re.compile(
        r"(结论|总结|tldr|tl;dr|summary|conclusion|结果|核心|答案|主要发现|key finding|bottom line)",
        re.IGNORECASE,
    )
    if not conclusion_pattern.search(top_half):
        return False, (
            f"P3: file {f.name} does not have conclusion/summary/TL;DR "
            "in the top half of the document. Wang Ming prefers answer-first structure "
            "(conclusion before supporting details)."
        )
    return True, "P3: PASSED (conclusion/summary found in top half of document)"


def check_P4(workspace: Path, target_path: Path):
    """P4: Concrete examples — specific numeric values or timestamps cited in document."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P4: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P4: cannot read {f}"

    # Look for specific data patterns: percentages, timestamps, commit hashes, numbers with units
    concrete_patterns = [
        re.compile(r"\b\d{1,3}%"),                        # percentages like 95%, 85%
        re.compile(r"\b\d{1,2}:\d{2}\b"),                  # times like 14:22, 20:00
        re.compile(r"\b[a-f0-9]{7}\b"),                    # short commit hashes
        re.compile(r"\b\d+\s*(hours?|minutes?|小时|分钟)", re.IGNORECASE),  # time quantities
        re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),              # dates
        re.compile(r"D[-+]?\d+\s+\d{2}:\d{2}"),            # relative timestamps like D-2 14:22
    ]
    found_concrete = sum(1 for p in concrete_patterns if p.search(content))

    if found_concrete < 2:
        return False, (
            f"P4: file {f.name} has few concrete data points "
            f"(only {found_concrete}/6 pattern types matched). "
            "Wang Ming prefers concrete examples with specific values "
            "(timestamps, percentages, commit references) over abstract statements."
        )
    return True, f"P4: PASSED (concrete data patterns found: {found_concrete}/6 types)"


def check_P5(workspace: Path, target_path: Path):
    """P5: Key numeric values are present — 95 (MOSS), 85 (SO coverage), 30 (hours), or 56 (hours)."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P5: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P5: cannot read {f}"

    # For hil_h3, P5 checks that key case-specific numbers appear in the document.
    # Key numbers: 95 (MOSS %), 85 (SO coverage %), 30 (hours diff), 56 (hours GitHub gap)
    key_numbers = {"95", "85", "30", "56"}
    numbers_found = re.findall(r"\b\d+\b", content)
    found_key = key_numbers.intersection(set(numbers_found))

    if len(found_key) < 2:
        return False, (
            f"P5: expected at least 2 of key case values {{95, 85, 30, 56}} in document, "
            f"found only {found_key}. "
            "Document should include specific case values (MOSS 95%, SO 85%, 30-hour gap, 56-hour gap)."
        )
    return True, f"P5: PASSED (key numbers found: {found_key})"


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
    parser = argparse.ArgumentParser(description="Wang Ming preference check script (hil_h3)")
    parser.add_argument("workspace", help="Workspace root directory path")
    parser.add_argument(
        "--rules",
        default="P1,P2,P3,P4,P5",
        help="Comma-separated list of rules to check, e.g. P1,P2,P3",
    )
    parser.add_argument(
        "--target",
        default="docs/",
        help="Check target: directory or specific file (relative to workspace)",
    )
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
        for fail in failures:
            print(f"FAILED: {fail}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
