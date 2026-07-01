"""Complex composed workflow tasks built from safe-core + high-volatility command chains."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import itertools
import re
from typing import Any, Callable, Iterator

from openclaw_env.core.task import TaskData
from openclaw_env.tasks.generation_options import get_generation_options
from openclaw_env.tasks.registry import BaseTaskGenerator, Fail, Pass, SetupResult

_MODELS = [
    "anthropic/claude-opus-4-6",
    "anthropic/claude-sonnet-4-5-20250929",
    "openai/gpt-4o",
    "openai/gpt-4.1",
]

_PLUGINS = ["discord", "slack", "telegram", "whatsapp"]
_CHANNELS = ["discord", "slack", "telegram", "whatsapp"]
_TARGETS = ["#general", "@team", "@alice", "+1234567890"]

_LOCATIONS = ["New York", "London", "Tokyo", "Paris"]
_TIMEZONES = ["UTC", "America/New_York", "Europe/London"]
_WEATHER_DAYS = [3, 5, 7]

_EMAIL_QUERIES = ["proposal", "budget", "review", "meeting", "handover"]
_EMAIL_RECIPIENTS = [
    "alice@example.com",
    "bob@example.com",
    "team@example.com",
    "manager@example.com",
]
_EMAIL_SUBJECTS = [
    "Daily briefing",
    "Release readiness",
    "Incident follow-up",
    "Customer status",
]
_EMAIL_BODIES = [
    "Sharing a short update and next actions.",
    "Please review and confirm the plan.",
    "Documenting impact and mitigations.",
    "Following up with proposed timelines.",
]

_TASK_TITLES = [
    "Prepare planning memo",
    "Review release checklist",
    "Write retro notes",
    "Refine milestone draft",
    "Draft project update",
    "Collect stakeholder feedback",
]
_TASK_DUES = ["2026-03-08", "2026-03-09", "2026-03-10", "2026-03-11"]

_EVENT_TITLES = [
    "Planning sync",
    "Execution review",
    "Risk check-in",
    "Roadmap alignment",
]
_EVENT_STARTS = [
    "2026-03-10T09:00",
    "2026-03-10T13:00",
    "2026-03-11T10:00",
    "2026-03-12T14:00",
]
_LIST_FROM_DATES = ["2026-03-08", "2026-03-09", "2026-03-10"]
_LIST_TO_DATES = ["2026-03-12", "2026-03-13", "2026-03-14"]

_GATEWAY_PORTS = [18789, 18801, 18811, 18821, 18831, 18841]
_SCHEDULES = ["0 9 * * *", "0 18 * * 1-5", "*/30 * * * *", "15 8 * * 1-5"]
_AGENT_NAMES = ["planner", "scheduler", "reviewer", "tracker", "notifier", "coordinator"]

_WEBHOOK_URLS = [
    "https://hooks.example.com/notify",
    "https://api.myapp.io/webhook",
    "https://alerts.ops.io/incoming",
    "https://notify.service.io/events",
]

_FILE_PATHS = [
    "/notes/postmortem.txt",
    "/reports/release-summary.txt",
    "/ops/incident-brief.txt",
    "/workspace/status-note.txt",
]

_MESSAGE_BODIES = [
    "Status summary posted. Please review.",
    "Incident triage started. Acknowledge in thread.",
    "Release gate passed. Proceed to rollout.",
    "Daily briefing compiled and shared.",
]


# Legacy profile catalog (older benchmark-style scenarios)
_LEGACY_SCENARIO_CATALOG: dict[str, dict[str, str]] = {
    "triage_weather_task": {
        "slug": "triage_weather_task",
        "title": "Morning Field Triage",
        "goal": "Prepare a same-day execution plan before teams head out.",
    },
    "audit_email_calendar": {
        "slug": "audit_email_calendar",
        "title": "Inbox Risk Follow-up",
        "goal": "Turn potentially risky inbox signals into scheduled follow-up work.",
    },
    "plugin_forecast_capture": {
        "slug": "plugin_forecast_capture",
        "title": "Ops Snapshot Capture",
        "goal": "Collect operational context and record forecast-driven tracking work.",
    },
    "doctor_mark_complete": {
        "slug": "doctor_mark_complete",
        "title": "Housekeeping Sweep",
        "goal": "Run health cleanup and close out outstanding maintenance items.",
    },
    "config_status_calendar_task": {
        "slug": "config_status_calendar_task",
        "title": "Pre-Launch Control Check",
        "goal": "Adjust runtime configuration and align execution blocks before launch.",
    },
    "agent_inbox_followup": {
        "slug": "agent_inbox_followup",
        "title": "Delegation Follow-up Loop",
        "goal": "Create a focused helper agent and convert inbox findings into tasks.",
    },
    "plugin_weather_schedule": {
        "slug": "plugin_weather_schedule",
        "title": "Channel Ops Readiness",
        "goal": "Enable a target channel plugin and schedule location-based check-ins.",
    },
    "cron_forecast_today": {
        "slug": "cron_forecast_today",
        "title": "Daily Briefing Automation",
        "goal": "Set up recurring briefing automation and validate day context signals.",
    },
    "model_port_plan_block": {
        "slug": "model_port_plan_block",
        "title": "Planning Control-Plane Sync",
        "goal": "Synchronize model and gateway settings with concrete execution blocks.",
    },
    "agent_plugin_cron_review": {
        "slug": "agent_plugin_cron_review",
        "title": "Ops Orchestration Runbook",
        "goal": "Wire agent, plugin, and cron foundations before doing live checks.",
    },
}


# life_work profile catalog (new realistic scenarios)
_LIFE_WORK_SCENARIOS: dict[str, dict[str, str]] = {
    "morning_briefing_and_notify": {
        "slug": "morning_briefing_and_notify",
        "title": "Morning Briefing And Notify",
        "goal": "Run a morning check and notify the team with conditions.",
    },
    "email_to_calendar_commitment": {
        "slug": "email_to_calendar_commitment",
        "title": "Email To Calendar Commitment",
        "goal": "Turn an inbox commitment into a scheduled calendar action.",
    },
    "meeting_conflict_replan": {
        "slug": "meeting_conflict_replan",
        "title": "Meeting Conflict Replan",
        "goal": "Review calendar conflicts and create a replacement task plan.",
    },
    "travel_weather_reschedule": {
        "slug": "travel_weather_reschedule",
        "title": "Travel Weather Reschedule",
        "goal": "Use travel weather outlook to re-block meetings.",
    },
    "release_readiness_gate": {
        "slug": "release_readiness_gate",
        "title": "Release Readiness Gate",
        "goal": "Validate release prerequisites before locking execution slots.",
    },
    "incident_channel_triage": {
        "slug": "incident_channel_triage",
        "title": "Incident Channel Triage",
        "goal": "Establish incident comms and create the first triage task.",
    },
    "agent_delegation_followup": {
        "slug": "agent_delegation_followup",
        "title": "Agent Delegation Followup",
        "goal": "Delegate inbox-driven follow-up work to a dedicated helper agent.",
    },
    "plugin_rollout_validation": {
        "slug": "plugin_rollout_validation",
        "title": "Plugin Rollout Validation",
        "goal": "Enable and validate a channel plugin before rollout messaging.",
    },
    "security_audit_and_alert": {
        "slug": "security_audit_and_alert",
        "title": "Security Audit And Alert",
        "goal": "Run a security audit and issue an operational alert.",
    },
    "cron_digest_automation": {
        "slug": "cron_digest_automation",
        "title": "Cron Digest Automation",
        "goal": "Automate recurring digests and verify daily context.",
    },
    "customer_followup_pipeline": {
        "slug": "customer_followup_pipeline",
        "title": "Customer Followup Pipeline",
        "goal": "Convert customer-related inbox signal into a tracked action.",
    },
    "device_pairing_confirmation": {
        "slug": "device_pairing_confirmation",
        "title": "Device Pairing Confirmation",
        "goal": "Pair a device and capture immediate operational follow-up.",
    },
    "webhook_integration_check": {
        "slug": "webhook_integration_check",
        "title": "Webhook Integration Check",
        "goal": "Configure webhook routing and verify downstream scheduling.",
    },
    "multi_channel_status_broadcast": {
        "slug": "multi_channel_status_broadcast",
        "title": "Multi Channel Status Broadcast",
        "goal": "Push a status update through channel tooling and retain evidence.",
    },
    "task_inbox_calendar_sync": {
        "slug": "task_inbox_calendar_sync",
        "title": "Task Inbox Calendar Sync",
        "goal": "Synchronize inbox findings, tasks, and calendar blocks.",
    },
    "postmortem_capture_workflow": {
        "slug": "postmortem_capture_workflow",
        "title": "Postmortem Capture Workflow",
        "goal": "Capture postmortem notes and schedule formal review.",
    },
}


def _command_history_check(command: str, name: str) -> dict[str, Any]:
    return {
        "type": "output",
        "match_type": "regex",
        "expected": re.escape(command) + r".*?'exit_code':\s*0",
        "output_field": "command_history",
        "name": name,
        "ignore_case": False,
    }


def _final_exit_zero_check() -> dict[str, Any]:
    return {
        "type": "output",
        "condition": "exit_code_zero",
        "expected": None,
        "name": "final command succeeds",
    }


@dataclass(frozen=True)
class AtomicOp:
    op_id: str
    is_openclaw: bool
    mutates: bool
    build_cmd: Callable[[dict[str, Any]], str]
    build_checks: Callable[[dict[str, Any]], list[dict[str, Any]]]


@dataclass(frozen=True)
class WorkflowSpec:
    template_id: str
    variant_id: int
    scenario_slug: str
    scenario_title: str
    scenario_goal: str
    realism_tier: str
    high_volatility: bool
    strict_online_risk: str
    instruction: str
    commands: list[str]
    checks: list[dict[str, Any]]
    openclaw_step_count: int
    causal_chain_score: float = 0.0
    entity_consistency_pass: bool = True
    filler_step_count: int = 0
    anchors: dict[str, str] | None = None


_TITLE_RE = re.compile(r"--title '([^']+)'")
_SUBJECT_RE = re.compile(r"--subject '([^']+)'")
_BODY_RE = re.compile(r"--body '([^']+)'")
_LOCATION_RE = re.compile(r"--location '([^']+)'")


def _ctx_product(count: int, **axes: list[Any]) -> list[dict[str, Any]]:
    keys = list(axes.keys())
    values = [axes[k] for k in keys]
    combos = list(itertools.product(*values))
    if len(combos) < count:
        raise ValueError(
            f"Not enough combinations for count={count}; only {len(combos)} available."
        )
    out: list[dict[str, Any]] = []
    for i, combo in enumerate(combos[:count], start=1):
        item = dict(zip(keys, combo))
        item["variant_id"] = i
        out.append(item)
    return out


def _agent_name(ctx: dict[str, Any]) -> str:
    return f"{ctx['agent_base']}-{ctx['variant_id']:02d}"


def _cron_name(ctx: dict[str, Any]) -> str:
    return f"cwf-{ctx['template_id'].replace('_', '-')}-{ctx['variant_id']:02d}"


def _scenario_prefix(title: str, goal: str) -> str:
    return f"[{title}] {goal}"


def _complex_task_id(scenario_slug: str, variant_id: int) -> str:
    return f"complex_{scenario_slug}_{variant_id}"


_OPS: dict[str, AtomicOp] = {
    "oc_status": AtomicOp(
        op_id="oc_status",
        is_openclaw=True,
        mutates=False,
        build_cmd=lambda ctx: "openclaw status",
        build_checks=lambda ctx: [],
    ),
    "oc_doctor": AtomicOp(
        op_id="oc_doctor",
        is_openclaw=True,
        mutates=False,
        build_cmd=lambda ctx: "openclaw doctor",
        build_checks=lambda ctx: [],
    ),
    "oc_security_audit": AtomicOp(
        op_id="oc_security_audit",
        is_openclaw=True,
        mutates=False,
        build_cmd=lambda ctx: "openclaw security audit",
        build_checks=lambda ctx: [],
    ),
    "oc_agents_list": AtomicOp(
        op_id="oc_agents_list",
        is_openclaw=True,
        mutates=False,
        build_cmd=lambda ctx: "openclaw agents list",
        build_checks=lambda ctx: [],
    ),
    "oc_plugins_list": AtomicOp(
        op_id="oc_plugins_list",
        is_openclaw=True,
        mutates=False,
        build_cmd=lambda ctx: "openclaw plugins list",
        build_checks=lambda ctx: [],
    ),
    "oc_channels_list_json": AtomicOp(
        op_id="oc_channels_list_json",
        is_openclaw=True,
        mutates=False,
        build_cmd=lambda ctx: "openclaw channels list --json",
        build_checks=lambda ctx: [],
    ),
    "oc_cron_list": AtomicOp(
        op_id="oc_cron_list",
        is_openclaw=True,
        mutates=False,
        build_cmd=lambda ctx: "openclaw cron list",
        build_checks=lambda ctx: [],
    ),
    "oc_devices_list": AtomicOp(
        op_id="oc_devices_list",
        is_openclaw=True,
        mutates=False,
        build_cmd=lambda ctx: "openclaw devices list",
        build_checks=lambda ctx: [],
    ),
    "oc_models_set": AtomicOp(
        op_id="oc_models_set",
        is_openclaw=True,
        mutates=True,
        build_cmd=lambda ctx: f"openclaw models set {ctx['model']}",
        build_checks=lambda ctx: [
            {
                "type": "config",
                "config_path": "agent.model",
                "condition": "equals",
                "expected": ctx["model"],
                "name": "model configured",
            }
        ],
    ),
    "oc_config_port": AtomicOp(
        op_id="oc_config_port",
        is_openclaw=True,
        mutates=True,
        build_cmd=lambda ctx: f"openclaw config set gateway.port {ctx['gateway_port']}",
        build_checks=lambda ctx: [
            {
                "type": "config",
                "config_path": "gateway.port",
                "condition": "equals",
                "expected": ctx["gateway_port"],
                "name": "gateway port configured",
            }
        ],
    ),
    "oc_set_remote_url": AtomicOp(
        op_id="oc_set_remote_url",
        is_openclaw=True,
        mutates=True,
        build_cmd=lambda ctx: f"openclaw config set gateway.remote.url {ctx['webhook_url']}",
        build_checks=lambda ctx: [
            {
                "type": "config",
                "config_path": "gateway.remote.url",
                "condition": "equals",
                "expected": ctx["webhook_url"],
                "name": "gateway remote url configured",
            }
        ],
    ),
    "oc_agents_add": AtomicOp(
        op_id="oc_agents_add",
        is_openclaw=True,
        mutates=True,
        build_cmd=lambda ctx: f"openclaw agents add {_agent_name(ctx)} --model {ctx['model']}",
        build_checks=lambda ctx: [
            {
                "type": "state",
                "field": f"agents.{_agent_name(ctx)}",
                "condition": "exists",
                "expected": None,
                "name": "agent created",
            }
        ],
    ),
    "oc_channels_login": AtomicOp(
        op_id="oc_channels_login",
        is_openclaw=True,
        mutates=True,
        build_cmd=lambda ctx: f"openclaw channels login --channel {ctx['channel']}",
        build_checks=lambda ctx: [
            {
                "type": "state",
                "field": f"channels.{ctx['channel']}",
                "condition": "exists",
                "expected": None,
                "name": "channel configured",
            }
        ],
    ),
    "oc_plugins_enable": AtomicOp(
        op_id="oc_plugins_enable",
        is_openclaw=True,
        mutates=True,
        build_cmd=lambda ctx: f"openclaw plugins enable {ctx['plugin']}",
        build_checks=lambda ctx: [
            {
                "type": "effect",
                "effect_type": "plugins_installed",
                "condition": "field_equals",
                "expected": {"field": "name", "value": ctx["plugin"]},
                "name": "plugin enabled",
            }
        ],
    ),
    "oc_cron_add": AtomicOp(
        op_id="oc_cron_add",
        is_openclaw=True,
        mutates=True,
        build_cmd=lambda ctx: (
            f"openclaw cron add --name {_cron_name(ctx)} "
            f"--cron '{ctx['schedule']}' --message '{ctx['cron_message']}'"
        ),
        build_checks=lambda ctx: [
            {
                "type": "effect",
                "effect_type": "cron_jobs_created",
                "condition": "count_gte",
                "expected": 1,
                "name": "cron job created",
            }
        ],
    ),
    "oc_devices_pair": AtomicOp(
        op_id="oc_devices_pair",
        is_openclaw=True,
        mutates=True,
        build_cmd=lambda ctx: "openclaw devices pair",
        build_checks=lambda ctx: [],
    ),
    "oc_message_send": AtomicOp(
        op_id="oc_message_send",
        is_openclaw=True,
        mutates=True,
        build_cmd=lambda ctx: (
            f"openclaw message send --channel {ctx['channel']} "
            f"--target {ctx['target']} --message '{ctx['message_body']}'"
        ),
        build_checks=lambda ctx: [
            {
                "type": "effect",
                "effect_type": "messages_sent",
                "condition": "count_gte",
                "expected": 1,
                "name": "message sent",
            }
        ],
    ),
    "oc_message_search": AtomicOp(
        op_id="oc_message_search",
        is_openclaw=True,
        mutates=False,
        build_cmd=lambda ctx: (
            "openclaw message search --channel discord "
            "--guild-id 123456789012345678 --channel-id 234567890123456789 "
            f"--query '{ctx['email_query']}'"
        ),
        build_checks=lambda ctx: [],
    ),
    "weather_get": AtomicOp(
        op_id="weather_get",
        is_openclaw=False,
        mutates=False,
        build_cmd=lambda ctx: f"weather get --location '{ctx['location']}'",
        build_checks=lambda ctx: [],
    ),
    "weather_forecast": AtomicOp(
        op_id="weather_forecast",
        is_openclaw=False,
        mutates=False,
        build_cmd=lambda ctx: (
            f"weather forecast --location '{ctx['location']}' --days {ctx['days']}"
        ),
        build_checks=lambda ctx: [],
    ),
    "email_search": AtomicOp(
        op_id="email_search",
        is_openclaw=False,
        mutates=False,
        build_cmd=lambda ctx: f"email search --query '{ctx['email_query']}'",
        build_checks=lambda ctx: [],
    ),
    "email_list_unread": AtomicOp(
        op_id="email_list_unread",
        is_openclaw=False,
        mutates=False,
        build_cmd=lambda ctx: "email list --folder inbox --unread",
        build_checks=lambda ctx: [],
    ),
    "email_move_seed": AtomicOp(
        op_id="email_move_seed",
        is_openclaw=False,
        mutates=True,
        build_cmd=lambda ctx: (
            f"email move --id {ctx['seed_email_id']} --folder {ctx['mail_folder']}"
        ),
        build_checks=lambda ctx: [
            {
                "type": "effect",
                "effect_type": "emails_moved",
                "condition": "count_gte",
                "expected": 1,
                "name": "email moved",
            }
        ],
    ),
    "email_send": AtomicOp(
        op_id="email_send",
        is_openclaw=False,
        mutates=True,
        build_cmd=lambda ctx: (
            f"email send --to {ctx['recipient']} "
            f"--subject '{ctx['subject']}' --body '{ctx['body']}'"
        ),
        build_checks=lambda ctx: [
            {
                "type": "effect",
                "effect_type": "emails_sent",
                "condition": "count_gte",
                "expected": 1,
                "name": "email sent",
            }
        ],
    ),
    "tasks_add": AtomicOp(
        op_id="tasks_add",
        is_openclaw=False,
        mutates=True,
        build_cmd=lambda ctx: (
            f"tasks add --title '{ctx['task_title']}' "
            f"--priority {ctx['priority']} --due {ctx['task_due']}"
        ),
        build_checks=lambda ctx: [
            {
                "type": "effect",
                "effect_type": "tasks_created",
                "condition": "count_gte",
                "expected": 1,
                "name": "task created",
            }
        ],
    ),
    "tasks_search": AtomicOp(
        op_id="tasks_search",
        is_openclaw=False,
        mutates=False,
        build_cmd=lambda ctx: f"tasks search --query '{ctx['email_query']}'",
        build_checks=lambda ctx: [],
    ),
    "tasks_list_pending": AtomicOp(
        op_id="tasks_list_pending",
        is_openclaw=False,
        mutates=False,
        build_cmd=lambda ctx: "tasks list --status pending",
        build_checks=lambda ctx: [],
    ),
    "tasks_complete_seed": AtomicOp(
        op_id="tasks_complete_seed",
        is_openclaw=False,
        mutates=True,
        build_cmd=lambda ctx: f"tasks complete --id {ctx['seed_task_id']}",
        build_checks=lambda ctx: [
            {
                "type": "effect",
                "effect_type": "tasks_completed",
                "condition": "count_gte",
                "expected": 1,
                "name": "task completed",
            }
        ],
    ),
    "calendar_add": AtomicOp(
        op_id="calendar_add",
        is_openclaw=False,
        mutates=True,
        build_cmd=lambda ctx: (
            f"calendar add-event --title '{ctx['event_title']}' "
            f"--start {ctx['event_start']}"
        ),
        build_checks=lambda ctx: [
            {
                "type": "effect",
                "effect_type": "calendar_events_created",
                "condition": "count_gte",
                "expected": 1,
                "name": "calendar event created",
            }
        ],
    ),
    "calendar_list_range": AtomicOp(
        op_id="calendar_list_range",
        is_openclaw=False,
        mutates=False,
        build_cmd=lambda ctx: f"calendar list --from {ctx['from_date']} --to {ctx['to_date']}",
        build_checks=lambda ctx: [],
    ),
    "calendar_today": AtomicOp(
        op_id="calendar_today",
        is_openclaw=False,
        mutates=False,
        build_cmd=lambda ctx: f"calendar today --timezone {ctx['timezone']}",
        build_checks=lambda ctx: [],
    ),
    "file_create": AtomicOp(
        op_id="file_create",
        is_openclaw=False,
        mutates=True,
        build_cmd=lambda ctx: f"file create --path '{ctx['file_path']}' --content '{ctx['file_content']}'",
        build_checks=lambda ctx: [
            {
                "type": "effect",
                "effect_type": "files_created",
                "condition": "count_gte",
                "expected": 1,
                "name": "file created",
            }
        ],
    ),
}


def _build_workflow_checks(
    ctx: dict[str, Any],
    commands: list[str],
    ops: list[AtomicOp],
) -> list[dict[str, Any]]:
    # Realism-first evaluation: prioritize outcome/effects over rigid step order.
    # This keeps agent policy space flexible while still enforcing core results.
    checks: list[dict[str, Any]] = [_final_exit_zero_check()]
    for op in ops:
        checks.extend(op.build_checks(ctx))

    # For high-volatility command chains, enforce at least one explicit verification command.
    if any(
        op.op_id in {"oc_channels_login", "oc_message_send", "oc_plugins_enable"}
        for op in ops
    ):
        verify_pattern = (
            r"(openclaw\ channels\ list\ \-\-json|openclaw\ plugins\ list|"
            r"openclaw\ message\ search)"
        )
        checks.append(
            {
                "type": "output",
                "match_type": "regex",
                "expected": verify_pattern,
                "output_field": "command_history",
                "name": "high-volatility flow includes verification step",
                "ignore_case": False,
            }
        )

    return checks


def _entity_dependency_score(
    ctx: dict[str, Any],
    op_ids: list[str],
) -> tuple[float, bool]:
    possible = 0
    satisfied = 0
    consistent = True

    topic = str(ctx.get("topic_label", "")).lower()
    query = str(ctx.get("email_query", "")).lower()
    location = str(ctx.get("location", "")).lower()
    task_title = str(ctx.get("task_title", "")).lower()
    event_title = str(ctx.get("event_title", "")).lower()
    subject = str(ctx.get("subject", "")).lower()
    body = str(ctx.get("body", "")).lower()
    message_body = str(ctx.get("message_body", "")).lower()
    text_blob = " ".join([task_title, event_title, subject, body, message_body])

    if "oc_channels_login" in op_ids and "oc_message_send" in op_ids:
        possible += 1
        channel = str(ctx.get("channel", "")).strip().lower()
        ok = bool(channel)
        satisfied += int(ok)
        consistent = consistent and ok

    if "email_search" in op_ids and any(
        op in op_ids for op in {"tasks_add", "calendar_add", "email_send"}
    ):
        possible += 1
        ok = bool(query and (query in text_blob or topic in text_blob))
        satisfied += int(ok)
        consistent = consistent and ok

    if any(op in op_ids for op in {"weather_get", "weather_forecast"}) and any(
        op in op_ids for op in {"calendar_add", "email_send", "tasks_add", "file_create"}
    ):
        possible += 1
        ok = bool(location and location in text_blob)
        satisfied += int(ok)
        consistent = consistent and ok

    if "oc_plugins_enable" in op_ids and "oc_plugins_list" in op_ids:
        possible += 1
        ok = bool(str(ctx.get("plugin", "")).strip())
        satisfied += int(ok)
        consistent = consistent and ok

    if "oc_cron_add" in op_ids and "oc_cron_list" in op_ids:
        possible += 1
        ok = bool(str(ctx.get("schedule", "")).strip() and str(ctx.get("cron_message", "")).strip())
        satisfied += int(ok)
        consistent = consistent and ok

    if "tasks_add" in op_ids and "tasks_search" in op_ids:
        possible += 1
        ok = bool(query and query in task_title)
        satisfied += int(ok)
        consistent = consistent and ok

    if possible == 0:
        return 1.0, True
    return (satisfied / possible), consistent


def _filler_step_count(commands: list[str]) -> int:
    return sum(1 for cmd in commands if cmd.strip() == "openclaw status")


def _make_spec(
    template_id: str,
    scenario_slug: str,
    scenario_title: str,
    scenario_goal: str,
    realism_tier: str,
    high_volatility: bool,
    strict_online_risk: str,
    ctx: dict[str, Any],
    op_ids: list[str],
    instruction: str,
) -> WorkflowSpec:
    ops = [_OPS[op_id] for op_id in op_ids]
    commands = [op.build_cmd(ctx) for op in ops]
    checks = _build_workflow_checks(ctx, commands, ops)
    causal_score, entity_ok = _entity_dependency_score(ctx, op_ids)
    anchors = {
        "topic_label": str(ctx.get("topic_label", "")),
        "email_query": str(ctx.get("email_query", "")),
        "location": str(ctx.get("location", "")),
        "task_title": str(ctx.get("task_title", "")),
        "event_title": str(ctx.get("event_title", "")),
    }
    return WorkflowSpec(
        template_id=template_id,
        variant_id=int(ctx["variant_id"]),
        scenario_slug=scenario_slug,
        scenario_title=scenario_title,
        scenario_goal=scenario_goal,
        realism_tier=realism_tier,
        high_volatility=high_volatility,
        strict_online_risk=strict_online_risk,
        instruction=f"{_scenario_prefix(scenario_title, scenario_goal)} {instruction}",
        commands=commands,
        checks=checks,
        openclaw_step_count=sum(1 for op in ops if op.is_openclaw),
        causal_chain_score=round(causal_score, 4),
        entity_consistency_pass=entity_ok,
        filler_step_count=_filler_step_count(commands),
        anchors=anchors,
    )


def _validate_specs(
    specs: list[WorkflowSpec],
    *,
    expected_count: int,
    expected_scenarios: int,
    enforce_realism_rules: bool = False,
) -> None:
    if len(specs) != expected_count:
        raise RuntimeError(f"Expected {expected_count} complex workflow specs, found {len(specs)}.")

    scenario_counts: dict[str, int] = {}
    first_status_count = 0
    final_tasks_add_count = 0
    title_counts: Counter[str] = Counter()
    subject_counts: Counter[str] = Counter()
    body_counts: Counter[str] = Counter()
    location_counts: Counter[str] = Counter()
    causal_scores: list[float] = []
    entity_pass = 0
    for spec in specs:
        if len(spec.commands) < 3 or len(spec.commands) > 5:
            raise RuntimeError(
                f"Step count must be 3-5, got {len(spec.commands)} for {spec.scenario_slug}_{spec.variant_id}."
            )
        if not any(cmd.startswith("openclaw ") for cmd in spec.commands):
            raise RuntimeError(f"No openclaw command in {spec.scenario_slug}_{spec.variant_id}.")
        if not any(not cmd.startswith("openclaw ") for cmd in spec.commands):
            raise RuntimeError(f"No non-openclaw command in {spec.scenario_slug}_{spec.variant_id}.")
        joined = " ".join(spec.commands)
        if "email_seed_" in joined or "task_seed_" in joined:
            raise RuntimeError(f"Legacy seed-only flow detected in {spec.scenario_slug}_{spec.variant_id}.")
        if spec.commands and spec.commands[0].strip() == "openclaw status":
            first_status_count += 1
        if spec.commands and spec.commands[-1].startswith("tasks add "):
            final_tasks_add_count += 1
        if spec.entity_consistency_pass:
            entity_pass += 1
        causal_scores.append(float(spec.causal_chain_score))
        for cmd in spec.commands:
            title = _TITLE_RE.search(cmd)
            if title:
                title_counts[title.group(1)] += 1
            subject = _SUBJECT_RE.search(cmd)
            if subject:
                subject_counts[subject.group(1)] += 1
            body = _BODY_RE.search(cmd)
            if body:
                body_counts[body.group(1)] += 1
            location = _LOCATION_RE.search(cmd)
            if location:
                location_counts[location.group(1)] += 1
        scenario_counts[spec.scenario_slug] = scenario_counts.get(spec.scenario_slug, 0) + 1

    if len(scenario_counts) != expected_scenarios:
        raise RuntimeError(
            f"Expected {expected_scenarios} scenario slugs, found {len(scenario_counts)}."
        )
    if enforce_realism_rules:
        if first_status_count / len(specs) > 0.2:
            raise RuntimeError(
                f"Too many filler starts with openclaw status: {first_status_count}/{len(specs)}"
            )
        if final_tasks_add_count / len(specs) > 0.4:
            raise RuntimeError(
                f"Too many tasks-add endings: {final_tasks_add_count}/{len(specs)}"
            )
        if entity_pass != len(specs):
            raise RuntimeError(
                f"Entity consistency failed for {len(specs)-entity_pass} workflows."
            )
        avg_causal = sum(causal_scores) / len(causal_scores) if causal_scores else 0.0
        if avg_causal < 0.8:
            raise RuntimeError(f"Causal chain score too low: {avg_causal:.4f}")

        def _max_counter(counter: Counter[str]) -> int:
            return counter.most_common(1)[0][1] if counter else 0

        if _max_counter(title_counts) > 24:
            raise RuntimeError("Task/event title repetition too high; exceeds cap 24.")
        if _max_counter(subject_counts) > 24:
            raise RuntimeError("Email subject repetition too high; exceeds cap 24.")
        if _max_counter(body_counts) > 24:
            raise RuntimeError("Email/file body repetition too high; exceeds cap 24.")
        if _max_counter(location_counts) > 40:
            raise RuntimeError("Location repetition too high; exceeds cap 40.")


def _build_legacy_workflow_specs() -> list[WorkflowSpec]:
    """Preserve older benchmark-style pack (120 tasks) for compatibility replay."""

    specs: list[WorkflowSpec] = []

    for ctx in _ctx_product(8, location=_LOCATIONS, task_title=_TASK_TITLES[:2]):
        ctx.update(
            {
                "template_id": "triage_weather_task",
                "priority": "medium",
                "task_due": _TASK_DUES[(ctx["variant_id"] - 1) % len(_TASK_DUES)],
            }
        )
        meta = _LEGACY_SCENARIO_CATALOG["triage_weather_task"]
        specs.append(
            _make_spec(
                template_id="triage_weather_task",
                scenario_slug=meta["slug"],
                scenario_title=meta["title"],
                scenario_goal=meta["goal"],
                realism_tier="legacy",
                high_volatility=False,
                strict_online_risk="medium",
                ctx=ctx,
                op_ids=["oc_status", "weather_get", "tasks_add"],
                instruction=(
                    f"Start with a quick gateway sanity check, confirm current weather in "
                    f"{ctx['location']} for field conditions, then create task "
                    f"'{ctx['task_title']}' due {ctx['task_due']}."
                ),
            )
        )

    for ctx in _ctx_product(8, email_query=_EMAIL_QUERIES[:4], event_start=_EVENT_STARTS[:2]):
        ctx.update(
            {
                "template_id": "audit_email_calendar",
                "event_title": f"{ctx['email_query'].capitalize()} follow-up",
            }
        )
        meta = _LEGACY_SCENARIO_CATALOG["audit_email_calendar"]
        specs.append(
            _make_spec(
                template_id="audit_email_calendar",
                scenario_slug=meta["slug"],
                scenario_title=meta["title"],
                scenario_goal=meta["goal"],
                realism_tier="legacy",
                high_volatility=False,
                strict_online_risk="medium",
                ctx=ctx,
                op_ids=["oc_security_audit", "email_search", "calendar_add"],
                instruction=(
                    f"Run a security audit first, search inbox messages about "
                    f"'{ctx['email_query']}', then schedule '{ctx['event_title']}' at "
                    f"{ctx['event_start']} so follow-up is time-blocked."
                ),
            )
        )

    for ctx in _ctx_product(8, location=_LOCATIONS, days=_WEATHER_DAYS[:2]):
        ctx.update(
            {
                "template_id": "plugin_forecast_capture",
                "task_title": f"Capture {ctx['location']} forecast",
                "priority": "low",
                "task_due": _TASK_DUES[(ctx["variant_id"] - 1) % len(_TASK_DUES)],
            }
        )
        meta = _LEGACY_SCENARIO_CATALOG["plugin_forecast_capture"]
        specs.append(
            _make_spec(
                template_id="plugin_forecast_capture",
                scenario_slug=meta["slug"],
                scenario_title=meta["title"],
                scenario_goal=meta["goal"],
                realism_tier="legacy",
                high_volatility=True,
                strict_online_risk="medium",
                ctx=ctx,
                op_ids=["oc_plugins_list", "weather_forecast", "tasks_add"],
                instruction=(
                    f"Check currently available plugins, gather a {ctx['days']}-day forecast for "
                    f"{ctx['location']}, then capture it as task '{ctx['task_title']}'."
                ),
            )
        )

    for ctx in _ctx_product(8, email_query=_EMAIL_QUERIES[:4], task_title=_TASK_TITLES[:2]):
        ctx.update(
            {
                "template_id": "doctor_mark_complete",
                "priority": "medium",
                "task_due": _TASK_DUES[(ctx["variant_id"] - 1) % len(_TASK_DUES)],
            }
        )
        meta = _LEGACY_SCENARIO_CATALOG["doctor_mark_complete"]
        specs.append(
            _make_spec(
                template_id="doctor_mark_complete",
                scenario_slug=meta["slug"],
                scenario_title=meta["title"],
                scenario_goal=meta["goal"],
                realism_tier="legacy",
                high_volatility=False,
                strict_online_risk="low",
                ctx=ctx,
                op_ids=["oc_doctor", "email_search", "tasks_add"],
                instruction=(
                    f"Run diagnostics, search inbox for '{ctx['email_query']}', and create "
                    f"maintenance task '{ctx['task_title']}' due {ctx['task_due']}."
                ),
            )
        )

    for ctx in _ctx_product(12, gateway_port=_GATEWAY_PORTS, event_start=_EVENT_STARTS[:2]):
        idx = ctx["variant_id"] - 1
        ctx.update(
            {
                "template_id": "config_status_calendar_task",
                "event_title": _EVENT_TITLES[idx % len(_EVENT_TITLES)],
                "task_title": _TASK_TITLES[idx % len(_TASK_TITLES)],
                "priority": "high",
                "task_due": _TASK_DUES[idx % len(_TASK_DUES)],
            }
        )
        meta = _LEGACY_SCENARIO_CATALOG["config_status_calendar_task"]
        specs.append(
            _make_spec(
                template_id="config_status_calendar_task",
                scenario_slug=meta["slug"],
                scenario_title=meta["title"],
                scenario_goal=meta["goal"],
                realism_tier="legacy",
                high_volatility=False,
                strict_online_risk="medium",
                ctx=ctx,
                op_ids=["oc_config_port", "oc_status", "calendar_add", "tasks_add"],
                instruction=(
                    f"Set gateway port to {ctx['gateway_port']} and verify status, then reserve "
                    f"'{ctx['event_title']}' at {ctx['event_start']} and create matching task "
                    f"'{ctx['task_title']}'."
                ),
            )
        )

    for ctx in _ctx_product(12, agent_base=_AGENT_NAMES, email_query=_EMAIL_QUERIES[:2]):
        idx = ctx["variant_id"] - 1
        ctx.update(
            {
                "template_id": "agent_inbox_followup",
                "model": _MODELS[idx % len(_MODELS)],
                "task_title": f"Follow up on {ctx['email_query']}",
                "priority": "medium",
                "task_due": _TASK_DUES[idx % len(_TASK_DUES)],
            }
        )
        meta = _LEGACY_SCENARIO_CATALOG["agent_inbox_followup"]
        specs.append(
            _make_spec(
                template_id="agent_inbox_followup",
                scenario_slug=meta["slug"],
                scenario_title=meta["title"],
                scenario_goal=meta["goal"],
                realism_tier="legacy",
                high_volatility=False,
                strict_online_risk="medium",
                ctx=ctx,
                op_ids=["oc_agents_add", "oc_agents_list", "email_search", "tasks_add"],
                instruction=(
                    f"Create helper agent '{_agent_name(ctx)}' and confirm it appears in agent list, "
                    f"search inbox for '{ctx['email_query']}', then add follow-up task due {ctx['task_due']}."
                ),
            )
        )

    for ctx in _ctx_product(12, plugin=_PLUGINS, location=_LOCATIONS[:3]):
        idx = ctx["variant_id"] - 1
        ctx.update(
            {
                "template_id": "plugin_weather_schedule",
                "event_title": f"Weather sync {ctx['location']}",
                "event_start": _EVENT_STARTS[idx % len(_EVENT_STARTS)],
            }
        )
        meta = _LEGACY_SCENARIO_CATALOG["plugin_weather_schedule"]
        specs.append(
            _make_spec(
                template_id="plugin_weather_schedule",
                scenario_slug=meta["slug"],
                scenario_title=meta["title"],
                scenario_goal=meta["goal"],
                realism_tier="legacy",
                high_volatility=True,
                strict_online_risk="high",
                ctx=ctx,
                op_ids=["oc_plugins_enable", "oc_plugins_list", "weather_get", "calendar_add"],
                instruction=(
                    f"Enable plugin '{ctx['plugin']}' and verify plugin inventory, check current "
                    f"weather in {ctx['location']}, then schedule '{ctx['event_title']}' at {ctx['event_start']}."
                ),
            )
        )

    for ctx in _ctx_product(12, schedule=_SCHEDULES, timezone=_TIMEZONES):
        idx = ctx["variant_id"] - 1
        ctx.update(
            {
                "template_id": "cron_forecast_today",
                "location": _LOCATIONS[idx % len(_LOCATIONS)],
                "days": _WEATHER_DAYS[idx % len(_WEATHER_DAYS)],
                "cron_message": "Run periodic health summary",
            }
        )
        meta = _LEGACY_SCENARIO_CATALOG["cron_forecast_today"]
        specs.append(
            _make_spec(
                template_id="cron_forecast_today",
                scenario_slug=meta["slug"],
                scenario_title=meta["title"],
                scenario_goal=meta["goal"],
                realism_tier="legacy",
                high_volatility=False,
                strict_online_risk="medium",
                ctx=ctx,
                op_ids=["oc_cron_add", "oc_cron_list", "weather_forecast", "calendar_today"],
                instruction=(
                    f"Create recurring briefing cron on '{ctx['schedule']}' and verify it is listed, "
                    f"pull a {ctx['days']}-day forecast for {ctx['location']}, then check today's "
                    f"calendar context in timezone {ctx['timezone']}."
                ),
            )
        )

    for ctx in _ctx_product(20, model=_MODELS, gateway_port=_GATEWAY_PORTS[:5]):
        idx = ctx["variant_id"] - 1
        ctx.update(
            {
                "template_id": "model_port_plan_block",
                "task_title": _TASK_TITLES[idx % len(_TASK_TITLES)],
                "priority": "high",
                "task_due": _TASK_DUES[idx % len(_TASK_DUES)],
                "event_title": _EVENT_TITLES[idx % len(_EVENT_TITLES)],
                "event_start": _EVENT_STARTS[idx % len(_EVENT_STARTS)],
            }
        )
        meta = _LEGACY_SCENARIO_CATALOG["model_port_plan_block"]
        specs.append(
            _make_spec(
                template_id="model_port_plan_block",
                scenario_slug=meta["slug"],
                scenario_title=meta["title"],
                scenario_goal=meta["goal"],
                realism_tier="legacy",
                high_volatility=False,
                strict_online_risk="medium",
                ctx=ctx,
                op_ids=["oc_models_set", "oc_config_port", "oc_status", "tasks_add", "calendar_add"],
                instruction=(
                    f"Set default model to {ctx['model']} and gateway port {ctx['gateway_port']}, "
                    f"confirm system status, create task '{ctx['task_title']}', then block calendar "
                    f"event '{ctx['event_title']}' at {ctx['event_start']}."
                ),
            )
        )

    for ctx in _ctx_product(20, agent_base=_AGENT_NAMES[:5], plugin=_PLUGINS):
        idx = ctx["variant_id"] - 1
        ctx.update(
            {
                "template_id": "agent_plugin_cron_review",
                "model": _MODELS[idx % len(_MODELS)],
                "schedule": _SCHEDULES[idx % len(_SCHEDULES)],
                "cron_message": "Run agent/plugin review sweep",
                "email_query": _EMAIL_QUERIES[idx % len(_EMAIL_QUERIES)],
                "location": _LOCATIONS[idx % len(_LOCATIONS)],
            }
        )
        meta = _LEGACY_SCENARIO_CATALOG["agent_plugin_cron_review"]
        specs.append(
            _make_spec(
                template_id="agent_plugin_cron_review",
                scenario_slug=meta["slug"],
                scenario_title=meta["title"],
                scenario_goal=meta["goal"],
                realism_tier="legacy",
                high_volatility=True,
                strict_online_risk="high",
                ctx=ctx,
                op_ids=["oc_agents_add", "oc_plugins_enable", "oc_cron_add", "email_search", "weather_get"],
                instruction=(
                    f"Create agent '{_agent_name(ctx)}', enable plugin '{ctx['plugin']}', and add cron "
                    f"schedule '{ctx['schedule']}' to establish the runbook baseline; then search email "
                    f"for '{ctx['email_query']}' and check weather in {ctx['location']}."
                ),
            )
        )

    _validate_specs(specs, expected_count=120, expected_scenarios=10)
    return specs


def _rotate(values: list[str], offset: int) -> list[str]:
    if not values:
        return values
    idx = offset % len(values)
    return values[idx:] + values[:idx]


_LIFE_WORK_LOCATIONS = [
    "New York",
    "London",
    "Tokyo",
    "Paris",
    "Atlanta",
    "Seattle",
    "Berlin",
    "Singapore",
    "Sydney",
    "San Francisco",
]
_LIFE_WORK_TIMEZONE_BY_LOCATION = {
    "New York": "America/New_York",
    "London": "Europe/London",
    "Tokyo": "Asia/Tokyo",
    "Paris": "Europe/Paris",
    "Atlanta": "America/New_York",
    "Seattle": "America/Los_Angeles",
    "Berlin": "Europe/Berlin",
    "Singapore": "Asia/Singapore",
    "Sydney": "Australia/Sydney",
    "San Francisco": "America/Los_Angeles",
}
_LIFE_WORK_QUERIES = [
    "proposal",
    "meeting",
    "budget",
    "report",
    "proposal",
    "meeting",
    "budget",
    "report",
    "proposal",
    "meeting",
]
_LIFE_WORK_RECIPIENTS = [
    "alice@example.com",
    "team@example.com",
    "manager@example.com",
    "ops@example.com",
    "pm@example.com",
    "eng@example.com",
    "support@example.com",
    "product@example.com",
    "lead@example.com",
    "coordinator@example.com",
]
_LIFE_WORK_CHANNELS = [
    "discord",
    "slack",
    "telegram",
    "discord",
    "slack",
    "whatsapp",
    "discord",
    "telegram",
    "slack",
    "discord",
]
_LIFE_WORK_TOPIC_SUFFIXES = [
    "handover",
    "risk review",
    "owner sync",
    "action memo",
    "status digest",
    "decision log",
    "timeline check",
    "follow-up loop",
    "readiness pass",
    "execution block",
]
_LIFE_WORK_EVENT_STARTS = [
    "2026-03-10T09:00",
    "2026-03-10T14:00",
    "2026-03-11T09:30",
    "2026-03-11T16:00",
    "2026-03-12T10:00",
    "2026-03-12T15:00",
    "2026-03-13T09:00",
    "2026-03-13T13:30",
    "2026-03-14T10:30",
    "2026-03-14T16:30",
]
_LIFE_WORK_DUE_DATES = [
    "2026-03-09",
    "2026-03-09",
    "2026-03-10",
    "2026-03-10",
    "2026-03-11",
    "2026-03-11",
    "2026-03-12",
    "2026-03-12",
    "2026-03-13",
    "2026-03-13",
]
_LIFE_WORK_FROM_DATES = [
    "2026-03-08",
    "2026-03-08",
    "2026-03-09",
    "2026-03-09",
    "2026-03-10",
    "2026-03-10",
    "2026-03-11",
    "2026-03-11",
    "2026-03-12",
    "2026-03-12",
]
_LIFE_WORK_TO_DATES = [
    "2026-03-12",
    "2026-03-12",
    "2026-03-13",
    "2026-03-13",
    "2026-03-14",
    "2026-03-14",
    "2026-03-15",
    "2026-03-15",
    "2026-03-16",
    "2026-03-16",
]

_SCENARIO_ORDER = list(_LIFE_WORK_SCENARIOS.keys())
_SCENARIO_LOCATION_POOLS = {
    slug: _rotate(_LIFE_WORK_LOCATIONS, idx) for idx, slug in enumerate(_SCENARIO_ORDER)
}
_SCENARIO_QUERY_POOLS = {
    slug: _rotate(_LIFE_WORK_QUERIES, idx) for idx, slug in enumerate(_SCENARIO_ORDER)
}
_SCENARIO_RECIPIENT_POOLS = {
    slug: _rotate(_LIFE_WORK_RECIPIENTS, idx) for idx, slug in enumerate(_SCENARIO_ORDER)
}
_SCENARIO_CHANNEL_POOLS = {
    slug: _rotate(_LIFE_WORK_CHANNELS, idx) for idx, slug in enumerate(_SCENARIO_ORDER)
}
_SCENARIO_TOPIC_POOLS = {
    slug: [
        f"{_LIFE_WORK_SCENARIOS[slug]['title']} {_LIFE_WORK_TOPIC_SUFFIXES[(idx + i) % len(_LIFE_WORK_TOPIC_SUFFIXES)]}"
        for i in range(10)
    ]
    for idx, slug in enumerate(_SCENARIO_ORDER)
}
_SCENARIO_PLUGIN_POOLS = {
    slug: _rotate(_PLUGINS * 3, idx)[:10] for idx, slug in enumerate(_SCENARIO_ORDER)
}
_SCENARIO_MODEL_POOLS = {
    slug: _rotate(_MODELS * 3, idx)[:10] for idx, slug in enumerate(_SCENARIO_ORDER)
}
_SCENARIO_SCHEDULE_POOLS = {
    slug: _rotate(_SCHEDULES * 3, idx)[:10] for idx, slug in enumerate(_SCENARIO_ORDER)
}
_SCENARIO_WEBHOOK_POOLS = {
    slug: _rotate(_WEBHOOK_URLS * 3, idx)[:10] for idx, slug in enumerate(_SCENARIO_ORDER)
}
_SCENARIO_FILE_POOLS = {
    slug: _rotate(_FILE_PATHS * 3, idx)[:10] for idx, slug in enumerate(_SCENARIO_ORDER)
}
_SCENARIO_AGENT_BASE_POOLS = {
    slug: [f"{slug.split('_')[0]}-{name}" for name in _rotate(_AGENT_NAMES * 3, idx)[:10]]
    for idx, slug in enumerate(_SCENARIO_ORDER)
}


def _target_for_channel(channel: str, idx: int) -> str:
    if channel == "whatsapp":
        return "+15550000001"
    if channel == "telegram":
        return "@ops_bridge"
    if channel == "slack":
        return "#ops-bridge"
    targets = ["#general", "#incident-room", "@oncall"]
    return targets[idx % len(targets)]


def _seed_email_id_for_query(query: str) -> str:
    if query == "proposal":
        return "email_seed_1"
    if query == "meeting":
        return "email_seed_2"
    return "email_seed_3"


def _life_work_context(scenario_slug: str, i: int) -> dict[str, Any]:
    variant_id = i + 1
    location = _SCENARIO_LOCATION_POOLS[scenario_slug][i]
    timezone = _LIFE_WORK_TIMEZONE_BY_LOCATION.get(location, "UTC")
    query = _SCENARIO_QUERY_POOLS[scenario_slug][i]
    topic_label = _SCENARIO_TOPIC_POOLS[scenario_slug][i]
    channel = _SCENARIO_CHANNEL_POOLS[scenario_slug][i]
    recipient = _SCENARIO_RECIPIENT_POOLS[scenario_slug][i]
    task_title = f"{topic_label} task for {location} ({query})"
    event_title = f"{topic_label} sync for {location}"
    subject = f"{topic_label} update for {location}"
    body = (
        f"{topic_label}: completed triage on {query} and captured next actions for {location}."
    )
    return {
        "variant_id": variant_id,
        "topic_label": topic_label,
        "location": location,
        "days": _WEATHER_DAYS[i % len(_WEATHER_DAYS)],
        "timezone": timezone,
        "email_query": query,
        "recipient": recipient,
        "subject": subject,
        "body": body,
        "task_title": task_title,
        "priority": ["high", "medium", "low"][i % 3],
        "task_due": _LIFE_WORK_DUE_DATES[i],
        "event_title": event_title,
        "event_start": _LIFE_WORK_EVENT_STARTS[i],
        "from_date": _LIFE_WORK_FROM_DATES[i],
        "to_date": _LIFE_WORK_TO_DATES[i],
        "gateway_port": _GATEWAY_PORTS[i % len(_GATEWAY_PORTS)],
        "schedule": _SCENARIO_SCHEDULE_POOLS[scenario_slug][i],
        "cron_message": f"Send {topic_label.lower()} digest for {location}",
        "agent_base": _SCENARIO_AGENT_BASE_POOLS[scenario_slug][i],
        "model": _SCENARIO_MODEL_POOLS[scenario_slug][i],
        "plugin": _SCENARIO_PLUGIN_POOLS[scenario_slug][i],
        "channel": channel,
        "target": _target_for_channel(channel, i),
        "message_body": f"{topic_label}: post update for {location} and confirm ownership.",
        "webhook_url": _SCENARIO_WEBHOOK_POOLS[scenario_slug][i],
        "file_path": _SCENARIO_FILE_POOLS[scenario_slug][i],
        "file_content": f"{topic_label} notes for {location} with query {query}.",
        "seed_email_id": _seed_email_id_for_query(query),
        "seed_task_id": f"task_seed_{(i % 3) + 1}",
        "mail_folder": ["archive", "important", "followup"][i % 3],
    }


def _build_life_work_workflow_specs() -> list[WorkflowSpec]:
    specs: list[WorkflowSpec] = []

    # 3-step scenarios (5 * 10 = 50)
    scenario_plans_3 = [
        (
            "morning_briefing_and_notify",
            ["weather_get", "email_send", "oc_cron_add"],
            False,
            "medium",
            lambda c: (
                f"Check current weather for {c['location']}, send a briefing email to {c['recipient']} "
                f"using the same location context, then schedule digest automation on '{c['schedule']}'."
            ),
        ),
        (
            "email_to_calendar_commitment",
            ["email_search", "oc_agents_add", "calendar_add"],
            False,
            "medium",
            lambda c: (
                f"Search inbox for '{c['email_query']}', create helper agent '{_agent_name(c)}' for delegation, "
                f"then schedule commitment block '{c['event_title']}' at {c['event_start']}."
            ),
        ),
        (
            "meeting_conflict_replan",
            ["calendar_list_range", "oc_agents_add", "tasks_add"],
            False,
            "medium",
            lambda c: (
                f"Review calendar between {c['from_date']} and {c['to_date']}, create helper agent "
                f"'{_agent_name(c)}' for replanning, then create task '{c['task_title']}' due {c['task_due']}."
            ),
        ),
        (
            "travel_weather_reschedule",
            ["weather_forecast", "calendar_add", "oc_cron_add"],
            False,
            "medium",
            lambda c: (
                f"Pull a {c['days']}-day forecast for {c['location']}, reschedule '{c['event_title']}' at "
                f"{c['event_start']}, then add a weather-monitor cron on '{c['schedule']}'."
            ),
        ),
        (
            "customer_followup_pipeline",
            ["oc_agents_add", "email_search", "tasks_add"],
            False,
            "medium",
            lambda c: (
                f"Create helper agent '{_agent_name(c)}' for customer follow-up, search inbox for "
                f"'{c['email_query']}', then create task '{c['task_title']}' due {c['task_due']}."
            ),
        ),
    ]

    for template_id, op_ids, high_volatility, risk, instr_builder in scenario_plans_3:
        meta = _LIFE_WORK_SCENARIOS[template_id]
        for i in range(10):
            ctx = _life_work_context(template_id, i)
            ctx["template_id"] = template_id
            specs.append(
                _make_spec(
                    template_id=template_id,
                    scenario_slug=meta["slug"],
                    scenario_title=meta["title"],
                    scenario_goal=meta["goal"],
                    realism_tier="life_work",
                    high_volatility=high_volatility,
                    strict_online_risk=risk,
                    ctx=ctx,
                    op_ids=op_ids,
                    instruction=instr_builder(ctx),
                )
            )

    # 4-step scenarios (7 * 10 = 70)
    scenario_plans_4 = [
        (
            "release_readiness_gate",
            ["oc_models_set", "oc_plugins_list", "tasks_add", "calendar_add"],
            True,
            "high",
            lambda c: (
                f"Set release model to {c['model']}, verify plugin inventory, "
                f"create gate task '{c['task_title']}' due {c['task_due']}, then schedule decision block "
                f"'{c['event_title']}' at {c['event_start']}."
            ),
        ),
        (
            "incident_channel_triage",
            ["oc_channels_login", "oc_message_send", "oc_channels_list_json", "tasks_add"],
            True,
            "high",
            lambda c: (
                f"Log into {c['channel']}, send incident kickoff message to {c['target']}, "
                f"verify current channel configuration, then create triage task '{c['task_title']}' "
                f"due {c['task_due']}."
            ),
        ),
        (
            "agent_delegation_followup",
            ["oc_agents_add", "oc_agents_list", "email_search", "tasks_add"],
            False,
            "medium",
            lambda c: (
                f"Create helper agent '{_agent_name(c)}', verify agents list, search inbox for '{c['email_query']}', "
                f"then add delegated follow-up task '{c['task_title']}' due {c['task_due']}."
            ),
        ),
        (
            "plugin_rollout_validation",
            ["oc_plugins_enable", "oc_plugins_list", "calendar_add", "email_send"],
            True,
            "high",
            lambda c: (
                f"Enable plugin '{c['plugin']}', verify plugin list, schedule rollout checkpoint '{c['event_title']}' "
                f"at {c['event_start']}, then send rollout note to {c['recipient']}."
            ),
        ),
        (
            "security_audit_and_alert",
            ["oc_security_audit", "oc_channels_login", "oc_channels_list_json", "email_send"],
            True,
            "high",
            lambda c: (
                f"Run security audit, log into {c['channel']}, verify channel config, "
                f"then send remediation alert email to {c['recipient']}."
            ),
        ),
        (
            "cron_digest_automation",
            ["oc_cron_add", "oc_cron_list", "weather_forecast", "calendar_today"],
            False,
            "medium",
            lambda c: (
                f"Create digest cron on '{c['schedule']}', verify cron list, pull {c['days']}-day forecast for {c['location']}, "
                f"then check today's calendar in {c['timezone']}."
            ),
        ),
        (
            "device_pairing_confirmation",
            ["oc_devices_pair", "oc_devices_list", "email_send", "tasks_search"],
            True,
            "medium",
            lambda c: (
                f"Start device pairing and verify paired devices, send pairing update to {c['recipient']}, "
                f"then search outstanding tasks for '{c['email_query']}' to confirm follow-up coverage."
            ),
        ),
    ]

    for template_id, op_ids, high_volatility, risk, instr_builder in scenario_plans_4:
        meta = _LIFE_WORK_SCENARIOS[template_id]
        for i in range(10):
            ctx = _life_work_context(template_id, i)
            ctx["template_id"] = template_id
            specs.append(
                _make_spec(
                    template_id=template_id,
                    scenario_slug=meta["slug"],
                    scenario_title=meta["title"],
                    scenario_goal=meta["goal"],
                    realism_tier="life_work",
                    high_volatility=high_volatility,
                    strict_online_risk=risk,
                    ctx=ctx,
                    op_ids=op_ids,
                    instruction=instr_builder(ctx),
                )
            )

    # 5-step scenarios (4 * 10 = 40)
    scenario_plans_5 = [
        (
            "webhook_integration_check",
            ["oc_set_remote_url", "file_create", "oc_cron_add", "oc_cron_list", "email_send"],
            False,
            "medium",
            lambda c: (
                f"Configure webhook URL {c['webhook_url']}, capture integration note in {c['file_path']}, "
                f"create and verify cron schedule '{c['schedule']}', then email integration status to {c['recipient']}."
            ),
        ),
        (
            "multi_channel_status_broadcast",
            ["oc_channels_login", "oc_message_send", "oc_channels_list_json", "weather_get", "email_send"],
            True,
            "high",
            lambda c: (
                f"Log into {c['channel']}, broadcast status to {c['target']}, verify channel listing, "
                f"check weather in {c['location']}, then email the same status summary to {c['recipient']}."
            ),
        ),
        (
            "task_inbox_calendar_sync",
            ["email_search", "tasks_add", "tasks_search", "oc_agents_add", "calendar_add"],
            False,
            "medium",
            lambda c: (
                f"Search inbox for '{c['email_query']}', create task '{c['task_title']}' due {c['task_due']}, "
                f"verify it via task search, "
                f"create helper agent '{_agent_name(c)}' for execution, then block '{c['event_title']}' "
                f"at {c['event_start']}."
            ),
        ),
        (
            "postmortem_capture_workflow",
            ["oc_doctor", "oc_security_audit", "file_create", "tasks_add", "calendar_add"],
            False,
            "low",
            lambda c: (
                f"Run doctor and security audit, capture postmortem note in {c['file_path']}, "
                f"create action task '{c['task_title']}' due {c['task_due']}, then schedule review "
                f"'{c['event_title']}' at {c['event_start']}."
            ),
        ),
    ]

    for template_id, op_ids, high_volatility, risk, instr_builder in scenario_plans_5:
        meta = _LIFE_WORK_SCENARIOS[template_id]
        for i in range(10):
            ctx = _life_work_context(template_id, i)
            ctx["template_id"] = template_id
            specs.append(
                _make_spec(
                    template_id=template_id,
                    scenario_slug=meta["slug"],
                    scenario_title=meta["title"],
                    scenario_goal=meta["goal"],
                    realism_tier="life_work",
                    high_volatility=high_volatility,
                    strict_online_risk=risk,
                    ctx=ctx,
                    op_ids=op_ids,
                    instruction=instr_builder(ctx),
                )
            )

    _validate_specs(
        specs,
        expected_count=160,
        expected_scenarios=16,
        enforce_realism_rules=True,
    )
    return specs


_LEGACY_WORKFLOW_SPECS = _build_legacy_workflow_specs()
_LIFE_WORK_WORKFLOW_SPECS = _build_life_work_workflow_specs()
_MAX_WORKFLOW_COUNT = max(len(_LEGACY_WORKFLOW_SPECS), len(_LIFE_WORK_WORKFLOW_SPECS))


@BaseTaskGenerator.register("complex_composed_workflow")
class ComplexComposedWorkflowGenerator(BaseTaskGenerator):
    """Deterministic complex workflow pack (legacy or life_work profile)."""

    required_domains = (
        "composite",
        "monitoring",
        "tasks",
        "calendar",
        "email",
        "weather",
        "setup_config",
        "plugin_skill",
        "cron_webhook",
        "agent_mgmt",
        "security",
        "channel_mgmt",
        "messaging",
        "device_node",
        "file",
    )
    difficulty = 3
    parameters = {
        "workflow_index": list(range(_MAX_WORKFLOW_COUNT)),
    }

    def _active_specs(self) -> list[WorkflowSpec]:
        profile = get_generation_options().complex_scenario_profile
        if profile == "legacy":
            return _LEGACY_WORKFLOW_SPECS
        return _LIFE_WORK_WORKFLOW_SPECS

    def _spec(self, params: dict[str, Any]) -> WorkflowSpec:
        specs = self._active_specs()
        idx = int(params["workflow_index"])
        return specs[idx]

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        del initial_config
        options = get_generation_options()
        if options.complex_task_pack == "off":
            yield Fail("complex task pack disabled"), TaskData()
            return

        idx = int(params["workflow_index"])
        specs = self._active_specs()
        if idx >= len(specs):
            yield Fail("workflow index outside selected scenario profile"), TaskData()
            return

        spec = specs[idx]
        step_count = len(spec.commands)
        if not (options.complex_min_steps <= step_count <= options.complex_max_steps):
            yield Fail("step count filtered by generation options"), TaskData()
            return

        data = TaskData(
            public={
                "complex_template": spec.template_id,
                "complex_variant": spec.variant_id,
                "complex_scenario": spec.scenario_title,
                "complex_scenario_slug": spec.scenario_slug,
                "step_count": step_count,
                "openclaw_steps": spec.openclaw_step_count,
                "complex_high_volatility": spec.high_volatility,
                "strict_online_risk": spec.strict_online_risk,
                "realism_tier": spec.realism_tier,
                "causal_chain_score": spec.causal_chain_score,
                "entity_consistency_pass": spec.entity_consistency_pass,
                "filler_step_count": spec.filler_step_count,
            },
            private={},
        )
        yield Pass(), data

    def build_task_id(
        self, params: dict[str, Any], data: TaskData, task_counter: int
    ) -> str:
        del data, task_counter
        spec = self._spec(params)
        return _complex_task_id(spec.scenario_slug, spec.variant_id)

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        del data
        return self._spec(params).instruction

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        del data
        return list(self._spec(params).commands)

    def get_task_schema_metadata(
        self,
        params: dict[str, Any],
        data: TaskData,
        instruction: str,
        solution: list[str],
        checks: list[dict[str, Any]],
    ) -> dict[str, Any]:
        del data, instruction, checks
        spec = self._spec(params)
        tags = ["life_work" if spec.realism_tier == "life_work" else "legacy_complex"]
        if spec.high_volatility:
            tags.append("high_volatility")
        if spec.strict_online_risk in {"medium", "high"}:
            tags.append("online_required")
        if len(solution) >= 5 and (spec.high_volatility or spec.causal_chain_score >= 0.9):
            tags.append("challenge")
        online_requirement = "required" if spec.strict_online_risk in {"medium", "high"} else "optional"
        availability_tier = (
            "flaky" if spec.high_volatility else "external-risk"
        )
        return {
            "canonical_instruction": spec.instruction,
            "instruction_variants": [],
            "decision_requirements": ["infer_title"] if spec.high_volatility else [],
            "realism_tags": tags,
            "online_requirement": online_requirement,
            "availability_tier": availability_tier,
        }

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        del data
        return list(self._spec(params).checks)
