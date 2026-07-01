"""check_q6.py — wave3 s_hospital_safety_event_review q6 checker.

q6 验证点（C 混合类型：session_reuse + multimodal_image）：
  1. findings/imaging_factfinding.md 存在
  2. 文档字数 ≥ 150 个词
  3. 至少引用 1 条 imaging/ 下的影像路径
     （ct_chest_annotated_PT_2026_00847.png
       或 xray_followup_annotated_PT_2026_00847.png）
  4. 至少引用 2 份前轮产物（event_evidence / rca_findings / medwatch_draft /
     timeline_evidence / q_s_email / rca_plan）
  5. 真 session_reuse：sessions/main.jsonl 中某个非空 session_id 续传给
     RunSubagent ≥ 2 次（无文件 / 无真续接均致命 FAIL）

真 resume 信号 = agent 把同一个 session_id 续传给 ≥ 2 次 RunSubagent。复用
subagent_id 而不传 session_id 是假信号（每次新建会话）。此处只看 session_id，
≥ 2 次 → 真复用，否则致命 FAIL。

Tags: session_reuse, incremental_context_load, multimodal_image, stateful_subagent
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterator


# ---------------------------------------------------------------------------
# Helper：解析 sessions/main.jsonl
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
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        yield ev


def _tool_calls(ev: dict) -> list[dict]:
    """兼容多种落盘形态：.tool_calls[] / .tool + .name。"""
    if "tool_calls" in ev and isinstance(ev["tool_calls"], list):
        return ev["tool_calls"]
    if ev.get("tool") or ev.get("name"):
        return [ev]
    return []


def _session_id_counts(ws: Path) -> Counter:
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
# Main
# ---------------------------------------------------------------------------

def main(workspace: Path) -> int:
    findings_path = workspace / "findings" / "imaging_factfinding.md"

    # 1. 文件存在
    if not findings_path.exists():
        print("FAIL: findings/imaging_factfinding.md not found")
        return 1

    text = findings_path.read_text(encoding="utf-8", errors="ignore")

    # 2. 字数 ≥ 150
    word_count = len(text.split())
    if word_count < 150:
        print(
            f"FAIL: findings/imaging_factfinding.md has only {word_count} words "
            "(minimum 150 required). Add more ROI descriptions and cross-round analysis."
        )
        return 1

    # 3. 至少引用 1 条 imaging/ 影像路径
    imaging_patterns = [
        r"imaging/ct_chest_annotated",
        r"ct_chest_annotated_PT_2026_00847\.png",
        r"imaging/xray_followup_annotated",
        r"xray_followup_annotated_PT_2026_00847\.png",
        r"imaging/.*annotated.*\.png",
    ]
    has_imaging_ref = any(
        re.search(pat, text, re.IGNORECASE) for pat in imaging_patterns
    )
    if not has_imaging_ref:
        print(
            "FAIL: findings/imaging_factfinding.md does not reference any annotated "
            "image path from imaging/. Include paths such as "
            "'imaging/ct_chest_annotated_PT_2026_00847.png' or "
            "'imaging/xray_followup_annotated_PT_2026_00847.png'."
        )
        return 1

    # 4. 至少引用 2 份前轮产物
    prior_round_patterns = [
        r"event_evidence",
        r"rca_findings",
        r"medwatch_draft",
        r"timeline_evidence",
        r"q_s_email",
        r"rca_plan",
    ]
    prior_hits: list[str] = []
    for pat in prior_round_patterns:
        if re.search(pat, text, re.IGNORECASE):
            prior_hits.append(pat.replace("_", " ").strip("\\"))
    if len(prior_hits) < 2:
        print(
            f"FAIL: findings/imaging_factfinding.md cites only {len(prior_hits)} "
            f"prior-round file(s) ({prior_hits}); ≥ 2 required. "
            "Reference at least two of: event_evidence.md, rca_findings.yaml, "
            "medwatch_draft.md, timeline_evidence.md."
        )
        return 1

    # 5. 真 session_reuse check（无文件 / 无真续接均致命 FAIL）
    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    counts = _session_id_counts(workspace)
    if not counts or max(counts.values()) < 2:
        print(
            "FAIL (session_reuse): genuine session reuse not observed — the task asked "
            "you to continue the same subagent session (thread the same session_id), "
            "not spawn a fresh one"
        )
        return 1
    top_id = counts.most_common(1)[0][0]
    print(
        f"  [session_reuse] PASS: session_id '{top_id}' used {counts[top_id]} times"
    )

    print(
        f"PASS: findings/imaging_factfinding.md OK — "
        f"{word_count} words, imaging ref found, "
        f"{len(prior_hits)} prior-round citation(s): {prior_hits}"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
