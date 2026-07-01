"""check_q3.py — Wave3 s_devops_runbook_sync q3 checker.

Verifies output/test_report.md:
1. SC2086 present (shellcheck warning from pre_check.sh:31)
2. pre_check.sh line 31 reference (shellcheck stderr)
3. pre_migration_checks.bats line 23 reference (bats test failure)
4. LOCK_TIMEOUT_REQUIRED present (failing bats assertion string)

Session reuse audit (I-dimension) — ADVISORY ONLY (non-gating):
- Parse sessions/main.jsonl
- q2 subagent session_id ideally matches q3 subagent session_id
- 决策（dev2）：跨轮 session-reuse 维度降级为非 gating，仅 advisory 警告。
  真实 main.jsonl 的 round 切分与 subagent_id 落盘形态不稳定，强行 gating 会
  冤判内容正确的提交，故此处不再 return 1、不影响退出码。
- 其它内容校验（SC2086 / pre_check.sh:31 / pre_migration_checks.bats:23 /
  LOCK_TIMEOUT_REQUIRED）保持致命不变。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Session reuse parsing
# ---------------------------------------------------------------------------
#
# 收紧动机（C3）：旧实现把整条记录 json.dumps 后用裸子串 "q2"/"q3" 当 round 命中，
# 再从**顶层 record** 上读 session_id/subagent_id/... —— 但真实 main.jsonl 里
# (a) "q2"/"q3" 只出现在题面/提示的散文中、从不作为 session id 的标签，
# (b) subagent_id / session_id 实际嵌在 tool_calls[].arguments 里、顶层 record 没有这些键。
# 两点叠加导致 q2_ids/q3_ids 恒为空、审计永久 SKIP，等于对真实日志彻底失效。
#
# 现在改为真正的 round-aware 复用审计：
#   - 用 is_real_user_question 标记切分各 round（第 N 个标记 = 第 N 题 q1..q6）；
#   - 在 q2、q3 两个 round 内分别收集 RunSubagent 调用的 subagent_id；
#   - 要求两者有交集（q3 复用了 q2 用过的同一个 subagent）。
# 若日志缺失或某一 round 根本没有 RunSubagent，则 graceful skip（不冤判没跑 subagent
# 的提交，那类提交会在别处因缺产物失败）。

def _read_records(jsonl_path: Path) -> list[dict]:
    records: list[dict] = []
    try:
        text = jsonl_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return records
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            records.append(obj)
    return records


def _tool_calls(ev: dict) -> list[dict]:
    """Yield tool-call dicts across flat tool_calls / content-block / bare-event forms."""
    calls: list[dict] = []
    tcs = ev.get("tool_calls")
    if isinstance(tcs, list):
        calls.extend(t for t in tcs if isinstance(t, dict))
    content = ev.get("content")
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                calls.append(block)
    return calls


def _tool_name(tc: dict) -> str:
    return tc.get("tool") or tc.get("name") or (tc.get("function") or {}).get("name", "") or ""


def _get_args(tc: dict) -> dict:
    args = tc.get("args")
    if args is None:
        args = tc.get("arguments")
    if args is None:
        args = (tc.get("function") or {}).get("arguments")
    if args is None:
        args = tc.get("input")
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except Exception:
            args = {}
    return args if isinstance(args, dict) else {}


def _round_of(idx: int, bounds: list[int]) -> int:
    """1-based round number for record at position idx given round-start bounds."""
    rnd = 0
    for b in bounds:
        if idx >= b:
            rnd += 1
        else:
            break
    return rnd


def _run_subagent_ids_by_round(records: list[dict]) -> dict[int, set[str]]:
    """Map round number -> set of subagent_id values invoked via RunSubagent."""
    bounds = [i for i, r in enumerate(records) if r.get("is_real_user_question")]
    by_round: dict[int, set[str]] = {}
    for i, r in enumerate(records):
        for tc in _tool_calls(r):
            if _tool_name(tc) != "RunSubagent":
                continue
            sid = _get_args(tc).get("subagent_id")
            if isinstance(sid, str) and sid:
                by_round.setdefault(_round_of(i, bounds), set()).add(sid)
    return by_round


def _run_subagent_session_id_counts(records: list[dict]) -> dict[str, int]:
    """Count non-empty RunSubagent ``session_id`` args — the real resume signal.

    The harness only continues a session when the same session_id is threaded
    back (new_session = session_id is None or session_id not in harnesses); a
    subagent_id alone spawns a fresh session each round.
    """
    counts: dict[str, int] = {}
    for r in records:
        for tc in _tool_calls(r):
            if _tool_name(tc) != "RunSubagent":
                continue
            sid = _get_args(tc).get("session_id")
            if isinstance(sid, str) and sid:
                counts[sid] = counts.get(sid, 0) + 1
    return counts


# ---------------------------------------------------------------------------
# Main check
# ---------------------------------------------------------------------------

def main(workspace: Path) -> int:
    out = workspace / "output" / "test_report.md"
    if not out.exists():
        print("FAIL: output/test_report.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. SC2086 shellcheck warning
    if not re.search(r"SC2086", text):
        print("FAIL: 'SC2086' shellcheck warning not found in test_report.md — "
              "must run shellcheck on pre_check.sh and parse stderr")
        return 1

    # 2. pre_check.sh line 31
    if not re.search(r"pre_check\.sh", text, re.IGNORECASE):
        print("FAIL: 'pre_check.sh' not found in test_report.md")
        return 1
    if not re.search(r"\b31\b", text):
        print("FAIL: line number 31 not found in test_report.md "
              "(SC2086 warning is on pre_check.sh line 31)")
        return 1

    # 3. pre_migration_checks.bats line 23
    if not re.search(r"pre_migration_checks\.bats", text, re.IGNORECASE):
        print("FAIL: 'pre_migration_checks.bats' not found in test_report.md")
        return 1
    if not re.search(r"\b23\b", text):
        print("FAIL: line number 23 not found in test_report.md "
              "(failing bats test is on line 23)")
        return 1

    # 4. LOCK_TIMEOUT_REQUIRED (the failing assert_output pattern)
    if not re.search(r"LOCK_TIMEOUT_REQUIRED", text):
        print("FAIL: 'LOCK_TIMEOUT_REQUIRED' not found in test_report.md — "
              "must capture the bats assert_output failure string")
        return 1

    # 5. Session reuse audit (I-dimension) — FATAL on the REAL resume signal.
    #    q3 题面要求 "continue with the same LLM subagent from q2 — no need to
    #    start fresh"。真复用的唯一信号是把同一个非空 session_id 续传给 RunSubagent
    #    (harness: new_session = session_id is None or session_id not in harnesses)；
    #    只传 subagent_id 而不传 session_id 会每轮新建会话，不算复用。
    sessions_path = workspace / "sessions" / "main.jsonl"
    records = _read_records(sessions_path) if sessions_path.exists() else []
    session_id_counts = _run_subagent_session_id_counts(records)
    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    if not session_id_counts or max(session_id_counts.values()) < 2:
        print(
            "FAIL: genuine session reuse not observed — the task asked you to continue the same "
            "subagent session (thread the same session_id), not spawn a fresh one each round"
        )
        return 1

    print(
        "PASS: test_report.md has SC2086 + pre_check.sh:31 + "
        "pre_migration_checks.bats:23 + LOCK_TIMEOUT_REQUIRED "
        "+ genuine session reuse (same session_id threaded)"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
