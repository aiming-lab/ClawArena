"""Plugin loader — load external .py files that register adapters."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_plugins(paths: list[str]) -> None:
    """Import .py plugin files that register external adapters.

    Each file is executed; it should call
    ``clawarena.adapters.registry.register_adapter()`` to make new
    frameworks available to --framework.
    """
    for raw in paths:
        p = Path(raw).resolve()
        if not p.is_file():
            raise FileNotFoundError(f"Plugin file not found: {p}")
        name = f"_clawarena_plugin_{p.stem}"
        spec = importlib.util.spec_from_file_location(name, p)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot create module spec for: {p}")
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
