"""Tests for adapters and registry."""

import pytest

from clawarena.adapters.registry import get_adapter, ADAPTER_REGISTRY
from clawarena.adapters.base import FrameworkAdapter


def test_get_openclaw_adapter():
    adapter = get_adapter("openclaw")
    assert isinstance(adapter, FrameworkAdapter)
    assert adapter.name == "openclaw"


def test_get_unknown_adapter():
    with pytest.raises(ValueError, match="Unknown framework"):
        get_adapter("nonexistent")


def test_registry_has_openclaw():
    assert "openclaw" in ADAPTER_REGISTRY


def test_adapter_get_qtype():
    adapter = get_adapter("openclaw")
    qtype = adapter.get_qtype("multi_choice")
    assert qtype.name == "multi_choice"
