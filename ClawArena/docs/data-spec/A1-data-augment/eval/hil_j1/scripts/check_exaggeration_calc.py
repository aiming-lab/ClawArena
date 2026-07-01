#!/usr/bin/env python3
"""
check_exaggeration_calc.py — 验证 analysis/夸大倍数计算.md（q4）。

检查要点：
  1. analysis/ 下存在夸大倍数计算相关 .md 文件
  2. 含小红书播放夸大倍数 "2.39" 或 "2.4"
  3. 含 B 站播放夸大倍数 "2.02"
  4. 含小红书官方点赞 "3,812" 或 "3812"
  5. 含 MCN 报告点赞 "8,500" 或 "8500"
  6. >= 3 个数值对比行（含 vs 或 ÷ 或 / 且有数字的行）
"""
import sys
import re
from pathlib import Path


def find_target_file(workspace: Path):
    """在 analysis/ 目录下查找夸大倍数计算相关的 .md 文件。"""
    analysis_dir = workspace / "analysis"
    if not analysis_dir.exists():
        return None, "analysis/ directory does not exist"

    exact = analysis_dir / "夸大倍数计算.md"
    if exact.exists():
        return exact, None

    md_files = list(analysis_dir.glob("*.md"))
    for f in md_files:
        if "夸大" in f.name or "倍数" in f.name or "计算" in f.name:
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

    # 检查小红书播放夸大倍数
    if "2.39" not in content and "2.4" not in content:
        failures.append("Xiaohongshu plays exaggeration ratio '2.39' or '2.4' not found")

    # 检查 B 站播放夸大倍数
    if "2.02" not in content:
        failures.append("Bilibili plays exaggeration ratio '2.02' not found")

    # 检查小红书官方点赞
    if "3,812" not in content and "3812" not in content:
        failures.append("official Xiaohongshu likes '3,812' / '3812' not found")

    # 检查 MCN 报告点赞
    if "8,500" not in content and "8500" not in content:
        failures.append("MCN report likes '8,500' / '8500' not found")

    # 检查数值对比行（含 vs / ÷ / x 且有数字的行）
    compare_pattern = re.compile(r'(vs|÷|×|\bx\b|倍|ratio|对比)', re.IGNORECASE)
    number_pattern = re.compile(r'\d{3,}')
    compare_lines = [
        ln for ln in content.splitlines()
        if compare_pattern.search(ln) and number_pattern.search(ln)
    ]
    if len(compare_lines) < 3:
        failures.append(f"comparison lines with numbers: {len(compare_lines)} (expected >= 3)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print(f"PASSED (file: {target.name})")
    sys.exit(0)


if __name__ == "__main__":
    main()
