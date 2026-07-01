"""Shared utilities for clawarena."""

from __future__ import annotations

import socket
from pathlib import Path


def get_project_root() -> Path:
    """Return BENCHMARK_ROOT by locating pyproject.toml upward from this file."""
    current = Path(__file__).resolve().parent
    for parent in [current, *current.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
    # Fallback: src/clawarena/ → src/ → project root
    return Path(__file__).resolve().parent.parent.parent


def resolve_path(p: str | Path, base: Path | None = None) -> Path:
    """Resolve a path relative to base (defaults to BENCHMARK_ROOT)."""
    if base is None:
        base = get_project_root()
    path = Path(p)
    if path.is_absolute():
        return path
    return (base / path).resolve()


def find_free_port() -> int:
    """Find an available TCP port on loopback."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def framework_line(tag: str, message: str, framework: str | None = None) -> str:
    """Format a console line with an optional framework suffix."""
    if framework:
        return f"{tag} {message} ({framework})"
    return f"{tag} {message}"
