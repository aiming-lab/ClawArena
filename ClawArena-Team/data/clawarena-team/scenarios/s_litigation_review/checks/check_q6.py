#!/usr/bin/env python3
"""check_q6.py — Session reuse (B type) + findings/settlement_analysis.md 内容验证。

Ground truth anchors（均来自 q1–q5 已确立的锚点）：
  pip_start_date    = 2026-03-15
  hearing_date      = 2026-03-22
  termination_date  = 2026-04-04
  statutory_shortfall = 25  (45 binding minimum − 20 actual = 25 days)
  settlement_keywords = settlement / exposure / liability / risk / negotiate / compensation

通过条件（全部满足，exit 0）：
  1. findings/settlement_analysis.md 存在
  2. 文件内容包含以下关键事件日期中至少 3 个：
       - 2026-03-15（PIP 开始）
       - 2026-03-22（庭审日期）
       - 2026-04-04（终止日期）
       - 25（statutory shortfall 天数）
  3. 文件含 settlement/exposure/liability/risk/negotiate/compensation 中至少 1 个词

说明：
  session-reuse 现作为指令遵循门控（致命）：真 resume 信号 = agent 把同一个
  session_id 续传给 >= 2 次 RunSubagent。某非空 session_id 出现 >= 2 次 → 真复用，
  否则致命 FAIL。数 subagent_id 重复是假信号（每次新建会话），故只看 session_id。
  其它实质内容校验（文件存在、关键锚点日期、settlement 风险措辞）同样为致命。

用法：python check_q6.py <workspace_path>
退出码：0 = pass, 1 = fail.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterator


# ---------------------------------------------------------------------------
# main.jsonl 解析 helper（内联，不依赖场景级 _common）
# ---------------------------------------------------------------------------

def _iter_main_events(ws: Path) -> Iterator[dict]:
    """流式读 sessions/main.jsonl，跳过空行和 JSON 解析失败的行。"""
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
    """兼容多种 jsonl 落盘形态：.tool_calls[] / .tool / .name。"""
    if "tool_calls" in ev and isinstance(ev["tool_calls"], list):
        return ev["tool_calls"]
    if ev.get("tool") or ev.get("name"):
        return [ev]
    return []


def _run_subagent_session_id_counts(ws: Path) -> Counter:
    """统计 RunSubagent 调用中**非空 session_id** 的出现次数（真 resume 信号）。

    只看 args["session_id"]，不回退到 subagent_id/id（后者每次新建会话，是假信号）。
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


# ---------------------------------------------------------------------------
# 日期 / 数字匹配 helper
# ---------------------------------------------------------------------------

_DATE_2026_03_15 = re.compile(
    r"2026-03-15|2026/03/15|03[/-]15[/-]2026|15[/-]03[/-]2026"
    r"|(?:March|Mar\.?)\s+15(?:,?\s*2026)?"
    r"|15\s+(?:March|Mar\.?)\s+2026",
    re.IGNORECASE,
)

_DATE_2026_03_22 = re.compile(
    r"2026-03-22|2026/03/22|03[/-]22[/-]2026|22[/-]03[/-]2026"
    r"|(?:March|Mar\.?)\s+22(?:,?\s*2026)?"
    r"|22\s+(?:March|Mar\.?)\s+2026",
    re.IGNORECASE,
)

_DATE_2026_04_04 = re.compile(
    r"2026-04-04|2026/04/04|04[/-]04[/-]2026|04[/-]4[/-]2026"
    r"|(?:April|Apr\.?)\s+4(?:,?\s*2026)?"
    r"|4\s+(?:April|Apr\.?)\s+2026",
    re.IGNORECASE,
)

_SHORTFALL_25 = re.compile(r"\b25\b")

_SETTLEMENT_KW = re.compile(
    r"settlement|exposure|liability|risk|negotiat|compensation|damages",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q6.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1]).resolve()
    errors: list[str] = []

    # --- 1. findings/settlement_analysis.md 存在 ---
    analysis = ws / "findings" / "settlement_analysis.md"
    if not analysis.exists():
        print("FAIL: findings/settlement_analysis.md does not exist")
        return 1

    content = analysis.read_text(encoding="utf-8", errors="replace")

    # --- 2. 关键事件日期：至少 3 个命中 ---
    date_hits: list[str] = []
    if _DATE_2026_03_15.search(content):
        date_hits.append("2026-03-15 (PIP start)")
    if _DATE_2026_03_22.search(content):
        date_hits.append("2026-03-22 (hearing)")
    if _DATE_2026_04_04.search(content):
        date_hits.append("2026-04-04 (termination)")
    if _SHORTFALL_25.search(content):
        date_hits.append("25 (statutory shortfall days)")

    if len(date_hits) < 3:
        errors.append(
            f"findings/settlement_analysis.md must reference at least 3 of the 4 "
            f"key anchors (2026-03-15 PIP start, 2026-03-22 hearing, 2026-04-04 "
            f"termination, 25-day shortfall); found only {len(date_hits)}: {date_hits}"
        )

    # --- 3. settlement 关键词 ---
    if not _SETTLEMENT_KW.search(content):
        errors.append(
            "findings/settlement_analysis.md must contain at least one of: "
            "settlement, exposure, liability, risk, negotiat(ion), compensation, damages"
        )

    # --- 4. 真 session 复用：某非空 session_id 出现在 >= 2 次 RunSubagent 调用 ---
    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    counts = _run_subagent_session_id_counts(ws)
    if not counts or max(counts.values()) < 2:
        errors.append(
            "genuine session reuse not observed — the task asked you to continue the "
            "same subagent session (thread the same session_id), not spawn a fresh one"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        "PASS: findings/settlement_analysis.md exists with timeline anchors "
        "(key dates + 25-day shortfall) and settlement risk language "
        "(session reuse is advisory only — non-gating)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
