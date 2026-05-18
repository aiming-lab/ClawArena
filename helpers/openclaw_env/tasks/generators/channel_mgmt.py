"""Task generators for Channel Management domain (D4)."""

from __future__ import annotations

from typing import Any, Iterator

from openclaw_env.core.task import TaskData
from openclaw_env.tasks.registry import BaseTaskGenerator, Pass, SetupResult

_CHANNELS = [
    "telegram",
    "discord",
    "slack",
    "whatsapp",
    "msteams",
    "matrix",
]

# Channel configuration keys and sample values
_CHANNEL_SETTINGS = [
    ("notification_level", "all"),
    ("notification_level", "mentions"),
    ("auto_reply", "true"),
    ("auto_reply", "false"),
    ("message_history", "100"),
    ("message_history", "500"),
    ("thread_support", "true"),
    ("thread_support", "false"),
    ("read_receipts", "true"),
    ("typing_indicators", "false"),
    ("media_auto_download", "true"),
    ("archive_messages", "true"),
]


@BaseTaskGenerator.register("login_channel")
class LoginChannelGenerator(BaseTaskGenerator):
    """Log into a messaging channel."""

    required_domains = ("channel_mgmt",)
    difficulty = 1
    parameters = {
        "channel": _CHANNELS,
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={"channel": params["channel"]},
            private={"expected_channel": params["channel"]},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return f"Log into the {params['channel']} channel."

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [f"openclaw channels login --channel {params['channel']}"]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "state",
                "field": f"channels.{params['channel']}",
                "condition": "exists",
                "expected": None,
                "name": f"{params['channel']} channel configured",
            },
            {
                "type": "state",
                "field": f"channels.{params['channel']}.status",
                "condition": "equals",
                "expected": "connected",
                "name": f"{params['channel']} channel connected",
            },
        ]


@BaseTaskGenerator.register("login_and_check_channel")
class LoginAndCheckChannelGenerator(BaseTaskGenerator):
    """Multi-step: log into a channel then check its configuration."""

    required_domains = ("channel_mgmt",)
    difficulty = 2
    parameters = {
        "channel": _CHANNELS[:4],  # telegram, discord, slack, whatsapp
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={"channel": params["channel"]},
            private={"expected_channel": params["channel"]},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"Log into the {params['channel']} channel, then check and display "
            f"its current configuration."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            f"openclaw channels login --channel {params['channel']}",
            "openclaw channels list --json",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "state",
                "field": f"channels.{params['channel']}",
                "condition": "exists",
                "expected": None,
                "name": f"{params['channel']} configured",
            },
            {
                "type": "output",
                "match_type": "regex",
                "expected": r"(\{|\}|config|status)",
                "output_field": "last_stdout",
                "name": "channel config displayed",
                "ignore_case": True,
            },
        ]


@BaseTaskGenerator.register("configure_channel_setting")
class ConfigureChannelSettingGenerator(BaseTaskGenerator):
    """Multi-step: log into a channel then set a configuration value."""

    required_domains = ("channel_mgmt",)
    difficulty = 2
    parameters = {
        "channel": _CHANNELS[:4],
        "setting": _CHANNEL_SETTINGS[:5],  # first 5 settings = 20 tasks
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        key, value = params["setting"]
        data = TaskData(
            public={
                "channel": params["channel"],
                "key": key,
                "value": value,
            },
            private={
                "expected_channel": params["channel"],
                "expected_key": key,
                "expected_value": value,
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        key, value = params["setting"]
        return (
            f"Log into the {params['channel']} channel, then set its "
            f"'{key}' configuration to '{value}'."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        key, value = params["setting"]
        return [
            f"openclaw channels login --channel {params['channel']}",
            f"openclaw config set channels.{params['channel']}.config.{key} {value}",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        key, value = params["setting"]
        return [
            {
                "type": "state",
                "field": f"channels.{params['channel']}",
                "condition": "exists",
                "expected": None,
                "name": f"{params['channel']} configured",
            },
            {
                "type": "config",
                "config_path": f"channels.{params['channel']}.config.{key}",
                "condition": "equals",
                "expected": value,
                "name": f"{params['channel']}.{key} = {value}",
            },
        ]


@BaseTaskGenerator.register("list_channels")
class ListChannelsGenerator(BaseTaskGenerator):
    """List all configured channels."""

    required_domains = ("channel_mgmt",)
    difficulty = 1
    parameters = {}

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        yield Pass(), TaskData()

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return "List all currently configured messaging channels."

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return ["openclaw channels list"]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "output",
                "match_type": "regex",
                "expected": r"(Channel|channel|No channels)",
                "output_field": "last_stdout",
                "name": "channels listed",
                "ignore_case": True,
            }
        ]
