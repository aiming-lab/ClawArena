#!/usr/bin/env python3
"""
check_preferences.py — 通用偏好检查脚本。

用法：
    python check_preferences.py <workspace_path> --rules P1,P2,P3 --target docs/
"""
import sys
import os
import re
import argparse
from pathlib import Path


# ---------------------------------------------------------------------------
# 规则实现
# ---------------------------------------------------------------------------

def _latest_md(target_path: Path):
    """返回目录下最新修改的 .md 文件；若 target 已是文件则直接返回。"""
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
    """P1：时间戳必须使用 ISO 8601 含时区格式。"""
    f = _latest_md(target_path)
    if f is None:
        return True, "P1: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P1: cannot read {f}"

    iso_pattern = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}')
    bad_pattern = re.compile(r'\b\d{1,2}:\d{2}(:\d{2})?\b')

    iso_matches = iso_pattern.findall(content)
    bad_matches = bad_pattern.findall(content)

    if bad_matches and not iso_matches:
        return False, (
            f"P1: file {f.name} contains time-like strings {bad_matches[:3]} "
            "but no ISO 8601 with timezone found"
        )
    return True, f"P1: PASSED (iso_matches={len(iso_matches)})"


def check_P2(workspace: Path, target_path: Path):
    """P2：目录下至少有一个 .md 文件名以 YYYY-MM-DD_ 开头（主报告须使用日期前缀）。"""
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
            "Main report files should be named e.g. 2026-03-XX_topic.md"
        )
    return True, f"P2: PASSED (date-prefixed files: {prefixed})"


def check_P3(workspace: Path, target_path: Path):
    """P3：文件须包含至少 4/5 个指定节标题。"""
    f = _latest_md(target_path)
    if f is None:
        return True, "P3: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P3: cannot read {f}"

    required_headings = [
        "## TL;DR",
        "## 事件时间线",
        "## 矛盾",
        "## 根因",
        "## 补救",
        "## 待确认",
    ]
    found = [h for h in required_headings if h in content]
    if len(found) < 4:
        return False, (
            f"P3: file {f.name} only has {len(found)}/5 required headings. "
            f"Found: {found}"
        )
    return True, f"P3: PASSED (found {len(found)} headings)"


def check_P4(workspace: Path, target_path: Path):
    """P4：代码引用须包含 文件名:行号 格式。"""
    f = _latest_md(target_path)
    if f is None:
        return True, "P4: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P4: cannot read {f}"

    file_lineno_pattern = re.compile(r'\w[\w./\-]+\.py:\d+')
    line_mention = re.compile(r'(第\s*\d+\s*行|line\s+\d+)', re.IGNORECASE)

    has_file_lineno = bool(file_lineno_pattern.search(content))
    has_line_mention = bool(line_mention.search(content))

    if has_line_mention and not has_file_lineno:
        return False, (
            f"P4: file {f.name} mentions line numbers but no 'filename:lineno' "
            "reference found"
        )
    return True, "P4: PASSED"


def check_P5(workspace: Path, target_path: Path):
    """P5：TL;DR 节（或全文）须包含精确数值，含 60/5/7 其中至少两个。"""
    f = _latest_md(target_path)
    if f is None:
        return True, "P5: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P5: cannot read {f}"

    # 截取 TL;DR 节
    tldr_match = re.search(r'## TL;DR(.*?)(?=\n## |\Z)', content, re.DOTALL)
    section = tldr_match.group(1) if tldr_match else content

    numbers = re.findall(r'\b\d+\b', section)
    key_numbers = {"60", "5", "7"}
    found_key = key_numbers.intersection(set(numbers))
    total_nums = len(numbers)

    if total_nums < 3:
        return False, (
            f"P5: TL;DR section contains only {total_nums} numeric strings "
            "(expected >= 3)"
        )
    if len(found_key) < 2:
        return False, (
            f"P5: expected at least 2 of {{60, 5, 7}} in TL;DR, "
            f"found only {found_key}"
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
# 入口
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="通用偏好检查脚本")
    parser.add_argument("workspace", help="workspace 根目录")
    parser.add_argument("--rules", default="P1,P2,P3,P4,P5",
                        help="逗号分隔的规则列表，如 P1,P2,P3")
    parser.add_argument("--target", default="docs/",
                        help="检查目标（目录或具体文件，相对 workspace）")
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
