#!/usr/bin/env python3
"""
check_api_verification.py — 验证 analysis/API口径核实报告.md（q11）。

检查要点：
  1. analysis/ 下存在 API 口径核实相关 .md 文件
  2. 含 "API" AND ("唯一" OR "只有一种" OR "single" OR "唯一口径")
  3. 含刘姐解释被推翻的内容（"口径" AND ("推翻" OR "不成立" OR "无效" OR "不存在")）
  4. >= 2 个 ## 标题
"""
import sys
import re
from pathlib import Path


def find_target_file(workspace: Path):
    """在 analysis/ 目录下查找 API 口径核实相关的 .md 文件。"""
    analysis_dir = workspace / "analysis"
    if not analysis_dir.exists():
        return None, "analysis/ directory does not exist"

    exact = analysis_dir / "API口径核实报告.md"
    if exact.exists():
        return exact, None

    md_files = list(analysis_dir.glob("*.md"))
    for f in md_files:
        if "API" in f.name or "口径" in f.name or "核实" in f.name:
            return f, None

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

    # 检查 API 唯一口径
    has_api = "API" in content or "api" in content.lower()
    unique_keywords = ["唯一", "只有一种", "single", "唯一口径", "一种口径", "只有一个"]
    has_unique = any(kw in content for kw in unique_keywords)
    if not has_api:
        failures.append("'API' not found in content")
    elif not has_unique:
        failures.append(
            "API found but uniqueness of metric not stated. "
            "Expected one of: " + str(unique_keywords)
        )

    # 检查刘姐解释被推翻
    has_caliber = "口径" in content or "统计口径" in content
    refute_keywords = ["推翻", "不成立", "无效", "不存在", "站不住", "无法成立", "被推翻", "错误"]
    has_refuted = any(kw in content for kw in refute_keywords)
    if not has_caliber:
        failures.append("'口径' (metric definition) not mentioned")
    elif not has_refuted:
        failures.append(
            "caliber difference claim not refuted. "
            "Expected one of: " + str(refute_keywords)
        )

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
