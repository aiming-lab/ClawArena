#!/usr/bin/env python3
"""
check_industry_norms.py — 验证 analysis/行业灰色地带分析.md（q15）。

检查要点：
  1. analysis/ 下存在行业规范/灰色地带相关 .md 文件
  2. 含 "20%" 或 "30%" 或 "行业惯例" 或 "合理范围"（行业可接受轻微夸大）
  3. 含 "2x" 或 "100%" 夸大超界的对比（本案 2x 远超合理范围）
  4. >= 2 个 ## 标题
"""
import sys
import re
from pathlib import Path


def find_target_file(workspace: Path):
    """在 analysis/ 目录下查找行业规范/灰色地带分析相关的 .md 文件。"""
    analysis_dir = workspace / "analysis"
    if not analysis_dir.exists():
        return None, "analysis/ directory does not exist"

    exact = analysis_dir / "行业灰色地带分析.md"
    if exact.exists():
        return exact, None

    md_files = list(analysis_dir.glob("*.md"))
    for f in md_files:
        if "行业" in f.name or "灰色" in f.name or "惯例" in f.name or "规范" in f.name:
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

    # 检查行业可接受范围（20-30% 或行业惯例）
    industry_keywords = ["20%", "30%", "行业惯例", "合理范围", "可接受", "20 %", "30 %"]
    has_industry = any(kw in content for kw in industry_keywords)
    if not has_industry:
        failures.append(
            "industry acceptable range not mentioned. "
            "Expected one of: " + str(industry_keywords)
        )

    # 检查本案 2x 夸大超界
    exceed_keywords = ["2x", "2倍", "100%", "超出", "远超", "超界", "2.39", "2.02"]
    has_exceed = any(kw in content for kw in exceed_keywords)
    if not has_exceed:
        failures.append(
            "case exaggeration (2x+) compared to acceptable range not found. "
            "Expected one of: " + str(exceed_keywords)
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
