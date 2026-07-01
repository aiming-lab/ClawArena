"""Tests for the plugin system — external adapter registration."""

import pytest
from pathlib import Path

from clawarena.adapters.registry import ADAPTER_REGISTRY, get_adapter, register_adapter
from clawarena.adapters.base import FrameworkAdapter
from clawarena.plugins.loader import load_plugins


class TestRegisterAdapter:
    def test_register_and_get(self):
        called = []

        def factory():
            called.append(1)
            from clawarena.data_handlers.openclaw.handler import OpenClawDataHandler
            from clawarena.engines.openclaw.engine import OpenClawEngine
            return FrameworkAdapter("test_fw", OpenClawEngine(), OpenClawDataHandler())

        register_adapter("test_fw", factory)
        try:
            assert "test_fw" in ADAPTER_REGISTRY
            adapter = get_adapter("test_fw")
            assert adapter.name == "test_fw"
            assert len(called) == 1
        finally:
            ADAPTER_REGISTRY.pop("test_fw", None)

    def test_register_overwrites(self):
        register_adapter("overwrite_test", lambda: None)
        register_adapter("overwrite_test", lambda: "new")
        try:
            assert ADAPTER_REGISTRY["overwrite_test"]() == "new"
        finally:
            ADAPTER_REGISTRY.pop("overwrite_test", None)


class TestLoadPlugins:
    def test_load_plugin_registers_adapter(self, tmp_path):
        plugin_file = tmp_path / "my_adapter.py"
        plugin_file.write_text(
            "from clawarena.adapters.registry import register_adapter\n"
            "from clawarena.adapters.base import FrameworkAdapter\n"
            "from clawarena.data_handlers.openclaw.handler import OpenClawDataHandler\n"
            "from clawarena.engines.openclaw.engine import OpenClawEngine\n"
            "\n"
            "def _factory():\n"
            "    return FrameworkAdapter('ext_fw', OpenClawEngine(), OpenClawDataHandler())\n"
            "\n"
            "register_adapter('ext_fw', _factory)\n"
        )
        load_plugins([str(plugin_file)])
        try:
            assert "ext_fw" in ADAPTER_REGISTRY
            adapter = get_adapter("ext_fw")
            assert adapter.name == "ext_fw"
        finally:
            ADAPTER_REGISTRY.pop("ext_fw", None)

    def test_load_missing_file(self, tmp_path):
        missing = tmp_path / "nonexistent.py"
        with pytest.raises(FileNotFoundError):
            load_plugins([str(missing)])

    def test_load_multiple_plugins(self, tmp_path):
        for name in ("fw_a", "fw_b"):
            f = tmp_path / f"{name}.py"
            f.write_text(
                "from clawarena.adapters.registry import register_adapter\n"
                "from clawarena.adapters.base import FrameworkAdapter\n"
                "from clawarena.data_handlers.openclaw.handler import OpenClawDataHandler\n"
                "from clawarena.engines.openclaw.engine import OpenClawEngine\n"
                f"register_adapter('{name}', lambda: FrameworkAdapter('{name}', OpenClawEngine(), OpenClawDataHandler()))\n"
            )
        load_plugins([str(tmp_path / "fw_a.py"), str(tmp_path / "fw_b.py")])
        try:
            assert "fw_a" in ADAPTER_REGISTRY
            assert "fw_b" in ADAPTER_REGISTRY
        finally:
            ADAPTER_REGISTRY.pop("fw_a", None)
            ADAPTER_REGISTRY.pop("fw_b", None)
