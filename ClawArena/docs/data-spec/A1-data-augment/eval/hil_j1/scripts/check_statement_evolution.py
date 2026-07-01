#!/usr/bin/env python3
"""
check_statement_evolution.py — 验证 analysis/刘姐陈述演变分析.md（q19）。

检查要点：
  1. analysis/ 下存在刘姐陈述演变相关 .md 文件
  2. 含初始辩护"口径"相关内容（"统计口径"或"口径不同"）
  3. 含最终承认"估算"（"内部估算"或"估算"）
  4. >= 3 个演变阶段（## 标题或阶段关键词）
  5. >= 3 个 ## 标题
"""
import sys
import re
from pathlib import Path


def find_target_file(workspace: Path):
    """在 analysis/ 目录下查找刘姐陈述演变相关的 .md 文件。"""
    analysis_dir = workspace / "analysis"
    if not analysis_dir.exists():
        return None, "analysis/ directory does not exist"

    exact = analysis_dir / "刘姐陈述演变分析.md"
    if exact.exists():
        return exact, None

    md_files = list(analysis_dir.glob("*.md"))
    for f in md_files:
        if "刘姐" in f.name or "陈述" in f.name or "演变" in f.name:
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

    # 检查初始辩护（口径相关）
    initial_keywords = ["统计口径", "口径不同", "口径差异", "全渠道", "曝光量", "口径"]
    has_initial = any(kw in content for kw in initial_keywords)
    if not has_initial:
        failures.append(
            "initial defense ('口径' caliber argument) not found. "
            "Expected one of: " + str(initial_keywords)
        )

    # 检查最终承认（估算相关）
    admission_keywords = ["估算", "内部估算", "承认", "internal estimate", "虚构"]
    has_admission = any(kw in content for kw in admission_keywords)
    if not has_admission:
        failures.append(
            "final admission ('估算' internal estimate) not found. "
            "Expected one of: " + str(admission_keywords)
        )

    # 检查演变触发事件（API 推翻或 timeline 相关）
    trigger_keywords = ["API", "推翻", "核实", "触发", "转变", "因此", "在此之后", "然后"]
    has_trigger = any(kw in content for kw in trigger_keywords)
    if not has_trigger:
        failures.append(
            "change trigger event not described. "
            "Expected one of: " + str(trigger_keywords)
        )

    # 检查 ## 标题数量（演变阶段）
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 3:
        failures.append(f"'##' headings: {len(headings)} (expected >= 3 for 3 evolution phases)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print(f"PASSED (file: {target.name})")
    sys.exit(0)


if __name__ == "__main__":
    main()
