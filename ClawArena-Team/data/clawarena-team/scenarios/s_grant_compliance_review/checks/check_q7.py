#!/usr/bin/env python3
"""check_q7.py — Validate q7 (C 混合：background audit + session_reuse final synthesis).

Pass conditions (all must hold):
  1. ADVISORY ONLY (non-gating): has_background_run(ws) is True
     — main.jsonl 中存在 RunSubagent(run_in_background=true)。
  2. ADVISORY ONLY (non-gating): run_subagent_id_counts(ws).most_common(1)[0][1] >= 2
     — 至少有一个 subagent_id 被 RunSubagent 调用 ≥ 2 次（session_reuse）。
  3. output/final_compliance_audit.md 存在且 >= 5 bullet。
  4. final_compliance_audit.md 中引用 ≥ 2 个前轮产物文件名（output/ 目录中）。
  5. workspace/figures/grant_flow_diagram.png 存在（模型需读取并引用）。

Usage: python check_q7.py <workspace_abs_path>
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
# sessions/main.jsonl 解析（自包含，不依赖外部 helper）
# ---------------------------------------------------------------------------

BULLET_RE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+\S", re.MULTILINE)

# 前轮产物文件名白名单（q1–q6 输出）
PRIOR_ROUND_FILES = [
    "audit_intake.md",
    "terms_crosstab.md",
    "receipt_verification.md",
    "noncompliance_list.md",
    "compliance_report.md",
]


def _iter_main_events(ws: Path) -> Iterator[dict]:
    """流式读 sessions/main.jsonl，跳过不可解析行。"""
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
    """兼容多种 jsonl 落盘形态：.tool / .tool_calls[] / .name 等。"""
    if "tool_calls" in ev and isinstance(ev["tool_calls"], list):
        return ev["tool_calls"]
    if ev.get("tool") or ev.get("name"):
        return [ev]
    return []


def has_background_run(ws: Path) -> bool:
    """返回 True 当且仅当 sessions/main.jsonl 中存在 background RunSubagent。"""
    for ev in _iter_main_events(ws):
        for tc in _tool_calls(ev):
            name = tc.get("tool") or tc.get("name")
            if name in ("RunSubagent", "Bash"):
                args = tc.get("args") or tc.get("arguments") or {}
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except Exception:
                        args = {}
                rib = args.get("run_in_background")
                if rib in (True, 1) or (
                    isinstance(rib, str) and rib.strip().lower() in ("true", "1", "yes")
                ):
                    return True
                if name == "Bash":
                    _cmd = str(args.get("command") or args.get("cmd") or "")
                    if (
                        re.search(r"(?<!&)&\s*$", _cmd.strip())
                        or re.search(r"(?:^|\s)(?:nohup|setsid)\b", _cmd)
                        or "disown" in _cmd
                    ):
                        return True
    return False


def run_subagent_id_counts(ws: Path) -> Counter:
    """统计每个 subagent_id 被 RunSubagent 调用的次数。"""
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


# ---------------------------------------------------------------------------
# main check
# ---------------------------------------------------------------------------


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q7.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1]).resolve()
    errors: list[str] = []

    # 1. has_background_run
    # instruction-following gate: prompt explicitly asks to launch this in the background
    if not has_background_run(ws):
        errors.append(
            "background subagent not observed — the task asked you to launch this as a "
            "background RunSubagent(run_in_background=true) and not block the main thread"
        )

    # 2. session_reuse: max per-subagent_id count >= 2 (advisory only, non-gating)
    counts = run_subagent_id_counts(ws)
    if counts:
        top_count = counts.most_common(1)[0][1]
    else:
        top_count = 0
    if top_count < 2:
        print(
            "NOTE: session reuse not verified — advisory only, non-gating",
            file=sys.stderr,
        )

    # 3. output/final_compliance_audit.md exists and has >= 5 bullets
    audit_path = ws / "output" / "final_compliance_audit.md"
    if not audit_path.exists():
        errors.append(
            "output/final_compliance_audit.md is missing. q7 requires the model to produce "
            "a final compliance audit report synthesising all prior rounds."
        )
    else:
        text = audit_path.read_text(encoding="utf-8", errors="ignore")
        bullets = BULLET_RE.findall(text)
        if len(bullets) < 5:
            errors.append(
                f"output/final_compliance_audit.md has only {len(bullets)} bullet point(s); "
                "expected >= 5. The final audit report must include a structured bullet list "
                "covering key findings, resolved items, outstanding NC codes, and next steps."
            )

        # 4. references >= 2 prior-round output files
        referenced = [fname for fname in PRIOR_ROUND_FILES if fname in text]
        if len(referenced) < 2:
            errors.append(
                f"output/final_compliance_audit.md references only {len(referenced)} prior-round "
                f"file(s) ({referenced}); expected >= 2. The report must explicitly cite at least "
                "two of the prior deliverables: audit_intake.md, terms_crosstab.md, "
                "receipt_verification.md, noncompliance_list.md, compliance_report.md."
            )

    # 5. figures/grant_flow_diagram.png exists (model should have read and referenced it)
    diagram_path = ws / "figures" / "grant_flow_diagram.png"
    if not diagram_path.exists():
        errors.append(
            "workspace/figures/grant_flow_diagram.png is missing. The engineering diagram "
            "must be present so the model can reference the grant flow when composing the "
            "final compliance audit."
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
