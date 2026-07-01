#!/usr/bin/env python3
"""
check_screenshot_defect.py — 验证 analysis/截图证据缺陷分析.md（q7）。

检查要点：
  1. analysis/ 下存在截图证据缺陷分析相关 .md 文件
  2. 含 "截图" 缺陷相关内容
  3. 含 "API" 或 "官方" 导出对比
  4. >= 3 个缺陷点（出现 "缺陷" 或 "问题" 或 "无法" 或 "可伪造" 或 "无时间戳" 等关键词 >= 3 处）
  5. >= 2 个 ## 标题
"""
import sys
import re
from pathlib import Path


def find_target_file(workspace: Path):
    """在 analysis/ 目录下查找截图证据缺陷分析相关的 .md 文件。"""
    analysis_dir = workspace / "analysis"
    if not analysis_dir.exists():
        return None, "analysis/ directory does not exist"

    exact = analysis_dir / "截图证据缺陷分析.md"
    if exact.exists():
        return exact, None

    md_files = list(analysis_dir.glob("*.md"))
    for f in md_files:
        if "截图" in f.name or "缺陷" in f.name or "证据" in f.name:
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

    # 检查截图相关内容
    if "截图" not in content:
        failures.append("'截图' (screenshot) not found in content")

    # 检查 API 或官方导出对比
    has_api_official = "API" in content or "api" in content.lower() or "官方" in content
    if not has_api_official:
        failures.append("'API' or '官方' comparison not found")

    # 检查缺陷关键词出现次数（至少 3 个不同缺陷点）
    defect_keywords = [
        r'缺陷', r'伪造', r'可伪造', r'时间戳', r'无法验证', r'无法核实',
        r'不可信', r'局限', r'问题', r'风险', r'不足',
    ]
    defect_count = sum(
        1 for kw in defect_keywords
        if re.search(kw, content)
    )
    if defect_count < 3:
        failures.append(
            f"defect keywords found: {defect_count} (expected >= 3 distinct defect points)"
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
