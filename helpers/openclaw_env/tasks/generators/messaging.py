"""Task generators for Messaging domain (D2)."""

from __future__ import annotations

import shlex
from typing import Any, Iterator

from openclaw_env.core.task import TaskData
from openclaw_env.tasks.generation_options import get_generation_options
from openclaw_env.tasks.registry import BaseTaskGenerator, Fail, Pass, SetupResult


def _split_csv(raw: str) -> list[str]:
    return [v.strip() for v in raw.split(",") if v.strip()]


def _maybe_message_dry_run(command: str) -> str:
    if not get_generation_options().message_dry_run:
        return command
    try:
        tokens = shlex.split(command)
    except ValueError:
        return f"{command} --dry-run"
    if tokens[:2] != ["openclaw", "message"]:
        return command
    if "--dry-run" in tokens:
        return command
    tokens.append("--dry-run")
    return shlex.join(tokens)


@BaseTaskGenerator.register("msg_send_text")
class MessageSendTextGenerator(BaseTaskGenerator):
    """Generate tasks for sending text messages."""

    required_domains = ("messaging",)
    difficulty = 1
    parameters = {
        "channel": ["telegram", "whatsapp", "discord", "slack"],
        "target": ["@alice", "@bob", "+1234567890", "#general"],
        "content": [
            "Hello, how are you?",
            "Meeting at 3pm tomorrow",
            "Please review the document",
            "Happy birthday!",
        ],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "channel": params["channel"],
                "target": params["target"],
                "content": params["content"],
            },
            private={
                "expected_target": params["target"],
                "expected_channel": params["channel"],
                "expected_content": params["content"],
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"Send a text message to {params['target']} on {params['channel']} "
            f"saying '{params['content']}'."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        cmd = (
            f"openclaw message send --channel {params['channel']} "
            f"--target {params['target']} --message '{params['content']}'"
        )
        return [_maybe_message_dry_run(cmd)]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "effect",
                "effect_type": "messages_sent",
                "condition": "field_equals",
                "expected": {"field": "target", "value": params["target"]},
                "name": "message sent to correct target",
            },
            {
                "type": "effect",
                "effect_type": "messages_sent",
                "condition": "field_contains",
                "expected": {"field": "message", "value": params["content"]},
                "name": "message content correct",
            },
        ]


@BaseTaskGenerator.register("msg_broadcast")
class MessageBroadcastGenerator(BaseTaskGenerator):
    """Generate tasks for broadcasting messages to multiple targets."""

    required_domains = ("messaging",)
    difficulty = 2
    parameters = {
        "targets": [
            "@alice,@bob",
            "@alice,@bob,@charlie",
            "#general,#random",
        ],
        "content": [
            "Team standup in 10 minutes",
            "Server maintenance tonight at 11pm",
        ],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        target_list = [t.strip() for t in params["targets"].split(",")]
        data = TaskData(
            public={
                "targets": params["targets"],
                "content": params["content"],
            },
            private={
                "expected_targets": target_list,
                "expected_count": len(target_list),
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"Broadcast the message '{params['content']}' to the following "
            f"targets: {params['targets']}."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        targets = " ".join(_split_csv(params["targets"]))
        cmd = (
            f"openclaw message broadcast --targets {params['targets']} "
            f"--message '{params['content']}'"
        )
        cmd = cmd.replace(params["targets"], targets)
        return [_maybe_message_dry_run(cmd)]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        target_count = len(params["targets"].split(","))
        return [
            {
                "type": "effect",
                "effect_type": "messages_sent",
                "condition": "count_gte",
                "expected": target_count,
                "name": f"broadcast sent to {target_count} targets",
            },
        ]


@BaseTaskGenerator.register("msg_create_poll")
class MessageCreatePollGenerator(BaseTaskGenerator):
    """Generate tasks for creating polls."""

    required_domains = ("messaging",)
    difficulty = 2
    parameters = {
        "target": ["#general", "@team-lead", "#planning"],
        "question": [
            "What time works for the meeting?",
            "Where should we have lunch?",
            "Which project should we prioritize?",
        ],
        "options": [
            "10am,2pm,4pm",
            "Italian,Chinese,Mexican",
            "Project A,Project B,Project C",
        ],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "target": params["target"],
                "question": params["question"],
                "options": params["options"],
            },
            private={
                "expected_question": params["question"],
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"Create a poll in {params['target']} asking '{params['question']}' "
            f"with options: {params['options']}."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        options = _split_csv(params["options"])
        option_flags = " ".join(f"--poll-option '{opt}'" for opt in options)
        cmd = (
            f"openclaw message poll --target {params['target']} "
            f"--poll-question '{params['question']}' {option_flags}"
        )
        return [_maybe_message_dry_run(cmd)]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "effect",
                "effect_type": "messages_sent",
                "condition": "exists",
                "expected": None,
                "name": "poll created",
            },
        ]


@BaseTaskGenerator.register("msg_search")
class MessageSearchGenerator(BaseTaskGenerator):
    """Search messages by keyword in a channel."""

    required_domains = ("messaging",)
    difficulty = 2
    parameters = {
        "channel": ["discord", "discord", "discord", "discord"],
        "query": ["meeting", "report", "update", "reminder", "deadline"],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "channel": params["channel"],
                "query": params["query"],
            },
            private={"expected_query": params["query"]},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"Search messages in the {params['channel']} channel "
            f"for the keyword '{params['query']}'."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        cmd = (
            f"openclaw message search --channel {params['channel']} "
            f"--guild-id 123456789012345678 --channel-id 234567890123456789 "
            f"--query {params['query']}"
        )
        return [_maybe_message_dry_run(cmd)]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "output",
                "match_type": "regex",
                # In dry-run mode, OpenClaw returns a planning line instead of
                # concrete search results; accept both forms.
                "expected": r"(Found|No messages|message|dry-run|would run search)",
                "output_field": "last_stdout",
                "name": "search results shown",
                "ignore_case": True,
            }
        ]


@BaseTaskGenerator.register("msg_react")
class MessageReactGenerator(BaseTaskGenerator):
    """React to a message with an emoji."""

    required_domains = ("messaging",)
    difficulty = 1
    parameters = {
        "channel": ["telegram", "slack", "discord", "whatsapp"],
        "target": ["@alice", "@bob", "@charlie", "#general"],
        "emoji": ["👍", "❤️", "🎉", "✅"],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "channel": params["channel"],
                "target": params["target"],
                "emoji": params["emoji"],
            },
            private={"expected_emoji": params["emoji"]},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"React to the latest message from {params['target']} "
            f"on {params['channel']} with the {params['emoji']} emoji."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        cmd = (
            f"openclaw message react --channel {params['channel']} "
            f"--target {params['target']} --message-id 1 --emoji '{params['emoji']}'"
        )
        return [_maybe_message_dry_run(cmd)]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "output",
                "match_type": "regex",
                "expected": r"(React|react|emoji)",
                "output_field": "last_stdout",
                "name": "reaction sent",
                "ignore_case": True,
            }
        ]
