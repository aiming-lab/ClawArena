"""
Test suite for requests/hooks.py hook dispatching mechanism.

Tests verify that hooks are correctly registered, dispatched, and chained.
"""
import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from requests.hooks import default_hooks, dispatch_hook, HOOKS


class TestDefaultHooks:
    def test_hooks_list(self):
        assert "response" in HOOKS

    def test_default_hooks_returns_dict(self):
        h = default_hooks()
        assert isinstance(h, dict)
        assert "response" in h
        assert h["response"] == []


class TestDispatchHook:
    def test_dispatch_no_hooks(self):
        data = {"key": "value"}
        result = dispatch_hook("response", {}, data)
        assert result == data

    def test_dispatch_callable_hook(self):
        called = []
        def my_hook(data, **kwargs):
            called.append(data)
            return {"modified": True}
        result = dispatch_hook("response", {"response": my_hook}, {"original": True})
        assert result == {"modified": True}
        assert len(called) == 1

    def test_dispatch_list_of_hooks(self):
        results = []
        def hook1(data, **kwargs):
            results.append(1)
        def hook2(data, **kwargs):
            results.append(2)
        dispatch_hook("response", {"response": [hook1, hook2]}, "data")
        assert results == [1, 2]
