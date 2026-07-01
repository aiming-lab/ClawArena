"""Task generators for Composite (cross-domain) tasks (D10)."""

from __future__ import annotations

import hashlib
import shlex
from typing import Any, Iterator

from openclaw_env.core.task import TaskData
from openclaw_env.tasks.generation_options import get_generation_options
from openclaw_env.tasks.generators.weather_tasks import (
    build_universal_weather_on_date_commands,
)
from openclaw_env.tasks.registry import BaseTaskGenerator, Pass, SetupResult

_MODELS = [
    "anthropic/claude-opus-4-6",
    "anthropic/claude-sonnet-4-5-20250929",
    "openai/gpt-4o",
]

_CHANNELS = ["telegram", "discord", "slack", "whatsapp"]

_TARGETS = ["@alice", "@bob", "#general", "@team"]

_SCHEDULES = [
    "0 9 * * *",
    "0 9 * * 1-5",
    "*/30 * * * *",
    "0 0 * * *",
]

_PLUGINS = [
    "slack",
    "discord",
    "telegram",
    "whatsapp",
    "matrix",
]


def _job_name(prefix: str, params: dict[str, Any]) -> str:
    seed = "|".join(f"{k}={params[k]}" for k in sorted(params))
    digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()[:8]
    return f"{prefix}-{digest}"


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


def _is_universal_profile() -> bool:
    return get_generation_options().command_profile == "universal"


def _calendar_add_command(title: str, start: str, location: str | None = None) -> str:
    if _is_universal_profile():
        cmd = f"gcalcli add --title '{title}' --when {start}"
        if location:
            cmd += f" --where '{location}'"
        return cmd

    cmd = f"calendar add-event --title '{title}' --start {start}"
    if location:
        cmd += f" --location '{location}'"
    return cmd


