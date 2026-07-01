"""check_q6.py — wave3 s_ecommerce_chargeback_dispute q6 checker.

验证 findings/dispute_resolution.md（B reuse 终局）：
  1. 文件存在，字数 >= 200
  2. 含 dispute 或 chargeback 关键词
  3. 引用 >= 2 前轮产物文件名（来自 q1-q5 output/）
  4. 致命门控：sessions/main.jsonl 中某非空 session_id 被 RunSubagent 续传 >= 2 次（真实续接信号）
  5. 含 >= 2 个关键节点（通过识别 ## 标题或 节点/node/step 关键词）

通过条件（全部满足，exit 0），失败 exit 1。
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterator


# ---------------------------------------------------------------------------
# sessions/main.jsonl 解析 helper（参照 WAVE4_AUTHORING_GUIDE §5.1 模板）
# ---------------------------------------------------------------------------

def _iter_main_events(ws: Path) -> Iterator[dict]:
    """流式读 main.jsonl，跳过非工具调用条目。"""
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
    """兼容多种 jsonl 落盘形态：.tool / .tool_calls[] / .name 等。"""
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


# ---------------------------------------------------------------------------
# 前轮产物文件名集合（q1-q5 output/ 文件，用于引用检测）
# ---------------------------------------------------------------------------

_PRIOR_ROUND_FILES = [
    # q1
    "dispute_plan.md",
    # q2
    "customer_intent.md",
    # q3
    "delivery_proof.md",
    # q4
    "decision_fields.csv",
    # q5
    "customer_email.md",
    "representment_packet.md",
]

# 关键词：dispute / chargeback
_DISPUTE_PATTERN = re.compile(
    r"\b(?:dispute|chargeback|charge.?back)\b",
    re.IGNORECASE,
)

# 关键节点识别：## 标题，或含 node/step/phase/stage/milestone/checkpoint/key 的行
_KEY_NODE_PATTERN = re.compile(
    r"^#{1,3}\s+.+|"
    r"\b(?:node|step|phase|stage|milestone|checkpoint|key\s+(?:finding|point|decision|event|node))\b",
    re.IGNORECASE | re.MULTILINE,
)


# ---------------------------------------------------------------------------
# Main check
# ---------------------------------------------------------------------------

def main(workspace: Path) -> int:
    findings = workspace / "findings" / "dispute_resolution.md"

    # 1. 文件存在
    if not findings.exists():
        print("FAIL: findings/dispute_resolution.md not found")
        return 1

    text = findings.read_text(encoding="utf-8", errors="ignore")

    # 2. 字数 >= 200
    word_count = len(text.split())
    if word_count < 200:
        print(
            f"FAIL: findings/dispute_resolution.md has only {word_count} words "
            f"(need >= 200). Provide a comprehensive dispute resolution analysis."
        )
        return 1

    # 3. 含 dispute 或 chargeback 关键词
    if not _DISPUTE_PATTERN.search(text):
        print(
            "FAIL: findings/dispute_resolution.md must contain 'dispute' or "
            "'chargeback' keyword to confirm on-topic analysis."
        )
        return 1

    # 4. 引用 >= 2 前轮产物文件名
    cited = [f for f in _PRIOR_ROUND_FILES if re.search(re.escape(f), text, re.IGNORECASE)]
    if len(cited) < 2:
        print(
            f"FAIL: findings/dispute_resolution.md must reference >= 2 prior-round "
            f"output files (e.g., dispute_plan.md, customer_intent.md, delivery_proof.md, "
            f"decision_fields.csv, customer_email.md, representment_packet.md). "
            f"Found only: {cited}"
        )
        return 1

    # 5. 含 >= 2 个关键节点标记
    nodes_found = _KEY_NODE_PATTERN.findall(text)
    if len(nodes_found) < 2:
        print(
            f"FAIL: findings/dispute_resolution.md must contain >= 2 key nodes / sections "
            f"(e.g., ## headings or explicit step/phase/milestone references). "
            f"Found {len(nodes_found)} match(es)."
        )
        return 1

    # 6. 真实 session 续接（致命门控）
    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    counts = _session_id_counts(workspace)
    if not counts or max(counts.values()) < 2:
        print(
            "FAIL: genuine session reuse not observed — the task asked you to continue the "
            "same subagent session: thread the same session_id, not spawn a fresh one. "
            "No non-empty session_id appears in >= 2 RunSubagent calls."
        )
        return 1

    print(
        f"PASS: findings/dispute_resolution.md — "
        f"{word_count} words + dispute/chargeback keyword + "
        f"cited {len(cited)} prior file(s) {cited} + "
        f"{len(nodes_found)} key node(s)"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
