"""openclaw layout — native multi-session via state/agents/<sid>/sessions/."""

from __future__ import annotations

from pathlib import Path

from clawarena.stats.base import FrameworkLayout
from clawarena.stats.session_parser import parse_openclaw_session


class OpenclawLayout(FrameworkLayout):
    """openclaw stores main + history sessions as jsonl under the agent dir."""

    @property
    def name(self) -> str:
        return "openclaw"

    @property
    def main_session_parser(self):
        return parse_openclaw_session

    @property
    def history_session_parser(self):
        return parse_openclaw_session

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
        return ad / "sessions" / f"{sess}.jsonl"

    def history_session_paths(
        self, agent_info: dict, manifest_dir: Path, sid: str,
    ) -> list[Path]:
        ad = self._agent_dir(agent_info, manifest_dir)
        if not ad:
            return []
        return [
            ad / "sessions" / f"{h}.jsonl"
            for h in agent_info.get("history_sessions", [])
        ]
