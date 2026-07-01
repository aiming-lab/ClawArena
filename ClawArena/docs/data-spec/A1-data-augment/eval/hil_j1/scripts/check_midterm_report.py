#!/usr/bin/env python3
"""
check_midterm_report.py — 验证 docs/YYYY-MM-DD_调查中期报告.md（q21）。

检查要点：
  1. docs/ 下存在含日期前缀的中期报告 .md 文件
  2. 含 Markdown 表格（| 行）
  3. 含 emoji
  4. 含 "50,234" 或 "50234"（官方播放量）
  5. 含 "2.39"（夸大倍数）
  6. 含 "7.3"（合同条款）
  7. >= 4 个 ## 标题
"""
import sys
import re
from pathlib import Path


def find_target_file(workspace: Path):
    """在 docs/ 目录下查找含日期前缀的中期报告 .md 文件。"""
    docs_dir = workspace / "docs"
    if not docs_dir.exists():
        return None, "docs/ directory does not exist"

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    md_files = list(docs_dir.glob("*.md"))

    # 优先查找含日期前缀且含中期报告关键词的文件
    for f in md_files:
        if date_prefix.match(f.name) and ("中期" in f.name or "调查" in f.name):
            return f, None

    # 次选：最新的含日期前缀文件
    date_files = [f for f in md_files if date_prefix.match(f.name)]
    if date_files:
        latest = sorted(date_files, key=lambda p: p.stat().st_mtime, reverse=True)[0]
        return latest, None

    return None, "no date-prefixed .md file found in docs/"


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target, err = find_target_file(workspace)

    if target is None:
        print(f"FAILED: {err}")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8").strip()
    except Exception as e:
        print(f"FAILED: cannot read file {target}: {e}")
        sys.exit(1)

    if not content:
        print(f"FAILED: file is empty: {target}")
        sys.exit(1)

    failures = []

    # 检查 Markdown 表格
    table_lines = [ln for ln in content.splitlines() if '|' in ln]
    if len(table_lines) < 3:
        failures.append(f"table rows with '|': {len(table_lines)} (expected >= 3)")

    # 检查 emoji
    emoji_range = re.search(r'[\U0001F300-\U0001FFFF]', content)
    common_emoji = re.search(r'[🔴🟢⚠️✅❌💡📊🔶🔷⭐🚨📌📝🔍]', content)
    if not (emoji_range or common_emoji):
        failures.append("no emoji found")

    # 检查官方播放量
    if "50,234" not in content and "50234" not in content:
        failures.append("official plays '50,234' / '50234' not found")

    # 检查夸大倍数
    if "2.39" not in content:
        failures.append("exaggeration ratio '2.39' not found")

    # 检查合同条款 7.3
    if "7.3" not in content:
        failures.append("contract clause '7.3' not found")

    # 检查 ## 标题数量
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 4:
        failures.append(f"'##' headings: {len(headings)} (expected >= 4)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print(f"PASSED (file: {target.name})")
    sys.exit(0)


if __name__ == "__main__":
    main()
