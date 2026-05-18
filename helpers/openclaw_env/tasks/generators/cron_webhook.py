"""Task generators for Cron & Webhook domain (D7)."""

from __future__ import annotations

import hashlib
from typing import Any, Iterator

from openclaw_env.core.task import TaskData
from openclaw_env.tasks.registry import BaseTaskGenerator, Pass, SetupResult

_SCHEDULES = [
    "0 9 * * *",       # Every day at 9am
    "0 9 * * 1-5",     # Weekdays at 9am
    "*/15 * * * *",    # Every 15 minutes
    "0 8 * * 1",       # Every Monday at 8am
    "30 17 * * 5",     # Every Friday at 5:30pm
    "0 12 1 * *",      # First of month at noon
    "0 */6 * * *",     # Every 6 hours
    "0 0 * * *",       # Midnight daily
]

_TARGETS = [
    "@alice",
    "#general",
    "@team",
    "+1234567890",
]

_CHANNELS = ["telegram", "slack", "discord", "whatsapp"]

_WEBHOOK_URLS = [
    "https://hooks.example.com/notify",
    "https://api.myapp.io/webhook",
    "https://alerts.ops.io/incoming",
    "https://notify.service.io/events",
    "https://hooks.n8n.cloud/workflow/abc123",
]


def _job_name(prefix: str, params: dict[str, Any]) -> str:
    seed = "|".join(f"{k}={params[k]}" for k in sorted(params))
    digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()[:8]
    return f"{prefix}-{digest}"


@BaseTaskGenerator.register("create_cron_job")
class CreateCronJobGenerator(BaseTaskGenerator):
    """Create a scheduled cron job with a custom command."""

    required_domains = ("cron_webhook",)
    difficulty = 2
    parameters = {
        "schedule": _SCHEDULES[:6],
        "target": _TARGETS,
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "schedule": params["schedule"],
                "target": params["target"],
            },
            private={
                "expected_schedule": params["schedule"],
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"Create a cron job that runs on schedule '{params['schedule']}' "
            f"and sends a status update message to {params['target']}."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        job_name = _job_name("status-update", params)
        return [
            f"openclaw cron add --name {job_name} --cron '{params['schedule']}' "
            f"--message 'Send scheduled status update to {params['target']}'"
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "effect",
                "effect_type": "cron_jobs_created",
                "condition": "count_gte",
                "expected": 1,
                "name": "cron job created",
            },
            {
                "type": "effect",
                "effect_type": "cron_jobs_created",
                "condition": "field_contains",
                "expected": {"field": "schedule", "value": params["schedule"]},
                "name": f"cron schedule is '{params['schedule']}'",
            },
        ]


@BaseTaskGenerator.register("cron_send_message")
class CronSendMessageGenerator(BaseTaskGenerator):
    """Create a cron job to periodically send messages via a specific channel."""

    required_domains = ("cron_webhook", "messaging")
    difficulty = 2
    parameters = {
        "channel": _CHANNELS,
        "target": _TARGETS,
        "schedule": _SCHEDULES[:4],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "channel": params["channel"],
                "target": params["target"],
                "schedule": params["schedule"],
            },
            private={
                "expected_channel": params["channel"],
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"Log into the {params['channel']} channel, then create a cron job "
            f"with schedule '{params['schedule']}' that sends a daily report "
            f"to {params['target']} via {params['channel']}."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        job_name = _job_name("daily-report", params)
        return [
            f"openclaw channels login --channel {params['channel']}",
            f"openclaw cron add --name {job_name} --cron '{params['schedule']}' "
            f"--message 'Send daily report to {params['target']} via {params['channel']}'",
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


@BaseTaskGenerator.register("list_cron_jobs")
class ListCronJobsGenerator(BaseTaskGenerator):
    """List all configured cron jobs."""

    required_domains = ("cron_webhook",)
    difficulty = 1
    parameters = {}

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        yield Pass(), TaskData()

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return "List all currently configured cron jobs."

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return ["openclaw cron list"]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "output",
                "match_type": "regex",
                "expected": r"(cron|Cron|No cron)",
                "output_field": "last_stdout",
                "name": "cron jobs listed",
                "ignore_case": True,
            }
        ]


@BaseTaskGenerator.register("add_webhook")
class AddWebhookGenerator(BaseTaskGenerator):
    """Register a webhook URL for event notifications."""

    required_domains = ("cron_webhook",)
    difficulty = 1
    parameters = {
        "url": _WEBHOOK_URLS,
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={"url": params["url"]},
            private={"expected_url": params["url"]},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"Configure the gateway remote URL to '{params['url']}' "
            f"for webhook/event routing."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        # `integrations.webhooks.*` is rejected by current OpenClaw config schema.
        # Use a stable, supported URL-bearing path instead.
        return [f"openclaw config set gateway.remote.url {params['url']}"]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "config",
                "config_path": "gateway.remote.url",
                "condition": "equals",
                "expected": params["url"],
                "name": "gateway remote url configured",
            },
        ]
