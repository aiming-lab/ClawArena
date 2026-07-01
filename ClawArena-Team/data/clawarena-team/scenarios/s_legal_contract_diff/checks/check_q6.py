#!/usr/bin/env python3
"""check_q6.py (wave3) — session reuse + clause_evolution.md + mp4 路径 + 前轮引用。

通过条件（全部满足，exit 0）：
  1. findings/clause_evolution.md 存在且字符数 ≥ 300
  2. 文件含帧号（整数，如 frame 1 / frame 10 / 第 N 帧 / 帧号 N 等）
  3. 文件含 clause 关键词（termination / SLA / liability / notice / 条款）
  4. 文件含 mp4 路径引用（visualizations/clause_evolution.mp4 或 clause_evolution）
  5. 文件含 ≥ 2 个前轮 findings 引用
     （output/v3_v4_diff / v3_v4_diff / output/audio_and_encrypted_review /
       audio_and_encrypted_review / output/clause_diff_zh_en / clause_diff_zh_en /
       output/legal_audit_report / legal_audit_report / output/work_plan / work_plan /
       q1 / q2 / q3 / q4 / q5 中的任意 2 个不同来源）
  6. 真实 session 续接（instruction-following gate，致命）：sessions/main.jsonl 中某非空
     session_id 被 RunSubagent 续传 >= 2 次。题面请求"延续同一会话、不要新建"，故为致命
     门控（真信号——复用 subagent_id 不续接 session，不算数）。
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterator


# ---------------------------------------------------------------------------
# sessions/main.jsonl 解析 helper（内联，不依赖外部 _common.py）
# ---------------------------------------------------------------------------

def _iter_main_events(ws: Path) -> Iterator[dict]:
    p = ws / "sessions" / "main.jsonl"
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue


def _tool_calls(ev: dict) -> list[dict]:
    """兼容多种 jsonl 落盘形态。"""
    if "tool_calls" in ev and isinstance(ev["tool_calls"], list):
        return ev["tool_calls"]
    if ev.get("tool") or ev.get("name"):
        return [ev]
    return []


def run_subagent_id_counts(ws: Path) -> Counter:
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


def session_id_counts(ws: Path) -> Counter:
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


# ---------------------------------------------------------------------------
# 主检查逻辑
# ---------------------------------------------------------------------------

def main() -> int:
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    target = ws / "findings" / "clause_evolution.md"

    # 1. 文件存在且长度满足
    if not target.exists():
        print("FAIL: findings/clause_evolution.md does not exist")
        sys.exit(1)

    content = target.read_text(encoding="utf-8", errors="ignore")
    if len(content.strip()) < 300:
        print(
            f"FAIL: findings/clause_evolution.md too short "
            f"({len(content.strip())} chars; need ≥ 300)"
        )
        sys.exit(1)

    text = content.lower()

    # 2. 含帧号（frame N / 第 N 帧 / 帧 N / frame number N）
    frame_pattern = re.compile(
        r"(?:frame|帧|帧号|第\s*\d+\s*帧)\s*(?:number\s*)?[#:]?\s*\d+"
        r"|frame\s+\d+"
        r"|\d+\s*(?:st|nd|rd|th)\s+frame",
        re.IGNORECASE,
    )
    if not frame_pattern.search(content):
        print(
            "FAIL: findings/clause_evolution.md must reference a frame number "
            "(e.g., 'frame 1', 'Frame 10', '第 3 帧', 'frame number 5')"
        )
        sys.exit(1)

    # 3. 含 clause 关键词
    clause_keywords = [
        "termination", "sla", "liability", "notice", "条款", "clause",
        "uptime", "cap", "amendment",
    ]
    if not any(kw in text for kw in clause_keywords):
        print(
            f"FAIL: findings/clause_evolution.md missing clause keywords "
            f"(need one of: {clause_keywords})"
        )
        sys.exit(1)

    # 4. 含 mp4 路径引用
    mp4_pattern = re.compile(
        r"clause[\s_-]?evolution"
        r"|visualizations[/\\]clause"
        r"|clause[\s_-]?evolution\.mp4"
        r"|clause_evolution",
        re.IGNORECASE,
    )
    if not mp4_pattern.search(content):
        print(
            "FAIL: findings/clause_evolution.md must reference the mp4 path "
            "(e.g., 'visualizations/clause_evolution.mp4' or 'clause_evolution')"
        )
        sys.exit(1)

    # 5. 含 ≥ 2 个前轮 findings 引用（不同来源）
    prior_sources: list[tuple[str, re.Pattern]] = [
        ("v3_v4_diff", re.compile(
            r"v3[_\s-]?v4[_\s-]?diff|v3.to.v4|version\s+3.to.version\s+4", re.IGNORECASE
        )),
        ("audio_and_encrypted_review", re.compile(
            r"audio[_\s-]?and[_\s-]?encrypted|audio_and_encrypted|encrypted_review"
            r"|voice\s*memo|external\s*counsel\s*memo", re.IGNORECASE
        )),
        ("clause_diff_zh_en", re.compile(
            r"clause[_\s-]?diff[_\s-]?zh[_\s-]?en|clause_diff|zh[_\s-]?en[_\s-]?diff"
            r"|compliance\s+floor|bilingual\s+table", re.IGNORECASE
        )),
        ("legal_audit_report", re.compile(
            r"legal[_\s-]?audit[_\s-]?report|audit[_\s-]?report\.yaml"
            r"|compliance_pass|sla_final|termination_cap_final", re.IGNORECASE
        )),
        ("work_plan", re.compile(
            r"work[_\s-]?plan|output/work_plan", re.IGNORECASE
        )),
        ("q_reference", re.compile(
            r"\bq[1-5]\b|\bq[1-5]\s+findings|\bq[1-5]\s+result|\bq[1-5]\s+output"
            r"|\bround\s+[1-5]\b|prior\s+round", re.IGNORECASE
        )),
    ]
    matched_sources = [name for name, pat in prior_sources if pat.search(content)]
    if len(matched_sources) < 2:
        print(
            f"FAIL: findings/clause_evolution.md must reference ≥ 2 prior-round "
            f"findings sources (matched {len(matched_sources)}: {matched_sources}); "
            "expected references to e.g. v3_v4_diff, audio_and_encrypted_review, "
            "clause_diff_zh_en, legal_audit_report, or q1–q5 outputs"
        )
        sys.exit(1)

    # 6. 真实 session 续接（致命门控）
    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    sess_counts = session_id_counts(ws)
    if not sess_counts or max(sess_counts.values()) < 2:
        print(
            "FAIL: genuine session reuse not observed — the task asked you to continue "
            "the same subagent session: thread the same session_id, not spawn a fresh one. "
            "No non-empty session_id appears in >= 2 RunSubagent calls."
        )
        sys.exit(1)

    print("PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
