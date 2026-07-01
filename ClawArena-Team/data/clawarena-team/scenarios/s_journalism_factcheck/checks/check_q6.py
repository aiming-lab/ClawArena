#!/usr/bin/env python3
"""check_q6.py (wave3) — fact-check 终局：dashboard 交叉引用报告验证。

检查条件（全部通过才 PASS）：
1. findings/dashboard_factcheck.md 存在且 ≥ 200 字
2. 至少引用 1 张 dashboard PNG 路径（stat_*.png 或 dashboards/）
3. 引用 ≥ 2 个前轮产物（q1-q5 输出文件名关键字）
4. 包含 ≥ 2 个跨数据源交叉引用表述
5. 真实 session 续接（instruction-following gate，致命）：某非空 session_id 被 RunSubagent
   续传 ≥ 2 次。题面请求"延续同一会话、不要新建"，故为致命门控（真信号——复用
   subagent_id 不续接 session，不算数）。
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterator


# ---------------------------------------------------------------------------
# sessions/main.jsonl 解析 helper（内联，避免跨文件依赖）
# ---------------------------------------------------------------------------

def _workspace_root() -> Path:
    if len(sys.argv) < 2:
        print("usage: check_q6.py <workspace>", file=sys.stderr)
        sys.exit(2)
    return Path(sys.argv[1]).resolve()


def _iter_main_events(ws: Path) -> Iterator[dict]:
    p = ws / "sessions" / "main.jsonl"
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        yield ev


def _tool_calls(ev: dict) -> list[dict]:
    if "tool_calls" in ev and isinstance(ev["tool_calls"], list):
        return ev["tool_calls"]
    if ev.get("tool") or ev.get("name"):
        return [ev]
    return []


def _run_subagent_id_counts(ws: Path) -> Counter:
    counts: Counter[str] = Counter()
    for ev in _iter_main_events(ws):
        for tc in _tool_calls(ev):
            name = tc.get("tool") or tc.get("name")
            if name != "RunSubagent":
                continue
            args = tc.get("args") or tc.get("arguments") or {}
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {}
            sid = args.get("subagent_id") or args.get("id") or args.get("session_id")
            if sid:
                counts[str(sid)] += 1
    return counts


def _session_id_counts(ws: Path) -> Counter:
    """统计被 RunSubagent 显式续传的非空 session_id 出现次数。

    真实续接信号：harness 仅当同一 session_id 被再次传入时才视为续接
    （new_session = session_id is None or session_id not in harnesses）。
    复用 subagent_id 并不会续接 session，故只按 session_id 计数。
    """
    counts: Counter[str] = Counter()
    for ev in _iter_main_events(ws):
        for tc in _tool_calls(ev):
            name = tc.get("tool") or tc.get("name")
            if name != "RunSubagent":
                continue
            args = tc.get("args") or tc.get("arguments") or {}
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {}
            sid = args.get("session_id")
            if sid:
                counts[str(sid)] += 1
    return counts


def _fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def _pass() -> None:
    print("PASS")
    sys.exit(0)


# ---------------------------------------------------------------------------
# main check
# ---------------------------------------------------------------------------

def main() -> int:
    ws = _workspace_root()
    report = ws / "findings" / "dashboard_factcheck.md"

    # 1. 文件存在
    if not report.exists():
        _fail("findings/dashboard_factcheck.md does not exist")

    text = report.read_text(encoding="utf-8", errors="ignore")
    text_low = text.lower()

    # 2. 最少 200 字
    word_count = len(text.split())
    if word_count < 200:
        _fail(
            f"findings/dashboard_factcheck.md too short: {word_count} words "
            "(need >= 200)"
        )

    # 3. 引用至少 1 张真实 dashboard PNG 路径
    #    注意：必须排除报告自身文件名 'dashboard_factcheck'（findings/dashboard_factcheck.md）。
    #    报告标题/正文几乎必然出现该词，若把它算作命中等于不验证任何真实 PNG 引用。
    #    真实 dashboard 截图位于 workspace/dashboards/，文件名形如
    #    stat_procurement_dashboard.png / stat_coi_network_dashboard.png。
    png_ref = bool(re.search(
        r"stat_\w*\.png|dashboards[/\\]stat_|"
        r"stat_procurement_dashboard|stat_coi_network_dashboard",
        text_low,
    ))
    if not png_ref:
        _fail(
            "findings/dashboard_factcheck.md must reference at least one real "
            "dashboard screenshot path (e.g., 'stat_procurement_dashboard.png' "
            "or 'dashboards/stat_coi_network_dashboard.png'). The report's own "
            "filename 'dashboard_factcheck' does NOT count as a PNG reference."
        )

    # 4. 引用 ≥ 2 个前轮产物（output/ 下的产出文件名关键字）
    prior_round_refs = [
        # q1 产物
        (r"factcheck_plan\.md|factcheck.plan", "factcheck_plan.md"),
        # q2 产物
        (r"contract_and_audio_facts\.md|contract_and_audio", "contract_and_audio_facts.md"),
        # q3 产物
        (r"coi_chain\.md|coi.chain", "coi_chain.md"),
        # q4 产物
        (r"final_finding\.json|final.finding", "final_finding.json"),
        # q5 产物
        (r"editor_report\.md|editor.report", "editor_report.md"),
    ]
    matched_prior = [label for pattern, label in prior_round_refs
                     if re.search(pattern, text_low)]
    if len(matched_prior) < 2:
        _fail(
            f"findings/dashboard_factcheck.md must reference >= 2 prior-round "
            f"output files (e.g., factcheck_plan.md, coi_chain.md, "
            f"final_finding.json, editor_report.md). "
            f"Found only: {matched_prior}"
        )

    # 5. ≥ 2 个跨数据源交叉引用表述
    cross_ref_patterns = [
        r"cross.?referen",
        r"corroborate",
        r"confirm[a-z]*.{0,30}(by|via|from|with|in).{0,30}(dashboard|report|registry|xlsx|pdf|audio|wav|screenshot|png)",
        r"(dashboard|screenshot|png).{0,60}(consistent|match|align|agree|corroborate|confirm)",
        r"(registry|xlsx|pdf|audio|wav).{0,60}(dashboard|screenshot)",
        r"both.{0,60}(source|document|dashboard|data)",
        r"(dashboard|screenshot).{0,60}(dashboard|screenshot)",
        r"验证|交叉|佐证|互相印证|两个来源|多源",
    ]
    cross_count = sum(
        1 for p in cross_ref_patterns if re.search(p, text_low)
    )
    if cross_count < 2:
        _fail(
            "findings/dashboard_factcheck.md must contain >= 2 cross-source "
            "reference statements (e.g., 'corroborated by', 'consistent with', "
            "'confirmed by both sources'). "
            f"Matched {cross_count} cross-reference pattern(s)."
        )

    # 6. 真实 session 续接（致命门控）
    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    sess_counts = _session_id_counts(ws)
    if not sess_counts or max(sess_counts.values()) < 2:
        _fail(
            "genuine session reuse not observed — the task asked you to continue the "
            "same subagent session: thread the same session_id, not spawn a fresh one. "
            "No non-empty session_id appears in >= 2 RunSubagent calls."
        )

    _pass()
    return 0


if __name__ == "__main__":
    sys.exit(main())