@BaseTaskGenerator.register("setup_channel_and_send")
class SetupChannelAndSendGenerator(BaseTaskGenerator):
    """Cross-domain: configure a channel, then send a message through it."""

    required_domains = ("channel_mgmt", "messaging")
    difficulty = 3
    parameters = {
        "channel": ["telegram", "discord", "slack"],
        "target": ["@alice", "#general"],
        "content": [
            "Hello from the newly configured channel!",
            "Channel setup complete, testing messaging.",
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
                "expected_channel": params["channel"],
                "expected_target": params["target"],
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"First, log into the {params['channel']} channel. "
            f"Then send a message to {params['target']} saying "
            f"'{params['content']}'."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        msg_cmd = (
            f"openclaw message send --channel {params['channel']} "
            f"--target {params['target']} --message '{params['content']}'"
        )
        return [
            f"openclaw channels login --channel {params['channel']}",
            _maybe_message_dry_run(msg_cmd),
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
                "type": "effect",
                "effect_type": "messages_sent",
                "condition": "field_equals",
                "expected": {"field": "target", "value": params["target"]},
                "name": "message sent to correct target",
            },
        ]


@BaseTaskGenerator.register("full_agent_workflow")
class FullAgentWorkflowGenerator(BaseTaskGenerator):
    """Cross-domain: create agent, configure channel, set up cron for periodic messaging."""

    required_domains = ("agent_mgmt", "channel_mgmt", "cron_webhook")
    difficulty = 3
    parameters = {
        "agent_name": ["daily-reporter", "status-monitor"],
        "channel": ["telegram", "slack"],
        "schedule": ["0 9 * * *", "*/30 * * * *"],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "agent_name": params["agent_name"],
                "channel": params["channel"],
                "schedule": params["schedule"],
            },
            private={
                "expected_agent": params["agent_name"],
                "expected_channel": params["channel"],
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"Set up an automated workflow:\n"
            f"1. Create a new agent named '{params['agent_name']}'\n"
            f"2. Log into the {params['channel']} channel\n"
            f"3. Create a cron job with schedule '{params['schedule']}' "
            f"that triggers the agent to send a status report"
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        job_name = _job_name("agent-report", params)
        return [
            f"openclaw agents add {params['agent_name']}",
            f"openclaw channels login --channel {params['channel']}",
            f"openclaw cron add --name {job_name} --cron '{params['schedule']}' "
            f"--message 'Trigger agent {params['agent_name']} status report'",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "state",
                "field": f"agents.{params['agent_name']}",
                "condition": "exists",
                "expected": None,
                "name": f"agent '{params['agent_name']}' created",
            },
            {
                "type": "state",
                "field": f"channels.{params['channel']}",
                "condition": "exists",
                "expected": None,
                "name": f"{params['channel']} configured",
            },
            {
                "type": "state",
                "field": "cron_jobs",
                "condition": "count_gte",
                "expected": 1,
                "name": "cron job created",
            },
        ]


@BaseTaskGenerator.register("agent_cron_workflow")
class AgentCronWorkflowGenerator(BaseTaskGenerator):
    """Cross-domain: create an agent, configure a channel, set up cron for automated messaging."""

    required_domains = ("agent_mgmt", "channel_mgmt", "cron_webhook")
    difficulty = 3
    parameters = {
        "agent_name": ["reporter", "monitor", "notifier", "assistant"],
        "channel": _CHANNELS,
        "schedule": _SCHEDULES,
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "agent_name": params["agent_name"],
                "channel": params["channel"],
                "schedule": params["schedule"],
            },
            private={
                "expected_agent": params["agent_name"],
                "expected_channel": params["channel"],
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"Set up an automated notification workflow:\n"
            f"1. Create an agent named '{params['agent_name']}'\n"
            f"2. Log into the {params['channel']} channel\n"
            f"3. Create a cron job with schedule '{params['schedule']}' "
            f"that uses the agent to send a status update via {params['channel']}"
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        job_name = _job_name("agent-status", params)
        return [
            f"openclaw agents add {params['agent_name']}",
            f"openclaw channels login --channel {params['channel']}",
            f"openclaw cron add --name {job_name} --cron '{params['schedule']}' "
            f"--message 'Run agent {params['agent_name']} status update'",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "state",
                "field": f"agents.{params['agent_name']}",
                "condition": "exists",
                "expected": None,
                "name": f"agent '{params['agent_name']}' created",
            },
            {
                "type": "state",
                "field": f"channels.{params['channel']}",
                "condition": "exists",
                "expected": None,
                "name": f"{params['channel']} channel configured",
            },
            {
                "type": "effect",
                "effect_type": "cron_jobs_created",
                "condition": "count_gte",
                "expected": 1,
                "name": "cron job created",
            },
        ]


@BaseTaskGenerator.register("plugin_and_message")
class PluginAndMessageGenerator(BaseTaskGenerator):
    """Cross-domain: install a plugin, configure a channel, send a message."""

    required_domains = ("plugin_skill", "channel_mgmt", "messaging")
    difficulty = 3
    parameters = {
        "plugin": _PLUGINS,
        "channel": _CHANNELS,
        "target": _TARGETS,
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "plugin": params["plugin"],
                "channel": params["channel"],
                "target": params["target"],
            },
            private={
                "expected_plugin": params["plugin"],
                "expected_target": params["target"],
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        plugin = params["plugin"]
        return (
            f"Complete the following setup:\n"
            f"1. Install the '{plugin}' plugin\n"
            f"2. Log into the {params['channel']} channel\n"
            f"3. Send a message to {params['target']} saying "
            f"'Setup complete, {plugin} is active'"
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        plugin = params["plugin"]
        msg_cmd = (
            f"openclaw message send --channel {params['channel']} "
            f"--target {params['target']} "
            f"--message 'Setup complete, {plugin} is active'"
        )
        return [
            f"openclaw plugins enable {plugin}",
            f"openclaw channels login --channel {params['channel']}",
            _maybe_message_dry_run(msg_cmd),
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "effect",
                "effect_type": "plugins_installed",
                "condition": "field_equals",
                "expected": {"field": "name", "value": params["plugin"]},
                "name": f"plugin '{params['plugin']}' installed",
            },
            {
                "type": "state",
                "field": f"channels.{params['channel']}",
                "condition": "exists",
                "expected": None,
                "name": f"{params['channel']} configured",
            },
            {
                "type": "effect",
                "effect_type": "messages_sent",
                "condition": "field_equals",
                "expected": {"field": "target", "value": params["target"]},
                "name": "message sent to correct target",
            },
        ]


@BaseTaskGenerator.register("secure_channel_and_send")
class SecureChannelAndSendGenerator(BaseTaskGenerator):
    """Cross-domain: configure security, set up a channel, send a message."""

    required_domains = ("security", "channel_mgmt", "messaging")
    difficulty = 3
    parameters = {
        "channel": _CHANNELS[:3],
        "target": _TARGETS[:3],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "channel": params["channel"],
                "target": params["target"],
            },
            private={
                "expected_channel": params["channel"],
                "expected_target": params["target"],
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"Perform a secure setup:\n"
            f"1. Set a security token for the gateway (use 'secure-token-env-test')\n"
            f"2. Log into the {params['channel']} channel\n"
            f"3. Send a message to {params['target']} confirming the secure setup"
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        msg_cmd = (
            f"openclaw message send --channel {params['channel']} "
            f"--target {params['target']} --message 'Secure setup complete'"
        )
        return [
            "openclaw config set gateway.auth.token secure-token-env-test",
            f"openclaw channels login --channel {params['channel']}",
            _maybe_message_dry_run(msg_cmd),
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "config",
                "config_path": "gateway.auth.token",
                "condition": "equals",
                "expected": "secure-token-env-test",
                "name": "auth token configured",
            },
            {
                "type": "state",
                "field": f"channels.{params['channel']}",
                "condition": "exists",
                "expected": None,
                "name": f"{params['channel']} configured",
            },
            {
                "type": "effect",
                "effect_type": "messages_sent",
                "condition": "field_equals",
                "expected": {"field": "target", "value": params["target"]},
                "name": "confirmation message sent",
            },
        ]


@BaseTaskGenerator.register("full_setup_and_monitor")
class FullSetupAndMonitorGenerator(BaseTaskGenerator):
    """Cross-domain: configure model, start gateway, connect channel, check health."""

    required_domains = ("setup_config", "monitoring", "channel_mgmt")
    difficulty = 3
    parameters = {
        "model": _MODELS,
        "channel": _CHANNELS,
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "model": params["model"],
                "channel": params["channel"],
            },
            private={
                "expected_model": params["model"],
                "expected_channel": params["channel"],
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"Perform a complete openclaw setup:\n"
            f"1. Set the default model to '{params['model']}'\n"
            f"2. Start the gateway\n"
            f"3. Log into the {params['channel']} channel\n"
            f"4. Verify the system health"
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            f"openclaw models set {params['model']}",
            "openclaw gateway start",
            f"openclaw channels login --channel {params['channel']}",
            "openclaw health",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "config",
                "config_path": "agent.model",
                "condition": "equals",
                "expected": params["model"],
                "name": "model configured",
            },
            {
                "type": "state",
                "field": "gateway_status.running",
                "condition": "equals",
                "expected": True,
                "name": "gateway running",
            },
            {
                "type": "state",
                "field": f"channels.{params['channel']}",
                "condition": "exists",
                "expected": None,
                "name": f"{params['channel']} connected",
            },
        ]


@BaseTaskGenerator.register("calendar_weather_check")
class CalendarWeatherCheckGenerator(BaseTaskGenerator):
    """Cross-app: check weather for an event date; if rainy, reschedule."""

    required_domains = ("calendar", "weather")
    difficulty = 3
    parameters = {
        "event_title": ["Team offsite", "Company picnic", "Outdoor workshop"],
        "rainy_date": ["2026-03-01", "2026-03-02"],
        "fallback_date": ["2026-03-03T10:00", "2026-03-05T10:00"],
        "location": ["New York", "London"],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "event_title": params["event_title"],
                "original_date": params["rainy_date"],
                "fallback_datetime": params["fallback_date"],
                "location": params["location"],
            },
            private={
                "expected_reschedule_datetime": params["fallback_date"],
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"I planned '{params['event_title']}' for {params['rainy_date']} in "
            f"{params['location']}. Check the forecast — if it's rainy, reschedule to "
            f"{params['fallback_date']}; otherwise book it at {params['rainy_date']}T10:00."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        if _is_universal_profile():
            return build_universal_weather_on_date_commands(
                params["location"],
                params["rainy_date"],
            ) + [
                _calendar_add_command(
                    params["event_title"],
                    params["fallback_date"],
                    location=params["location"],
                )
            ]
        return [
            f"weather get --location '{params['location']}' --date {params['rainy_date']}",
            _calendar_add_command(
                params["event_title"],
                params["fallback_date"],
                location=params["location"],
            ),
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "effect",
                "effect_type": "calendar_events_created",
                "condition": "count_gte",
                "expected": 1,
                "name": "event added to calendar",
            },
        ]


@BaseTaskGenerator.register("email_to_task")
class EmailToTaskGenerator(BaseTaskGenerator):
    """Cross-app: find an email then create a task from its subject."""

    required_domains = ("email", "tasks")
    difficulty = 3
    parameters = {
        "email_query": ["proposal", "budget", "review"],
        "priority": ["high", "medium"],
        "due": ["2026-03-07", "2026-03-10"],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "email_query": params["email_query"],
                "priority": params["priority"],
                "due": params["due"],
            },
            private={
                "expected_priority": params["priority"],
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"I got an email about '{params['email_query']}' that needs follow-up. "
            f"Search my inbox, then create a {params['priority']}-priority task "
            f"due {params['due']} based on the subject."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        # Map query to expected subject for known seeds
        query_to_title = {
            "proposal": "Follow up: Project proposal",
            "budget": "Follow up: Budget report",
            "review": "Follow up: Quarterly review",
        }
        task_title = query_to_title.get(params["email_query"], f"Follow up: {params['email_query']}")
        return [
            f"email search --query '{params['email_query']}'",
            f"tasks add --title '{task_title}' "
            f"--priority {params['priority']} --due {params['due']}",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "effect",
                "effect_type": "tasks_created",
                "condition": "count_gte",
                "expected": 1,
                "name": "task created from email",
            },
        ]


@BaseTaskGenerator.register("email_to_calendar")
class EmailToCalendarGenerator(BaseTaskGenerator):
    """Cross-app: find an email mentioning a meeting, create a calendar event."""

    required_domains = ("email", "calendar")
    difficulty = 3
    parameters = {
        "email_query": ["meeting", "review", "standup"],
        "event_start": ["2026-03-10T14:00", "2026-03-11T10:00", "2026-03-12T09:00"],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "email_query": params["email_query"],
                "event_start": params["event_start"],
            },
            private={},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"There's an email in my inbox about '{params['email_query']}' mentioning a meeting. "
            f"Find it and create a calendar event based on the subject, starting at {params['event_start']}."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        query_to_title = {
            "meeting": "Meeting from email",
            "review": "Review session",
            "standup": "Standup meeting",
        }
        event_title = query_to_title.get(params["email_query"], f"Event: {params['email_query']}")
        return [
            f"email search --query '{params['email_query']}'",
            _calendar_add_command(event_title, params["event_start"]),
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "effect",
                "effect_type": "calendar_events_created",
                "condition": "count_gte",
                "expected": 1,
                "name": "calendar event created from email",
            },
        ]


