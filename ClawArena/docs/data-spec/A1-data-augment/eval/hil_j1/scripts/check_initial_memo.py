#!/usr/bin/env python3
"""
check_initial_memo.py — 验证 docs/YYYY-MM-DD_初步调查备忘录.md（q9）。

检查要点：
  1. docs/ 下存在含日期前缀的 .md 文件（YYYY-MM-DD_ 格式）
  2. 含官方播放量 "50,234" 或 "50234"
  3. 含合同条款 "7.3"
  4. 含结论段（含"结论"或"总结"或"发现"或"判断"）
  5. >= 4 个 ## 标题
"""
import sys
import re
from pathlib import Path


def find_target_file(workspace: Path):
    """在 docs/ 目录下查找日期前缀的备忘录 .md 文件。"""
    docs_dir = workspace / "docs"
    if not docs_dir.exists():
        return None, "docs/ directory does not exist"

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    md_files = list(docs_dir.glob("*.md"))

    # 优先查找含日期前缀且含备忘录关键词的文件
    for f in md_files:
        if date_prefix.match(f.name) and ("备忘录" in f.name or "初步" in f.name or "memo" in f.name.lower()):
            return f, None

    # 次选：任意含日期前缀的文件
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

    # 检查官方播放量
    if "50,234" not in content and "50234" not in content:
        failures.append("official Xiaohongshu plays '50,234' / '50234' not found")

    # 检查合同条款 7.3
    if "7.3" not in content:
        failures.append("contract clause '7.3' not found")

    # 检查结论段
    conclusion_keywords = ["结论", "总结", "发现", "判断", "概况", "初步判断"]
    if not any(kw in content for kw in conclusion_keywords):
        failures.append(
            "conclusion section not found. Expected one of: " + str(conclusion_keywords)
        )

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
