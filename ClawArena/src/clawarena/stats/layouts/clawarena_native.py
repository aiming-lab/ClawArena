"""clawarena-native layout —— 多 session（仿 openclaw），但精简布局：

session jsonl 直接落在 ``agent_dir`` 下（无 openclaw 的 ``sessions/`` 子层），且用 native
紧凑格式（每行 ``{role, content, tool_calls?}``）。token 统计沿用通用的 flat-role 解析器。
"""
from __future__ import annotations

from pathlib import Path

from clawarena.stats.base import FrameworkLayout
from clawarena.stats.session_parser import parse_flat_role_jsonl


class ClawArenaNativeLayout(FrameworkLayout):
    """clawarena-native 把 main + history session 以 native jsonl 存于 agent_dir 下。"""

    @property
    def name(self) -> str:
        return "clawarena-native"

    @property
    def main_session_parser(self):
        return parse_flat_role_jsonl

    @property
    def history_session_parser(self):
        return parse_flat_role_jsonl

    def _agent_dir(self, agent_info: dict, manifest_dir: Path) -> Path | None:
        rel = agent_info.get("agent_dir")
        return manifest_dir / rel if rel else None

    def main_session_path(
        self, agent_info: dict, manifest_dir: Path, sid: str,
    ) -> Path | None:
        ad = self._agent_dir(agent_info, manifest_dir)
        sess = agent_info.get("session", "")
        if not ad or not sess:
            return None
        return ad / f"{sess}.jsonl"

    def history_session_paths(
        self, agent_info: dict, manifest_dir: Path, sid: str,
    ) -> list[Path]:
        ad = self._agent_dir(agent_info, manifest_dir)
        if not ad:
            return []
        return [ad / f"{h}.jsonl" for h in agent_info.get("history_sessions", [])]