@BaseTaskGenerator.register("task_and_calendar_sync")
class TaskAndCalendarSyncGenerator(BaseTaskGenerator):
    """Cross-app: add a task and a matching calendar time block."""

    required_domains = ("tasks", "calendar")
    difficulty = 2
    parameters = {
        "title": ["Deep work session", "Code review block", "Planning session"],
        "due": ["2026-03-08", "2026-03-09", "2026-03-10"],
        "start": ["2026-03-08T09:00", "2026-03-09T10:00", "2026-03-10T13:00"],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "title": params["title"],
                "due": params["due"],
                "start": params["start"],
            },
            private={},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"Keep my task list and calendar in sync: "
            f"add '{params['title']}' as a task due {params['due']}, "
            f"and block that time on the calendar at {params['start']}."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            f"tasks add --title '{params['title']}' --due {params['due']}",
            _calendar_add_command(params["title"], params["start"]),
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "effect",
                "effect_type": "tasks_created",
                "condition": "count_gte",
                "expected": 1,
                "name": "task created",
            },
            {
                "type": "effect",
                "effect_type": "calendar_events_created",
                "condition": "count_gte",
                "expected": 1,
                "name": "calendar block created",
            },
        ]


@BaseTaskGenerator.register("send_and_calendar")
class SendAndCalendarGenerator(BaseTaskGenerator):
    """Cross-app: send a message via openclaw AND book a follow-up meeting."""

    required_domains = ("messaging", "calendar")
    difficulty = 3
    parameters = {
        "channel": ["telegram", "slack"],
        "target": ["@alice", "@bob"],
        "message": [
            "Let's sync up. I'm booking a meeting for us.",
            "Following up — scheduling a call to discuss.",
        ],
        "meeting_start": ["2026-03-10T15:00", "2026-03-11T10:00"],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "channel": params["channel"],
                "target": params["target"],
                "message": params["message"],
                "meeting_start": params["meeting_start"],
            },
            private={
                "expected_target": params["target"],
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"I want to reach out to {params['target']} and lock in a meeting. "
            f"Send them on {params['channel']}: '{params['message']}'. "
            f"Then book a follow-up at {params['meeting_start']} "
            f"titled 'Follow-up with {params['target']}'."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        msg_cmd = (
            f"openclaw message send --channel {params['channel']} "
            f"--target {params['target']} --message '{params['message']}'"
        )
        return [
            f"openclaw channels login --channel {params['channel']}",
            _maybe_message_dry_run(msg_cmd),
            _calendar_add_command(
                f"Follow-up with {params['target']}",
                params["meeting_start"],
            ),
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "effect",
                "effect_type": "messages_sent",
                "condition": "field_equals",
                "expected": {"field": "target", "value": params["target"]},
                "name": f"message sent to {params['target']}",
            },
            {
                "type": "effect",
                "effect_type": "calendar_events_created",
                "condition": "count_gte",
                "expected": 1,
                "name": "follow-up meeting booked",
            },
        ]


