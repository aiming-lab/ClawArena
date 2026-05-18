"""Question type registry."""

from __future__ import annotations

from clawarena.qtypes.base import QuestionType

_REGISTRY: dict[str, QuestionType] = {}


def _init_registry() -> None:
    """Register built-in question types."""
    if _REGISTRY:
        return
    from clawarena.qtypes.multi_choice import MultiChoice
    from clawarena.qtypes.exec_check import ExecCheck
    _REGISTRY["multi_choice"] = MultiChoice()
    _REGISTRY["exec_check"] = ExecCheck()


def get_qtype(type_name: str) -> QuestionType:
    """Get a registered question type by name."""
    _init_registry()
    if type_name not in _REGISTRY:
        raise ValueError(f"Unknown question type: {type_name}")
    return _REGISTRY[type_name]


def register_qtype(name: str, qtype: QuestionType) -> None:
    """Register a custom question type."""
    _init_registry()
    _REGISTRY[name] = qtype


def registered_types() -> list[str]:
    """Return list of registered type names."""
    _init_registry()
    return list(_REGISTRY.keys())
