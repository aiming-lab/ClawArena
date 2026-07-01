"""Framework adapter — composition of Engine + DataHandler + QType overrides."""

from __future__ import annotations

from clawarena.data_handlers.base import DataHandler
from clawarena.engines.base import AgentEngine
from clawarena.qtypes.base import QuestionType
from clawarena.qtypes.registry import get_qtype


class FrameworkAdapter:
    """Bundles an engine, data handler, and optional qtype overrides."""

    def __init__(
        self,
        name: str,
        engine: AgentEngine,
        data_handler: DataHandler,
        qtype_overrides: dict[str, QuestionType] | None = None,
    ):
        self.name = name
        self.engine = engine
        self.data_handler = data_handler
        self.qtype_overrides = qtype_overrides or {}

    def get_qtype(self, type_name: str) -> QuestionType:
        if type_name in self.qtype_overrides:
            return self.qtype_overrides[type_name]
        return get_qtype(type_name)
