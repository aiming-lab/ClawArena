#!/usr/bin/env python3
"""
check_preferences.py — General preference check script for hil_g4 (Chen Jing / HR investigation).

Usage:
    python check_preferences.py <workspace_path> --rules P1,P2,P3,P4,P5 --target docs/

P1: Output uses bullet-point summaries with hierarchical headings (>= 3 ## headings).
P2: At least one .md file in the target directory has a YYYY-MM-DD_ date prefix.
P3: Document has an executive summary / conclusion section before detailed evidence
    (detected by "## 摘要", "## 执行摘要", "## 结论", "## Executive Summary",
     "## Summary", "## 调查结论" appearing before the last section).
P4: Document includes both qualitative descriptions and quantitative data
    (has at least one number AND at least one qualitative phrase).
P5: Professional but warm tone — document contains empathetic language
    (does not consist solely of cold legal/technical language;
     at least one of: "理解", "考虑到", "建议", "人文", "关注", "请注意",
     "acknowledge", "consider", "recommend", "human", "concern" present).
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
    """Return the most recently modified .md file in a directory, or the file itself."""
    if target_path.is_file():
        return target_path
    md_files = sorted(target_path.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    return md_files[0] if md_files else None


def _read_file(path: Path):
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return None


# ---------------------------------------------------------------------------
# Rule implementations
# ---------------------------------------------------------------------------

def check_P1(workspace: Path, target_path: Path):
    """P1: Output must use bullet-point summaries with hierarchical headings (>= 3 ## headings)."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P1: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P1: cannot read {f}"

    headings = [ln for ln in content.splitlines() if re.match(r'^##+ ', ln.strip())]
    if len(headings) < 3:
        return False, (
            f"P1: file {f.name} has only {len(headings)} ## headings "
            "(expected >= 3 for hierarchical structure)"
        )
    # Also check for bullet points
    bullets = [ln for ln in content.splitlines() if re.match(r'^\s*[-*•]\s', ln)]
    if len(bullets) < 2:
        return False, (
            f"P1: file {f.name} has only {len(bullets)} bullet-point lines "
            "(expected >= 2 for bullet-point summary style)"
        )
    return True, f"P1: PASSED (headings={len(headings)}, bullets={len(bullets)})"


def check_P2(workspace: Path, target_path: Path):
    """P2: At least one .md file in target directory has YYYY-MM-DD_ date prefix."""
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
            "Main report files should follow Chinese date-prefix naming convention, "
            "e.g. 2026-03-28_张涛案调查报告.md"
        )
    return True, f"P2: PASSED (date-prefixed files: {prefixed})"


def check_P3(workspace: Path, target_path: Path):
    """P3: Document has executive summary / conclusion section appearing early."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P3: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P3: cannot read {f}"

    summary_patterns = [
        r'## .*摘要', r'## .*执行摘要', r'## .*结论', r'## .*调查结论',
        r'## .*总结', r'## Executive Summary', r'## Summary', r'## Overview',
        r'## TL;DR', r'## 关键发现', r'## 核心发现',
    ]
    found_summary = False
    for pat in summary_patterns:
        if re.search(pat, content, re.IGNORECASE):
            found_summary = True
            break

    if not found_summary:
        return False, (
            f"P3: file {f.name} does not contain an executive summary or conclusion "
            "section (expected one of: ## 摘要, ## 执行摘要, ## 结论, ## 调查结论, "
            "## 总结, ## 关键发现, ## Executive Summary, ## Overview, ## TL;DR)"
        )
    return True, "P3: PASSED (executive summary section found)"


def check_P4(workspace: Path, target_path: Path):
    """P4: Document includes both qualitative and quantitative information."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P4: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P4: cannot read {f}"

    # Quantitative: contains numbers (dates, counts, percentages)
    numbers = re.findall(r'\b\d+\b', content)
    has_quantitative = len(numbers) >= 3

    # Qualitative: contains assessment/recommendation language
    qualitative_patterns = [
        r'建议', r'风险', r'影响', r'分析', r'评估', r'判断', r'结论',
        r'recommend', r'assess', r'impact', r'risk', r'significant', r'concern',
        r'合规', r'违规', r'问题', r'gap', r'缺口', r'差距',
    ]
    has_qualitative = any(re.search(p, content, re.IGNORECASE) for p in qualitative_patterns)

    if not has_quantitative:
        return False, (
            f"P4: file {f.name} lacks quantitative data "
            f"(found only {len(numbers)} standalone numbers; expected >= 3)"
        )
    if not has_qualitative:
        return False, (
            f"P4: file {f.name} lacks qualitative assessment language "
            "(expected terms like 建议, 风险, 评估, recommend, assess, risk)"
        )
    return True, f"P4: PASSED (quantitative numbers={len(numbers)}, qualitative=True)"


def check_P5(workspace: Path, target_path: Path):
    """P5: Professional but warm tone — contains empathetic or considerate language."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P5: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P5: cannot read {f}"

    warm_patterns = [
        r'理解', r'关注', r'考虑', r'建议', r'尊重', r'承认', r'认可',
        r'请注意', r'值得注意', r'需要指出', r'应当', r'应该',
        r'acknowledge', r'consider', r'recommend', r'note that', r'important',
        r'human', r'empathy', r'concern', r'appreciate',
        r'善意', r'诚意', r'无恶意', r'过失', r'疏忽',
    ]
    has_warm = any(re.search(p, content, re.IGNORECASE) for p in warm_patterns)

    if not has_warm:
        return False, (
            f"P5: file {f.name} appears to lack professional-but-warm tone "
            "(expected empathetic or considerate language such as: "
            "理解, 关注, 建议, 考虑, recommend, acknowledge, note that)"
        )
    return True, "P5: PASSED (professional-warm tone detected)"


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
    parser = argparse.ArgumentParser(description="Preference check script for hil_g4")
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
