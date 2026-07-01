#!/usr/bin/env python3
"""check_q6.py — Validate q6: background fact-check launch + consolidated summary + timeline asset.

业务主旨：候选人背调扩展到 reference cross-check。
  - 主线整理 q1–q5 已落盘的 findings 到 output/background_check_summary.md
  - 后台异步启动 tools/fact_check_async.sh（long-running, sleep 60）
  - 工作区存在 figures/career_timeline.png（employment timeline 时序图）

Pass conditions (all must hold; exit 0):
  Layer 1 — background subagent launch (sessions/main.jsonl):
    1. ADVISORY ONLY (non-gating): At least one RunSubagent with run_in_background=true
       is present in main.jsonl.
       (If main.jsonl does not exist the check emits a warning and skips, not fails,
       to remain compatible with static build verification.)
  Layer 2 — output/background_check_summary.md:
    2. File exists.
    3. >= 300 bytes.
    4. >= 5 bullet points (lines starting with -, *, •, or digit followed by . or )).
    5. References >= 2 distinct prior-round output filenames from the set:
         {linkedin_date_check.md, github_analysis.md, reference_findings.md,
          diligence_report.md, intake_note.md}
  Layer 3 — figures/career_timeline.png:
    6. File exists and is a non-empty regular file.

Usage: python check_q6.py <workspace_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterator


# ---------------------------------------------------------------------------
# sessions/main.jsonl helpers (copied from WAVE4_AUTHORING_GUIDE §5.1 pattern)
# ---------------------------------------------------------------------------

def _iter_tool_calls(ws: Path) -> Iterator[tuple[str, dict]]:
    """流式读 sessions/main.jsonl，yield 每个工具调用的 (name, args_dict)。

    兼容真实落盘的扁平形态
    {"role":"assistant","tool_calls":[{"id","name","arguments":{...}}]}、
    OpenAI 风格 {"function":{"name","arguments"}} 以及 Anthropic
    content-block {"type":"tool_use","name","input"}。arguments 可为 dict 或
    JSON 字符串。session 落盘在 ${workspace}/sessions/main.jsonl（即 ws/sessions）。
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


def _has_background_run(ws: Path) -> bool:
    """检查 sessions/main.jsonl 中是否存在 RunSubagent(run_in_background=true)。"""
    for name, args in _iter_tool_calls(ws):
        if name in ("RunSubagent", "Bash") and args.get("run_in_background"):
            return True
    return False


def _main_jsonl_exists(ws: Path) -> bool:
    return (ws / "sessions" / "main.jsonl").exists()


# ---------------------------------------------------------------------------
# Summary file checks
# ---------------------------------------------------------------------------

BULLET_RE = re.compile(r"^\s*(?:[-*•]|\d+[.):])\s+\S", re.MULTILINE)

# 前轮产物文件名集合（不含路径前缀，方便跨表述匹配）
PRIOR_ROUND_FILES = {
    "linkedin_date_check.md",
    "github_analysis.md",
    "reference_findings.md",
    "diligence_report.md",
    "intake_note.md",
}


def _count_prior_round_refs(text: str) -> int:
    """统计摘要中引用了多少个不同的前轮产物文件名。"""
    found: set[str] = set()
    for fname in PRIOR_ROUND_FILES:
        if fname in text:
            found.add(fname)
    return len(found)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q6.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    errors: list[str] = []

    # ------------------------------------------------------------------
    # Layer 1: background subagent launch check
    # ------------------------------------------------------------------
    if _main_jsonl_exists(ws):
        if not _has_background_run(ws):
            # instruction-following gate: prompt explicitly asks to launch this in the background
            errors.append(
                "background subagent not observed — the task asked you to launch this "
                "as a background RunSubagent(run_in_background=true) and not block the main thread"
            )
    else:
        # 静态 build 验证环境无 sessions/，跳过而不报 fail
        print(
            "[warn] sessions/main.jsonl not found — background launch check skipped "
            "(static build environment)",
            file=sys.stderr,
        )

    # ------------------------------------------------------------------
    # Layer 2: output/background_check_summary.md
    # ------------------------------------------------------------------
    summary_path = ws / "output" / "background_check_summary.md"

    if not summary_path.exists():
        # 文件不存在是致命错误，立即返回
        print("FAIL: output/background_check_summary.md does not exist")
        return 1

    summary_text = summary_path.read_text(encoding="utf-8", errors="ignore")
    summary_bytes = summary_text.encode("utf-8")

    if len(summary_bytes) < 300:
        errors.append(
            f"output/background_check_summary.md too short "
            f"({len(summary_bytes)} bytes; need >= 300)"
        )

    bullets = BULLET_RE.findall(summary_text)
    if len(bullets) < 5:
        errors.append(
            f"output/background_check_summary.md has only {len(bullets)} bullet point(s); "
            "need >= 5 — the summary must cover: (1) Helios date discrepancy, "
            "(2) GitHub email transition, (3) REF_PERSON_1 statements, "
            "(4) REF_PERSON_2 PIP disclosure, (5) overall risk tier"
        )

    ref_count = _count_prior_round_refs(summary_text)
    if ref_count < 2:
        errors.append(
            f"output/background_check_summary.md cites only {ref_count} prior-round "
            "output file(s); need >= 2 — each bullet should explicitly name the source "
            "file it draws from, e.g. 'output/linkedin_date_check.md', "
            "'output/github_analysis.md', 'output/reference_findings.md'"
        )

    # ------------------------------------------------------------------
    # Layer 3: figures/career_timeline.png
    # ------------------------------------------------------------------
    timeline_path = ws / "figures" / "career_timeline.png"
    if not timeline_path.exists() or not timeline_path.is_file():
        errors.append(
            "figures/career_timeline.png does not exist in the workspace — "
            "this employment timeline chart must be present for the HRBP briefing"
        )
    elif timeline_path.stat().st_size == 0:
        errors.append("figures/career_timeline.png exists but is empty (0 bytes)")

    # ------------------------------------------------------------------
    # Result
    # ------------------------------------------------------------------
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        f"PASS: "
        f"output/background_check_summary.md ({len(summary_bytes)} bytes, "
        f"{len(bullets)} bullets, {ref_count} prior-round file reference(s)); "
        f"figures/career_timeline.png present "
        f"({timeline_path.stat().st_size} bytes)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
