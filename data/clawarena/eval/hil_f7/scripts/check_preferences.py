#!/usr/bin/env python3
"""
check_preferences.py — hil_f7 preference check script.

Usage:
    python check_preferences.py <workspace_path> --rules P1,P2,P3,P4,P5 --target docs/
"""
import sys
import os
import re
import argparse
from pathlib import Path


# ---------------------------------------------------------------------------
# Rule implementations
# ---------------------------------------------------------------------------

def _latest_md(target_path: Path):
    """Return the most recently modified .md file in target_path; if target is a file, return it directly."""
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
    """P1: Output must use structured formats (JSON blocks, markdown tables, ## headings)."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P1: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P1: cannot read {f}"

    has_table = bool(re.search(r'^\|.+\|', content, re.MULTILINE))
    has_json_block = bool(re.search(r'```json', content, re.IGNORECASE))
    has_headings = len(re.findall(r'^#{1,3} ', content, re.MULTILINE)) >= 2

    if not (has_table or has_json_block or has_headings):
        return False, (
            f"P1: file {f.name} appears to be unstructured prose — "
            "no markdown table (|...|), no ```json block, and fewer than 2 ## headings found"
        )
    return True, f"P1: PASSED (table={has_table}, json_block={has_json_block}, headings={has_headings})"


def check_P2(workspace: Path, target_path: Path):
    """P2: At least one .md file in the target directory must have YYYY-MM-DD_ prefix."""
    if target_path.is_file():
        files = [target_path]
    else:
        files = list(target_path.glob("*.md"))

    if not files:
        return True, "P2: no .md files found, skip"

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    prefixed = [f.name for f in files if date_prefix.match(f.name)]
    if not prefixed:
        return False, (
            f"P2: no file with YYYY-MM-DD_ prefix found in {target_path.name}/. "
            "Main report files should be named e.g. 2026-06-28_topic.md"
        )
    return True, f"P2: PASSED (date-prefixed files: {prefixed})"


def check_P3(workspace: Path, target_path: Path):
    """P3: Report must present evidence before conclusions (evidence-first structure)."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P3: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P3: cannot read {f}"

    lines = content.splitlines()
    heading_lines = [(i, ln.strip()) for i, ln in enumerate(lines) if ln.strip().startswith('##')]

    evidence_keywords = re.compile(
        r'证据|evidence|事实|timeline|矛盾|contradiction|分析|analysis|数据|data|记录|record',
        re.IGNORECASE
    )
    conclusion_keywords = re.compile(
        r'结论|conclusion|建议|recommendation|总结|summary|法律|legal|主张|claim',
        re.IGNORECASE
    )

    evidence_pos = None
    conclusion_pos = None
    for idx, heading in heading_lines:
        if evidence_pos is None and evidence_keywords.search(heading):
            evidence_pos = idx
        if conclusion_keywords.search(heading):
            conclusion_pos = idx

    if conclusion_pos is not None and evidence_pos is not None and evidence_pos > conclusion_pos:
        return False, (
            f"P3: file {f.name} has conclusion section before evidence section — "
            "evidence-first structure required"
        )

    if len(heading_lines) < 2:
        return False, (
            f"P3: file {f.name} has only {len(heading_lines)} ## headings — "
            "structured sections required (evidence before conclusions)"
        )
    return True, "P3: PASSED"


def check_P4(workspace: Path, target_path: Path):
    """P4: All monetary amounts must be stated precisely to the fen level (two decimal places)."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P4: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P4: cannot read {f}"

    cny_pattern = re.compile(r'[¥￥]\s*[\d,]+')
    precise_pattern = re.compile(r'[¥￥]\s*[\d,]+\.\d{2}')

    cny_amounts = cny_pattern.findall(content)
    precise_amounts = precise_pattern.findall(content)

    if cny_amounts and not precise_amounts:
        return False, (
            f"P4: file {f.name} contains currency amounts {cny_amounts[:3]} "
            "but none are expressed to 2 decimal places (e.g., ¥72,999.00)"
        )
    return True, f"P4: PASSED (precise amounts found: {len(precise_amounts)})"


def check_P5(workspace: Path, target_path: Path):
    """P5: TL;DR section (or full file) must contain key quantitative values from this case."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P5: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P5: cannot read {f}"

    tldr_match = re.search(r'## TL;DR(.*?)(?=\n## |\Z)', content, re.DOTALL)
    section = tldr_match.group(1) if tldr_match else content

    key_numbers = {"72999", "32000", "40999", "72,999", "32,000", "40,999"}
    found_key = [k for k in key_numbers if k in section]
    total_nums = len(re.findall(r'\b\d+\b', section))

    if total_nums < 3:
        return False, (
            f"P5: TL;DR section contains only {total_nums} numeric strings "
            "(expected >= 3 quantitative values)"
        )
    if len(found_key) < 2:
        return False, (
            f"P5: expected at least 2 of the key amounts {{72999, 32000, 40999}} in TL;DR, "
            f"found only {found_key}"
        )
    return True, f"P5: PASSED (key amounts found: {found_key})"


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
    parser = argparse.ArgumentParser(description="hil_f7 preference check script")
    parser.add_argument("workspace", help="workspace root directory")
    parser.add_argument("--rules", default="P1,P2,P3,P4,P5",
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
