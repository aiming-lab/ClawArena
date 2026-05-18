"""picoclaw layout — main jsonl in memory/, history transcribed as jsonl
inside workspace/<sid>/message_logs/."""

from __future__ import annotations

from pathlib import Path

from clawarena.stats.base import FrameworkLayout
from clawarena.stats.session_parser import parse_picoclaw_session


def _file_from_session_key(session_key: str) -> str:
    """Convert ``bench:hil_s1`` to ``bench_hil_s1.jsonl``."""
    return session_key.replace(":", "_") + ".jsonl"


class PicoclawLayout(FrameworkLayout):
    @property
    def name(self) -> str:
        return "picoclaw"

    @property
    def workspace_excludes(self) -> set[str]:
        return {"message_logs"}

    @property
    def session_update_types(self) -> set[str]:
        return {"session", "workspace_jsonl"}

    @property
    def main_session_parser(self):
        return parse_picoclaw_session

    @property
    def history_session_parser(self):
        # History is jsonl transcribed into workspace/message_logs --
        # also a flat ``{role, content, ...}`` schema.
        return parse_picoclaw_session

    def main_session_path(
        self, agent_info: dict, manifest_dir: Path, sid: str,
    ) -> Path | None:
        session_key = agent_info.get("session_key", f"bench:{sid}")
        return manifest_dir / "memory" / _file_from_session_key(session_key)

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
