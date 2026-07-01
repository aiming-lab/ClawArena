"""check_q6.py — background subagent 发起验证 + postmortem_final.md 最终综合验证。

通过条件（全部满足，exit 0）：

A. ADVISORY ONLY (non-gating): sessions/main.jsonl 中存在 RunSubagent(run_in_background=true)
   （后台 metrics 拉取子代理已发起）

B. output/postmortem_final.md 存在且字节数 >= 500
   （主线综合摘要已生成）

C. postmortem_final.md 至少引用以下五个前轮落盘文件中的三个：
     q1_scope.md, q2_first_error.md, q3_dashboard.md,
     q4_comms_vs_data.md, rca_summary.json

D. postmortem_final.md 含根因关键词：
   'deadlock' 和 ('migration' 或 'v23')

E. postmortem_final.md 含三个冲击数字：
   - 事故时长：'23'（紧邻 'min'/'minute'）
   - 用户影响：数字 4500（或 '4,500'）
   - 营收损失：'87' + ('000' 或 ',000') 或 '87000'
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterator


# ---------------------------------------------------------------------------
# sessions/main.jsonl 解析 helper（不依赖外部模块，直接内嵌）
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


def _tool_calls_from_event(ev: dict) -> list[dict]:
    """兼容多种 jsonl 落盘形态。"""
    if "tool_calls" in ev and isinstance(ev["tool_calls"], list):
        return ev["tool_calls"]
    if ev.get("tool") or ev.get("name"):
        return [ev]
    return []


def workflow_call_count(ws: Path) -> int:
    """统计 sessions/main.jsonl 中 name == 'Workflow' 的工具调用次数。"""
    count = 0
    for ev in _iter_main_events(ws):
        for tc in _tool_calls_from_event(ev):
            name = tc.get("tool") or tc.get("name") or (tc.get("function") or {}).get("name", "")
            if name == "Workflow":
                count += 1
    return count


def has_background_run(ws: Path) -> bool:
    """检测 sessions/main.jsonl 中是否存在 RunSubagent(run_in_background=true)。"""
    for ev in _iter_main_events(ws):
        for tc in _tool_calls_from_event(ev):
            name = tc.get("tool") or tc.get("name")
            if name != "RunSubagent":
                continue
            args = tc.get("args") or tc.get("arguments") or {}
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {}
            if args.get("run_in_background"):
                return True
    return False


# ---------------------------------------------------------------------------
# 正则辅助
# ---------------------------------------------------------------------------

DURATION_RE = re.compile(r"\b23\b[^a-z]{0,8}(min|minute)", re.IGNORECASE)

USER_RE = re.compile(
    r"(\d{1,3}(?:[,]?\d{3}))\s+(?:\S+\s+){0,3}(?:users?|customers?|affected|impacted)",
    re.IGNORECASE,
)
USER_RE2 = re.compile(
    r"(?:users?|customers?|affected|impacted)(?:\s+\S+){0,3}\s*[:=~-]?\s*(\d{1,3}(?:[,]?\d{3}))",
    re.IGNORECASE,
)

REVENUE_RE = re.compile(r"\$\s*87[,.]?000", re.IGNORECASE)
REVENUE_RE2 = re.compile(r"\b87000\b")


def _has_user_anchor(text: str) -> bool:
    for pat in (USER_RE, USER_RE2):
        for m in pat.finditer(text):
            val = int(m.group(1).replace(",", ""))
            if val == 4500:
                return True
    return False


def _has_revenue_anchor(text: str) -> bool:
    return bool(REVENUE_RE.search(text) or REVENUE_RE2.search(text))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

PRIOR_ROUND_FILES = [
    "q1_scope.md",
    "q2_first_error.md",
    "q3_dashboard.md",
    "q4_comms_vs_data.md",
    "rca_summary.json",
]
MIN_PRIOR_REFS = 3


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q6.py <workspace>", file=sys.stderr)
        return 2

    ws = Path(sys.argv[1]).resolve()
    errors: list[str] = []

    # ------------------------------------------------------------------
    # 0. Workflow orchestration
    # instruction-following gate: prompt asks to orchestrate this via the Workflow tool (single script managing sub-agents)
    # ------------------------------------------------------------------
    if workflow_call_count(ws) == 0:
        errors.append(
            "Workflow tool not used — the task asked you to orchestrate this as a single "
            "workflow script managing the sub-agents"
        )

    # ------------------------------------------------------------------
    # A. background RunSubagent
    # ------------------------------------------------------------------
    sessions_path = ws / "sessions" / "main.jsonl"
    # instruction-following gate: prompt explicitly asks to launch this in the background
    if not sessions_path.exists():
        print("[warn] sessions/main.jsonl not found; skipping background check")
    elif not has_background_run(ws):
        errors.append(
            "background subagent not observed — the task asked you to launch this as a "
            "background RunSubagent(run_in_background=true) and not block the main thread"
        )

    # ------------------------------------------------------------------
    # B. output/postmortem_final.md exists and is non-trivial
    # ------------------------------------------------------------------
    final_md = ws / "output" / "postmortem_final.md"
    if not final_md.exists():
        errors.append("missing output/postmortem_final.md — main-thread synthesis not completed")
        # Cannot proceed with content checks
        _print_result(errors)
        return 1 if errors else 0

    final_bytes = final_md.read_bytes()
    final_text = final_bytes.decode("utf-8", errors="ignore")
    if len(final_bytes) < 500:
        errors.append(
            f"output/postmortem_final.md is too short ({len(final_bytes)} bytes); "
            "expected >= 500 bytes for a substantive executive summary"
        )

    # ------------------------------------------------------------------
    # C. references to prior-round files (at least MIN_PRIOR_REFS of 5)
    # ------------------------------------------------------------------
    text_lower = final_text.lower()
    refs_hit = [f for f in PRIOR_ROUND_FILES if f.lower() in text_lower]
    if len(refs_hit) < MIN_PRIOR_REFS:
        errors.append(
            f"output/postmortem_final.md references only {len(refs_hit)} prior-round "
            f"file(s) ({refs_hit!r}); need >= {MIN_PRIOR_REFS} of {PRIOR_ROUND_FILES}"
        )

    # ------------------------------------------------------------------
    # D. root-cause anchors: 'deadlock' AND ('migration' OR 'v23')
    # ------------------------------------------------------------------
    if "deadlock" not in text_lower:
        errors.append(
            "output/postmortem_final.md missing root-cause keyword 'deadlock'"
        )
    if "migration" not in text_lower and "v23" not in text_lower:
        errors.append(
            "output/postmortem_final.md missing root-cause keyword 'migration' or 'v23'"
        )

    # ------------------------------------------------------------------
    # E. impact numbers
    # ------------------------------------------------------------------
    if not DURATION_RE.search(final_text):
        errors.append(
            "output/postmortem_final.md missing duration anchor '23 min(ute)'"
        )
    if not _has_user_anchor(final_text):
        errors.append(
            "output/postmortem_final.md missing user-impact number 4500 near 'users'/'affected'"
        )
    if not _has_revenue_anchor(final_text):
        errors.append(
            "output/postmortem_final.md missing revenue anchor '$87,000' or '87000'"
        )

    _print_result(errors)
    return 1 if errors else 0


def _print_result(errors: list[str]) -> None:
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
    else:
        print(
            "PASS: background RunSubagent launched; output/postmortem_final.md "
            "synthesizes prior-round findings with root-cause, impact numbers, "
            "and references to >= 3 prior output files"
        )


if __name__ == "__main__":
    sys.exit(main())
