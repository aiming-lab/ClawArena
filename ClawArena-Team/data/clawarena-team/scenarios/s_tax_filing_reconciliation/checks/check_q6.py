#!/usr/bin/env python3
"""check_q6.py — wave3 s_tax_filing_reconciliation q6 checker.

通过条件（全部满足，exit 0）：
  1. [ADVISORY ONLY (non-gating)] sessions/main.jsonl 中存在 RunSubagent(run_in_background=true)（后台任务已启动）
  2. output/filing_summary.md 存在且 ≥ 200 chars
  3. output/filing_summary.md 含 ≥ 5 个 bullet（行首 '- ' 或 '* '）
  4. output/filing_summary.md 引用 ≥ 2 个前轮产物关键词
     （filing_plan / income_summary / rental_audit / lacerte_update / client_letter）
  5. output/filing_summary.md 含决策关键词 file_amendment 或 no_amendment
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterator


# ---------------------------------------------------------------------------
# sessions/main.jsonl 解析 helper（wave4 范式，复制至本 check）
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
    if "tool_calls" in ev and isinstance(ev["tool_calls"], list):
        return ev["tool_calls"]
    if ev.get("tool") or ev.get("name"):
        return [ev]
    return []


# 视为"可能发起后台任务"的工具名集合。
#   - Bash:           直接以 run_in_background 或 shell 后台语法发起 tax_agg.sh
#   - RunSubagent:    把后台任务委派给子代理执行（run_in_background=true）
#   - CreateSubagent: 真实运行中创建子代理所用的工具名；当其 prompt/system_prompt
#                     中以后台方式发起 tax_agg.sh 时也应被识别（旧逻辑漏掉了它）
_LAUNCH_TOOL_NAMES = ("RunSubagent", "Bash", "CreateSubagent")

# shell 后台启动语法：结尾 '&'（排除 '&&'）、nohup/setsid、disown
_BG_SHELL_RE = re.compile(r"(?<!&)&\s*$")
_BG_NOHUP_RE = re.compile(r"(?:^|\s)(?:nohup|setsid)\b")


def _is_truthy_rib(rib) -> bool:
    if rib in (True, 1):
        return True
    return isinstance(rib, str) and rib.strip().lower() in ("true", "1", "yes")


def _launches_aggregate_in_background(text: str) -> bool:
    """文本中是否以后台方式启动 tax_agg.sh（用于扫描 Bash 命令或子代理 prompt）。"""
    if "tax_agg.sh" not in text:
        # 若委派文本没有点名聚合脚本，则仅在出现明确后台 shell 语法时不作判定，
        # 避免把无关子代理误判为后台聚合任务。
        return False
    for segment in text.splitlines():
        seg = segment.strip()
        if (
            _BG_SHELL_RE.search(seg)
            or _BG_NOHUP_RE.search(seg)
            or "disown" in seg
            or "run_in_background" in seg
        ):
            return True
    return False


def _has_background_run(ws: Path) -> bool:
    for ev in _iter_main_events(ws):
        for tc in _tool_calls(ev):
            name = tc.get("tool") or tc.get("name")
            if name not in _LAUNCH_TOOL_NAMES:
                continue
            args = tc.get("args") or tc.get("arguments") or {}
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {}
            if not isinstance(args, dict):
                continue
            # 1) 显式 run_in_background 字段（Bash / RunSubagent / CreateSubagent 通用）
            if _is_truthy_rib(args.get("run_in_background")):
                return True
            # 2) Bash：直接命令里带 shell 后台语法
            if name == "Bash":
                _cmd = str(args.get("command") or args.get("cmd") or "")
                if (
                    _BG_SHELL_RE.search(_cmd.strip())
                    or _BG_NOHUP_RE.search(_cmd)
                    or "disown" in _cmd
                ):
                    return True
            # 3) 子代理类工具：把后台启动 tax_agg.sh 的指令写进 prompt/system_prompt
            if name in ("RunSubagent", "CreateSubagent"):
                _delegated = " ".join(
                    str(args.get(k) or "")
                    for k in ("prompt", "system_prompt", "command", "task")
                )
                if _launches_aggregate_in_background(_delegated):
                    return True
    return False


# ---------------------------------------------------------------------------
# 前轮产物关键词集
# ---------------------------------------------------------------------------

_PRIOR_ROUND_KEYWORDS = [
    "filing_plan",
    "income_summary",
    "rental_audit",
    "lacerte_update",
    "client_letter",
    "irs_disclosure",
]

# 决策关键词
_DECISION_KEYWORDS = ["file_amendment", "no_amendment"]


# ---------------------------------------------------------------------------
# 主检查逻辑
# ---------------------------------------------------------------------------


def _count_bullets(text: str) -> int:
    count = 0
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- ") or stripped.startswith("* "):
            count += 1
    return count


def _count_prior_round_refs(text: str) -> int:
    low = text.lower()
    return sum(1 for kw in _PRIOR_ROUND_KEYWORDS if kw in low)


def _has_decision_keyword(text: str) -> bool:
    low = text.lower()
    return any(kw in low for kw in _DECISION_KEYWORDS)


def main(workspace: Path) -> int:
    summary = workspace / "output" / "filing_summary.md"

    # 1. background RunSubagent
    # instruction-following gate: prompt explicitly asks to launch this in the background
    if not _has_background_run(workspace):
        print(
            "FAIL: background subagent not observed — the task asked you to launch this "
            "as a background RunSubagent(run_in_background=true) and not block the main thread",
            file=sys.stderr,
        )
        return 1

    # 2. output/filing_summary.md 存在且足够长
    if not summary.exists():
        print("FAIL: output/filing_summary.md not found", file=sys.stderr)
        return 1

    text = summary.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 200:
        print(
            f"FAIL: output/filing_summary.md too short ({len(text.strip())} chars, need ≥ 200)",
            file=sys.stderr,
        )
        return 1

    # 3. ≥ 5 bullet points
    bullet_count = _count_bullets(text)
    if bullet_count < 5:
        print(
            f"FAIL: output/filing_summary.md has {bullet_count} bullet point(s), need ≥ 5 "
            "(lines starting with '- ' or '* ')",
            file=sys.stderr,
        )
        return 1

    # 4. 引用 ≥ 2 个前轮产物
    ref_count = _count_prior_round_refs(text)
    if ref_count < 2:
        found = [kw for kw in _PRIOR_ROUND_KEYWORDS if kw in text.lower()]
        print(
            f"FAIL: output/filing_summary.md references {ref_count} prior output file(s) "
            f"(found: {found}), need ≥ 2 from "
            f"{_PRIOR_ROUND_KEYWORDS}",
            file=sys.stderr,
        )
        return 1

    # 5. 含决策关键词
    if not _has_decision_keyword(text):
        print(
            "FAIL: output/filing_summary.md must contain amendment decision keyword — "
            "use 'file_amendment' (if amended return needed) or 'no_amendment' (if complete)",
            file=sys.stderr,
        )
        return 1

    print(
        "PASS: background task launched; output/filing_summary.md has "
        f"{bullet_count} bullets, {ref_count} prior-round refs, and amendment decision keyword."
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
