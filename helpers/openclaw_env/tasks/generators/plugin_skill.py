"""Task generators for Plugin & Skill domain (D6)."""

from __future__ import annotations

import re
from typing import Any, Iterator

from openclaw_env.core.task import TaskData
from openclaw_env.tasks.generation_options import get_generation_options
from openclaw_env.tasks.registry import BaseTaskGenerator, Pass, SetupResult

_PLUGINS = [
    "discord",
    "slack",
    "telegram",
    "whatsapp",
    "matrix",
    "mattermost",
    "signal",
    "line",
    "nostr",
    "irc",
]

_ONLINE_INSTALL_PLUGIN_PACKAGE_BY_ID = {
    "discord": "@openclaw/discord",
    "slack": "@openclaw/slack",
    "telegram": "@openclaw/telegram",
    "whatsapp": "@openclaw/whatsapp",
}
_ONLINE_INSTALL_PLUGIN_IDS = list(_ONLINE_INSTALL_PLUGIN_PACKAGE_BY_ID.keys())

_SKILLS = [
    "healthcheck",
    "skill-creator",
    "tmux",
    "weather",
    "healthcheck",
    "weather",
]


def _use_online_install(plugin_id: str) -> bool:
    options = get_generation_options()
    return (
        options.plugin_install_mode == "mixed"
        and plugin_id in _ONLINE_INSTALL_PLUGIN_PACKAGE_BY_ID
    )


def _plugin_install_command(plugin_id: str) -> str:
    if _use_online_install(plugin_id):
        pkg = _ONLINE_INSTALL_PLUGIN_PACKAGE_BY_ID[plugin_id]
        return f"openclaw plugins install {pkg}"
    return f"openclaw plugins enable {plugin_id}"


def _plugin_list_presence_regex(plugin_id: str) -> str:
    pkg = _ONLINE_INSTALL_PLUGIN_PACKAGE_BY_ID.get(plugin_id, "")
    if pkg:
        return f"({re.escape(plugin_id)}|{re.escape(pkg)})"
    return re.escape(plugin_id)


@BaseTaskGenerator.register("install_plugin")
class InstallPluginGenerator(BaseTaskGenerator):
    """Install a named plugin."""

    required_domains = ("plugin_skill",)
    difficulty = 1
    parameters = {
        "name": _PLUGINS,
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={"name": params["name"]},
            private={"expected_plugin": params["name"]},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        if _use_online_install(params["name"]):
            return f"Install the '{params['name']}' plugin."
        return f"Enable the '{params['name']}' plugin."

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [_plugin_install_command(params["name"])]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        if _use_online_install(params["name"]):
            return [
                {
                    "type": "output",
                    "match_type": "regex",
                    "expected": r"(install|already)",
                    "output_field": "last_stdout",
                    "name": f"plugin '{params['name']}' installed",
                    "ignore_case": True,
                }
            ]
        return [
            {
                "type": "output",
                "match_type": "contains",
                "expected": "enable",
                "output_field": "last_stdout",
                "name": f"plugin '{params['name']}' enabled",
                "ignore_case": True,
            }
        ]


@BaseTaskGenerator.register("install_skill")
class InstallSkillGenerator(BaseTaskGenerator):
    """Install a named skill."""

    required_domains = ("plugin_skill",)
    difficulty = 1
    parameters = {
        "name": _SKILLS,
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={"name": params["name"]},
            private={"expected_skill": params["name"]},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return f"Show detailed information for the '{params['name']}' skill."

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [f"openclaw skills info {params['name']}"]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "output",
                "match_type": "regex",
                "expected": r"(skill|name|description|missing|not found)",
                "output_field": "last_stdout",
                "name": f"skill '{params['name']}' info shown",
                "ignore_case": True,
            }
        ]


@BaseTaskGenerator.register("list_plugins")
class ListPluginsGenerator(BaseTaskGenerator):
    """List all installed plugins."""

    required_domains = ("plugin_skill",)
    difficulty = 1
    parameters = {}

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        yield Pass(), TaskData()

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return "List all currently installed plugins."

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return ["openclaw plugins list"]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "output",
                "match_type": "regex",
                "expected": r"(plugin|Plugin|No plugins)",
                "output_field": "last_stdout",
                "name": "plugins listed",
            }
        ]


@BaseTaskGenerator.register("install_and_verify_plugin")
class InstallAndVerifyPluginGenerator(BaseTaskGenerator):
    """Multi-step: install a plugin then verify it appears in the list."""

    required_domains = ("plugin_skill",)
    difficulty = 2
    parameters = {
        "name": _PLUGINS[:8],  # 8 variations
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={"name": params["name"]},
            private={"expected_plugin": params["name"]},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        if _use_online_install(params["name"]):
            return (
                f"Install the '{params['name']}' plugin, then verify it appears "
                f"in plugin list output."
            )
        return (
            f"Enable the '{params['name']}' plugin, then verify it appears "
            f"in plugin list output."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            _plugin_install_command(params["name"]),
            "openclaw plugins list",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        checks: list[dict[str, Any]] = []
        expected_effect_plugin = params["name"]
        if _use_online_install(params["name"]):
            install_cmd = _plugin_install_command(params["name"])
            expected_effect_plugin = _ONLINE_INSTALL_PLUGIN_PACKAGE_BY_ID[params["name"]]
            checks.append(
                {
                    "type": "output",
                    "match_type": "regex",
                    "expected": re.escape(install_cmd) + r".*?'exit_code':\s*0",
                    "output_field": "command_history",
                    "name": "install step executed successfully",
                    "ignore_case": False,
                }
            )

        checks.extend(
            [
                {
                    "type": "effect",
                    "effect_type": "plugins_installed",
                    "condition": "field_equals",
                    "expected": {"field": "name", "value": expected_effect_plugin},
                    "name": f"plugin '{params['name']}' installed/enabled",
                },
                {
                    "type": "output",
                    "match_type": "regex",
                    "expected": _plugin_list_presence_regex(params["name"]),
                    "output_field": "last_stdout",
                    "name": "plugin appears in list output",
                    "ignore_case": True,
                },
            ]
        )
        return checks


@BaseTaskGenerator.register("install_then_remove_plugin")
class InstallThenRemovePluginGenerator(BaseTaskGenerator):
    """Multi-step: install a plugin then remove it (tests lifecycle)."""

    required_domains = ("plugin_skill",)
    difficulty = 2
    parameters = {
        "name": _PLUGINS[:4],  # keep 4 variations while using valid built-in plugin ids
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={"name": params["name"]},
            private={},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"Enable the '{params['name']}' plugin, verify it appears "
            f"by listing plugins, then disable it."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            f"openclaw plugins enable {params['name']}",
            "openclaw plugins list",
            f"openclaw plugins disable {params['name']}",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "output",
                "match_type": "contains",
                "expected": "disable",
                "output_field": "last_stdout",
                "name": "plugin disabled",
                "ignore_case": True,
            },
        ]
