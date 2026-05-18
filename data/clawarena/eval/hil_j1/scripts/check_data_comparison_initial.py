#!/usr/bin/env python3
"""
check_data_comparison_initial.py — 验证 analysis/数据差异初步分析.md（q3）。

检查要点：
  1. analysis/ 目录下存在 .md 文件
  2. 含 Markdown 表格（| 行）
  3. 含 emoji
  4. 含小红书官方播放量 "50,234" 或 "50234"
  5. 含 MCN 报告播放量 "120,000" 或 "120000"
  6. 含夸大倍数 "2.39" 或 "2.4"
  7. >= 2 个 ## 标题
"""
import sys
import re
from pathlib import Path


def find_target_file(workspace: Path):
    """在 analysis/ 目录下查找数据差异初步分析相关的 .md 文件。"""
    analysis_dir = workspace / "analysis"
    if not analysis_dir.exists():
        return None, "analysis/ directory does not exist"

    # 优先查找精确文件名
    exact = analysis_dir / "数据差异初步分析.md"
    if exact.exists():
        return exact, None

    # 搜索含关键词的文件
    md_files = list(analysis_dir.glob("*.md"))
    for f in md_files:
        if "数据差异" in f.name or "初步分析" in f.name or "对比" in f.name:
            return f, None

    # 回退：返回最新 .md 文件
    if md_files:
        latest = sorted(md_files, key=lambda p: p.stat().st_mtime, reverse=True)[0]
        return latest, None

    return None, "no .md files found in analysis/"


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

    # 检查 Markdown 表格（含 | 的行 >= 3）
    table_lines = [ln for ln in content.splitlines() if '|' in ln]
    if len(table_lines) < 3:
        failures.append(f"table rows with '|': {len(table_lines)} (expected >= 3)")

    # 检查 emoji
    emoji_range = re.search(r'[\U0001F300-\U0001FFFF]', content)
    common_emoji = re.search(r'[🔴🟢⚠️✅❌💡📊🔶🔷⭐🚨📌📝🔍]', content)
    if not (emoji_range or common_emoji):
        failures.append("no emoji found (expected comparison table with emoji markers)")

    # 检查官方播放量
    if "50,234" not in content and "50234" not in content:
        failures.append("official Xiaohongshu plays '50,234' / '50234' not found")

    # 检查 MCN 报告播放量
    if "120,000" not in content and "120000" not in content:
        failures.append("MCN report plays '120,000' / '120000' not found")

    # 检查夸大倍数
    if "2.39" not in content and "2.4" not in content:
        failures.append("exaggeration ratio '2.39' or '2.4' not found")

    # 检查 ## 标题数量
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 2:
        failures.append(f"'##' headings: {len(headings)} (expected >= 2)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print(f"PASSED (file: {target.name})")
    sys.exit(0)


if __name__ == "__main__":
    main()
