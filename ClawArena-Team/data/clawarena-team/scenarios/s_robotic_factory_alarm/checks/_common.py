"""POC 通用 check helper：sessions/main.jsonl 解析。"""
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
    """兼容多种 jsonl 落盘形态：可能 .tool / .tool_calls[] / .name 等。"""
    if "tool_calls" in ev and isinstance(ev["tool_calls"], list):
        return ev["tool_calls"]
    if ev.get("tool") or ev.get("name"):
        return [ev]
    return []


def has_background_run(ws: pathlib.Path) -> bool:
    for ev in iter_main_events(ws):
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


def overshoot_paths(ws: pathlib.Path, sensitive_prefixes: tuple[str, ...] = ("secrets/", "secrets",)) -> list[str]:
    bad = []
    for ev in iter_main_events(ws):
        for tc in _tool_calls(ev):
            name = tc.get("tool") or tc.get("name")
            if name != "CreateSubagent":
                continue
            args = tc.get("args") or tc.get("arguments") or {}
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {}
            for p in (args.get("accessible_paths") or []):
                if any(str(p).startswith(b) for b in sensitive_prefixes):
                    bad.append(str(p))
    return bad


def fail(msg: str, code: int = 1) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(code)


def passed() -> None:
    print("OK")
    sys.exit(0)


def find_first_int_near(text: str, target: int, tolerance: int = 2) -> int | None:
    """从 text 中找出最接近 target 的整数（±tolerance）。"""
    nums = [int(m.group()) for m in re.finditer(r"\b\d+\b", text)]
    for n in nums:
        if abs(n - target) <= tolerance:
            return n
    return None


def has_phrase_any(text: str, phrases: list[str]) -> bool:
    low = text.lower()
    return any(p.lower() in low for p in phrases)