@BaseTaskGenerator.register("full_workflow_multi_app")
class FullWorkflowMultiAppGenerator(BaseTaskGenerator):
    """Cross-app full workflow: email → task + calendar → notify via message."""

    required_domains = ("email", "tasks", "calendar", "messaging")
    difficulty = 3
    parameters = {
        "email_query": ["proposal", "budget"],
        "channel": ["telegram", "slack"],
        "notify_target": ["@alice", "#general"],
        "task_due": ["2026-03-10", "2026-03-12"],
        "meeting_start": ["2026-03-11T10:00", "2026-03-13T14:00"],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "email_query": params["email_query"],
                "channel": params["channel"],
                "notify_target": params["notify_target"],
                "task_due": params["task_due"],
                "meeting_start": params["meeting_start"],
            },
            private={},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"There's an email about '{params['email_query']}' that needs action. "
            f"Search my inbox, create a follow-up task due {params['task_due']}, "
            f"block time at {params['meeting_start']} on my calendar, "
            f"then let {params['notify_target']} know via {params['channel']} that you're on it."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        query_map = {
            "proposal": ("Follow up: Project proposal", "Project proposal review"),
            "budget": ("Follow up: Budget report", "Budget review session"),
        }
        task_title, event_title = query_map.get(
            params["email_query"],
            (f"Follow up: {params['email_query']}", f"{params['email_query'].capitalize()} session"),
        )
        eq = params["email_query"]
        msg_cmd = (
            f"openclaw message send --channel {params['channel']} "
            f"--target {params['notify_target']} "
            f"--message 'I am working on the {eq} follow-up.'"
        )
        return [
            f"email search --query '{eq}'",
            f"tasks add --title '{task_title}' --priority high --due {params['task_due']}",
            _calendar_add_command(event_title, params["meeting_start"]),
            f"openclaw channels login --channel {params['channel']}",
            _maybe_message_dry_run(msg_cmd),
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "effect",
                "effect_type": "tasks_created",
                "condition": "count_gte",
                "expected": 1,
                "name": "task created",
            },
            {
                "type": "effect",
                "effect_type": "calendar_events_created",
                "condition": "count_gte",
                "expected": 1,
                "name": "calendar block created",
            },
            {
                "type": "effect",
                "effect_type": "messages_sent",
                "condition": "count_gte",
                "expected": 1,
                "name": "notification sent",
            },
        ]


