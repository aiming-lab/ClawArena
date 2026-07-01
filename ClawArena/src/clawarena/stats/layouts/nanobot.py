"""nanobot layout — main jsonl in workspace/<sid>/sessions/, history as md
inside workspace/<sid>/message_logs/."""

from __future__ import annotations

from pathlib import Path

from clawarena.stats.base import FrameworkLayout
from clawarena.stats.session_parser import parse_nanobot_session


def _file_from_session_key(session_key: str) -> str:
    return session_key.replace(":", "_") + ".jsonl"


class NanobotLayout(FrameworkLayout):
    @property
    def name(self) -> str:
        return "nanobot"

    @property
    def workspace_excludes(self) -> set[str]:
        return {"sessions", "message_logs"}

    @property
    def session_update_types(self) -> set[str]:
        return {"session", "workspace_md"}

    @property
    def main_session_parser(self):
        return parse_nanobot_session

    @property
    def history_session_parser(self):
        # History is transcribed as markdown; counted verbatim.
        return None

    def main_session_path(
        self, agent_info: dict, manifest_dir: Path, sid: str,
    ) -> Path | None:
        ws_rel = agent_info.get("workspace")
        if not ws_rel:
            return None
        session_key = agent_info.get("session_key", f"bench:{sid}")
        return manifest_dir / ws_rel / "sessions" / _file_from_session_key(session_key)

    def history_session_paths(
        self, agent_info: dict, manifest_dir: Path, sid: str,
    ) -> list[Path]:
        ws_rel = agent_info.get("workspace")
        if not ws_rel:
            return []
        d = manifest_dir / ws_rel / "message_logs"
        if not d.exists():
            return []
        return sorted(p for p in d.iterdir() if p.is_file())
