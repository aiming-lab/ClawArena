"""Branch-sensitive workflow tasks with observable state probes and result-first checks."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import random
from typing import Any, Iterator

from openclaw_env.core.task import TaskData
from openclaw_env.tasks.generation_options import get_generation_options
from openclaw_env.tasks.registry import (
    BaseTaskGenerator,
    Fail,
    Pass,
    SetupResult,
    _extract_constraints,
    _split_constraints,
)


@dataclass(frozen=True)
class BranchSensitiveSpec:
    task_id: str
    scenario_slug: str
    variant_id: int
    prompt_style: str
    branch_basis: str
    instruction: str
    commands: list[str]
    checks: list[dict[str, Any]]


_DEFAULT_MODEL = "anthropic/claude-sonnet-4-5-20250929"
_PROMPT_STYLES = ["brief", "conditional", "brief", "conditional", "brief", "conditional"]

_CITY_TIMEZONE_BUNDLES = [
    {"city": "New York", "timezone": "America/New_York"},
    {"city": "London", "timezone": "Europe/London"},
    {"city": "Tokyo", "timezone": "Asia/Tokyo"},
    {"city": "Paris", "timezone": "Europe/Paris"},
    {"city": "Sydney", "timezone": "Australia/Sydney"},
    {"city": "Berlin", "timezone": "UTC"},
    {"city": "Austin", "timezone": "America/Chicago"},
    {"city": "Dublin", "timezone": "Europe/Dublin"},
]

_INBOX_BRANCH_BUNDLES = [
    {"query": "proposal", "seed_id": "email_seed_1", "requires_sync": True, "cue": "proposal"},
    {"query": "meeting", "seed_id": "email_seed_2", "requires_sync": True, "cue": "meeting notes"},
    {"query": "budget", "seed_id": "email_seed_3", "requires_sync": False, "cue": "budget report"},
    {"query": "hackathon", "seed_id": "email_seed_4", "requires_sync": False, "cue": "registration follow-up"},
    {"query": "review", "seed_id": "email_seed_5", "requires_sync": True, "cue": "scheduled review"},
]

_CHANNEL_TARGET_BUNDLES = [
    {"channel": "slack", "target": "#incidents"},
    {"channel": "discord", "target": "#launch"},
    {"channel": "telegram", "target": "@ops"},
    {"channel": "whatsapp", "target": "+1234567890"},
    {"channel": "slack", "target": "@manager"},
    {"channel": "discord", "target": "#ops"},
]

_RELEASE_MODELS = [
    _DEFAULT_MODEL,
    "openai/gpt-4.1",
    "openai/gpt-5.2",
    "openai/gpt-4o",
    "anthropic/claude-opus-4-6",
]

_FILE_PATHS = [
    "/ops/release-gate.txt",
    "/workspace/release-gate.txt",
    "/reports/release-branch.txt",
    "/notes/release-gate.txt",
    "/ops/handoff-gate.txt",
    "/reports/release-review.txt",
]

_RECIPIENTS = [
    "alice@example.com",
    "team@example.com",
    "manager@example.com",
    "ops@example.com",
    "leadership@example.com",
    "pm@example.com",
]

_TOPICS = ["outage", "deploy", "rollback", "latency", "escalation", "capacity"]

_SCHEDULE_BUNDLES = [
    {"due": "2026-03-08", "start": "2026-03-10T09:00", "cron": "0 9 * * *"},
    {"due": "2026-03-09", "start": "2026-03-10T13:00", "cron": "15 8 * * 1-5"},
    {"due": "2026-03-10", "start": "2026-03-11T10:30", "cron": "*/30 * * * *"},
    {"due": "2026-03-11", "start": "2026-03-12T14:00", "cron": "0 18 * * 1-5"},
    {"due": "2026-03-12", "start": "2026-03-13T09:30", "cron": "0 7 * * *"},
    {"due": "2026-03-13", "start": "2026-03-14T11:00", "cron": "30 16 * * 1-5"},
]


def _quote(value: str) -> str:
    return value.replace("'", "")


def _prompt_style(index: int) -> str:
    return _PROMPT_STYLES[index % len(_PROMPT_STYLES)]


def _exit_zero_check() -> dict[str, Any]:
    return {
        "type": "output",
        "condition": "exit_code_zero",
        "expected": None,
        "name": "final command succeeds",
    }


def _task_title_contains(value: str) -> dict[str, Any]:
    return {
        "type": "effect",
        "effect_type": "tasks_created",
        "condition": "field_contains",
        "expected": {"field": "title", "value": value},
        "name": f"task title references {value}",
    }


def _calendar_title_contains(value: str) -> dict[str, Any]:
    return {
        "type": "effect",
        "effect_type": "calendar_events_created",
        "condition": "field_contains",
        "expected": {"field": "title", "value": value},
        "name": f"calendar title references {value}",
    }


def _email_to(recipient: str) -> dict[str, Any]:
    return {
        "type": "effect",
        "effect_type": "emails_sent",
        "condition": "field_equals",
        "expected": {"field": "to", "value": recipient},
        "name": f"email sent to {recipient}",
    }


def _message_target(target: str) -> dict[str, Any]:
    return {
        "type": "effect",
        "effect_type": "messages_sent",
        "condition": "field_equals",
        "expected": {"field": "target", "value": target},
        "name": f"message sent to {target}",
    }


def _cron_created() -> dict[str, Any]:
    return {
        "type": "effect",
        "effect_type": "cron_jobs_created",
        "condition": "count_gte",
        "expected": 1,
        "name": "cron job created",
    }


def _task_created() -> dict[str, Any]:
    return {
        "type": "effect",
        "effect_type": "tasks_created",
        "condition": "count_gte",
        "expected": 1,
        "name": "task created",
    }


def _calendar_created() -> dict[str, Any]:
    return {
        "type": "effect",
        "effect_type": "calendar_events_created",
        "condition": "count_gte",
        "expected": 1,
        "name": "calendar event created",
    }


def _file_created() -> dict[str, Any]:
    return {
        "type": "effect",
        "effect_type": "files_created",
        "condition": "count_gte",
        "expected": 1,
        "name": "file created",
    }


def _model_set(model: str) -> dict[str, Any]:
    return {
        "type": "config",
        "config_path": "agent.model",
        "condition": "equals",
        "expected": model,
        "name": f"model set to {model}",
    }


def _calendar_not_created() -> dict[str, Any]:
    return {
        "type": "effect",
        "effect_type": "calendar_events_created",
        "condition": "not_exists",
        "expected": None,
        "name": "no calendar event created",
    }


def _build_inbox_triage_spec(task_id: str, variant_id: int, ctx: dict[str, Any]) -> BranchSensitiveSpec:
    city = ctx["city"]
    timezone = ctx["timezone"]
    query = ctx["query"]
    seed_id = ctx["seed_id"]
    requires_sync = bool(ctx["requires_sync"])
    recipient = ctx["recipient"]
    due = ctx["due"]
    start = ctx["start"]
    prompt_style = ctx["prompt_style"]
    task_title = f"{city} {query} next step"
    event_title = f"{city} {query} live follow-up"
    subject = f"{query.title()} update for {city}"
    body = f"Tracking the next step for {city}."
    if prompt_style == "brief":
        instruction = (
            f"Review the {query}-related email. If it clearly needs a live follow-up, schedule one in {city}; "
            f"either way keep a {city} next-step task on the board and send {recipient} an update."
        )
    else:
        instruction = (
            f"Review the {query}-related email thread, decide whether it needs a live follow-up in {city}, "
            f"keep the next step on the board, and send {recipient} a short update."
        )
    commands = [
        f"email search --query '{_quote(query)}'",
        f"email read --id {seed_id}",
        f"tasks add --title '{_quote(task_title)}' --priority high --due {due}",
    ]
    if requires_sync:
        commands.extend(
            [
                f"calendar today --timezone {timezone}",
                f"calendar add-event --title '{_quote(event_title)}' --start {start}",
            ]
        )
    commands.append(
        f"email send --to {recipient} --subject '{_quote(subject)}' --body '{_quote(body)}'"
    )
    checks = [_exit_zero_check(), _task_created(), _email_to(recipient)]
    if requires_sync:
        checks.append(_calendar_created())
    else:
        checks.append(_calendar_not_created())
    return BranchSensitiveSpec(
        task_id=task_id,
        scenario_slug="inbox_stateful_triage",
        variant_id=variant_id,
        prompt_style=prompt_style,
        branch_basis="email_read",
        instruction=instruction,
        commands=commands,
        checks=checks,
    )


def _build_channel_recovery_spec(task_id: str, variant_id: int, ctx: dict[str, Any]) -> BranchSensitiveSpec:
    channel = ctx["channel"]
    target = ctx["target"]
    topic = ctx["topic"]
    recipient = ctx["recipient"]
    due = ctx["due"]
    prompt_style = ctx["prompt_style"]
    message = f"{topic.title()} delivery update: path recovered and status posted."
    task_title = f"{topic.title()} delivery follow-up for {target}"
    if prompt_style == "brief":
        instruction = (
            f"Get the {topic} update into {channel} for {target}, recover the delivery path if it is not ready, "
            f"keep a {topic} follow-up task on the board, and email {recipient} a recap."
        )
    else:
        instruction = (
            f"Check whether the {channel} delivery path for {target} is ready, recover it if needed, post the {topic} update, "
            f"keep the next step on the board, and email {recipient} a recap."
        )
    return BranchSensitiveSpec(
        task_id=task_id,
        scenario_slug="channel_delivery_recovery",
        variant_id=variant_id,
        prompt_style=prompt_style,
        branch_basis="channels_list",
        instruction=instruction,
        commands=[
            "openclaw channels list --json",
            f"openclaw channels login --channel {channel}",
            f"openclaw message send --channel {channel} --target {target} --message '{_quote(message)}'",
            f"tasks add --title '{_quote(task_title)}' --priority high --due {due}",
            f"email send --to {recipient} --subject '{_quote(topic.title())} delivery recap' --body 'The delivery path is recovered and the update is posted.'",
        ],
        checks=[
            _exit_zero_check(),
            _message_target(target),
            _task_created(),
            _email_to(recipient),
        ],
    )


def _build_release_gate_spec(task_id: str, variant_id: int, ctx: dict[str, Any]) -> BranchSensitiveSpec:
    city = ctx["city"]
    timezone = ctx["timezone"]
    model = ctx["model"]
    path = ctx["path"]
    due = ctx["due"]
    start = ctx["start"]
    prompt_style = ctx["prompt_style"]
    task_title = f"{city} release gate next step"
    event_title = f"{city} release gate sync"
    content = f"{city} release gate handoff notes."
    if prompt_style == "brief":
        instruction = (
            f"Prepare the {city} release gate. Check the current release model, switch to {model} only if it is not already active, "
            f"write the handoff, keep a {city} gate task on the board, and schedule the gate sync."
        )
    else:
        instruction = (
            f"Review the current release gate setup for {city}, switch the default model to {model} only if the current one does not match, "
            f"write the handoff notes, keep a {city} release gate task on the board, and block time for the gate sync."
        )
    commands = [
        "openclaw config get agent.model",
        "openclaw doctor",
    ]
    if model != _DEFAULT_MODEL:
        commands.append(f"openclaw models set {model}")
    commands.extend(
        [
            f"file create --path '{_quote(path)}' --content '{_quote(content)}'",
            f"tasks add --title '{_quote(task_title)}' --priority high --due {due}",
            f"calendar add-event --title '{_quote(event_title)}' --start {start}",
            f"calendar today --timezone {timezone}",
        ]
    )
    return BranchSensitiveSpec(
        task_id=task_id,
        scenario_slug="release_gate_branch",
        variant_id=variant_id,
        prompt_style=prompt_style,
        branch_basis="config_get_agent_model",
        instruction=instruction,
        commands=commands,
        checks=[
            _exit_zero_check(),
            _model_set(model),
            _file_created(),
            _task_created(),
            _calendar_created(),
        ],
    )


def _build_ops_commitment_spec(task_id: str, variant_id: int, ctx: dict[str, Any]) -> BranchSensitiveSpec:
    city = ctx["city"]
    timezone = ctx["timezone"]
    due = ctx["due"]
    start = ctx["start"]
    cron = ctx["cron"]
    risky_weather = bool(ctx["risky_weather"])
    prompt_style = ctx["prompt_style"]
    task_title = f"{city} ops next step"
    event_kind = "backup" if risky_weather else "primary"
    event_title = f"{city} {event_kind} ops review"
    cron_name = f"branch-ops-{variant_id:02d}-{city.lower().replace(' ', '-') }"
    if prompt_style == "brief":
        instruction = (
            f"Set up the recurring ops follow-through for {city}. Check the forecast and today's {timezone} calendar context; "
            f"if the weather looks risky, book the backup review block, otherwise book the primary review block. "
            f"In either case keep a {city} next-step task on the board and make sure the daily check is scheduled."
        )
    else:
        instruction = (
            f"For {city}, inspect the forecast and today's {timezone} calendar context before you set the recurring ops follow-through. "
            f"Book a backup review block when the weather looks risky, otherwise book the primary block, keep the next step on the board, "
            f"and make sure the daily check is scheduled."
        )
    return BranchSensitiveSpec(
        task_id=task_id,
        scenario_slug="ops_commitment_branch",
        variant_id=variant_id,
        prompt_style=prompt_style,
        branch_basis="weather_forecast",
        instruction=instruction,
        commands=[
            f"weather forecast --location '{_quote(city)}' --days 1",
            f"calendar today --timezone {timezone}",
            "openclaw cron list",
            "tasks list --status pending",
            f"tasks add --title '{_quote(task_title)}' --priority medium --due {due}",
            f"openclaw cron add --name {cron_name} --cron '{cron}' --message 'Run {_quote(city)} daily ops check'",
            f"calendar add-event --title '{_quote(event_title)}' --start {start}",
        ],
        checks=[
            _exit_zero_check(),
            _task_created(),
            _cron_created(),
            _calendar_created(),
        ],
    )


def _sample_candidate_contexts(scenario_slug: str, count: int) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    if scenario_slug == "inbox_stateful_triage":
        for city_tz in _CITY_TIMEZONE_BUNDLES:
            for inbox in _INBOX_BRANCH_BUNDLES:
                for recipient in _RECIPIENTS[:5]:
                    for schedule in _SCHEDULE_BUNDLES:
                        candidates.append(
                            {
                                **city_tz,
                                **inbox,
                                "recipient": recipient,
                                **schedule,
                                "prompt_style": _prompt_style(len(candidates)),
                            }
                        )
    elif scenario_slug == "channel_delivery_recovery":
        for bundle in _CHANNEL_TARGET_BUNDLES:
            for topic in _TOPICS:
                for recipient in _RECIPIENTS:
                    for schedule in _SCHEDULE_BUNDLES:
                        candidates.append(
                            {
                                **bundle,
                                "topic": topic,
                                "recipient": recipient,
                                **schedule,
                                "prompt_style": _prompt_style(len(candidates)),
                            }
                        )
    elif scenario_slug == "release_gate_branch":
        for city_tz in _CITY_TIMEZONE_BUNDLES:
            for model in _RELEASE_MODELS:
                for path in _FILE_PATHS:
                    for schedule in _SCHEDULE_BUNDLES:
                        candidates.append(
                            {
                                **city_tz,
                                "model": model,
                                "path": path,
                                **schedule,
                                "prompt_style": _prompt_style(len(candidates)),
                            }
                        )
    elif scenario_slug == "ops_commitment_branch":
        for city_tz in _CITY_TIMEZONE_BUNDLES[:6]:
            risky_weather = city_tz["city"] in {"New York", "London"}
            for schedule in _SCHEDULE_BUNDLES:
                candidates.append(
                    {
                        **city_tz,
                        **schedule,
                        "risky_weather": risky_weather,
                        "prompt_style": _prompt_style(len(candidates)),
                    }
                )
    else:
        raise ValueError(f"unknown branch-sensitive scenario: {scenario_slug}")
    rng = random.Random(f"branch-sensitive:{scenario_slug}:v1")
    rng.shuffle(candidates)
    return candidates[:count]


def _signature(spec: BranchSensitiveSpec) -> tuple[str, tuple[str, ...]]:
    return spec.instruction, tuple(spec.commands)


@lru_cache(maxsize=8)
def _build_specs(variants_per_scenario: int) -> tuple[BranchSensitiveSpec, ...]:
    if variants_per_scenario <= 0:
        return tuple()
    specs: list[BranchSensitiveSpec] = []
    seen: set[tuple[str, tuple[str, ...]]] = set()
    builders = {
        "inbox_stateful_triage": _build_inbox_triage_spec,
        "channel_delivery_recovery": _build_channel_recovery_spec,
        "release_gate_branch": _build_release_gate_spec,
        "ops_commitment_branch": _build_ops_commitment_spec,
    }
    scenario_order = [
        "inbox_stateful_triage",
        "channel_delivery_recovery",
        "release_gate_branch",
        "ops_commitment_branch",
    ]
    for scenario_slug in scenario_order:
        candidates = _sample_candidate_contexts(scenario_slug, variants_per_scenario * 8)
        builder = builders[scenario_slug]
        variant_id = 1
        for ctx in candidates:
            spec = builder(
                task_id=f"branch_sensitive_workflow_{len(specs) + 1}",
                variant_id=variant_id,
                ctx=ctx,
            )
            sig = _signature(spec)
            if sig in seen:
                continue
            specs.append(spec)
            seen.add(sig)
            variant_id += 1
            if variant_id > variants_per_scenario:
                break
        if variant_id <= variants_per_scenario:
            raise RuntimeError(
                f"Unable to build enough unique {scenario_slug} variants for count={variants_per_scenario}."
            )
    return tuple(specs)


@BaseTaskGenerator.register("branch_sensitive_workflow")
class BranchSensitiveWorkflowGenerator(BaseTaskGenerator):
    """Harder branch-sensitive workflows with observable probes and conditional next steps."""

    required_domains = (
        "composite",
        "email",
        "tasks",
        "calendar",
        "messaging",
        "channel_mgmt",
        "monitoring",
        "setup_config",
        "plugin_skill",
        "weather",
        "file",
        "cron_webhook",
    )
    difficulty = 3

    @property
    def parameters(self) -> dict[str, list[Any]]:  # type: ignore[override]
        specs = self._specs()
        return {"workflow_index": list(range(len(specs)))}

    def _specs(self) -> tuple[BranchSensitiveSpec, ...]:
        opts = get_generation_options()
        if not opts.include_branch_sensitive:
            return tuple()
        return _build_specs(opts.branch_sensitive_variants_per_scenario)

    def _spec(self, params: dict[str, Any]) -> BranchSensitiveSpec:
        return self._specs()[int(params["workflow_index"])]

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        del initial_config
        idx = int(params["workflow_index"])
        specs = self._specs()
        if idx >= len(specs):
            yield Fail("workflow index outside branch-sensitive pack"), TaskData()
            return
        spec = specs[idx]
        yield Pass(), TaskData(
            public={
                "branch_sensitive_scenario": spec.scenario_slug,
                "branch_sensitive_variant": spec.variant_id,
                "branch_basis": spec.branch_basis,
                "prompt_style": spec.prompt_style,
                "step_count": len(spec.commands),
            },
            private={},
        )

    def build_task_id(
        self, params: dict[str, Any], data: TaskData, task_counter: int
    ) -> str:
        del data, task_counter
        return self._spec(params).task_id

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        del data
        return self._spec(params).instruction

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        del data
        return list(self._spec(params).commands)

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        del data
        return list(self._spec(params).checks)

    def get_task_schema_metadata(
        self,
        params: dict[str, Any],
        data: TaskData,
        instruction: str,
        solution: list[str],
        checks: list[dict[str, Any]],
    ) -> dict[str, Any]:
        del data, checks
        spec = self._spec(params)
        _, hidden_constraints = _split_constraints(instruction, _extract_constraints(solution))
        if spec.scenario_slug == "release_gate_branch":
            decision_requirements = ["infer_schedule", "infer_title", "infer_model"]
        elif spec.scenario_slug == "channel_delivery_recovery":
            decision_requirements = ["infer_target", "infer_title", "infer_message"]
        elif spec.scenario_slug == "ops_commitment_branch":
            decision_requirements = ["infer_schedule", "infer_title"]
        else:
            decision_requirements = ["infer_schedule", "infer_title", "infer_message"]
        return {
            "canonical_instruction": spec.instruction,
            "instruction_variants": [],
            "hidden_constraints": [
                item
                for item in hidden_constraints
                if str(item.get("type", "")) not in {"datetime", "cron", "timezone"}
            ],
            "decision_requirements": decision_requirements,
            "realism_tags": [
                "challenge",
                "branch_sensitive",
                "state_branching",
                "multi_step",
                "cross_domain",
            ],
            "online_requirement": "optional",
            "availability_tier": "external-risk",
        }
