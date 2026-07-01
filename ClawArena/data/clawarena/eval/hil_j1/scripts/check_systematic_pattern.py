#!/usr/bin/env python3
"""
check_systematic_pattern.py — 验证 analysis/系统性模式证据.md（q25）。

检查要点：
  1. analysis/ 下存在系统性模式证据相关 .md 文件
  2. 含"周芳" AND "2.39"
  3. 含"小林" AND "2.33"
  4. 含"系统性"或"模式"或"非偶然"（说明系统性操作特征）
  5. >= 2 个 ## 标题
"""
import sys
import re
from pathlib import Path


def find_target_file(workspace: Path):
    """在 analysis/ 目录下查找系统性模式证据相关的 .md 文件。"""
    analysis_dir = workspace / "analysis"
    if not analysis_dir.exists():
        return None, "analysis/ directory does not exist"

    exact = analysis_dir / "系统性模式证据.md"
    if exact.exists():
        return exact, None

    md_files = list(analysis_dir.glob("*.md"))
    for f in md_files:
        if "系统性" in f.name or "模式" in f.name or "小林" in f.name:
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

    # 检查周芳 + 2.39
    has_zhouchao = "周芳" in content
    has_239 = "2.39" in content
    if not has_zhouchao:
        failures.append("'周芳' not found in content")
    if not has_239:
        failures.append("'2.39' (Zhou Fang exaggeration ratio) not found")

    # 检查小林 + 2.33
    has_xiaolin = "小林" in content
    has_233 = "2.33" in content
    if not has_xiaolin:
        failures.append("'小林' not found in content")
    if not has_233:
        failures.append("'2.33' (Xiaolin exaggeration ratio) not found")

    # 检查系统性/模式关键词
    pattern_keywords = ["系统性", "模式", "非偶然", "规律", "系统化", "普遍", "系统"]
    has_pattern = any(kw in content for kw in pattern_keywords)
    if not has_pattern:
        failures.append(
            "systematic pattern keywords not found. Expected one of: " + str(pattern_keywords)
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
