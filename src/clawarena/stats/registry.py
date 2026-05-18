"""Framework layout registry for stats.

Built-in layouts (openclaw / claude-code / picoclaw / nanobot) are registered
at first use. Unknown frameworks fall back to a generic agent_dir/sessions/
heuristic that mirrors the openclaw convention.
"""

from __future__ import annotations

from pathlib import Path

from clawarena.stats.base import FrameworkLayout


_REGISTRY: dict[str, FrameworkLayout] = {}


class _GenericLayout(FrameworkLayout):
    """Fallback for frameworks without a registered layout."""

    @property
    def name(self) -> str:
        return "_generic"

    def main_session_path(
        self, agent_info: dict, manifest_dir: Path, sid: str,
    ) -> Path | None:
        rel = agent_info.get("agent_dir")
        sess = agent_info.get("session", "")
        if not rel or not sess:
            return None
        return manifest_dir / rel / "sessions" / f"{sess}.jsonl"

    def history_session_paths(
        self, agent_info: dict, manifest_dir: Path, sid: str,
    ) -> list[Path]:
        rel = agent_info.get("agent_dir")
        if not rel:
            return []
        return [
            manifest_dir / rel / "sessions" / f"{h}.jsonl"
            for h in agent_info.get("history_sessions", [])
        ]


def _init_registry() -> None:
    if _REGISTRY:
        return
    from clawarena.stats.layouts.claude_code import ClaudeCodeLayout
    from clawarena.stats.layouts.nanobot import NanobotLayout
    from clawarena.stats.layouts.openclaw import OpenclawLayout
    from clawarena.stats.layouts.picoclaw import PicoclawLayout
    for cls in (OpenclawLayout, ClaudeCodeLayout, PicoclawLayout, NanobotLayout):
        layout = cls()
        _REGISTRY[layout.name] = layout


def get_layout(framework: str) -> FrameworkLayout:
    """Return the layout for `framework`, falling back to generic."""
    _init_registry()
    return _REGISTRY.get(framework, _GenericLayout())


def register_layout(layout: FrameworkLayout) -> None:
    """Register or override a framework layout."""
    _init_registry()
    _REGISTRY[layout.name] = layout


def registered_frameworks() -> list[str]:
    """Return names of all registered frameworks."""
    _init_registry()
    return list(_REGISTRY.keys())
