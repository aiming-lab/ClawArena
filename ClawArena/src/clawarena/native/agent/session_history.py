"""跨 session 历史读取（仿 openclaw 的多 session + sessions.json 索引设计）。

clawarena-native 的一个 agent 可拥有多条 session：一条 **active**（当前 round 在写的
主 session）+ 若干 **history** session（数据集预置的、来自其它 channel / 时间线的对话
记录）。main agent 通过 :class:`SessionHistoryTool` 读取这些历史 session 的消息记录。

这纠正了 picoclaw / nanobot 把历史记录摊平成 md 文件的做法——历史记录以独立 jsonl
分开存、用 ``sessions.json`` 索引，结构精简（直接以 session_id 为键，去掉 openclaw 的
``agent:{id}:`` 前缀与 lastChannel 等冗余字段；jsonl 沿用 native Message 紧凑 schema）。

``sessions.json`` 结构（每个 agent 一个，位于其 sessions 目录下）::

    {
      "<session_id>": {
        "session_file": "<session_id>.jsonl",
        "channel": "main",          # 来源标签：main / wechat / email / ...
        "is_active": true,          # 当前 round 在写的主 session
        "updated_at": 0             # 毫秒时间戳（统计用，可为 0）
      },
      ...
    }
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional


class SessionHistoryStore:
    """封装一个 agent 的 sessions 目录：sessions.json 索引 + 各 session jsonl 读取。"""

    def __init__(self, sessions_dir: Path, active_session_id: str):
        self.sessions_dir = Path(sessions_dir)
        self.active_session_id = active_session_id
        self.index_path = self.sessions_dir / "sessions.json"

    # ------------------------------------------------------------------
    # 索引
    # ------------------------------------------------------------------
    def load_index(self) -> dict[str, dict[str, Any]]:
        if not self.index_path.exists():
            return {}
        try:
            data = json.loads(self.index_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
        return data if isinstance(data, dict) else {}

    def upsert(
        self,
        session_id: str,
        *,
        channel: str = "main",
        is_active: bool = False,
        updated_at: int = 0,
    ) -> None:
        """登记 / 更新一条 session（init_session 写 active；数据集预置 history）。"""
        index = self.load_index()
        index[session_id] = {
            "session_file": f"{session_id}.jsonl",
            "channel": channel,
            "is_active": is_active,
            "updated_at": updated_at,
        }
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(
            json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    # ------------------------------------------------------------------
    # 读取
    # ------------------------------------------------------------------
    def list_history(self) -> list[dict[str, Any]]:
        """列出除 active 之外的所有 session（即可读历史）。"""
        out: list[dict[str, Any]] = []
        for sid, meta in self.load_index().items():
            if sid == self.active_session_id or meta.get("is_active"):
                continue
            out.append(
                {
                    "session_id": sid,
                    "channel": meta.get("channel", ""),
                    "updated_at": meta.get("updated_at", 0),
                    "messages": self._count_messages(sid, meta),
                }
            )
        out.sort(key=lambda e: e.get("updated_at", 0))
        return out

    def read_session(self, session_id: str, *, max_chars: int = 60000) -> str:
        """渲染指定 session 的 user/assistant/tool_result 转写（system 不回显）。

        仅允许读取 sessions.json 中登记过的 session，越权返回 forbidden 提示。
        """
        index = self.load_index()
        meta = index.get(session_id)
        if meta is None:
            avail = [s for s in index if s != self.active_session_id]
            return (
                f"forbidden: session '{session_id}' is not registered for this agent. "
                f"Available history sessions: {avail}"
            )
        path = self.sessions_dir / str(meta.get("session_file") or f"{session_id}.jsonl")
        if not path.exists():
            return f"session '{session_id}' has no transcript file on disk."
        lines = self._render_transcript(path)
        text = "\n".join(lines)
        if len(text) > max_chars:
            text = text[:max_chars] + f"\n…[truncated at {max_chars} chars]"
        header = f"=== session {session_id} (channel={meta.get('channel','')}) ===\n"
        return header + (text or "[empty session]")

    # ------------------------------------------------------------------
    # 内部
    # ------------------------------------------------------------------
    def _iter_raw(self, path: Path) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        except OSError:
            return []
        return rows

    def _count_messages(self, session_id: str, meta: dict[str, Any]) -> int:
        path = self.sessions_dir / str(meta.get("session_file") or f"{session_id}.jsonl")
        if not path.exists():
            return 0
        return sum(
            1
            for r in self._iter_raw(path)
            if r.get("role") in ("user", "assistant", "tool_result")
        )

    def _render_transcript(self, path: Path) -> list[str]:
        out: list[str] = []
        for r in self._iter_raw(path):
            role = r.get("role")
            if role not in ("user", "assistant", "tool_result"):
                continue  # 跳过 system / compact boundary 等
            content = (r.get("content") or "").strip()
            if role == "user":
                out.append(f"[user]\n{content}")
            elif role == "assistant":
                seg = f"[assistant]\n{content}" if content else "[assistant]"
                tcs = r.get("tool_calls") or []
                if tcs:
                    names = ", ".join(str(tc.get("name", "")) for tc in tcs)
                    seg += f"\n  (tool calls: {names})"
                out.append(seg)
            else:  # tool_result
                tool = (r.get("meta") or {}).get("tool", "")
                out.append(f"[tool_result {tool}]\n{content}")
        return out
