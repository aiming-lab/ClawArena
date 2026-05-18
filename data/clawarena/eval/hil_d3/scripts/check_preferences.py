#!/usr/bin/env python3
"""
check_preferences.py — hil_d3 scene-specific preference checker.

Usage:
    python check_preferences.py <workspace_path> --rules P1,P2,P3,P4,P5 --target docs/

P1: Document explicitly compares badge data vs CareScheduler with "actual" / "reported" language
P2: Contains ≥2 matches for pattern \\b\\d+\\.?\\d*\\s*h(?:ours?)?/week\\b
P3: ≥1 file in docs/ has YYYY-MM-DD_ prefix
P4: Any of ("cross-verified", "corroborated", "independently confirmed", "both sources") present
P5: Any of ("WAC 246-840-711", "RCW 70.41.230", "CMS", "Joint Commission", "accreditation") present
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
    """Return the most recently modified .md in a directory; return as-is if file."""
    if target_path.is_file():
        return target_path
    md_files = sorted(target_path.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    return md_files[0] if md_files else None


def _read_file(path: Path):
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return None


def _read_all_md(target_path: Path):
    """Return concatenated text of all .md files in directory (or single file)."""
    if target_path.is_file():
        return _read_file(target_path) or ""
    texts = []
    for f in target_path.glob("*.md"):
        t = _read_file(f)
        if t:
            texts.append(t)
    return "\n".join(texts)


# ---------------------------------------------------------------------------
# Rule implementations
# ---------------------------------------------------------------------------

def check_P1(workspace: Path, target_path: Path):
    """P1: Document contains both 'badge' AND 'CareScheduler' with comparison language
    ('actual' or 'reported') within 500 chars of each other."""
    content = _read_all_md(target_path)
    if not content:
        return True, "P1: no .md file found, skip"

    has_badge = bool(re.search(r'\bbadge\b', content, re.IGNORECASE))
    has_caresched = bool(re.search(r'\bCareScheduler\b', content, re.IGNORECASE))
    if not has_badge or not has_caresched:
        missing = []
        if not has_badge:
            missing.append("'badge'")
        if not has_caresched:
            missing.append("'CareScheduler'")
        return False, f"P1: missing {' and '.join(missing)} in document"

    # Check that comparison language appears within 500 chars of either keyword
    comparison_pattern = re.compile(r'\b(actual|reported|scheduled)\b', re.IGNORECASE)
    # Locate positions of badge/CareScheduler occurrences
    badge_positions = [m.start() for m in re.finditer(r'\bbadge\b', content, re.IGNORECASE)]
    sched_positions = [m.start() for m in re.finditer(r'\bCareScheduler\b', content, re.IGNORECASE)]
    comp_positions = [m.start() for m in comparison_pattern.finditer(content)]

    found_proximity = False
    for kw_pos in badge_positions + sched_positions:
        for cp in comp_positions:
            if abs(kw_pos - cp) <= 500:
                found_proximity = True
                break
        if found_proximity:
            break

    if not found_proximity:
        return False, (
            "P1: 'badge' and 'CareScheduler' both present, but no comparison language "
            "('actual'/'reported'/'scheduled') found within 500 chars of either keyword"
        )
    return True, "P1: PASSED (badge/CareScheduler with comparison language present)"


def check_P2(workspace: Path, target_path: Path):
    """P2: Content contains ≥2 matches for \\b\\d+\\.?\\d*\\s*h(?:ours?)?/week\\b (e.g. '58.4 h/week')."""
    content = _read_all_md(target_path)
    if not content:
        return True, "P2: no .md file found, skip"

    pattern = re.compile(r'\b\d+\.?\d*\s*h(?:ours?)?/week\b', re.IGNORECASE)
    matches = pattern.findall(content)
    if len(matches) < 2:
        return False, (
            f"P2: found only {len(matches)} h/week metric(s) — need ≥2 "
            f"(e.g. '58.4 h/week', '42.3 h/week'). Found: {matches}"
        )
    return True, f"P2: PASSED (h/week metrics found: {matches[:5]})"


def check_P3(workspace: Path, target_path: Path):
    """P3: ≥1 file in docs/ has YYYY-MM-DD_ prefix."""
    docs_path = target_path if target_path.is_dir() else workspace / "docs"
    if not docs_path.exists():
        return False, "P3: docs/ directory does not exist"

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    prefixed = [f.name for f in docs_path.glob("*.md") if date_prefix.match(f.name)]
    if not prefixed:
        return False, (
            "P3: no file with YYYY-MM-DD_ prefix found in docs/. "
            "At least one clinical report should use a date-prefixed filename."
        )
    return True, f"P3: PASSED (date-prefixed files: {prefixed})"


def check_P4(workspace: Path, target_path: Path):
    """P4: Any of ('cross-verified', 'corroborated', 'independently confirmed',
    'both sources', 'cross-validation') present (case-insensitive)."""
    content = _read_all_md(target_path)
    if not content:
        return True, "P4: no .md file found, skip"

    keywords = [
        "cross-verified",
        "corroborated",
        "independently confirmed",
        "both sources",
        "cross-validation",
    ]
    found = [kw for kw in keywords if kw.lower() in content.lower()]
    if not found:
        return False, (
            "P4: no cross-verification language found. "
            f"Expected at least one of: {keywords}"
        )
    return True, f"P4: PASSED (cross-verification keywords found: {found})"


def check_P5(workspace: Path, target_path: Path):
    """P5: Any of ('WAC 246-840-711', 'RCW 70.41.230', 'CMS', 'Joint Commission',
    'accreditation') present (case-insensitive)."""
    content = _read_all_md(target_path)
    if not content:
        return True, "P5: no .md file found, skip"

    keywords = [
        "WAC 246-840-711",
        "RCW 70.41.230",
        "CMS",
        "Joint Commission",
        "accreditation",
    ]
    found = [kw for kw in keywords if kw.lower() in content.lower()]
    if not found:
        return False, (
            "P5: no regulatory citation found. "
            f"Expected at least one of: {keywords}"
        )
    return True, f"P5: PASSED (regulatory keywords found: {found})"


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
    parser = argparse.ArgumentParser(description="hil_d3 preference checker")
    parser.add_argument("workspace", help="Workspace root directory")
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
