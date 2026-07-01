#!/usr/bin/env python3
"""check_q6.py — Validate q6: governance evolution analysis (B-type session reuse).

Ground truth anchors:
  - findings/governance_evolution.md 存在，字数 >= 200 词
  - 内容含 chair/committee/board 相关关键词（chair, committee, board）
  - 内容含 DIRECTOR_ALBA 的 Risk & Compliance 委员会职位引用
  - 内容含 Charter v3.2 引用
  - 真 session 复用（致命门控）

通过条件（全部满足，exit 0）：
  1. findings/governance_evolution.md 存在
  2. 文件字数 >= 200
  3. 含 chair / committee / board 关键词（至少两个）
  4. 含 DIRECTOR_ALBA 或 "Alba" 与 committee/risk 联用
  5. 含 Charter v3.2 / v3.2 / Charter 3.2 引用
  6. 真 session 复用：某非空 session_id 出现在 >= 2 次 RunSubagent 调用

真 resume 信号 = agent 把同一个 session_id 续传给 >= 2 次 RunSubagent。数
subagent_id 重复是假信号（每次新建会话）。此处只看 session_id，>= 2 次 → 真复用，
否则致命 FAIL；上述内容校验同样保持致命。

Usage: python check_q6.py <workspace_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterator


# ---------------------------------------------------------------------------
# sessions/main.jsonl 解析（self-contained，不依赖外部 helper）
# ---------------------------------------------------------------------------

def iter_main_events(ws: Path) -> Iterator[dict]:
    """流式读 main.jsonl，跳过非 JSON 行。"""
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
    """兼容多种 jsonl 落盘形态：.tool_calls[] / .tool / .name。"""
    if "tool_calls" in ev and isinstance(ev["tool_calls"], list):
        return ev["tool_calls"]
    if ev.get("tool") or ev.get("name"):
        return [ev]
    return []


def run_subagent_session_id_counts(ws: Path) -> Counter:
    """统计 RunSubagent 调用中**非空 session_id** 的出现次数（真 resume 信号）。

    只看 args["session_id"]，不回退到 subagent_id/id（后者每次新建会话，是假信号）。
    """
    counts: Counter[str] = Counter()
    for ev in iter_main_events(ws):
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
# Content-level patterns
# ---------------------------------------------------------------------------

CHAIR_RE = re.compile(r"\bchair\b", re.IGNORECASE)
COMMITTEE_RE = re.compile(r"\bcommittee\b", re.IGNORECASE)
BOARD_RE = re.compile(r"\bboard\b", re.IGNORECASE)

# DIRECTOR_ALBA 与 Risk/Compliance/Committee 联用（250 字符窗口）
ALBA_COMMITTEE_RE = re.compile(
    r"(?:DIRECTOR_ALBA|[Aa]lba).{0,250}(?:committee|risk|compliance|chair)"
    r"|(?:committee|risk|compliance|chair).{0,250}(?:DIRECTOR_ALBA|[Aa]lba)",
    re.IGNORECASE | re.DOTALL,
)

CHARTER_V32_RE = re.compile(
    r"v3\.2|version\s+3\.2|[Cc]harter\s+3\.2",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def _fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q6.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1]).resolve()
    findings_file = ws / "findings" / "governance_evolution.md"

    # 1. File existence
    if not findings_file.exists():
        _fail("findings/governance_evolution.md does not exist")

    content = findings_file.read_text(encoding="utf-8", errors="ignore")
    word_count = len(content.split())

    errors: list[str] = []

    # 2. Word count >= 200
    if word_count < 200:
        errors.append(
            f"findings/governance_evolution.md is too short ({word_count} words; need >= 200)"
        )

    # 3. Must contain at least 2 of: chair, committee, board
    keyword_hits = sum([
        bool(CHAIR_RE.search(content)),
        bool(COMMITTEE_RE.search(content)),
        bool(BOARD_RE.search(content)),
    ])
    if keyword_hits < 2:
        errors.append(
            "findings/governance_evolution.md must reference at least two of: "
            "'chair', 'committee', 'board' — found fewer than 2"
        )

    # 4. DIRECTOR_ALBA referenced in committee/risk context
    if not ALBA_COMMITTEE_RE.search(content):
        errors.append(
            "findings/governance_evolution.md must reference DIRECTOR_ALBA in the context "
            "of their committee role (Risk & Compliance chair)"
        )

    # 5. Charter v3.2 cited
    if not CHARTER_V32_RE.search(content):
        errors.append(
            "findings/governance_evolution.md must cite Charter v3.2 "
            "(as 'v3.2', 'version 3.2', or 'Charter 3.2')"
        )

    # 6. Genuine session reuse: some non-empty session_id used in >= 2 RunSubagent calls.
    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    counts = run_subagent_session_id_counts(ws)
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
        f"PASS: findings/governance_evolution.md ({word_count} words) covers chair appointment, "
        f"DIRECTOR_ALBA committee role, Charter v3.2 governance requirements"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
