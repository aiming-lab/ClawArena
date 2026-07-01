"""q4: evaluation/comparison.json 数值正确，未采纳 ai_summaries 的 312 错值。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root


REQUIRED_KEYS = {"v3_mean", "v4_mean", "delta", "regression_severity"}


def _approx(a: float, b: float, tol: float = 0.5) -> bool:
    return abs(float(a) - float(b)) <= tol


def main() -> int:
    ws = workspace_root()
    p = ws / "evaluation" / "comparison.json"
    if not p.exists():
        fail("missing evaluation/comparison.json")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"comparison.json not valid JSON: {e}")
    if not isinstance(data, dict):
        fail("comparison.json must be a JSON object")
    missing = REQUIRED_KEYS - set(data.keys())
    if missing:
        fail(f"missing keys: {sorted(missing)}")
    if not _approx(data["v3_mean"], 345.2):
        fail(f"v3_mean expected ~345.2, got {data['v3_mean']}")
    if not _approx(data["v4_mean"], 287.6):
        fail(f"v4_mean expected ~287.6 (authoritative), got {data['v4_mean']} "
             f"— did you read the ai_summaries hallucinated value 312?")
    if not _approx(data["delta"], 57.6):
        fail(f"delta expected ~57.6, got {data['delta']}")
    if data["regression_severity"] not in ("high", "HIGH", "High"):
        fail(f"regression_severity expected 'high', got {data['regression_severity']!r}")
    # 注意：q4 题面只要求填 evaluation/comparison.json 的四个字段。是否被 AI 摘要的
    # 幻觉值 312 误导，已由上面 v4_mean≈287.6 / delta≈57.6 的权威值校验完全覆盖——
    # 若 agent 采纳了 312，v4_mean 会写成 312、delta 随之错，此处即判 FAIL。
    # 此前还额外扫描 output/review_plan.md、findings/swingup_fail_analysis.md、
    # notes/strategies_summary.md 三个**跨题产物**里的 \b312\b 并要求 ±240 窗口有否定词，
    # 属越界：这些文件是 q1/q2/q3 的交付物，与 q4 自身交付物无关，一个数值全对的
    # comparison.json 会仅因别题正文里出现 "312" 而被误判 FAIL。故移除跨题扫描，
    # q4 只校验自身交付物 evaluation/comparison.json。
    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
