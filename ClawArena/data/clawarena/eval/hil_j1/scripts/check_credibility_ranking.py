#!/usr/bin/env python3
"""
check_credibility_ranking.py — 验证 analysis/MCN报告可信度评估.md（q8）。

检查要点：
  1. analysis/ 下存在可信度评估相关 .md 文件
  2. >= 4 个数据源被提及（官方后台 / API / 第三方 / 截图 / MCN自报 至少 4 种）
  3. 官方后台 / API 在截图 / MCN 报告之前排列（可信度更高）
  4. 含 "可信度" 或 "排序" 或 "评级" 等排序相关词
  5. >= 2 个 ## 标题
"""
import sys
import re
from pathlib import Path


def find_target_file(workspace: Path):
    """在 analysis/ 目录下查找可信度评估相关的 .md 文件。"""
    analysis_dir = workspace / "analysis"
    if not analysis_dir.exists():
        return None, "analysis/ directory does not exist"

    exact = analysis_dir / "MCN报告可信度评估.md"
    if exact.exists():
        return exact, None

    md_files = list(analysis_dir.glob("*.md"))
    for f in md_files:
        if "可信度" in f.name or "评估" in f.name or "MCN" in f.name:
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

    # 检查数据源（至少 4 种）
    sources = {
        "官方后台": ["官方后台", "官方数据", "后台数据"],
        "API": ["API", "api导出", "API导出"],
        "第三方": ["第三方", "监测", "第三方监测"],
        "截图": ["截图", "screenshot"],
        "MCN自报": ["MCN自报", "MCN报告", "MCN 报告", "自报数据"],
    }
    found_sources = []
    for source_name, keywords in sources.items():
        if any(kw in content for kw in keywords):
            found_sources.append(source_name)

    if len(found_sources) < 4:
        failures.append(
            f"data sources found: {found_sources} ({len(found_sources)}/4 required). "
            "Need: 官方后台, API, 第三方, 截图, MCN自报 (at least 4)"
        )

    # 检查可信度排序相关词
    ranking_keywords = ["可信度", "排序", "评级", "高于", "优于", "最高", "最低", "排名"]
    has_ranking = any(kw in content for kw in ranking_keywords)
    if not has_ranking:
        failures.append(
            "credibility ranking keywords not found. "
            "Expected one of: " + str(ranking_keywords)
        )

    # 官方/API 应优于截图/MCN（简单检查：内容中官方出现在截图之前）
    pos_official = min(
        (content.find(kw) for kw in ["官方后台", "官方数据", "API导出"] if content.find(kw) != -1),
        default=-1
    )
    pos_screenshot = content.find("截图")
    if pos_official != -1 and pos_screenshot != -1 and pos_official > pos_screenshot:
        # 如果内容中截图比官方先出现，再检查是否有明确的排序说明
        if "官方" not in content or "高于" not in content and "优于" not in content:
            failures.append(
                "credibility order unclear: official/API sources should rank higher than screenshots"
            )

    # 检查 ## 标题数量
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 2:
        failures.append(f"'##' headings: {len(headings)} (expected >= 2)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print(f"PASSED (file: {target.name}, sources: {found_sources})")
    sys.exit(0)


if __name__ == "__main__":
    main()
