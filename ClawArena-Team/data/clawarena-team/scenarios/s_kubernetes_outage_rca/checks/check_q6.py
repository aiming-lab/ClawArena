"""check_q6.py — Wave3 s_kubernetes_outage_rca q6 checker.

背景任务主导（类型 A bg）：
  - 后台发起 p99 历史数据拉取（has_background_run 为 True）
  - 主线同步整理 output/outage_rca.md（≥ 5 bullet，引用 ≥ 2 前轮产物，含 root_cause 关键词）

通过条件（全部满足，exit 0）：
  1. ADVISORY ONLY (non-gating): sessions/main.jsonl 中存在 RunSubagent(run_in_background=true)
  2. output/outage_rca.md 存在且有 ≥ 5 个 bullet 行
  3. output/outage_rca.md 引用 ≥ 2 个前轮产物文件名（rca_plan / oom_evidence / code_and_dashboard / rca_summary / postmortem）
  4. output/outage_rca.md 包含 root.cause（允许 root_cause / root-cause / root cause）
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterator


# ---------------------------------------------------------------------------
# sessions/main.jsonl 解析（复制自 WAVE4_AUTHORING_GUIDE §5.1 范式）
# ---------------------------------------------------------------------------


def _iter_tool_calls(ws: Path) -> Iterator[tuple[str, dict]]:
    """流式读 main.jsonl，yield 每个工具调用的 (name, args_dict)。

    兼容真实落盘的扁平形态
    {"role":"assistant","tool_calls":[{"id","name","arguments":{...}}]}、
    OpenAI 风格 {"function":{"name","arguments"}} 以及 Anthropic
    content-block {"type":"tool_use","name","input"}。arguments 可为 dict 或
    JSON 字符串。
    """
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

        # 扁平 / OpenAI 风格 tool_calls 列表
        for tc in ev.get("tool_calls") or []:
            if not isinstance(tc, dict):
                continue
            name = tc.get("name") or (tc.get("function") or {}).get("name") or ""
            args = tc.get("arguments")
            if args is None:
                args = (tc.get("function") or {}).get("arguments")
            if args is None:
                args = tc.get("args")
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    args = {}
            if name:
                yield str(name), (args if isinstance(args, dict) else {})

        # Anthropic content-block 形态
        content = ev.get("content")
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    name = block.get("name") or ""
                    args = block.get("input")
                    if name:
                        yield str(name), (args if isinstance(args, dict) else {})

        # legacy 扁平单工具事件
        if not ev.get("tool_calls") and not isinstance(content, list) and ev.get("tool"):
            args = ev.get("args") or ev.get("arguments") or {}
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    args = {}
            yield str(ev.get("tool")), (args if isinstance(args, dict) else {})


def has_background_run(ws: Path) -> bool:
    """检查是否存在 RunSubagent(run_in_background=true)。"""
    for name, args in _iter_tool_calls(ws):
        if name in ("RunSubagent", "Bash") and args.get("run_in_background"):
            return True
    return False


# ---------------------------------------------------------------------------
# 主检查
# ---------------------------------------------------------------------------

# 前轮产物文件名关键词（宽松匹配）
_PREV_ROUND_FILES = [
    r"rca_plan",
    r"oom_evidence",
    r"code_and_dashboard",
    r"rca_summary",
    r"postmortem",
]

# root_cause 多形态
_ROOT_CAUSE_PAT = re.compile(
    r"root[\s_\-]?cause",
    re.IGNORECASE,
)

# bullet 行：以 -、*、•、数字（含 N. N) N:）起头
_BULLET_PAT = re.compile(
    r"(?m)^[\s]*(?:[-*•]|\d+[.):])[\s]+\S",
)


def main(workspace: Path) -> int:
    # ------------------------------------------------------------------
    # 1. background RunSubagent
    # ------------------------------------------------------------------
    # instruction-following gate: prompt explicitly asks to launch this in the background
    if not has_background_run(workspace):
        print(
            "FAIL: background subagent not observed — the task asked you to launch this as a "
            "background RunSubagent(run_in_background=true) and not block the main thread"
        )
        return 1

    # ------------------------------------------------------------------
    # 2. output/outage_rca.md 存在且非空
    # ------------------------------------------------------------------
    rca_path = workspace / "output" / "outage_rca.md"
    if not rca_path.exists():
        print("FAIL: output/outage_rca.md not found")
        return 1

    text = rca_path.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 50:
        print("FAIL: output/outage_rca.md is too short (< 50 chars)")
        return 1

    # ------------------------------------------------------------------
    # 3. ≥ 5 bullet 行
    # ------------------------------------------------------------------
    bullets = _BULLET_PAT.findall(text)
    if len(bullets) < 5:
        print(
            f"FAIL: output/outage_rca.md has {len(bullets)} bullet line(s), "
            "need ≥ 5 (each finding should be a separate bullet)"
        )
        return 1

    # ------------------------------------------------------------------
    # 4. 引用 ≥ 2 前轮产物文件名
    # ------------------------------------------------------------------
    cited = [kw for kw in _PREV_ROUND_FILES if re.search(kw, text, re.IGNORECASE)]
    if len(cited) < 2:
        print(
            f"FAIL: output/outage_rca.md references only {len(cited)} prior-round "
            "file(s) — need ≥ 2 of: rca_plan, oom_evidence, code_and_dashboard, "
            "rca_summary, postmortem"
        )
        return 1

    # ------------------------------------------------------------------
    # 5. 含 root_cause 关键词
    # ------------------------------------------------------------------
    if not _ROOT_CAUSE_PAT.search(text):
        print(
            "FAIL: output/outage_rca.md does not contain 'root cause' / 'root_cause' "
            "/ 'root-cause' — the consolidated finding must name the root cause"
        )
        return 1

    print(
        f"PASS: outage_rca.md — background_run=True, {len(bullets)} bullets, "
        f"cited=[{', '.join(cited)}], root_cause present"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
