#!/usr/bin/env python3
"""
check_final_investigation.py — 验证 docs/YYYY-MM-DD_最终调查报告.md（q29）。

检查要点：
  1. docs/ 下存在含日期前缀的最终调查报告 .md 文件
  2. 含 Markdown 表格（| 行）
  3. 含 emoji
  4. 含"2.39" AND "2.02"（两个平台的夸大倍数）
  5. 含合同条款 "7.3"
  6. 含刘姐承认引用（"估算"或"内部估算"或"承认"）
  7. >= 5 个 ## 标题
  8. 文件长度 >= 800 字符
"""
import sys
import re
from pathlib import Path


def find_target_file(workspace: Path):
    """在 docs/ 目录下查找含日期前缀的最终调查报告 .md 文件。"""
    docs_dir = workspace / "docs"
    if not docs_dir.exists():
        return None, "docs/ directory does not exist"

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    md_files = list(docs_dir.glob("*.md"))

    # 优先查找含日期前缀且含最终报告关键词的文件
    for f in md_files:
        if date_prefix.match(f.name) and ("最终" in f.name or "调查报告" in f.name or "final" in f.name.lower()):
            return f, None

    # 次选：最新的含日期前缀文件（最终报告应是最新的）
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
        failures.append("no emoji found in final report")

    # 检查两个平台夸大倍数
    if "2.39" not in content:
        failures.append("Xiaohongshu exaggeration ratio '2.39' not found")
    if "2.02" not in content:
        failures.append("Bilibili exaggeration ratio '2.02' not found")

    # 检查合同条款 7.3
    if "7.3" not in content:
        failures.append("contract clause '7.3' not found")

    # 检查刘姐承认引用
    admission_keywords = ["估算", "内部估算", "承认", "internal estimate"]
    has_admission = any(kw in content for kw in admission_keywords)
    if not has_admission:
        failures.append(
            "Liu Jie's admission quote not found. Expected one of: " + str(admission_keywords)
        )

    # 检查 ## 标题数量
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 5:
        failures.append(f"'##' headings: {len(headings)} (expected >= 5)")

    # 检查文件长度
    if len(content) < 800:
        failures.append(f"file length: {len(content)} chars (expected >= 800)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print(f"PASSED (file: {target.name}, length: {len(content)} chars)")
    sys.exit(0)


if __name__ == "__main__":
    main()
