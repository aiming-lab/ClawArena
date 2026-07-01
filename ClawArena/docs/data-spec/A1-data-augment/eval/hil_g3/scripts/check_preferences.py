#!/usr/bin/env python3
"""
check_preferences.py — hil_g3 scene preference check script.

Usage:
    python check_preferences.py <workspace_path> --rules P1,P2,P3,P4,P5 --target docs/
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
    """Return the most recently modified .md file in a directory; if target is a file, return it directly."""
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
    """P1: Structured output — count ## headings >= 3."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P1: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P1: cannot read {f}"

    heading_pattern = re.compile(r'^## .+', re.MULTILINE)
    matches = heading_pattern.findall(content)
    if len(matches) < 3:
        return False, (
            f"P1: file {f.name} has only {len(matches)} '## ' headings "
            "(expected >= 3). Use structured sections with ## headings."
        )
    return True, f"P1: PASSED (## headings count={len(matches)})"


def check_P2(workspace: Path, target_path: Path):
    """P2: At least one file in docs/ with YYYY-MM-DD_ prefix."""
    if target_path.is_file():
        files = [target_path]
    else:
        files = list(target_path.glob("*.md")) + list(target_path.glob("*.json"))

    if not files:
        return True, "P2: no files found, skip"

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    prefixed = [f.name for f in files if date_prefix.match(f.name)]
    if not prefixed:
        return False, (
            f"P2: no file with YYYY-MM-DD_ prefix found in {target_path.name}/. "
            "Main report files should be named e.g. 2026-10-03_topic.md"
        )
    return True, f"P2: PASSED (date-prefixed files: {prefixed})"


def check_P3(workspace: Path, target_path: Path):
    """P3: First ## heading contains Executive Summary / Summary / TL;DR / Executive / Finding (case-insensitive)."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P3: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P3: cannot read {f}"

    heading_pattern = re.compile(r'^## .+', re.MULTILINE)
    headings = heading_pattern.findall(content)
    if not headings:
        return False, f"P3: file {f.name} has no ## headings"

    first_heading = headings[0].lower()
    summary_keywords = ["executive summary", "summary", "tl;dr", "executive", "finding"]
    if not any(kw in first_heading for kw in summary_keywords):
        return False, (
            f"P3: first ## heading '{headings[0]}' does not contain "
            "Executive Summary / Summary / TL;DR / Executive / Finding. "
            "The executive summary or TL;DR should appear first."
        )
    return True, f"P3: PASSED (first heading: '{headings[0]}')"


def check_P4(workspace: Path, target_path: Path):
    """P4: ISO 8601 + timezone pattern present AND file size in MB mentioned."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P4: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P4: cannot read {f}"

    iso_pattern = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}')
    mb_pattern = re.compile(r'\d+\.\d+\s*MB', re.IGNORECASE)

    has_iso = bool(iso_pattern.search(content))
    has_mb = bool(mb_pattern.search(content))

    if not has_iso and not has_mb:
        return False, (
            f"P4: file {f.name} is missing both ISO 8601 timestamps with timezone "
            "and file size in MB. Include exact timestamps and file sizes."
        )
    if not has_iso:
        return False, (
            f"P4: file {f.name} is missing ISO 8601 timestamp with timezone "
            "(e.g. 2026-09-25T14:22:17+08:00)"
        )
    if not has_mb:
        return False, (
            f"P4: file {f.name} is missing file size in MB format "
            "(e.g. 2.3 MB)"
        )
    return True, "P4: PASSED (ISO 8601 timestamp and MB size both present)"


def check_P5(workspace: Path, target_path: Path):
    """P5: Professional/empathetic tone — at least one hedging/empathetic phrase present (case-insensitive)."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P5: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P5: cannot read {f}"

    empathetic_phrases = [
        "based on",
        "evidence shows",
        "regardless of",
        "objectively",
        "based on the evidence",
    ]
    content_lower = content.lower()
    found = [phrase for phrase in empathetic_phrases if phrase in content_lower]

    if not found:
        return False, (
            f"P5: file {f.name} lacks professional/empathetic hedging phrases. "
            "Include at least one of: 'based on', 'evidence shows', 'regardless of', "
            "'objectively', 'based on the evidence'."
        )
    return True, f"P5: PASSED (found phrases: {found})"


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
    parser = argparse.ArgumentParser(description="hil_g3 preference check script")
    parser.add_argument("workspace", help="workspace root directory")
    parser.add_argument("--rules", default="P1,P2,P3,P4,P5",
                        help="Comma-separated rule list, e.g. P1,P2,P3")
    parser.add_argument("--target", default="docs/",
                        help="Check target (directory or specific file, relative to workspace)")
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