@BaseTaskGenerator.register("cron_with_plugin_workflow")
class CronWithPluginWorkflowGenerator(BaseTaskGenerator):
    """Cross-domain: install a plugin then create a cron job using it."""

    required_domains = ("plugin_skill", "cron_webhook")
    difficulty = 3
    parameters = {
        "plugin": _PLUGINS[:4],
        "schedule": _SCHEDULES,
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "plugin": params["plugin"],
                "schedule": params["schedule"],
            },
            private={},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"Set up an automated workflow:\n"
            f"1. Install the '{params['plugin']}' plugin\n"
            f"2. Create a cron job with schedule '{params['schedule']}' "
            f"that triggers a plugin action"
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        job_name = _job_name("plugin-cron", params)
        return [
            f"openclaw plugins enable {params['plugin']}",
            f"openclaw cron add --name {job_name} --cron '{params['schedule']}' "
            "--message 'Run periodic plugin check'",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "effect",
                "effect_type": "plugins_installed",
                "condition": "field_equals",
                "expected": {"field": "name", "value": params["plugin"]},
                "name": f"plugin '{params['plugin']}' installed",
            },
            {
                "type": "effect",
                "effect_type": "cron_jobs_created",
                "condition": "count_gte",
                "expected": 1,
                "name": "cron job created",
            },
        ]
