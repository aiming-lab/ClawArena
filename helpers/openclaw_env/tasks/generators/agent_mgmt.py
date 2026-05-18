"""Task generators for Agent Management domain (D3)."""

from __future__ import annotations

from typing import Any, Iterator

from openclaw_env.core.task import TaskData
from openclaw_env.tasks.registry import BaseTaskGenerator, Pass, SetupResult


@BaseTaskGenerator.register("agent_create")
class AgentCreateGenerator(BaseTaskGenerator):
    """Generate tasks for creating new agents."""

    required_domains = ("agent_mgmt",)
    difficulty = 1
    parameters = {
        "name": ["researcher", "assistant", "coder", "writer", "translator"],
        "model": [
            "anthropic/claude-opus-4-6",
            "anthropic/claude-sonnet-4-5-20250929",
            "openai/gpt-4o",
        ],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={"name": params["name"], "model": params["model"]},
            private={
                "expected_name": params["name"],
                "expected_model": params["model"],
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"Create a new agent named '{params['name']}' using the model "
            f"'{params['model']}'."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            f"openclaw agents add {params['name']} --model {params['model']}"
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "state",
                "field": f"agents.{params['name']}",
                "condition": "exists",
                "expected": None,
                "name": f"agent '{params['name']}' created",
            },
        ]


@BaseTaskGenerator.register("agent_create_and_configure")
class AgentCreateAndConfigureGenerator(BaseTaskGenerator):
    """Multi-step: create agent then set its identity."""

    required_domains = ("agent_mgmt",)
    difficulty = 2
    parameters = {
        "name": ["helper", "analyst", "reviewer"],
        "model": [
            "anthropic/claude-sonnet-4-5-20250929",
            "openai/gpt-4o",
        ],
        "emoji": ["🤖", "🧠", "📝", "🔍"],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "name": params["name"],
                "model": params["model"],
                "emoji": params["emoji"],
            },
            private={
                "expected_name": params["name"],
                "expected_emoji": params["emoji"],
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"Create a new agent named '{params['name']}' with model "
            f"'{params['model']}', then set its emoji to {params['emoji']}."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            f"openclaw agents add {params['name']} --model {params['model']}",
            f"openclaw agents set-identity --agent {params['name']} --emoji {params['emoji']}",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "state",
                "field": f"agents.{params['name']}",
                "condition": "exists",
                "expected": None,
                "name": f"agent '{params['name']}' created",
            },
            {
                "type": "state",
                "field": f"agents.{params['name']}.emoji",
                "condition": "equals",
                "expected": params["emoji"],
                "name": "emoji set correctly",
            },
        ]


@BaseTaskGenerator.register("agent_list_check")
class AgentListCheckGenerator(BaseTaskGenerator):
    """Generate tasks for listing and checking existing agents."""

    required_domains = ("agent_mgmt", "monitoring")
    difficulty = 1
    parameters = {}

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData()
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return "List all configured agents and report how many are currently set up."

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return ["openclaw agents list"]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "output",
                "match_type": "regex",
                "expected": r"(Agents|No agents|agent)",
                "output_field": "last_stdout",
                "name": "agents listed",
            }
        ]
