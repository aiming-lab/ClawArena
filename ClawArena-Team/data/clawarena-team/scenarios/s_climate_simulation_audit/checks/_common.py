"""s_climate_simulation_audit — check 公共 helper。

与 POC _common.py 对齐，仅保留本场景所需的解析工具。
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
from collections import Counter
from typing import Iterator


def workspace_root() -> pathlib.Path:
    if len(sys.argv) < 2:
        print("usage: check_qN.py <workspace>", file=sys.stderr)
        sys.exit(2)
    return pathlib.Path(sys.argv[1]).resolve()


def iter_main_events(ws: pathlib.Path) -> Iterator[dict]:
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
    """兼容多种 jsonl 落盘形态。"""
    if "tool_calls" in ev and isinstance(ev["tool_calls"], list):
        return ev["tool_calls"]
    if ev.get("tool") or ev.get("name"):
        return [ev]
    return []


def run_subagent_id_counts(ws: pathlib.Path) -> Counter:
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
            sid = args.get("subagent_id") or args.get("id") or args.get("session_id")
            if sid:
                counts[str(sid)] += 1
    return counts


def run_subagent_session_id_counts(ws: pathlib.Path) -> Counter:
    """Real session-reuse signal: count non-empty RunSubagent ``session_id`` args.

    Threading the SAME ``session_id`` across calls is the only thing the harness
    treats as genuine continuation (``new_session = session_id is None or
    session_id not in harnesses``). Passing a ``subagent_id`` without a
    ``session_id`` spawns a fresh session every time, so this counter keys solely
    on the threaded ``session_id`` and ignores ``subagent_id``.
    """
    def _calls(ev: dict) -> list[dict]:
        out: list[dict] = []
        if isinstance(ev.get("tool_calls"), list):
            out.extend(t for t in ev["tool_calls"] if isinstance(t, dict))
        content = ev.get("content")
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    out.append(block)
        if out:
            return out
        if ev.get("tool") or ev.get("name") or ev.get("type") == "tool_use":
            return [ev]
        return []

    counts: Counter[str] = Counter()
    for ev in iter_main_events(ws):
        for tc in _calls(ev):
            name = tc.get("tool") or tc.get("name") or (tc.get("function") or {}).get("name", "")
            if name != "RunSubagent":
                continue
            args = tc.get("args")
            if args is None:
                args = tc.get("arguments")
            if args is None:
                args = (tc.get("function") or {}).get("arguments")
            if args is None and tc.get("type") == "tool_use":
                args = tc.get("input")
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {}
            if not isinstance(args, dict):
                continue
            sid = args.get("session_id")
            if isinstance(sid, str) and sid:
                counts[sid] += 1
    return counts


def fail(msg: str, code: int = 1) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(code)


def passed() -> None:
    print("OK")
    sys.exit(0)


def find_first_int_near(text: str, target: int, tolerance: int = 3) -> int | None:
    """从 text 中找出最接近 target 的整数（±tolerance）。"""
    nums = [int(m.group()) for m in re.finditer(r"\b\d+\b", text)]
    for n in nums:
        if abs(n - target) <= tolerance:
            return n
    return None


def has_phrase_any(text: str, phrases: list[str]) -> bool:
    low = text.lower()
    return any(p.lower() in low for p in phrases)
