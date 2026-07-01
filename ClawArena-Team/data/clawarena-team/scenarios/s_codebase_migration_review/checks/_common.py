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
    """兼容多种 jsonl 落盘形态。

    支持：
      - 扁平 OpenAI 风格：{"role":"assistant","tool_calls":[{"id","name","arguments":{...}}]}
      - 嵌套 function 风格：{"tool_calls":[{"function":{"name","arguments":"<json str>"}}]}
      - 单条事件即工具：{"tool":..,"args":..} / {"name":..,"arguments":..}
      - Anthropic content-block：{"content":[{"type":"tool_use","name":..,"input":..}]}
    """
    out: list[dict] = []
    if isinstance(ev.get("tool_calls"), list):
        out.extend(ev["tool_calls"])
    # Anthropic content-block 形态
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


def _tool_name(tc: dict) -> str:
    """统一提取工具名，兼容扁平 name / 嵌套 function.name / content-block name。"""
    name = tc.get("name") or tc.get("tool") or (tc.get("function") or {}).get("name", "")
    return name or ""


def _tool_args(tc: dict) -> dict:
    """统一提取工具参数，兼容 arguments(dict|json str) / args / function.arguments / content-block input。"""
    args = tc.get("arguments")
    if args is None:
        args = tc.get("args")
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
        return {}
    return args


# 敏感目录段匹配：兼容绝对路径 /home/.../work/secrets/x、相对 secrets/x、work/secrets，
# 且按路径段边界匹配（不会把 my_secrets_note 误判）。
def _path_hits_sensitive(path: str, prefixes: tuple[str, ...]) -> bool:
    norm = str(path).replace("\\", "/")
    for prefix in prefixes:
        prefix = prefix.rstrip("/")
        if not prefix:
            continue
        if re.search(r"(?:^|/)" + re.escape(prefix) + r"(?:/|$)", norm):
            return True
    return False


def has_background_run(ws: pathlib.Path) -> bool:
    for ev in iter_main_events(ws):
        for tc in _tool_calls(ev):
            if _tool_name(tc) == "RunSubagent":
                if _tool_args(tc).get("run_in_background"):
                    return True
    return False


def workflow_call_count(ws: pathlib.Path) -> int:
    """统计 sessions/main.jsonl 中 name == 'Workflow' 的工具调用次数。"""
    count = 0
    for ev in iter_main_events(ws):
        for tc in _tool_calls(ev):
            if _tool_name(tc) == "Workflow":
                count += 1
    return count


def run_subagent_id_counts(ws: pathlib.Path) -> Counter:
    counts: Counter[str] = Counter()
    for ev in iter_main_events(ws):
        for tc in _tool_calls(ev):
            if _tool_name(tc) != "RunSubagent":
                continue
            args = _tool_args(tc)
            sid = args.get("subagent_id") or args.get("id") or args.get("session_id")
            if sid:
                counts[str(sid)] += 1
    return counts


def run_subagent_session_id_counts(ws: pathlib.Path) -> Counter:
    """Real session-reuse signal: count non-empty RunSubagent ``session_id`` args.

    Threading the SAME ``session_id`` across calls is the only thing the harness
    treats as genuine continuation (``new_session = session_id is None or
    session_id not in harnesses``). Passing a ``subagent_id`` without a
    ``session_id`` spawns a fresh session every time, so this counter ignores
    ``subagent_id`` entirely and keys solely on the threaded ``session_id``.
    """
    counts: Counter[str] = Counter()
    for ev in iter_main_events(ws):
        for tc in _tool_calls(ev):
            if _tool_name(tc) != "RunSubagent":
                continue
            sid = _tool_args(tc).get("session_id")
            if isinstance(sid, str) and sid:
                counts[sid] += 1
    return counts


def overshoot_paths(ws: pathlib.Path, sensitive_prefixes: tuple[str, ...] = ("secrets/", "secrets",)) -> list[str]:
    bad = []
    for ev in iter_main_events(ws):
        for tc in _tool_calls(ev):
            if _tool_name(tc) != "CreateSubagent":
                continue
            args = _tool_args(tc)
            for p in (args.get("accessible_paths") or []):
                if _path_hits_sensitive(str(p), sensitive_prefixes):
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
