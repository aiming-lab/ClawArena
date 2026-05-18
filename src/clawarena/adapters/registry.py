"""Adapter registry — maps framework names to adapter factory functions.

Built-in adapters are registered at import time. External adapters can
be registered via ``register_adapter()`` (typically called from plugin files
loaded with ``--plugin``).
"""

from __future__ import annotations

from typing import Callable

from .base import FrameworkAdapter


def _create_openclaw_adapter() -> FrameworkAdapter:
    from clawarena.data_handlers.openclaw.handler import OpenClawDataHandler
    from clawarena.engines.openclaw.engine import OpenClawEngine
    return FrameworkAdapter(
        name="openclaw",
        engine=OpenClawEngine(),
        data_handler=OpenClawDataHandler(),
    )


def _create_claude_code_adapter() -> FrameworkAdapter:
    from clawarena.data_handlers.claude_code.handler import ClaudeCodeDataHandler
    from clawarena.engines.claude_code.engine import ClaudeCodeEngine
    return FrameworkAdapter(
        name="claude-code",
        engine=ClaudeCodeEngine(),
        data_handler=ClaudeCodeDataHandler(),
    )


def _create_picoclaw_adapter() -> FrameworkAdapter:
    from clawarena.data_handlers.picoclaw.handler import PicoClawDataHandler
    from clawarena.engines.picoclaw.engine import PicoClawEngine
    return FrameworkAdapter(
        name="picoclaw",
        engine=PicoClawEngine(),
        data_handler=PicoClawDataHandler(),
    )


def _create_nanobot_adapter() -> FrameworkAdapter:
    from clawarena.data_handlers.nanobot.handler import NanobotDataHandler
    from clawarena.engines.nanobot.engine import NanobotEngine
    return FrameworkAdapter(
        name="nanobot",
        engine=NanobotEngine(),
        data_handler=NanobotDataHandler(),
    )


def _create_codex_adapter() -> FrameworkAdapter:
    from clawarena.data_handlers.codex.handler import CodexDataHandler
    from clawarena.engines.codex.engine import CodexEngine
    return FrameworkAdapter(
        name="codex",
        engine=CodexEngine(),
        data_handler=CodexDataHandler(),
    )


def _create_opencode_adapter() -> FrameworkAdapter:
    from clawarena.data_handlers.opencode.handler import OpenCodeDataHandler
    from clawarena.engines.opencode.engine import OpenCodeEngine
    return FrameworkAdapter(
        name="opencode",
        engine=OpenCodeEngine(),
        data_handler=OpenCodeDataHandler(),
    )


def _create_zeroclaw_adapter() -> FrameworkAdapter:
    from clawarena.data_handlers.zeroclaw.handler import ZeroClawDataHandler
    from clawarena.engines.zeroclaw.engine import ZeroClawEngine
    return FrameworkAdapter(
        name="zeroclaw",
        engine=ZeroClawEngine(),
        data_handler=ZeroClawDataHandler(),
    )


def _create_ironclaw_adapter() -> FrameworkAdapter:
    from clawarena.data_handlers.ironclaw.handler import IronClawDataHandler
    from clawarena.engines.ironclaw.engine import IronClawEngine
    return FrameworkAdapter(
        name="ironclaw",
        engine=IronClawEngine(),
        data_handler=IronClawDataHandler(),
    )


def _create_copaw_adapter() -> FrameworkAdapter:
    from clawarena.data_handlers.copaw.handler import CoPawDataHandler
    from clawarena.engines.copaw.engine import CoPawEngine
    return FrameworkAdapter(
        name="copaw",
        engine=CoPawEngine(),
        data_handler=CoPawDataHandler(),
    )


ADAPTER_REGISTRY: dict[str, Callable[[], FrameworkAdapter]] = {
    "openclaw":   _create_openclaw_adapter,
    "claude-code": _create_claude_code_adapter,
    "picoclaw":   _create_picoclaw_adapter,
    "nanobot":    _create_nanobot_adapter,
    "codex":      _create_codex_adapter,
    "opencode":   _create_opencode_adapter,
    "zeroclaw":   _create_zeroclaw_adapter,
    "ironclaw":   _create_ironclaw_adapter,
    "copaw":      _create_copaw_adapter,
}


def register_adapter(
    name: str,
    factory: Callable[[], FrameworkAdapter],
) -> None:
    """Register an external adapter factory.

    Called from plugin .py files to make new frameworks available::

        from clawarena.adapters.registry import register_adapter
        register_adapter("my_framework", lambda: FrameworkAdapter(...))
    """
    ADAPTER_REGISTRY[name] = factory


def get_adapter(framework: str) -> FrameworkAdapter:
    """Get or create an adapter for the given framework."""
    factory = ADAPTER_REGISTRY.get(framework)
    if factory is None:
        available = ", ".join(sorted(ADAPTER_REGISTRY.keys()))
        raise ValueError(
            f"Unknown framework '{framework}'. Available: {available}"
        )
    return factory()
