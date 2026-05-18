"""claude-code layout — main jsonl in state/projects, history transcribed as
md inside workspace/<sid>/message_logs/."""

from __future__ import annotations

from pathlib import Path

from clawarena.stats.base import FrameworkLayout
from clawarena.stats.session_parser import parse_claude_code_session


class ClaudeCodeLayout(FrameworkLayout):
    @property
    def name(self) -> str:
        return "claude-code"

    @property
    def workspace_excludes(self) -> set[str]:
        return {"message_logs"}

    @property
    def session_update_types(self) -> set[str]:
        return {"session", "workspace_md"}

    @property
    def main_session_parser(self):
        return parse_claude_code_session

    @property
    def history_session_parser(self):
        # History is transcribed as markdown -- count verbatim since
        # the agent reads the file contents as-is.
        return None

    def main_session_path(
        self, agent_info: dict, manifest_dir: Path, sid: str,
    ) -> Path | None:
        proj_rel = agent_info.get("project_dir")
        sess = agent_info.get("session", "")
        if not proj_rel or not sess:
            return None
        return manifest_dir / proj_rel / f"{sess}.jsonl"

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
