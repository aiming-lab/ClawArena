#!/usr/bin/env python3
"""把 openclaw 框架数据集转换为 clawarena-native 框架数据集。

读取（只读）原始 ``<SRC_ROOT>/data/<root>/openclaw/``，产出到
``<DST_ROOT>/data/<root>/clawarena-native/``。

转换要点：
- 会话 jsonl：openclaw 冗长格式（type/id/parentId/timestamp/message{role,content[]}
  + 控制事件 session/model_change/thinking_level_change/custom）→ native 紧凑格式
  （每行 ``{role, content[, tool_calls]}``，仅保留 type==message 行，去全部冗余字段）。
- 布局精简：openclaw 的 ``state/agents/{id}/sessions/`` → native 的 ``state/{id}/``；
  agent_dir 写成 ``state/{id}``。
- main session 的首条 user 消息（持久化的 persona/system 提示）转成 native
  ``SystemMessage``（role=system, subtype=prompt），其余为 user/assistant；history
  session 全部按 user/assistant 转（其首条是真实渠道消息，不当 system）。
- ``sessions.json`` 索引（key=session_id，去 openclaw 的 ``agent:`` 前缀/lastChannel）。
- updates：session 源 jsonl 一并转 native；workspace 文件原样复制；group 原样保留。

用法::

    python scripts/convert_openclaw_to_native.py \
        --src-root /home/xkaiwen/workspace/ClawArena \
        --dst-root /home/xkaiwen/workspace/tmp/clawarena-native \
        --roots clawarena metaclaw-bench metaclaw-bench-small
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# 内容 / 消息行转换
# ---------------------------------------------------------------------------
def _coerce_text(content: Any) -> tuple[str, list[dict]]:
    """把 openclaw 的 content（str 或 block 数组）拍平为 (text, tool_calls)。"""
    if isinstance(content, str):
        return content, []
    if not isinstance(content, list):
        return ("" if content is None else str(content)), []
    texts: list[str] = []
    tool_calls: list[dict] = []
    for b in content:
        if not isinstance(b, dict):
            texts.append(str(b))
            continue
        t = b.get("type")
        if t == "text":
            texts.append(b.get("text", ""))
        elif t == "tool_use":
            tool_calls.append(
                {"id": b.get("id", ""), "name": b.get("name", ""), "arguments": b.get("input", {})}
            )
        elif t == "tool_result":
            inner, _ = _coerce_text(b.get("content"))
            if inner:
                texts.append(inner)
        elif t in ("image", "image_url", "audio", "video"):
            texts.append(f"[{t}]")
    return "\n".join(x for x in texts if x), tool_calls


def convert_session(src_path: Path, dst_path: Path, *, is_main: bool) -> int:
    """转换一个 openclaw session jsonl → native 紧凑 jsonl。返回写出的消息条数。"""
    out: list[dict] = []
    system_done = False
    try:
        raw_lines = src_path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        raw_lines = []
    for raw in raw_lines:
        raw = raw.strip()
        if not raw:
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if obj.get("type") != "message":
            continue  # 丢弃 session/model_change/thinking_level_change/custom 控制事件
        msg = obj.get("message") or {}
        role = str(msg.get("role", "")).strip()
        if not role:
            continue
        text, tool_calls = _coerce_text(msg.get("content"))
        if is_main and not system_done and role == "user":
            # main session 首条 user = persona/system 提示 → native SystemMessage
            out.append({"role": "system", "subtype": "prompt", "content": text})
            system_done = True
            continue
        line: dict[str, Any] = {"role": role, "content": text}
        if role == "assistant" and tool_calls:
            line["tool_calls"] = tool_calls
        out.append(line)
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    # 末尾补 \n：jsonl 每行（含末行）以换行结尾，避免后续 append 新消息时拼到末行尾部。
    dst_path.write_text(
        "".join(json.dumps(o, ensure_ascii=False) + "\n" for o in out),
        encoding="utf-8",
    )
    return sum(1 for o in out if o.get("role") in ("user", "assistant", "tool_result"))


def _guess_channel(filename: str) -> str:
    lower = filename.lower()
    for ch in ("feishu", "slack", "discord", "telegram", "wechat", "email", "im", "ticket", "kefu"):
        if ch in lower:
            return ch
    return "unknown"


# ---------------------------------------------------------------------------
# 数据集转换
# ---------------------------------------------------------------------------
def convert_dataset(src_oc: Path, dst_native: Path) -> dict[str, Any]:
    src_manifest = json.loads((src_oc / "manifest.json").read_text(encoding="utf-8"))
    if dst_native.exists():
        shutil.rmtree(dst_native)
    dst_native.mkdir(parents=True)

    native_manifest: dict[str, Any] = {
        "framework": "clawarena-native",
        "state_dir": "state",
        "workspaces_dir": "workspaces",
        "updates_dir": "updates",
        "agents": {},
        "updates": {},
    }
    stats = {"agents": 0, "sessions": 0, "messages": 0, "updates": 0}

    for tid, info in src_manifest.get("agents", {}).items():
        agent_id = info.get("agent_id", tid)
        oc_agent_dir = src_oc / info.get("agent_dir", f"state/agents/{agent_id}")
        oc_sessions = oc_agent_dir / "sessions"
        dst_agent_dir = dst_native / "state" / agent_id
        dst_agent_dir.mkdir(parents=True, exist_ok=True)

        index: dict[str, Any] = {}
        # main session
        main_sid = info.get("session", "")
        if main_sid:
            src_main = oc_sessions / f"{main_sid}.jsonl"
            if src_main.exists():
                n = convert_session(src_main, dst_agent_dir / f"{main_sid}.jsonl", is_main=True)
                stats["sessions"] += 1
                stats["messages"] += n
            index[main_sid] = {
                "session_file": f"{main_sid}.jsonl",
                "channel": "main",
                "is_active": True,
                "updated_at": 0,
            }
        # history sessions
        for hsid in info.get("history_sessions", []) or []:
            src_h = oc_sessions / f"{hsid}.jsonl"
            if src_h.exists():
                n = convert_session(src_h, dst_agent_dir / f"{hsid}.jsonl", is_main=False)
                stats["sessions"] += 1
                stats["messages"] += n
            index[hsid] = {
                "session_file": f"{hsid}.jsonl",
                "channel": _guess_channel(hsid),
                "is_active": False,
                "updated_at": 0,
            }
        (dst_agent_dir / "sessions.json").write_text(
            json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # workspace（原样复制）
        ws_rel = info.get("workspace", f"workspaces/{agent_id}")
        src_ws = src_oc / ws_rel
        dst_ws = dst_native / "workspaces" / agent_id
        if src_ws.exists():
            shutil.copytree(src_ws, dst_ws, dirs_exist_ok=True)
        else:
            dst_ws.mkdir(parents=True, exist_ok=True)

        native_manifest["agents"][tid] = {
            "agent_id": agent_id,
            "agent_dir": f"state/{agent_id}",
            "session": main_sid,
            "history_sessions": list(info.get("history_sessions", []) or []),
            "workspace": f"workspaces/{agent_id}",
        }
        stats["agents"] += 1

    # updates
    for tid, group in (src_manifest.get("updates", {}) or {}).items():
        agent_id = src_manifest.get("agents", {}).get(tid, {}).get("agent_id", tid)
        native_group: dict[str, Any] = {}
        for uid, meta in group.items():
            utype = meta.get("type", "")
            if utype == "group":
                native_group[uid] = {
                    "type": "group",
                    "children": list(meta.get("children", []) or []),
                }
                continue
            rel_dir = meta.get("dir", f"updates/{agent_id}/{uid}")
            src_dir = src_oc / rel_dir
            dst_dir = dst_native / rel_dir
            dst_dir.mkdir(parents=True, exist_ok=True)
            files = meta.get("files", []) or []
            for item in files:
                name = item if isinstance(item, str) else item.get("name", "")
                if not name:
                    continue
                s = src_dir / name
                d = dst_dir / name
                d.parent.mkdir(parents=True, exist_ok=True)
                if not s.exists():
                    continue
                if utype == "session":
                    convert_session(s, d, is_main=False)  # update 片段全部按非 main 转
                else:  # workspace
                    shutil.copy2(s, d)
            native_group[uid] = {
                "type": utype,
                "dir": rel_dir,
                "files": files,
            }
            stats["updates"] += 1
        native_manifest["updates"][tid] = native_group

    (dst_native / "manifest.json").write_text(
        json.dumps(native_manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return stats


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src-root", default="/home/xkaiwen/workspace/ClawArena")
    ap.add_argument("--dst-root", default="/home/xkaiwen/workspace/tmp/clawarena-native")
    ap.add_argument("--roots", nargs="+", default=["clawarena", "metaclaw-bench", "metaclaw-bench-small"])
    args = ap.parse_args()

    for root in args.roots:
        src_oc = Path(args.src_root) / "data" / root / "openclaw"
        dst_native = Path(args.dst_root) / "data" / root / "clawarena-native"
        if not (src_oc / "manifest.json").exists():
            print(f"[skip] {root}: no openclaw manifest at {src_oc}")
            continue
        stats = convert_dataset(src_oc, dst_native)
        print(f"[{root}] -> {dst_native}")
        print(f"    agents={stats['agents']} sessions={stats['sessions']} "
              f"messages={stats['messages']} update_entries={stats['updates']}")


if __name__ == "__main__":
    main()
