"""check_q6.py — findings/negotiation_evolution.md + session reuse >= 2 + Slack refs.

通过条件（全部满足，exit 0）：

  1. findings/negotiation_evolution.md 存在
  2. 文件字数 >= 200 词（以空白分隔的 token 计数）
  3. 文件含让步/谈判关键词（concession / let-bu / term / contract / KPI 任一）
  4. 文件明确引用 >= 2 张 Slack 截图文件名：
       thread_001_xyc_concession_kpi.png
       thread_002_xyc_concession_revenue.png
       thread_003_xyc_concession_exit.png
  5. sessions/main.jsonl 中同一非空 session_id 续传给 RunSubagent >= 2 次（真 session 复用）

真 resume 信号 = agent 把同一个 session_id 续传给 >= 2 次 RunSubagent。复用
subagent_id 而不传 session_id 是假信号（每次新建会话）。此处只看 session_id，
>= 2 次 → 真复用，否则致命 FAIL。

tags: session_reuse, incremental_context_load, multimodal_image, stateful_subagent
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterator

# ---------------------------------------------------------------------------
# sessions/main.jsonl 解析 helper（自含，不依赖外部 _common）
# ---------------------------------------------------------------------------

_SLACK_FILENAMES = [
    "thread_001_xyc_concession_kpi.png",
    "thread_002_xyc_concession_revenue.png",
    "thread_003_xyc_concession_exit.png",
]

_KEYWORD_RE = re.compile(
    r"concession|let.?bu|让步|\bterm\b|contract|合同|条款|kpi",
    re.IGNORECASE,
)


def _iter_events(ws: Path) -> Iterator[dict]:
    """流式读取 sessions/main.jsonl，跳过无法解析的行。"""
    p = ws / "sessions" / "main.jsonl"
    if not p.exists():
        return
    for raw in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            yield json.loads(raw)
        except json.JSONDecodeError:
            continue


def _tool_calls(ev: dict) -> list[dict]:
    """兼容多种 jsonl 落盘形态：.tool_calls[] / .tool / .name 顶层字段。"""
    if "tool_calls" in ev and isinstance(ev.get("tool_calls"), list):
        return ev["tool_calls"]
    if ev.get("tool") or ev.get("name"):
        return [ev]
    # Claude Messages API 格式：content[].type == "tool_use"
    content = ev.get("content")
    if isinstance(content, list):
        return [
            {"tool": blk.get("name"), "args": blk.get("input", {})}
            for blk in content
            if isinstance(blk, dict) and blk.get("type") == "tool_use"
        ]
    return []


def _session_id_counts(ws: Path) -> Counter:
    """统计 RunSubagent 调用中**非空 session_id** 的出现次数（真 resume 信号）。

    只看 args["session_id"]，不回退到 subagent_id/id（后者每次新建会话，是假信号）。
    """
    counts: Counter[str] = Counter()
    for ev in _iter_events(ws):
        for tc in _tool_calls(ev):
            name = tc.get("tool") or tc.get("name") or ""
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
    if len(sys.argv) < 2:
        print("usage: check_q6.py <workspace>", file=sys.stderr)
        return 2

    ws = Path(sys.argv[1]).resolve()
    errors: list[str] = []

    target = ws / "findings" / "negotiation_evolution.md"

    # ── 1. 文件存在 ────────────────────────────────────────────────────────────
    if not target.exists():
        print(
            "FAIL: findings/negotiation_evolution.md does not exist; "
            "complete q6 and write the concession comparison table there."
        )
        return 1

    text = target.read_text(encoding="utf-8", errors="replace")

    # ── 2. 字数 >= 200 ─────────────────────────────────────────────────────────
    word_count = len(text.split())
    if word_count < 200:
        errors.append(
            f"findings/negotiation_evolution.md is too short ({word_count} words); "
            "must be >= 200 words — include the full concession comparison table "
            "and analysis for all three Slack threads."
        )

    # ── 3. 让步/谈判关键词 ──────────────────────────────────────────────────────
    if not _KEYWORD_RE.search(text):
        errors.append(
            "findings/negotiation_evolution.md missing negotiation keywords; "
            "expected at least one of: 'concession', 'term', 'contract', 'KPI', "
            "'让步', '条款', '合同'. Ensure the file discusses the negotiation terms."
        )

    # ── 4. >= 2 张 Slack 截图文件名明确引用 ────────────────────────────────────
    referenced = [fn for fn in _SLACK_FILENAMES if fn in text]
    if len(referenced) < 2:
        errors.append(
            f"findings/negotiation_evolution.md references only {len(referenced)} "
            f"Slack screenshot filename(s) ({referenced!r}); must reference >= 2 of: "
            + ", ".join(_SLACK_FILENAMES)
            + ". Read all three screenshots and cite them by filename."
        )

    # ── 5. 真 session 复用：同一非空 session_id 续传 >= 2 次 ──────────────────
    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    counts = _session_id_counts(ws)
    if not counts or counts.most_common(1)[0][1] < 2:
        errors.append(
            "genuine session reuse not observed — the task asked you to continue the "
            "same subagent session (thread the same session_id), not spawn a fresh one"
        )

    # ── 结果 ──────────────────────────────────────────────────────────────────
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    slack_refs_str = ", ".join(referenced)
    top_id, top_count = counts.most_common(1)[0]
    print(
        f"PASS: findings/negotiation_evolution.md present ({word_count} words), "
        f"contains negotiation keywords, references Slack screenshots ({slack_refs_str}), "
        f"and genuine session reuse confirmed (session_id={top_id!r} used {top_count} times)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
