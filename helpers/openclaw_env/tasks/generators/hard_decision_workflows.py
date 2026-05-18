"""Hard decision workflow tasks with underspecified but bounded execution goals."""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
import random
from typing import Any, Iterator

from openclaw_env.core.task import TaskData
from openclaw_env.skills.impl.weather_skill import _get_weather
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
class HardDecisionSpec:
    task_id: str
    scenario_slug: str
    variant_id: int
    prompt_style: str
    instruction: str
    commands: list[str]
    checks: list[dict[str, Any]]
    canonical_instruction: str = ""
    instruction_variants: tuple[str, ...] = ()
    initial_state: str = "default"
    initial_state_overrides: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class InstructionBundle:
    instruction: str
    canonical_instruction: str
    instruction_variants: tuple[str, ...]


_CITY_TIMEZONE_BUNDLES = [
    {"city": "Berlin", "timezone": "Europe/Berlin"},
    {"city": "Seattle", "timezone": "America/Los_Angeles"},
    {"city": "Singapore", "timezone": "Asia/Singapore"},
    {"city": "Tokyo", "timezone": "Asia/Tokyo"},
    {"city": "Paris", "timezone": "Europe/Paris"},
    {"city": "Austin", "timezone": "America/Chicago"},
    {"city": "London", "timezone": "Europe/London"},
    {"city": "New York", "timezone": "America/New_York"},
    {"city": "Toronto", "timezone": "America/Toronto"},
    {"city": "Sydney", "timezone": "Australia/Sydney"},
    {"city": "Dublin", "timezone": "Europe/Dublin"},
    {"city": "Boston", "timezone": "America/New_York"},
]
_INBOX_EMAILS = [
    {"query": "budget", "seed_id": "email_seed_3", "subject_key": "Budget", "requires_sync": False},
    {"query": "proposal", "seed_id": "email_seed_1", "subject_key": "Proposal", "requires_sync": True},
    {"query": "review", "seed_id": "email_seed_5", "subject_key": "Review", "requires_sync": True},
    {"query": "meeting", "seed_id": "email_seed_2", "subject_key": "Meeting", "requires_sync": True},
    {"query": "hackathon", "seed_id": "email_seed_4", "subject_key": "Hackathon", "requires_sync": False},
]
_RECIPIENTS = [
    "alice@example.com",
    "team@example.com",
    "manager@example.com",
    "ops@example.com",
    "support@example.com",
    "bob@example.com",
    "leadership@example.com",
    "finance@example.com",
    "pm@example.com",
    "coordination@example.com",
]
_MODELS = [
    "anthropic/claude-opus-4-6",
    "anthropic/claude-sonnet-4-5-20250929",
    "openai/gpt-4o",
    "openai/gpt-4.1",
    "openai/gpt-5.2",
    "anthropic/claude-3-7-sonnet-latest",
]
_RELEASE_FILE_PATHS = [
    "/ops/release-handoff.txt",
]

_RISKY_WEATHER_CONDITIONS = {"rainy", "heavy rain", "rain showers", "heavy rain showers", "thunderstorm", "drizzle"}

_FILE_PATHS = [
    "/ops/release-handoff.txt",
    "/ops/release-review.txt",
    "/notes/launch-summary.txt",
    "/workspace/release-brief.txt",
    "/reports/release-sync.txt",
    "/ops/decision-log.txt",
    "/reports/cutover-notes.txt",
    "/ops/rollback-handoff.txt",
    "/notes/release-summary.txt",
    "/workspace/launch-brief.txt",
]
_CHANNEL_TARGET_BUNDLES = [
    {"channel": "discord", "target": "#general"},
    {"channel": "slack", "target": "@team"},
    {"channel": "telegram", "target": "@alice"},
    {"channel": "whatsapp", "target": "+1234567890"},
    {"channel": "discord", "target": "#ops"},
    {"channel": "slack", "target": "@manager"},
    {"channel": "telegram", "target": "@ops"},
    {"channel": "slack", "target": "#incidents"},
    {"channel": "discord", "target": "#launch"},
    {"channel": "whatsapp", "target": "+1987654321"},
]
_TOPICS = [
    "incident",
    "rollback",
    "latency",
    "deploy",
    "escalation",
    "outage",
    "handoff",
    "degradation",
    "capacity",
    "alert",
]
_SCHEDULE_BUNDLES = [
    {"due": "2026-03-08", "start": "2026-03-10T09:00", "cron": "0 9 * * *", "days": 3},
    {"due": "2026-03-09", "start": "2026-03-10T13:00", "cron": "15 8 * * 1-5", "days": 5},
    {"due": "2026-03-10", "start": "2026-03-11T10:30", "cron": "*/30 * * * *", "days": 3},
    {"due": "2026-03-11", "start": "2026-03-12T14:00", "cron": "0 18 * * 1-5", "days": 5},
    {"due": "2026-03-12", "start": "2026-03-13T09:30", "cron": "0 7 * * *", "days": 7},
    {"due": "2026-03-13", "start": "2026-03-14T11:00", "cron": "30 16 * * 1-5", "days": 3},
    {"due": "2026-03-14", "start": "2026-03-17T09:00", "cron": "0 10 * * 1-5", "days": 4},
    {"due": "2026-03-15", "start": "2026-03-18T11:30", "cron": "45 7 * * *", "days": 6},
    {"due": "2026-03-16", "start": "2026-03-19T15:00", "cron": "0 12 * * 1-5", "days": 2},
    {"due": "2026-03-17", "start": "2026-03-20T08:30", "cron": "30 9 * * 1-5", "days": 5},
]
_PROMPT_STYLES = [
    "brief",
    "underspecified",
    "brief",
    "underspecified",
    "brief",
    "underspecified",
    "brief",
    "underspecified",
    "brief",
    "underspecified",
]


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


def _cron_not_created() -> dict[str, Any]:
    return {
        "type": "effect",
        "effect_type": "cron_jobs_created",
        "condition": "not_exists",
        "expected": None,
        "name": "no duplicate cron job created",
    }


def _task_created() -> dict[str, Any]:
    return {
        "type": "effect",
        "effect_type": "tasks_created",
        "condition": "count_gte",
        "expected": 1,
        "name": "task created",
    }


def _task_not_created() -> dict[str, Any]:
    return {
        "type": "effect",
        "effect_type": "tasks_created",
        "condition": "not_exists",
        "expected": None,
        "name": "no duplicate task created",
    }


def _calendar_created() -> dict[str, Any]:
    return {
        "type": "effect",
        "effect_type": "calendar_events_created",
        "condition": "count_gte",
        "expected": 1,
        "name": "calendar event created",
    }


def _calendar_not_created() -> dict[str, Any]:
    return {
        "type": "effect",
        "effect_type": "calendar_events_created",
        "condition": "not_exists",
        "expected": None,
        "name": "no duplicate calendar event created",
    }


def _calendar_updated() -> dict[str, Any]:
    return {
        "type": "effect",
        "effect_type": "calendar_events_updated",
        "condition": "count_gte",
        "expected": 1,
        "name": "calendar event updated",
    }



def _task_completed() -> dict[str, Any]:
    return {
        "type": "effect",
        "effect_type": "tasks_completed",
        "condition": "count_gte",
        "expected": 1,
        "name": "outdated task completed",
    }


def _file_created() -> dict[str, Any]:
    return {
        "type": "effect",
        "effect_type": "files_created",
        "condition": "count_gte",
        "expected": 1,
        "name": "file created",
    }


def _file_path_contains(value: str, *, name: str) -> dict[str, Any]:
    return {
        "type": "effect",
        "effect_type": "files_created",
        "condition": "field_contains",
        "expected": {"field": "path", "value": value},
        "name": name,
    }


def _handoff_file_checks() -> list[dict[str, Any]]:
    return [
        _file_created(),
        _file_path_contains('handoff', name='handoff file path references handoff'),
    ]


def _release_handoff_file_checks() -> list[dict[str, Any]]:
    return _handoff_file_checks()


def _model_set(model: str) -> dict[str, Any]:
    return {
        "type": "config",
        "config_path": "agent.model",
        "condition": "equals",
        "expected": model,
        "name": f"model set to {model}",
    }

def _state_count_gte(field: str, expected: int, name: str) -> dict[str, Any]:
    return {
        "type": "state",
        "field": field,
        "condition": "count_gte",
        "expected": expected,
        "name": name,
    }


def _scenario_prompt_style(index: int) -> str:
    return _PROMPT_STYLES[index % len(_PROMPT_STYLES)]


def _quote(value: str) -> str:
    return value.replace("'", "")


def _slugify(value: str) -> str:
    return value.lower().replace(" ", "-")


def _dedupe_texts(texts: list[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    ordered: list[str] = []
    for text in texts:
        normalized = " ".join(text.split())
        if normalized and normalized not in seen:
            seen.add(normalized)
            ordered.append(normalized)
    return tuple(ordered)


def _pick_variant(candidates: tuple[str, ...], variant_id: int, prompt_style: str, scenario_slug: str) -> str:
    if not candidates:
        raise ValueError(f"no instruction candidates for {scenario_slug}:{prompt_style}")
    offset = sum(ord(ch) for ch in f"{scenario_slug}:{prompt_style}")
    return candidates[(variant_id + offset) % len(candidates)]


def _instruction_bundle(
    *,
    scenario_slug: str,
    prompt_style: str,
    variant_id: int,
    brief: list[str],
    underspecified: list[str],
) -> InstructionBundle:
    brief_candidates = _dedupe_texts(brief)
    underspecified_candidates = _dedupe_texts(underspecified)
    selected_pool = brief_candidates if prompt_style == "brief" else underspecified_candidates
    instruction = _pick_variant(selected_pool, variant_id, prompt_style, scenario_slug)
    canonical_instruction = underspecified_candidates[0] if underspecified_candidates else selected_pool[0]
    instruction_variants = tuple(
        text
        for text in _dedupe_texts(list(brief_candidates) + list(underspecified_candidates))
        if text != instruction
    )
    return InstructionBundle(
        instruction=instruction,
        canonical_instruction=canonical_instruction,
        instruction_variants=instruction_variants,
    )


def _render_instruction_bundle(
    scenario_slug: str,
    prompt_style: str,
    variant_id: int,
    slots: dict[str, Any],
) -> InstructionBundle:
    city = slots.get("city", "")
    timezone = slots.get("timezone", "")
    query = slots.get("query", "")
    recipient = slots.get("recipient", "")
    channel = slots.get("channel", "")
    target = slots.get("target", "")
    topic = slots.get("topic", "")
    model = slots.get("model", "")
    existing_piece = slots.get("existing_piece", "")
    state_mode = slots.get("state_mode", "")
    repair_kind = slots.get("repair_kind", "")
    gap_kind = slots.get("gap_kind", "")
    replace_kind = slots.get("replace_kind", "")

    if scenario_slug == "inbox_followthrough":
        missing_hint = {
            "task_existing": "the next step is already on the board",
            "task_missing": "the board still lacks the next step",
        }.get(state_mode, "one follow-up piece is still missing")
        sync_hint = {
            "sync_required": "if it clearly needs a live follow-up, add the sync",
            "async_only": "if it only needs async follow-up, leave the calendar alone",
        }.get(slots.get("sync_mode", ""), "only add what the thread and current state still require")
        return _instruction_bundle(
            scenario_slug=scenario_slug,
            prompt_style=prompt_style,
            variant_id=variant_id,
            brief=[
                f"Handle the {query} email thread in the inbox first. Then check the {city} board and calendar; right now {missing_hint}, and {sync_hint}, so add only what is missing, note it in a handoff file, and send {recipient} a quick note.",
                f"Close out the {query} email thread in the inbox first. Then review the {city} board and calendar; right now {missing_hint}, and {sync_hint}, so fill only what is missing, note it in a handoff file, and send {recipient} a quick update.",
                f"Sort out the {query} email thread in the inbox first. Then check the {city} board and calendar; right now {missing_hint}, and {sync_hint}, so fill only what is missing, note it in a handoff file, and send {recipient} a quick update.",
                f"Wrap the {query} email thread in the inbox first. Then review the {city} board and calendar; right now {missing_hint}, and {sync_hint}, so add only what is missing, note it in a handoff file, and send {recipient} a short update.",
            ],
            underspecified=[
                f"The {query} email thread in the inbox needs attention today. Then check the {city} board and calendar; right now {missing_hint}, and {sync_hint}, so fill only what is missing, note it in a handoff file, and send {recipient} a quick update.",
                f"The {query} email thread in the inbox still needs to be closed out. Then review the {city} board and calendar; right now {missing_hint}, and {sync_hint}, so add only what is missing, note it in a handoff file, and send {recipient} a quick note.",
                f"Please handle the {query} email thread in the inbox first. Then check the {city} board and calendar; right now {missing_hint}, and {sync_hint}, so fill only what is missing, note it in a handoff file, and send {recipient} a quick update.",
                f"I still need the {query} email thread in the inbox handled today. Then review the {city} board and calendar; right now {missing_hint}, and {sync_hint}, so add only what is missing, note it in a handoff file, and send {recipient} a short update.",
            ],
        )
    if scenario_slug == "release_recovery_runbook":
        return _instruction_bundle(
            scenario_slug=scenario_slug,
            prompt_style=prompt_style,
            variant_id=variant_id,
            brief=[
                f"Can you get the {city} release review back into shape? Check what's already on the board and calendar, switch over to {model}, refresh the handoff file, and add only the missing review slot or decision-log task.",
                f"Please tighten up the {city} release review. Check what's already on the board and calendar, use {model}, refresh the handoff file, and add only the missing review slot or decision-log task.",
                f"Can you get the {city} release review settled? Look over what's already on the board and calendar, move to {model}, refresh the handoff file, and fill only the missing review slot or decision-log task.",
                f"Please get the {city} release review into good shape. Check what's already on the board and calendar, use {model}, refresh the handoff file, and add only the missing review slot or decision-log task.",
            ],
            underspecified=[
                f"I need the {city} release review cleaned up. Please check what's already on the board and calendar, move to {model}, refresh the handoff file, and add only the missing review slot or decision-log task.",
                f"Some of the {city} release review is already in place. Please check the board and calendar, use {model}, refresh the handoff file, and fill only the missing review slot or decision-log task.",
                f"The {city} release review is partly there already. Check what's on the board and calendar, switch over to {model}, refresh the handoff file, and add only the missing review slot or decision-log task.",
                f"I need the {city} release review wrapped up properly. Please check what's already on the board and calendar, move to {model}, refresh the handoff file, and add only the missing review slot or decision-log task.",
            ],
        )
    if scenario_slug == "channel_incident_recovery":
        return _instruction_bundle(
            scenario_slug=scenario_slug,
            prompt_style=prompt_style,
            variant_id=variant_id,
            brief=[
                f"Can you post the {topic} update to {target} on {channel}? Check what's already being tracked on the board, fill only the missing piece, and send {recipient} a recap.",
                f"Please get the {topic} update out to {target} on {channel}, look over the {topic} next step on the board, fill only the missing piece, and send {recipient} a recap.",
                f"Can you handle the {topic} update for {target} on {channel}? Review what's already being tracked on the board, add only the missing piece, and send {recipient} a quick recap.",
                f"Please push the {topic} update to {target} on {channel}, check whether the {topic} next step is already on the board, fill only the missing piece, and send {recipient} a short recap.",
            ],
            underspecified=[
                f"I need the {topic} update out to {target} on {channel}. Please look over what's already being tracked on the board, confirm whether the {topic} next step is already there, fill only the missing piece, and send {recipient} a quick recap once it's handled.",
                f"Please get the {topic} update to {target} on {channel}, check the {topic} next step on the board first to see whether it is already there, add only the missing piece, and send {recipient} a recap when it's handled.",
                f"The {topic} update still needs to reach {target} on {channel}. Please review what's already being tracked on the board, confirm whether the {topic} next step is already there, fill only the missing piece, and send {recipient} a quick recap afterward.",
                f"Please handle the {topic} update for {target} on {channel}, look over the {topic} next step on the board, add only the missing piece, and send {recipient} a short recap when it's done.",
            ],
        )
    if scenario_slug == "daily_ops_commitment_loop":
        return _instruction_bundle(
            scenario_slug=scenario_slug,
            prompt_style=prompt_style,
            variant_id=variant_id,
            brief=[
                f"Can you check today's {timezone} schedule for {city}, look at the next step on the board and the recurring daily check, and only fill the missing piece?",
                f"Please check today's {timezone} calendar for {city}, look over the next step on the board and the recurring daily check schedule, and only add what's still missing.",
                f"Can you use today's {timezone} schedule for {city}, review the next step on the board and the recurring daily check, and fill only the missing piece?",
                f"Please check today's {timezone} schedule for {city}, review the next step on the board and the recurring daily check, and only fill what's missing.",
            ],
            underspecified=[
                f"Part of the {city} daily ops setup may already be there. Please check today's {timezone} calendar context, the next step on the board, and the recurring daily check schedule, then finish only the missing piece.",
                f"The {city} daily ops setup should only need one missing piece filled. Please use today's {timezone} calendar context, check the next step on the board and the recurring daily check schedule, and add only what's missing.",
                f"I need the {city} daily ops setup cleaned up without rebuilding it. Check today's {timezone} calendar context, the next step on the board, and the recurring daily check schedule, then fill only the missing piece.",
                f"Please sort out the remaining {city} daily ops gap. Use today's {timezone} calendar context, check the next step on the board and the recurring daily check schedule, and only add what's still missing.",
            ],
        )
    if scenario_slug == "release_gate_followthrough":
        return _instruction_bundle(
            scenario_slug=scenario_slug,
            prompt_style=prompt_style,
            variant_id=variant_id,
            brief=[
                f"Can you get the {city} release gate ready? Check the current model, what's already on the board, and what's already on the calendar before you update the handoff file, the next step on the board, and the sync.",
                f"Please get the {city} release gate into shape. Confirm the current model, check the board and calendar first, then update the handoff file, the {city} next step on the board, and the sync on the calendar.",
                f"Can you tighten up the {city} release gate? Check the current model and the existing board and calendar state first, then refresh the handoff file, the next step on the board, and the sync.",
                f"Please get the {city} release gate sorted out. Confirm the current model, review the board and calendar first, then update the handoff file, the next step on the board, and the sync on the calendar.",
            ],
            underspecified=[
                f"I need the {city} release gate tightened up. Please confirm the current model, check the board and calendar first, then refresh the handoff file, the next step on the board, and the sync on the calendar.",
                f"The {city} release gate still needs to be cleaned up. Please review the current model plus the board and calendar state before you refresh the handoff file, the next step on the board, and the sync.",
                f"Please get the {city} release gate into good shape. Check the current model and the current board and calendar state first, then refresh the handoff file, the next step on the board, and the sync on the calendar.",
                f"I need the {city} release gate wrapped up properly. Confirm the current model, review the board and calendar first, then refresh the handoff file, the next step on the board, and the sync on the calendar.",
            ],
        )
    if scenario_slug == "delivery_update_followthrough":
        state_hint = {
            "task_existing": "the next step may already be on the board, so leave it alone if it is there",
            "task_missing": "the board still needs the next step before you close it out",
        }.get(state_mode, "fill only the missing piece")
        followup_hint = {
            "live_followup": "if the target is shared, leave a short live block on the calendar",
            "async_only": "if the target is direct, close it out without a calendar block",
        }.get(slots.get("followup_mode", ""), "leave only the follow-up that still makes sense")
        return _instruction_bundle(
            scenario_slug=scenario_slug,
            prompt_style=prompt_style,
            variant_id=variant_id,
            brief=[
                f"Can you get the {topic} update out to {target} on {channel}? Fix the delivery path if needed, check what's already on the board, {state_hint}, {followup_hint}, and send {recipient} a quick recap.",
                f"Please get the {topic} update to {target} on {channel}. Fix the delivery path if needed, review what's already on the board, {state_hint}, {followup_hint}, and send {recipient} a quick recap.",
                f"Can you handle the {topic} update for {target} on {channel}? Repair the path if needed, check what's already on the board, {state_hint}, {followup_hint}, and send {recipient} a short recap.",
                f"Please push the {topic} update to {target} on {channel}. Fix the path if needed, review what's already on the board, {state_hint}, {followup_hint}, and send {recipient} a recap.",
            ],
            underspecified=[
                f"I need the {topic} update to reach {target} on {channel}. Fix the delivery path if needed, check what's already on the board, {state_hint}, {followup_hint}, and email {recipient} a recap.",
                f"The {topic} update still needs to get to {target} on {channel}. Please fix the path if needed, review what's already on the board, {state_hint}, {followup_hint}, and send {recipient} a quick recap once it's through.",
                f"Please get the {topic} update over to {target} on {channel}. Clean up the path if needed, check what's already on the board, {state_hint}, {followup_hint}, and send {recipient} a recap afterward.",
                f"I need the {topic} update delivered to {target} on {channel}. Please repair the path if needed, review what's already on the board, {state_hint}, {followup_hint}, and send {recipient} a short recap when it's done.",
            ],
        )
    if scenario_slug == "ops_review_followthrough":
        return _instruction_bundle(
            scenario_slug=scenario_slug,
            prompt_style=prompt_style,
            variant_id=variant_id,
            brief=[
                f"For {city}, can you check the forecast, today's {timezone} schedule, the next step on the board, and the recurring daily check, then fill only the missing piece before you put the review on the calendar?",
                f"Can you look at the forecast and today's {timezone} calendar for {city}, review the next step on the board and the recurring daily check, and only add what's missing before you put the review on the calendar?",
                f"For {city}, can you use the forecast and today's {timezone} calendar to check the next step on the board and the recurring daily check, then fill only the missing piece and put the review on the calendar?",
                f"Please use the forecast and today's {timezone} schedule for {city} to review the next step on the board and the recurring daily check, fill only what's missing, and put the review on the calendar.",
            ],
            underspecified=[
                f"Please use the forecast and today's {timezone} calendar context to sort out the {city} ops review. Check the next step on the board and the recurring daily check too, then fill only the missing piece before you put the review on the calendar.",
                f"The {city} ops review still needs to be set the right way. Please use the forecast and today's {timezone} calendar context, check the next step on the board and the recurring daily check, then add only what's missing before you put the review on the calendar.",
                f"I need the {city} ops review lined up properly. Use the forecast and today's {timezone} calendar context, review the next step on the board and the recurring daily check, then fill only the missing piece before you put the review on the calendar.",
                f"Please check the forecast and today's {timezone} calendar for {city}, review the next step on the board and the recurring daily check, then only add what's missing before you put the review on the calendar.",
            ],
        )
    if scenario_slug == "existing_state_followthrough":
        piece_hint = {
            "cron": "the recurring daily check is the missing piece",
            "task": "the next step on the board is the missing piece",
            "calendar": "the review slot on the calendar is the missing piece",
        }[existing_piece]
        return _instruction_bundle(
            scenario_slug=scenario_slug,
            prompt_style=prompt_style,
            variant_id=variant_id,
            brief=[
                f"Some of the {city} daily ops setup is already there. Take stock of the next step on the board, the review slot on the calendar, and the recurring daily check, then finish only the missing piece and send {recipient} a short recap.",
                f"The {city} daily ops setup is only partway done. Look over the next step on the board, the review slot on the calendar, and the recurring daily check, then finish just the missing piece and send {recipient} a short recap.",
                f"Part of the {city} daily ops setup is already in motion. Review the next step on the board, the review slot on the calendar, and the recurring daily check, then finish only what's missing and send {recipient} a short recap.",
                f"For {city}, some of the daily ops setup is already handled. Check the next step on the board, the review slot on the calendar, and the recurring daily check, leave the rest alone, finish the missing piece, and send {recipient} a short recap.",
            ],
            underspecified=[
                f"For {city}, part of the recurring ops setup is already there, and {piece_hint}. Check the next step on the board, the review slot on the calendar, and the recurring daily check, then finish only the missing piece and send {recipient} a short recap.",
                f"Some of the {city} recurring ops setup is already in place, and {piece_hint}. Please check the next step on the board, the review slot on the calendar, and the recurring daily check, then finish only the missing piece and send {recipient} a short recap once it's clear what's left.",
                f"The {city} recurring ops setup is partway done, and {piece_hint}. Look over the next step on the board, the review slot on the calendar, and the recurring daily check, then finish only the missing piece and send {recipient} a short recap.",
                f"I already have part of the {city} recurring ops setup in motion, and {piece_hint}. Please review the next step on the board, the review slot on the calendar, and the recurring daily check, then finish only the missing piece and send {recipient} a short recap.",
            ],
        )
    if scenario_slug == "duplicate_avoidance_followthrough":
        followup_hint = (
            "add a backup review block on the calendar if the forecast looks risky; otherwise add a primary review block on the calendar"
        )
        return _instruction_bundle(
            scenario_slug=scenario_slug,
            prompt_style=prompt_style,
            variant_id=variant_id,
            brief=[
                f"Some of the {city} ops setup is already in place. Check the board, forecast, and calendar, then {followup_hint}, and avoid recreating the existing setup.",
                f"The {city} ops setup already has the basics in place. Check the current setup, forecast, and calendar, then {followup_hint}, and don't recreate anything that's already right.",
                f"For {city}, part of the ops setup is already covered. Review the current setup, forecast, and calendar, then {followup_hint}, and leave the existing pieces alone.",
                f"The {city} ops setup is mostly in place. Check the current setup, forecast, and calendar, then {followup_hint}, and avoid rebuilding anything that's already set.",
            ],
            underspecified=[
                f"Some of the {city} ops setup is already in place. Check the board, forecast, and calendar, then {followup_hint}, and avoid recreating the existing setup.",
                f"The {city} ops setup is partly there already. Check the current setup, forecast, and calendar, then {followup_hint}, and don't rebuild anything that's already in place.",
                f"I already have part of the {city} ops setup in motion. Review the current setup, forecast, and calendar, then {followup_hint}, and leave the existing pieces alone.",
                f"The {city} ops setup is mostly right already. Check the current setup, forecast, and calendar, then {followup_hint}, and avoid recreating anything that's already set.",
            ],
        )
    if scenario_slug == "multi_source_decision_followthrough":
        return _instruction_bundle(
            scenario_slug=scenario_slug,
            prompt_style=prompt_style,
            variant_id=variant_id,
            brief=[
                f"For {city}, use the review email note, the forecast, and the {timezone} calendar to decide whether this stays live or goes async. Leave the next step on the board, keep the daily check scheduled, put the review on the calendar if live, and send {recipient} an update only if async.",
                f"Can you use the review email note, the forecast, and the {timezone} calendar for {city} to decide whether this stays live or moves async? Leave the next step on the board, keep the daily check scheduled, put the review on the calendar if live, and send {recipient} an update only if async.",
                f"For {city}, check the review email note, the forecast, and the {timezone} calendar, decide whether this stays live or shifts async, leave the next step on the board, keep the daily check scheduled, put the review on the calendar if live, and send {recipient} an update only if async.",
                f"Please use the review email note, the forecast, and the {timezone} calendar for {city} to decide whether this stays live or goes async. Leave the next step on the board, keep the daily check scheduled, put the review on the calendar if live, and only send {recipient} an update if async.",
            ],
            underspecified=[
                f"Please use the review email note, the forecast, and the {timezone} calendar for {city} before deciding whether this stays live or moves async. Leave the next step on the board, keep the daily check scheduled, put the review on the calendar if live, and email {recipient} only if async.",
                f"I need a call on whether the {city} ops review stays live or moves async. Use the review email note, the forecast, and the {timezone} calendar, leave the next step on the board, keep the daily check scheduled, put the review on the calendar if live, and email {recipient} only if async.",
                f"For {city}, use the review email note, the forecast, and the {timezone} calendar before deciding whether this stays live or switches async. Leave the next step on the board, keep the daily check scheduled, put the review on the calendar if live, and email {recipient} only if async.",
                f"Please use the review email note, the forecast, and the {timezone} calendar for {city} to decide whether this stays live or moves async. Leave the next step on the board, keep the daily check scheduled, put the review on the calendar if live, and email {recipient} only if async.",
            ],
        )
    if scenario_slug == "state_repair_followthrough":
        stale_hint = {
            "model": "review the current model, the next-step task on the board, and the sync on the calendar",
            "calendar": "review the next-step task on the board and the sync on the calendar",
            "task": "review the next-step task on the board and the sync on the calendar",
        }[repair_kind]
        repair_target = {
            "model": "model setting",
            "calendar": "sync",
            "task": "next step",
        }[repair_kind]
        return _instruction_bundle(
            scenario_slug=scenario_slug,
            prompt_style=prompt_style,
            variant_id=variant_id,
            brief=[
                f"Something's off in the {city} release setup. {stale_hint.capitalize()}, fix the stale {repair_target}, update the handoff file, and leave the next step and sync correctly set.",
                f"The {city} release setup has something stale in it. {stale_hint.capitalize()}, repair the stale {repair_target}, refresh the handoff file, and leave the next step and sync correctly set.",
                f"Something in the {city} release setup is off. {stale_hint.capitalize()}, fix the stale {repair_target}, update the handoff file, and leave the next step and sync correctly set.",
                f"The {city} release setup needs a cleanup pass. {stale_hint.capitalize()}, repair the stale {repair_target}, refresh the handoff file, and leave the next step and sync correctly set.",
            ],
            underspecified=[
                f"I need the {city} release setup cleaned up. {stale_hint.capitalize()}, fix the stale {repair_target}, refresh the handoff file, and leave the sync and next step correctly set.",
                f"Something in the {city} release setup is stale. {stale_hint.capitalize()}, repair the stale {repair_target}, refresh the handoff file, and leave the sync and next step correctly set.",
                f"The {city} release setup still has one stale detail in it. {stale_hint.capitalize()}, fix the stale {repair_target}, refresh the handoff file, and leave the sync and next step correctly set.",
                f"I need the {city} release setup back in shape. {stale_hint.capitalize()}, repair the stale {repair_target}, refresh the handoff file, and leave the sync and next step correctly set.",
            ],
        )
    if scenario_slug == "completion_gap_followthrough":
        gap_hint = {
            "task_and_calendar": "the next step and the review sync are still missing",
            "calendar_only": "the review sync is the missing piece",
            "task_only": "the next step is the missing piece",
        }[gap_kind]
        gap_action = {
            "task_and_calendar": "finish the remaining next step on the board and sync on the calendar",
            "calendar_only": "leave the next step on the board in place and add only the missing sync on the calendar",
            "task_only": "leave the sync on the calendar in place and add only the missing next step on the board",
        }[gap_kind]
        return _instruction_bundle(
            scenario_slug=scenario_slug,
            prompt_style=prompt_style,
            variant_id=variant_id,
            brief=[
                f"Part of the {city} release work is already in place, but {gap_hint}. Check what's there, read the release notes, refresh the handoff file, and {gap_action}.",
                f"Some of the {city} release work is already in motion, but {gap_hint}. Please check what's there, read the release notes, refresh the handoff file, and {gap_action}.",
                f"The {city} release work is only partway done, and {gap_hint}. Review what's there, read the release notes, refresh the handoff file, and {gap_action}.",
                f"Part of the {city} release work is already handled, but {gap_hint}. Check what's there, read the release notes, refresh the handoff file, and {gap_action}.",
            ],
            underspecified=[
                f"Some of the {city} release work is already in place, and {gap_hint}. Review what's there, read the release notes, refresh the handoff file, {gap_action}, and leave the rest alone.",
                f"The {city} release work is partway done, and {gap_hint}. Please check what's there, read the release notes, refresh the handoff file, {gap_action}, and leave the existing pieces alone.",
                f"I already have part of the {city} release work in motion, and {gap_hint}. Review what's there, read the release notes, refresh the handoff file, {gap_action}, and leave the rest alone.",
                f"Part of the {city} release work is already set, and {gap_hint}. Please check what's there, read the release notes, refresh the handoff file, {gap_action}, and leave the existing pieces alone.",
            ],
        )
    if scenario_slug == "branch_resolution_followthrough":
        return _instruction_bundle(
            scenario_slug=scenario_slug,
            prompt_style=prompt_style,
            variant_id=variant_id,
            brief=[
                f"The {city} ops setup already has a next step and a recurring daily check scheduled. Check the forecast and today's {timezone} calendar, work out whether this stays live or moves async, and send {recipient} an update only if it moves async.",
                f"For {city}, the next step and recurring daily check are already there. Use the forecast and today's {timezone} calendar to work out whether this stays live or goes async, and only send {recipient} an update if it goes async.",
                f"The {city} ops setup already has the basics in place. Check the forecast and today's {timezone} calendar, work out whether this stays live or shifts async, and send {recipient} an update only if it shifts async.",
                f"For {city}, the next step and recurring daily check are already covered. Use the forecast and today's {timezone} calendar to work out whether this stays live or moves async, and only send {recipient} an update if it moves async.",
            ],
            underspecified=[
                f"Some of the {city} ops setup is already in place. Review the forecast, today's {timezone} calendar, the task already on the board, and the recurring daily check schedule before working out whether this should stay live or move async, and send {recipient} the update if you move it async.",
                f"The {city} ops setup already has part of the work in place. Please review the forecast, today's {timezone} calendar, the task already on the board, and the recurring daily check schedule before working out whether this stays live or moves async, and send {recipient} the update if it moves async.",
                f"I already have the basics of the {city} ops setup in motion. Please use the forecast, today's {timezone} calendar, the task already on the board, and the recurring daily check schedule before working out whether this stays live or moves async, and send {recipient} the update if it moves async.",
                f"Some of the {city} ops setup is already covered. Please review the forecast, today's {timezone} calendar, the task already on the board, and the recurring daily check schedule before working out whether this stays live or shifts async, and send {recipient} the update if it shifts async.",
            ],
        )
    if scenario_slug == "already_done_skip_followthrough":
        return _instruction_bundle(
            scenario_slug=scenario_slug,
            prompt_style=prompt_style,
            variant_id=variant_id,
            brief=[
                f"The {city} release setup should already be ready. Just verify the current model, the next-step task on the board, and the sync on the calendar before you send {recipient} a short recap without rebuilding anything.",
                f"I think the {city} release setup is already ready to go. Please verify the current model, the next-step task on the board, and the sync on the calendar before you send {recipient} a short recap and leave it alone.",
                f"The {city} release setup should already be set. Just verify the current model, the next-step task on the board, and the sync on the calendar before you send {recipient} a quick recap and leave it alone.",
                f"I think the {city} release setup is already in good shape. Please verify the current model, the next-step task on the board, and the sync on the calendar before you send {recipient} a short recap without rebuilding anything.",
            ],
            underspecified=[
                f"I think the {city} release setup is already in good shape. Please verify the current model, the next-step task on the board, and the sync on the calendar before you send {recipient} a short recap and leave it alone if it is already right.",
                f"The {city} release setup should already be in place. Please verify the current model, the next-step task on the board, and the sync on the calendar before you send {recipient} a short recap and leave it alone if it is already right.",
                f"I believe the {city} release setup is already ready. Please verify the current model, the next-step task on the board, and the sync on the calendar before you send {recipient} a short recap and leave it alone if it's already right.",
                f"The {city} release setup should already be in good shape. Please verify the current model, the next-step task on the board, and the sync on the calendar before you send {recipient} a short recap and leave it untouched if it is already right.",
            ],
        )
    if scenario_slug == "wrong_state_replacement_followthrough":
        stale_hint = {
            "model": "check whether the model is stale",
            "calendar": "check whether the sync is stale",
            "task": "check whether the next step is stale",
        }[replace_kind]
        replace_target = {
            "model": "model setting",
            "calendar": "sync",
            "task": "next step",
        }[replace_kind]
        return _instruction_bundle(
            scenario_slug=scenario_slug,
            prompt_style=prompt_style,
            variant_id=variant_id,
            brief=[
                f"One part of the {city} release setup was staged wrong. {stale_hint.capitalize()}, replace the stale {replace_target} with the correct version, and leave the next step and sync correctly set.",
                f"Something in the {city} release setup was staged wrong. {stale_hint.capitalize()}, retire the stale {replace_target} and put the correct version in place, and leave the next step and sync correctly set.",
                f"The {city} release setup still has one wrong detail in it. {stale_hint.capitalize()}, replace the stale {replace_target} with the correct version, and leave the next step and sync correctly set.",
                f"One part of the {city} release setup is wrong. {stale_hint.capitalize()}, retire the stale {replace_target} and put the correct version in place, and leave the next step and sync correctly set.",
            ],
            underspecified=[
                f"Something in the {city} release setup was staged wrong. {stale_hint.capitalize()}, replace the stale {replace_target} with the correct version, and leave the next step and sync correctly set.",
                f"The {city} release setup still has one wrong detail in it. {stale_hint.capitalize()}, retire the stale {replace_target} and put the correct version in place, and leave the next step and sync correctly set.",
                f"I need the {city} release setup corrected. {stale_hint.capitalize()}, replace the stale {replace_target} with the correct version, and leave the next step and sync correctly set.",
                f"One part of the {city} release setup was staged wrong. {stale_hint.capitalize()}, retire the stale {replace_target} and put the correct version in place, and leave the next step and sync correctly set.",
            ],
        )
    if scenario_slug == "interrupted_workflow_resume":
        resume_kind = slots.get("resume_kind", "")
        if resume_kind == "release_handoff_missing":
            return _instruction_bundle(
                scenario_slug=scenario_slug,
                prompt_style=prompt_style,
                variant_id=variant_id,
                brief=[
                    f"Some of the {city} release work is already in motion. Check the current model, the next step on the board, and the sync on the calendar, finish the missing handoff file, send {recipient} a recap, and don't recreate anything that's already in place.",
                    f"The {city} release work is already partly underway. Check the current model, the next step on the board, and the sync on the calendar, finish the missing handoff file, send {recipient} a recap, and avoid recreating anything that's already in place.",
                    f"Some of the {city} release work is already in motion. Check the current model, the next step on the board, and the sync on the calendar, finish the missing handoff file, send {recipient} a recap, and don't rebuild what is already there.",
                    f"The {city} release work already has pieces in place. Check the current model, the next step on the board, and the sync on the calendar, finish the missing handoff file, send {recipient} a recap, and leave the existing setup alone.",
                ],
                underspecified=[
                    f"Some of the {city} release work is already in motion. Please check the current model, the next step on the board, and the sync on the calendar, finish the missing handoff file, send {recipient} a recap, and don't recreate anything that's already in place.",
                    f"The {city} release work already has the core pieces moving. Please check the current model, the next step on the board, and the sync on the calendar, finish the missing handoff file, send {recipient} a recap, and leave the existing setup alone.",
                    f"I already have part of the {city} release work moving. Please check the current model, the next step on the board, and the sync on the calendar, finish the missing handoff file, send {recipient} a recap, and avoid rebuilding anything that's already in place.",
                    f"The {city} release work is already partly underway. Please check the current model, the next step on the board, and the sync on the calendar, finish the missing handoff file, send {recipient} a recap, and leave the existing pieces alone.",
                ],
            )
        return _instruction_bundle(
            scenario_slug=scenario_slug,
            prompt_style=prompt_style,
            variant_id=variant_id,
            brief=[
                f"Some of the {city} ops work is already in motion. Check what's on the board, what's on the calendar, and the recurring daily check, finish the missing pieces, close out the open work, send {recipient} a recap, and don't recreate anything that's already in place.",
                f"The {city} ops work already has some pieces in place. Check the board, the calendar, and the recurring daily check, finish what's still missing, close out the open work, send {recipient} a recap, and avoid recreating what's already there.",
                f"Some of the {city} ops work is already underway. Check the board, the calendar, and the recurring daily check, finish the missing pieces, close out the open work, send {recipient} a recap, and leave the existing setup alone.",
                f"The {city} ops work is already partly underway. Check the board, the calendar, and the recurring daily check, finish what's still missing, close out the open work, send {recipient} a recap, and don't rebuild anything that's already there.",
            ],
            underspecified=[
                f"Some of the {city} ops work is already in motion. Please check what's on the board, what's on the calendar, and the recurring daily check, finish the missing pieces, close out the open work, send {recipient} a recap, and don't recreate anything that's already in place.",
                f"The {city} ops work already has a few pieces moving. Please check the board, the calendar, and the recurring daily check, finish what's still missing, close out the open work, send {recipient} a recap, and leave the existing setup alone.",
                f"Part of the {city} ops work is already in motion. Please check the board, the calendar, and the recurring daily check, finish the missing pieces, close out the open work, send {recipient} a recap, and don't recreate anything that's already in place.",
                f"The {city} ops work is already partly underway. Please check the board, the calendar, and the recurring daily check, finish what's missing, close out the open work, send {recipient} a recap, and leave the existing pieces alone.",
            ],
        )
    if scenario_slug == "contradictory_source_resolution":
        return _instruction_bundle(
            scenario_slug=scenario_slug,
            prompt_style=prompt_style,
            variant_id=variant_id,
            brief=[
                f"Before making the call on {city}, check the latest {query} email note, the forecast, and today's {timezone} calendar. Leave the next step on the board, keep the recurring daily check scheduled, and either put the review on the calendar or send {recipient} the async update.",
                f"Please use the latest {query} email note, the forecast, and today's {timezone} calendar to make the call on {city}. Put the next step on the board, keep the recurring daily check scheduled, and either put the review on the calendar or send {recipient} the async update.",
                f"Use the latest {query} email note, the forecast, and today's {timezone} calendar to work out the right path for {city}. Leave the next step on the board, keep the recurring daily check scheduled, and either put the review on the calendar or send {recipient} the async update.",
                f"Please reconcile the latest {query} email note, the forecast, and today's {timezone} calendar for {city}. Leave the next step on the board, keep the recurring daily check scheduled, and either put the review on the calendar or send {recipient} the async update.",
            ],
            underspecified=[
                f"The latest {query} email note, the forecast, and today's {timezone} calendar don't line up cleanly for {city}. Please check them, leave the next step on the board, keep the recurring daily check scheduled, and either put the review on the calendar or send {recipient} the async update.",
                f"{city} still needs a decision because the {query} email note, the forecast, and today's {timezone} calendar don't line up cleanly. Please check them, leave the next step on the board, keep the daily check schedule in place, and either put the review on the calendar or send {recipient} the async update.",
                f"The latest {query} email note, the forecast, and today's {timezone} calendar are pulling {city} in different directions. Please check them, leave the next step on the board, keep the recurring daily check scheduled, and either put the review on the calendar or send {recipient} the async update.",
                f"I need a call on the current {city} plan after you compare the latest {query} email note, the forecast, and today's {timezone} calendar. Please leave the next step on the board, keep the recurring daily check scheduled, and either put the review on the calendar or send {recipient} the async update.",
            ],
        )
    raise ValueError(f"unknown instruction scenario: {scenario_slug}")


def _ops_initial_state_overrides(city: str, *, task: bool = False, calendar: bool = False, cron: bool = False) -> dict[str, Any]:
    overrides: dict[str, Any] = {}
    if task:
        overrides["tasks.json"] = [{
            "id": "task_existing_ops",
            "title": f"{city} existing ops next-step task",
            "due": "2026-03-12",
            "status": "pending",
            "priority": "medium",
            "duration": 1,
        }]
    if calendar:
        overrides["calendar_events.json"] = [{
            "id": "evt_existing_ops",
            "title": f"{city} existing ops review block",
            "start": "2026-03-13T09:00",
            "end": "2026-03-13T09:00",
            "location": city,
            "attendees": [],
        }]
    if cron:
        overrides["cron_jobs.json"] = [{
            "id": "cron_existing_ops",
            "name": f"{_slugify(city)}-existing-daily-ops-check",
            "schedule": "0 9 * * *",
            "message": f"Run {city} daily ops check",
            "status": "active",
        }]
    return overrides


def _single_task_override(
    title: str,
    *,
    due: str = "2026-03-12",
    task_id: str = "task_existing_follow_up",
    priority: str = "high",
) -> dict[str, Any]:
    return {
        "tasks.json": [{
            "id": task_id,
            "title": title,
            "due": due,
            "status": "pending",
            "priority": priority,
            "duration": 1,
        }]
    }


def _single_calendar_override(
    title: str,
    *,
    start: str = "2026-03-13T09:00",
    event_id: str = "evt_existing_follow_up",
    location: str = "Remote",
) -> dict[str, Any]:
    return {
        "calendar_events.json": [{
            "id": event_id,
            "title": title,
            "start": start,
            "end": start,
            "location": location,
            "attendees": [],
        }]
    }


def _blocked_review_override(city: str, *, start: str) -> dict[str, Any]:
    return {
        "calendar_events.json": [{
            "id": "evt_existing_blocked_review",
            "title": f"{city} blocker check-in",
            "start": start,
            "end": start,
            "location": city,
            "attendees": [],
        }]
    }


def _forecast_is_risky(city: str, *, days: int = 3) -> bool:
    for offset in range(days):
        date = f"2026-03-{offset + 1:02d}"
        condition = str(_get_weather(city, date).get("condition", "")).lower()
        if condition in _RISKY_WEATHER_CONDITIONS:
            return True
    return False


def _release_initial_state_overrides(
    city: str,
    *,
    next_step: bool = False,
    sync: bool = False,
    follow_up: bool = False,
) -> dict[str, Any]:
    overrides: dict[str, Any] = {}
    if next_step:
        overrides["tasks.json"] = [{
            "id": "task_existing_release_next_step" if not follow_up else "task_existing_release",
            "title": f"{city} existing release next step" if not follow_up else f"Existing {city} release follow-up",
            "due": "2026-03-12" if not follow_up else "2026-03-11",
            "status": "pending",
            "priority": "high" if not follow_up else "low",
            "duration": 1,
        }]
    if sync:
        overrides["calendar_events.json"] = [{
            "id": "evt_existing_release_sync" if not follow_up else "evt_release_sync",
            "title": f"{city} existing release sync",
            "start": "2026-03-13T09:00" if not follow_up else "2026-03-11T08:00",
            "end": "2026-03-13T09:00" if not follow_up else "2026-03-11T08:00",
            "location": city,
            "attendees": [],
        }]
    return overrides


def _resume_initial_state_overrides(
    city: str,
    path: str,
    *,
    resume_kind: str,
    review_start: str,
    cron: str,
) -> dict[str, Any]:
    if resume_kind == "ops_review_missing":
        return {
            **_ops_initial_state_overrides(city, task=True, cron=True),
        }
    if resume_kind == "ops_task_missing":
        return {
            **_ops_initial_state_overrides(city, calendar=True, cron=True),
        }
    return {
        **_release_initial_state_overrides(city, next_step=True, sync=True),
        "ops/release-review.txt": f"{city} release review notes already drafted.",
    }


def _ops_resume_state_overrides(
    city: str,
    *,
    task: bool = False,
    calendar: bool = False,
    cron: bool = False,
) -> dict[str, Any]:
    return {
        **_ops_initial_state_overrides(city, task=task, calendar=calendar, cron=cron),
        "ops/ops-resume-notes.txt": f"{city} partial ops notes already captured.",
    }


def _release_gap_initial_state_overrides(
    city: str,
    *,
    next_step: bool = False,
    sync: bool = False,
) -> dict[str, Any]:
    return {
        **_release_initial_state_overrides(city, next_step=next_step, sync=sync),
        "ops/release-review.txt": f"{city} release review notes already drafted.",
    }


def _contradictory_initial_state_overrides(city: str, *, blocked_today: bool) -> dict[str, Any]:
    if not blocked_today:
        return {}
    return {
        "calendar_events.json": [{
            "id": "evt_conflict_blocker",
            "title": f"{city} blocker check-in",
            "start": "2026-03-01T09:30",
            "end": "2026-03-01T10:00",
            "location": city,
            "attendees": [],
        }]
    }


def _build_inbox_spec(task_id: str, variant_id: int, ctx: dict[str, Any], *, core: bool) -> HardDecisionSpec:
    city = ctx["city"]
    timezone = ctx["timezone"]
    query = ctx["query"]
    seed_id = ctx["seed_id"]
    recipient = ctx["recipient"]
    due = ctx["due"]
    start = ctx["start"]
    task_title = f"{city} {query} follow-up"
    event_title = f"{city} follow-up sync"
    note_path = f"/handoff/{city.lower().replace(' ', '-')}-{query.lower().replace(' ', '-')}-followup.txt"
    subject = f"{query.title()} follow-up for {city}"
    body = f"Tracking the next step for {city}."
    state_mode = ctx.get("state_mode", "task_existing")
    requires_sync = bool(ctx.get("requires_sync", True))
    sync_mode = "sync_required" if requires_sync else "async_only"
    prompt_style = "underspecified" if core else ctx["prompt_style"]
    bundle = _render_instruction_bundle(
        "inbox_followthrough",
        prompt_style,
        variant_id,
        {
            "city": city,
            "query": query,
            "recipient": recipient,
            "state_mode": state_mode,
            "sync_mode": sync_mode,
        },
    )
    commands = [
        f"email search --query '{_quote(query)}'",
        f"email read --id {seed_id}",
        "tasks list --status pending",
        "calendar list",
        f"calendar today --timezone {timezone}",
    ]
    checks = [_exit_zero_check(), _email_to(recipient), *_handoff_file_checks()]
    initial_state_overrides: dict[str, Any]
    if state_mode == "task_existing":
        initial_state_overrides = _single_task_override(task_title, due=due)
        checks.extend([
            _state_count_gte("tasks", 1, "follow-up task already exists"),
            _task_not_created(),
        ])
        if requires_sync:
            checks.append(_calendar_created())
        else:
            checks.append(_calendar_not_created())
    else:
        initial_state_overrides = {}
        commands.append(f"tasks add --title '{_quote(task_title)}' --priority high --due {due}")
        checks.extend([
            _task_created(),
            _task_title_contains(city),
        ])
        if requires_sync:
            checks.append(_calendar_created())
        else:
            checks.append(_calendar_not_created())
    if requires_sync:
        commands.append(f"calendar add-event --title '{_quote(event_title)}' --start {start}")
    commands.extend(
        [
            f"file create --path '{_quote(note_path)}' --content '{_quote(city)} {query} follow-up handoff note.'",
            f"email send --to {recipient} --subject '{_quote(subject)}' --body '{_quote(body)}'",
        ]
    )
    return HardDecisionSpec(
        task_id=task_id,
        scenario_slug="inbox_followthrough",
        variant_id=variant_id,
        prompt_style=prompt_style,
        instruction=bundle.instruction,
        commands=commands,
        checks=checks,
        canonical_instruction=bundle.canonical_instruction,
        instruction_variants=bundle.instruction_variants,
        initial_state_overrides=initial_state_overrides,
    )


def _build_release_spec(task_id: str, variant_id: int, ctx: dict[str, Any], *, core: bool) -> HardDecisionSpec:
    city = ctx["city"]
    timezone = ctx["timezone"]
    model = ctx["model"]
    path = ctx["path"]
    due = ctx["due"]
    start = ctx["start"]
    existing_piece = ctx.get("existing_piece", "none")
    prompt_style = "brief" if core else ctx["prompt_style"]
    bundle = _render_instruction_bundle(
        "release_recovery_runbook",
        prompt_style,
        variant_id,
        {"city": city, "model": model},
    )
    commands = [
        "openclaw config get agent.model",
        "tasks list --status pending",
        "calendar list",
        f"calendar today --timezone {timezone}",
        f"openclaw models set {model}",
        f"file create --path '{_quote(path)}' --content '{_quote(city)} release handoff notes.'",
    ]
    checks = [
        _exit_zero_check(),
        _model_set(model),
        *_release_handoff_file_checks(),
    ]
    initial_state_overrides = {}
    if existing_piece == "decision_log":
        checks.extend([
            _state_count_gte("tasks", 1, "decision-log reminder already exists"),
            _task_not_created(),
        ])
        initial_state_overrides = _release_initial_state_overrides(city, next_step=True)
    else:
        commands.append(f"tasks add --title '{_quote(city)} release decision log' --priority high --due {due}")
        checks.append(_task_created())
    if existing_piece == "review_slot":
        checks.extend([
            _state_count_gte("calendar_events", 1, "review slot already exists"),
            _calendar_not_created(),
        ])
        initial_state_overrides = _release_initial_state_overrides(city, sync=True) if not initial_state_overrides else {
            **initial_state_overrides,
            **_release_initial_state_overrides(city, sync=True),
        }
    else:
        commands.append(f"calendar add-event --title '{_quote(city)} release review' --start {start}")
        checks.append(_calendar_created())
    return HardDecisionSpec(
        task_id=task_id,
        scenario_slug="release_recovery_runbook",
        variant_id=variant_id,
        prompt_style=prompt_style,
        instruction=bundle.instruction,
        commands=commands,
        checks=checks,
        canonical_instruction=bundle.canonical_instruction,
        instruction_variants=bundle.instruction_variants,
        initial_state_overrides=initial_state_overrides,
    )


def _build_incident_spec(task_id: str, variant_id: int, ctx: dict[str, Any], *, core: bool) -> HardDecisionSpec:
    channel = ctx["channel"]
    target = ctx["target"]
    topic = ctx["topic"]
    due = ctx["due"]
    recipient = ctx["recipient"]
    message = f"{topic.title()} escalation started. Please acknowledge."
    state_mode = ctx.get("state_mode", "task_existing")
    prompt_style = "underspecified" if core else ctx["prompt_style"]
    bundle = _render_instruction_bundle(
        "channel_incident_recovery",
        prompt_style,
        variant_id,
        {"topic": topic, "target": target, "channel": channel, "recipient": recipient, "state_mode": state_mode},
    )
    task_title = f"{topic.title()} escalation follow-up"
    commands = [
        "openclaw security audit",
        "tasks list --status pending",
        f"openclaw channels login --channel {channel}",
        f"openclaw message send --channel {channel} --target {target} --message '{_quote(message)}'",
        "openclaw channels list --json",
        f"email send --to {recipient} --subject '{_quote(topic.title())} escalation recap' --body 'The escalation is posted and being tracked.'",
    ]
    checks = [_exit_zero_check(), _message_target(target), _email_to(recipient)]
    initial_state_overrides = _single_task_override(task_title, due=due)
    checks.extend([
        _state_count_gte("tasks", 1, "next-step task already exists"),
        _task_not_created(),
    ])
    return HardDecisionSpec(
        task_id=task_id,
        scenario_slug="channel_incident_recovery",
        variant_id=variant_id,
        prompt_style=prompt_style,
        instruction=bundle.instruction,
        commands=commands,
        checks=checks,
        canonical_instruction=bundle.canonical_instruction,
        instruction_variants=bundle.instruction_variants,
        initial_state_overrides=initial_state_overrides,
    )


def _build_daily_ops_spec(task_id: str, variant_id: int, ctx: dict[str, Any], *, core: bool) -> HardDecisionSpec:
    city = ctx["city"]
    timezone = ctx["timezone"]
    days = ctx["days"]
    due = ctx["due"]
    cron = ctx["cron"]
    state_mode = ctx.get("state_mode", "none")
    task_title = ctx.get("task_title", f"{city} ops review")
    cron_name = ctx.get("cron_name", f"hard-ops-{variant_id:02d}")
    prompt_style = "brief" if core else ctx["prompt_style"]
    bundle = _render_instruction_bundle(
        "daily_ops_commitment_loop",
        prompt_style,
        variant_id,
        {"city": city, "timezone": timezone},
    )
    commands = [
        f"weather forecast --location '{_quote(city)}' --days {days}",
        f"calendar today --timezone {timezone}",
        "tasks list --status pending",
        "openclaw cron list",
    ]
    checks = [_exit_zero_check()]
    initial_state_overrides = {}
    if state_mode == "task_existing":
        checks.extend([
            _state_count_gte("tasks", 1, "next-step task already exists"),
            _task_not_created(),
        ])
        initial_state_overrides = _ops_initial_state_overrides(city, task=True)
    else:
        commands.append(f"tasks add --title '{_quote(task_title)}' --priority medium --due {due}")
        checks.append(_task_created())
    if state_mode == "cron_existing":
        checks.extend([
            _state_count_gte("cron_jobs", 1, "daily check already exists"),
            _cron_not_created(),
        ])
        initial_state_overrides = {**initial_state_overrides, **_ops_initial_state_overrides(city, cron=True)}
    else:
        commands.append(
            f"openclaw cron add --name {cron_name} --cron '{cron}' --message 'Run {_quote(city)} daily ops check'"
        )
        checks.append(_cron_created())
    return HardDecisionSpec(
        task_id=task_id,
        scenario_slug="daily_ops_commitment_loop",
        variant_id=variant_id,
        prompt_style=prompt_style,
        instruction=bundle.instruction,
        commands=commands,
        checks=checks,
        canonical_instruction=bundle.canonical_instruction,
        instruction_variants=bundle.instruction_variants,
        initial_state_overrides=initial_state_overrides,
    )


def _build_release_gate_followthrough_spec(
    task_id: str, variant_id: int, ctx: dict[str, Any], *, core: bool
) -> HardDecisionSpec:
    city = ctx["city"]
    timezone = ctx["timezone"]
    model = ctx["model"]
    path = ctx["path"]
    due = ctx["due"]
    start = ctx["start"]
    prompt_style = "brief" if core else ctx["prompt_style"]
    bundle = _render_instruction_bundle(
        "release_gate_followthrough",
        prompt_style,
        variant_id,
        {"city": city, "model": model},
    )
    commands = [
        "openclaw config get agent.model",
        "tasks list --status pending",
        "calendar list",
        f"calendar today --timezone {timezone}",
    ]
    if model != _MODELS[0]:
        commands.append(f"openclaw models set {model}")
    commands.extend(
        [
            f"file create --path '{_quote(path)}' --content '{_quote(city)} release gate handoff notes.'",
            f"tasks add --title '{_quote(city)} release gate follow-through' --priority high --due {due}",
            f"calendar add-event --title '{_quote(city)} release gate sync' --start {start}",
            f"calendar today --timezone {timezone}",
        ]
    )
    return HardDecisionSpec(
        task_id=task_id,
        scenario_slug="release_gate_followthrough",
        variant_id=variant_id,
        prompt_style=prompt_style,
        instruction=bundle.instruction,
        commands=commands,
        checks=[
            _exit_zero_check(),
            _model_set(model),
            *_release_handoff_file_checks(),
            _task_created(),
            _calendar_created(),
        ],
        canonical_instruction=bundle.canonical_instruction,
        instruction_variants=bundle.instruction_variants,
    )


def _build_delivery_update_followthrough_spec(
    task_id: str, variant_id: int, ctx: dict[str, Any], *, core: bool
) -> HardDecisionSpec:
    channel = ctx["channel"]
    target = ctx["target"]
    topic = ctx["topic"]
    due = ctx["due"]
    start = ctx["start"]
    recipient = ctx["recipient"]
    message = f"{topic.title()} update posted and being tracked."
    state_mode = ctx.get("state_mode", "task_existing")
    requires_live_followup = bool(ctx.get("requires_live_followup", str(target).startswith("#")))
    followup_mode = "live_followup" if requires_live_followup else "async_only"
    prompt_style = "underspecified" if core else ctx["prompt_style"]
    bundle = _render_instruction_bundle(
        "delivery_update_followthrough",
        prompt_style,
        variant_id,
        {
            "topic": topic,
            "target": target,
            "channel": channel,
            "recipient": recipient,
            "state_mode": state_mode,
            "followup_mode": followup_mode,
        },
    )
    task_title = f"{topic.title()} delivery next step"
    event_title = f"{topic.title()} delivery follow-up"
    commands = [
        "tasks list --status pending",
        "openclaw channels list --json",
        f"openclaw channels login --channel {channel}",
    ]
    checks = [_exit_zero_check()]
    initial_state_overrides: dict[str, Any] = {}
    if state_mode == "task_existing":
        initial_state_overrides = _single_task_override(task_title, due=due)
        checks.extend([
            _state_count_gte("tasks", 1, "next-step task already exists"),
            _task_not_created(),
        ])
    else:
        commands.append(f"tasks add --title '{_quote(task_title)}' --priority high --due {due}")
        checks.append(_task_created())
    if requires_live_followup:
        commands.append(f"calendar add-event --title '{_quote(event_title)}' --start {start}")
        checks.append(_calendar_created())
    else:
        checks.append(_calendar_not_created())
    commands.extend(
        [
        f"openclaw message send --channel {channel} --target {target} --message '{_quote(message)}'",
        f"email send --to {recipient} --subject '{_quote(topic.title())} delivery recap' --body 'The delivery path is recovered and the update is posted.'",
        ]
    )
    checks.extend([_message_target(target), _email_to(recipient)])
    return HardDecisionSpec(
        task_id=task_id,
        scenario_slug="delivery_update_followthrough",
        variant_id=variant_id,
        prompt_style=prompt_style,
        instruction=bundle.instruction,
        commands=commands,
        checks=checks,
        canonical_instruction=bundle.canonical_instruction,
        instruction_variants=bundle.instruction_variants,
        initial_state_overrides=initial_state_overrides,
    )


def _build_ops_review_followthrough_spec(
    task_id: str, variant_id: int, ctx: dict[str, Any], *, core: bool
) -> HardDecisionSpec:
    city = ctx["city"]
    timezone = ctx["timezone"]
    due = ctx["due"]
    start = ctx["start"]
    cron = ctx["cron"]
    risky_weather = bool(ctx["risky_weather"])
    state_mode = ctx.get("state_mode", "none")
    event_title = f"{city} {'backup' if risky_weather else 'primary'} ops review"
    cron_name = ctx.get("cron_name", f"ops-review-{variant_id:02d}")
    prompt_style = "brief" if core else ctx["prompt_style"]
    bundle = _render_instruction_bundle(
        "ops_review_followthrough",
        prompt_style,
        variant_id,
        {"city": city, "timezone": timezone},
    )
    commands = [
        f"weather forecast --location '{_quote(city)}' --days 1",
        f"calendar today --timezone {timezone}",
        "openclaw cron list",
        "tasks list --status pending",
    ]
    checks = [_exit_zero_check()]
    initial_state_overrides = {}
    if state_mode == "task_existing":
        checks.extend([
            _state_count_gte("tasks", 1, "next-step task already exists"),
            _task_not_created(),
        ])
        initial_state_overrides = _ops_initial_state_overrides(city, task=True)
    else:
        commands.append(f"tasks add --title '{_quote(city)} ops next step' --priority medium --due {due}")
        checks.append(_task_created())
    if state_mode == "cron_existing":
        checks.extend([
            _state_count_gte("cron_jobs", 1, "daily check already exists"),
            _cron_not_created(),
        ])
        initial_state_overrides = {**initial_state_overrides, **_ops_initial_state_overrides(city, cron=True)}
    else:
        commands.append(
            f"openclaw cron add --name {cron_name} --cron '{cron}' --message 'Run {_quote(city)} daily ops check'"
        )
        checks.append(_cron_created())
    commands.append(f"calendar add-event --title '{_quote(event_title)}' --start {start}")
    checks.append(_calendar_created())
    return HardDecisionSpec(
        task_id=task_id,
        scenario_slug="ops_review_followthrough",
        variant_id=variant_id,
        prompt_style=prompt_style,
        instruction=bundle.instruction,
        commands=commands,
        checks=checks,
        canonical_instruction=bundle.canonical_instruction,
        instruction_variants=bundle.instruction_variants,
        initial_state_overrides=initial_state_overrides,
    )


def _build_existing_state_followthrough_spec(
    task_id: str, variant_id: int, ctx: dict[str, Any], *, core: bool
) -> HardDecisionSpec:
    city = ctx["city"]
    timezone = ctx["timezone"]
    due = ctx["due"]
    start = ctx["start"]
    recipient = ctx["recipient"]
    missing_piece = ctx["existing_piece"]
    prompt_style = "brief" if core else ctx["prompt_style"]
    bundle = _render_instruction_bundle(
        "existing_state_followthrough",
        prompt_style,
        variant_id,
        {
            "city": city,
            "timezone": timezone,
            "existing_piece": missing_piece,
            "recipient": recipient,
        },
    )
    commands = [
        "openclaw cron list",
        "tasks list --status pending",
        "calendar list",
        f"calendar today --timezone {timezone}",
    ]
    checks = [_exit_zero_check()]
    if missing_piece == "cron":
        commands.extend(
            [
                f"openclaw cron add --name existing-hard-ops-{variant_id:02d} --cron '{ctx['cron']}' --message 'Run {_quote(city)} daily ops check'",
            ]
        )
        checks.extend(
            [
                _state_count_gte("tasks", 1, "follow-through task already exists"),
                _state_count_gte("calendar_events", 1, "review block already exists"),
                _task_not_created(),
                _calendar_not_created(),
                _cron_created(),
            ]
        )
    elif missing_piece == "task":
        commands.extend(
            [
                f"tasks add --title '{_quote(city)} ops next step' --priority medium --due {due}",
            ]
        )
        checks.extend(
            [
                _state_count_gte("calendar_events", 1, "review block already exists"),
                _state_count_gte("cron_jobs", 1, "daily check already exists"),
                _calendar_not_created(),
                _cron_not_created(),
                _task_created(),
            ]
        )
    else:
        commands.extend(
            [
                f"calendar add-event --title '{_quote(city)} ops review block' --start {start}",
            ]
        )
        checks.extend(
            [
                _state_count_gte("tasks", 1, "follow-through task already exists"),
                _state_count_gte("cron_jobs", 1, "daily check already exists"),
                _task_not_created(),
                _cron_not_created(),
                _calendar_created(),
            ]
        )
    if missing_piece == "cron":
        initial_state_overrides = _ops_initial_state_overrides(city, task=True, calendar=True)
    elif missing_piece == "task":
        initial_state_overrides = _ops_initial_state_overrides(city, calendar=True, cron=True)
    else:
        initial_state_overrides = _ops_initial_state_overrides(city, task=True, cron=True)
    commands.append(
        f"email send --to {recipient} --subject '{_quote(city)} ops setup recap' --body 'I reviewed the current {city} ops setup, filled the missing piece, and left the existing pieces alone.'"
    )
    checks.append(_email_to(recipient))
    return HardDecisionSpec(
        task_id=task_id,
        scenario_slug="existing_state_followthrough",
        variant_id=variant_id,
        prompt_style=prompt_style,
        instruction=bundle.instruction,
        commands=commands,
        checks=checks,
        initial_state="default",
        canonical_instruction=bundle.canonical_instruction,
        instruction_variants=bundle.instruction_variants,
        initial_state_overrides=initial_state_overrides,
    )


def _build_duplicate_avoidance_followthrough_spec(
    task_id: str, variant_id: int, ctx: dict[str, Any], *, core: bool
) -> HardDecisionSpec:
    city = ctx["city"]
    timezone = ctx["timezone"]
    recipient = ctx["recipient"]
    risky_weather = bool(ctx.get("risky_weather", False))
    if risky_weather:
        followup_mode = "backup_review"
    else:
        followup_mode = "primary_review"
    prompt_style = "underspecified" if core else ctx["prompt_style"]
    bundle = _render_instruction_bundle(
        "duplicate_avoidance_followthrough",
        prompt_style,
        variant_id,
        {"city": city, "recipient": recipient, "followup_mode": followup_mode},
    )
    commands = [
        "openclaw cron list",
        "tasks list --status pending",
        "calendar list",
        f"weather forecast --location '{_quote(city)}' --days 1",
        f"calendar today --timezone {timezone}",
    ]
    checks = [
        _exit_zero_check(),
        _state_count_gte("tasks", 1, "next-step task already exists"),
        _state_count_gte("cron_jobs", 1, "daily check already exists"),
        _task_not_created(),
        _cron_not_created(),
    ]
    initial_state_overrides: dict[str, Any] = _ops_initial_state_overrides(city, task=True, cron=True)
    if risky_weather:
        commands.append(f"calendar add-event --title '{_quote(city)} backup ops review block' --start {ctx['start']}")
        checks.extend([_calendar_created(), _calendar_title_contains("backup")])
    else:
        commands.append(f"calendar add-event --title '{_quote(city)} primary ops review block' --start {ctx['start']}")
        checks.extend([_calendar_created(), _calendar_title_contains("primary")])
    return HardDecisionSpec(
        task_id=task_id,
        scenario_slug="duplicate_avoidance_followthrough",
        variant_id=variant_id,
        prompt_style=prompt_style,
        instruction=bundle.instruction,
        commands=commands,
        checks=checks,
        initial_state="default",
        canonical_instruction=bundle.canonical_instruction,
        instruction_variants=bundle.instruction_variants,
        initial_state_overrides=initial_state_overrides,
    )


def _build_multi_source_decision_followthrough_spec(
    task_id: str, variant_id: int, ctx: dict[str, Any], *, core: bool
) -> HardDecisionSpec:
    city = ctx["city"]
    timezone = ctx["timezone"]
    due = ctx["due"]
    start = ctx["start"]
    cron = ctx["cron"]
    recipient = ctx["recipient"]
    risky_weather = bool(ctx["risky_weather"])
    prompt_style = "brief" if core else ctx["prompt_style"]
    bundle = _render_instruction_bundle(
        "multi_source_decision_followthrough",
        prompt_style,
        variant_id,
        {"city": city, "timezone": timezone, "recipient": recipient},
    )
    commands = [
        f"weather forecast --location '{_quote(city)}' --days 1",
        f"calendar today --timezone {timezone}",
        "email search --query 'review'",
        "email read --id email_seed_5",
        "openclaw cron list",
        "tasks list --status pending",
    ]
    commands.extend(
        [
            f"tasks add --title '{_quote(city)} ops next step' --priority medium --due {due}",
            f"openclaw cron add --name multi-source-hard-ops-{variant_id:02d} --cron '{cron}' --message 'Run {_quote(city)} daily ops check'",
        ]
    )
    checks = [_exit_zero_check(), _task_created(), _cron_created()]
    if risky_weather:
        commands.append(
            f"email send --to {recipient} --subject '{_quote(city)} backup ops plan' --body 'The forecast suggests a backup async follow-through for {city}, so I kept the next step on the board and left the daily check in place.'"
        )
        checks.append(_email_to(recipient))
        checks.append(_calendar_not_created())
    else:
        commands.append(
            f"calendar add-event --title '{_quote(city)} primary ops review' --start {start}"
        )
        checks.append(_calendar_created())
    return HardDecisionSpec(
        task_id=task_id,
        scenario_slug="multi_source_decision_followthrough",
        variant_id=variant_id,
        prompt_style=prompt_style,
        instruction=bundle.instruction,
        commands=commands,
        checks=checks,
        canonical_instruction=bundle.canonical_instruction,
        instruction_variants=bundle.instruction_variants,
    )

def _build_state_repair_followthrough_spec(
    task_id: str, variant_id: int, ctx: dict[str, Any], *, core: bool
) -> HardDecisionSpec:
    city = ctx["city"]
    timezone = ctx["timezone"]
    due = ctx["due"]
    start = ctx["start"]
    path = ctx["path"]
    model = ctx["model"]
    repair_kind = ctx["repair_kind"]
    initial_state = ctx["initial_state"]
    prompt_style = "brief" if core else ctx["prompt_style"]
    bundle = _render_instruction_bundle(
        "state_repair_followthrough",
        prompt_style,
        variant_id,
        {"city": city, "repair_kind": repair_kind},
    )
    existing_release_follow_up_title = f"Existing {city} release follow-up"
    if repair_kind == "model":
        commands = [
            "openclaw config get agent.model",
            "tasks list --status pending",
            "calendar list",
            f"file create --path '{_quote(path)}' --content '{_quote(city)} refreshed release handoff notes.'",
            f"openclaw models set {model}",
            f"tasks add --title '{_quote(city)} release follow-through' --priority high --due {due}",
            f"calendar add-event --title '{_quote(city)} release sync' --start {start}",
        ]
        checks = [_exit_zero_check(), *_release_handoff_file_checks(), _model_set(model), _task_created(), _calendar_created()]
    elif repair_kind == "calendar":
        commands = [
            "calendar list",
            f"calendar today --timezone {timezone}",
            "tasks list --status pending",
            f"file create --path '{_quote(path)}' --content '{_quote(city)} refreshed release handoff notes.'",
            f"calendar update-event --id evt_release_sync --start {start}",
            f"tasks add --title '{_quote(city)} release follow-through' --priority high --due {due}",
        ]
        checks = [_exit_zero_check(), *_release_handoff_file_checks(), _calendar_updated(), _calendar_not_created(), _task_created()]
    else:
        commands = [
            "tasks list --status pending",
            "calendar list",
            f"calendar today --timezone {timezone}",
            f"file create --path '{_quote(path)}' --content '{_quote(city)} refreshed release handoff notes.'",
            f"tasks complete --title '{_quote(existing_release_follow_up_title)}'",
            f"tasks add --title '{_quote(city)} release follow-through' --priority high --due {due}",
            f"calendar add-event --title '{_quote(city)} release sync' --start {start}",
        ]
        checks = [_exit_zero_check(), *_release_handoff_file_checks(), _task_completed(), _task_created(), _calendar_created()]
    if repair_kind == "calendar":
        initial_state_overrides = _release_initial_state_overrides(city, sync=True, follow_up=True)
    elif repair_kind == "task":
        initial_state_overrides = _release_initial_state_overrides(city, next_step=True, follow_up=True)
    else:
        initial_state_overrides = {}
    return HardDecisionSpec(
        task_id=task_id,
        scenario_slug="state_repair_followthrough",
        variant_id=variant_id,
        prompt_style=prompt_style,
        instruction=bundle.instruction,
        commands=commands,
        checks=checks,
        initial_state=initial_state,
        canonical_instruction=bundle.canonical_instruction,
        instruction_variants=bundle.instruction_variants,
        initial_state_overrides=initial_state_overrides,
    )


def _build_completion_gap_followthrough_spec(
    task_id: str, variant_id: int, ctx: dict[str, Any], *, core: bool
) -> HardDecisionSpec:
    city = ctx["city"]
    timezone = ctx["timezone"]
    due = ctx["due"]
    start = ctx["start"]
    path = ctx["path"]
    gap_kind = ctx["gap_kind"]
    initial_state = ctx["initial_state"]
    prompt_style = "brief" if core else ctx["prompt_style"]
    bundle = _render_instruction_bundle(
        "completion_gap_followthrough",
        prompt_style,
        variant_id,
        {"city": city, "gap_kind": gap_kind},
    )
    commands = [
        "openclaw config get agent.model",
        "tasks list --status pending",
        "calendar list",
        f"calendar today --timezone {timezone}",
        "file read --path '/ops/release-review.txt'",
        f"file create --path '{_quote(path)}' --content '{_quote(city)} completion-gap release handoff notes.'",
    ]
    checks = [_exit_zero_check(), *_release_handoff_file_checks()]
    if gap_kind == "task_and_calendar":
        commands.extend(
            [
                f"tasks add --title '{_quote(city)} release next step' --priority high --due {due}",
                f"calendar add-event --title '{_quote(city)} release sync' --start {start}",
            ]
        )
        checks.extend([_task_created(), _calendar_created()])
    elif gap_kind == "calendar_only":
        commands.extend(
            [
                f"tasks search --query '{_quote(city)} release next step'",
                f"calendar add-event --title '{_quote(city)} release sync' --start {start}",
            ]
        )
        checks.extend([
            _state_count_gte("tasks", 1, "follow-through task already exists"),
            _task_not_created(),
            _calendar_created(),
        ])
    else:
        commands.extend(
            [
                f"calendar list --from {start[:10]} --to {start[:10]}",
                f"tasks add --title '{_quote(city)} release next step' --priority high --due {due}",
            ]
        )
        checks.extend([
            _state_count_gte("calendar_events", 1, "release sync already exists"),
            _calendar_not_created(),
            _task_created(),
        ])
    if gap_kind == "calendar_only":
        initial_state_overrides = _release_gap_initial_state_overrides(city, next_step=True)
    elif gap_kind == "task_only":
        initial_state_overrides = _release_gap_initial_state_overrides(city, sync=True)
    else:
        initial_state_overrides = _release_gap_initial_state_overrides(city)
    return HardDecisionSpec(
        task_id=task_id,
        scenario_slug="completion_gap_followthrough",
        variant_id=variant_id,
        prompt_style=prompt_style,
        instruction=bundle.instruction,
        commands=commands,
        checks=checks,
        initial_state=initial_state,
        canonical_instruction=bundle.canonical_instruction,
        instruction_variants=bundle.instruction_variants,
        initial_state_overrides=initial_state_overrides,
    )


def _build_branch_resolution_followthrough_spec(
    task_id: str, variant_id: int, ctx: dict[str, Any], *, core: bool
) -> HardDecisionSpec:
    city = ctx["city"]
    timezone = ctx["timezone"]
    start = ctx["start"]
    recipient = ctx["recipient"]
    backup_path = bool(ctx["backup_path"])
    initial_state = ctx["initial_state"]
    prompt_style = "brief" if core else ctx["prompt_style"]
    bundle = _render_instruction_bundle(
        "branch_resolution_followthrough",
        prompt_style,
        variant_id,
        {"city": city, "timezone": timezone, "recipient": recipient},
    )
    commands = [
        f"weather forecast --location '{_quote(city)}' --days 1",
        f"calendar today --timezone {timezone}",
        "openclaw cron list",
        "tasks list --status pending",
    ]
    checks = [
        _exit_zero_check(),
        _state_count_gte("tasks", 1, "next-step task already exists"),
        _task_not_created(),
        _state_count_gte("cron_jobs", 1, "daily check already exists"),
        _cron_not_created(),
    ]
    if backup_path:
        commands.append(
            f"email send --to {recipient} --subject '{_quote(city)} backup ops plan' --body 'The current context points to the backup async path for {city}, so I left the staged task and daily check in place.'"
        )
        checks.extend([_email_to(recipient), _calendar_not_created()])
    else:
        commands.append(f"calendar add-event --title '{_quote(city)} primary ops review' --start {start}")
        checks.append(_calendar_created())
    return HardDecisionSpec(
        task_id=task_id,
        scenario_slug="branch_resolution_followthrough",
        variant_id=variant_id,
        prompt_style=prompt_style,
        instruction=bundle.instruction,
        commands=commands,
        checks=checks,
        initial_state=initial_state,
        canonical_instruction=bundle.canonical_instruction,
        instruction_variants=bundle.instruction_variants,
        initial_state_overrides=_ops_initial_state_overrides(city, task=True, cron=True),
    )


def _build_already_done_skip_followthrough_spec(
    task_id: str, variant_id: int, ctx: dict[str, Any], *, core: bool
) -> HardDecisionSpec:
    city = ctx["city"]
    timezone = ctx["timezone"]
    recipient = ctx["recipient"]
    prompt_style = "brief" if core else ctx["prompt_style"]
    stable_model = "anthropic/claude-sonnet-4-5-20250929"
    bundle = _render_instruction_bundle(
        "already_done_skip_followthrough",
        prompt_style,
        variant_id,
        {"city": city, "recipient": recipient},
    )
    commands = [
        "openclaw config get agent.model",
        "tasks list --status pending",
        "calendar list",
        f"calendar today --timezone {timezone}",
        f"email send --to {recipient} --subject '{_quote(city)} release recap' --body 'I verified that the current model, staged task, and release sync are already in place for {city}, so I left the follow-through as-is.'",
    ]
    checks = [
        _exit_zero_check(),
        _model_set(stable_model),
        _state_count_gte("tasks", 1, "next-step task already exists"),
        _state_count_gte("calendar_events", 1, "release sync already exists"),
        _email_to(recipient),
        _task_not_created(),
        _calendar_not_created(),
    ]
    return HardDecisionSpec(
        task_id=task_id,
        scenario_slug="already_done_skip_followthrough",
        variant_id=variant_id,
        prompt_style=prompt_style,
        instruction=bundle.instruction,
        commands=commands,
        checks=checks,
        initial_state="hard_full_release",
        canonical_instruction=bundle.canonical_instruction,
        instruction_variants=bundle.instruction_variants,
        initial_state_overrides=_release_initial_state_overrides(city, next_step=True, sync=True),
    )


def _build_wrong_state_replacement_followthrough_spec(
    task_id: str, variant_id: int, ctx: dict[str, Any], *, core: bool
) -> HardDecisionSpec:
    city = ctx["city"]
    timezone = ctx["timezone"]
    due = ctx["due"]
    start = ctx["start"]
    path = ctx["path"]
    model = ctx["model"]
    replace_kind = ctx["replace_kind"]
    initial_state = ctx["initial_state"]
    prompt_style = "brief" if core else ctx["prompt_style"]
    bundle = _render_instruction_bundle(
        "wrong_state_replacement_followthrough",
        prompt_style,
        variant_id,
        {"city": city, "replace_kind": replace_kind},
    )
    existing_release_follow_up_title = f"Existing {city} release follow-up"
    if replace_kind == "model":
        commands = [
            "openclaw config get agent.model",
            "tasks list --status pending",
            "calendar list",
            f"openclaw models set {model}",
            f"tasks add --title '{_quote(city)} release replacement next step' --priority high --due {due}",
            f"calendar add-event --title '{_quote(city)} replacement release sync' --start {start}",
        ]
        checks = [_exit_zero_check(), _model_set(model), _task_created(), _calendar_created()]
    elif replace_kind == "calendar":
        commands = [
            "calendar list",
            f"calendar today --timezone {timezone}",
            "tasks list --status pending",
            f"calendar update-event --id evt_release_sync --start {start}",
            f"tasks add --title '{_quote(city)} release replacement next step' --priority high --due {due}",
        ]
        checks = [_exit_zero_check(), _calendar_updated(), _calendar_not_created(), _task_created()]
    else:
        commands = [
            "tasks list --status pending",
            "calendar list",
            f"calendar today --timezone {timezone}",
            f"tasks complete --title '{_quote(existing_release_follow_up_title)}'",
            f"tasks add --title '{_quote(city)} release replacement next step' --priority high --due {due}",
            f"calendar add-event --title '{_quote(city)} replacement release sync' --start {start}",
        ]
        checks = [_exit_zero_check(), _task_completed(), _task_created(), _calendar_created()]
    if replace_kind == "calendar":
        initial_state_overrides = _release_initial_state_overrides(city, sync=True, follow_up=True)
    elif replace_kind == "task":
        initial_state_overrides = _release_initial_state_overrides(city, next_step=True, follow_up=True)
    else:
        initial_state_overrides = {}
    return HardDecisionSpec(
        task_id=task_id,
        scenario_slug="wrong_state_replacement_followthrough",
        variant_id=variant_id,
        prompt_style=prompt_style,
        instruction=bundle.instruction,
        commands=commands,
        checks=checks,
        initial_state=initial_state,
        canonical_instruction=bundle.canonical_instruction,
        instruction_variants=bundle.instruction_variants,
        initial_state_overrides=initial_state_overrides,
    )


def _build_interrupted_workflow_resume_spec(
    task_id: str, variant_id: int, ctx: dict[str, Any], *, core: bool
) -> HardDecisionSpec:
    city = ctx["city"]
    timezone = ctx["timezone"]
    recipient = ctx["recipient"]
    due = ctx["due"]
    start = ctx["start"]
    cron = ctx["cron"]
    path = ctx["path"]
    resume_kind = ctx["resume_kind"]
    prompt_style = "underspecified" if core else ctx["prompt_style"]
    bundle = _render_instruction_bundle(
        "interrupted_workflow_resume",
        prompt_style,
        variant_id,
        {"city": city, "timezone": timezone, "recipient": recipient, "resume_kind": resume_kind},
    )
    if resume_kind == "ops_review_missing":
        commands = [
            f"weather forecast --location '{_quote(city)}' --days 1",
            "tasks list --status pending",
            f"tasks search --query '{_quote(city)} ops next step'",
            "openclaw cron list",
            "calendar list",
            f"calendar today --timezone {timezone}",
            f"calendar add-event --title '{_quote(city)} resumed ops review' --start {start}",
            f"email send --to {recipient} --subject '{_quote(city)} ops resume recap' --body 'I checked the existing {city} ops setup, added the missing review, and left the existing task and daily check in place.'",
        ]
        checks = [
            _exit_zero_check(),
            _state_count_gte("tasks", 1, "next-step task already exists"),
            _state_count_gte("cron_jobs", 1, "daily check already exists"),
            _task_not_created(),
            _cron_not_created(),
            _calendar_created(),
            _email_to(recipient),
        ]
        initial_state_overrides = _ops_resume_state_overrides(city, task=True, cron=True)
    elif resume_kind == "ops_task_missing":
        commands = [
            f"weather forecast --location '{_quote(city)}' --days 1",
            "calendar list",
            f"calendar today --timezone {timezone}",
            "openclaw cron list",
            "tasks list --status pending",
            f"tasks search --query '{_quote(city)} ops'",
            f"tasks add --title '{_quote(city)} resumed ops next step' --priority medium --due {due}",
            f"email send --to {recipient} --subject '{_quote(city)} ops resume recap' --body 'I checked the existing {city} ops setup, added the missing next step, and left the review block and daily check in place.'",
        ]
        checks = [
            _exit_zero_check(),
            _state_count_gte("calendar_events", 1, "review block already exists"),
            _state_count_gte("cron_jobs", 1, "daily check already exists"),
            _calendar_not_created(),
            _cron_not_created(),
            _task_created(),
            _email_to(recipient),
        ]
        initial_state_overrides = _ops_resume_state_overrides(city, calendar=True, cron=True)
    else:
        commands = [
            "openclaw config get agent.model",
            "tasks list --status pending",
            f"tasks search --query '{_quote(city)} release'",
            "calendar list",
            f"calendar today --timezone {timezone}",
            "file read --path '/ops/release-review.txt'",
            f"file create --path '{_quote(path)}' --content '{_quote(city)} resumed release handoff notes.'",
            f"email send --to {recipient} --subject '{_quote(city)} release resume recap' --body 'I checked the existing {city} release setup, refreshed the missing handoff, and left the next step and sync in place.'",
        ]
        checks = [
            _exit_zero_check(),
            _state_count_gte("tasks", 1, "next-step task already exists"),
            _state_count_gte("calendar_events", 1, "release sync already exists"),
            _task_not_created(),
            _calendar_not_created(),
            *_release_handoff_file_checks(),
            _email_to(recipient),
        ]
        initial_state_overrides = _resume_initial_state_overrides(
            city,
            path,
            resume_kind=resume_kind,
            review_start=start,
            cron=cron,
        )
    return HardDecisionSpec(
        task_id=task_id,
        scenario_slug="interrupted_workflow_resume",
        variant_id=variant_id,
        prompt_style=prompt_style,
        instruction=bundle.instruction,
        commands=commands,
        checks=checks,
        canonical_instruction=bundle.canonical_instruction,
        instruction_variants=bundle.instruction_variants,
        initial_state_overrides=initial_state_overrides,
    )


def _build_contradictory_source_resolution_spec(
    task_id: str, variant_id: int, ctx: dict[str, Any], *, core: bool
) -> HardDecisionSpec:
    city = ctx["city"]
    timezone = ctx["timezone"]
    due = ctx["due"]
    start = ctx["start"]
    cron = ctx["cron"]
    recipient = ctx["recipient"]
    query = ctx["query"]
    seed_id = ctx["seed_id"]
    risky_weather = bool(ctx["risky_weather"])
    blocked_today = bool(ctx["blocked_today"])
    prompt_style = "brief" if core else ctx["prompt_style"]
    bundle = _render_instruction_bundle(
        "contradictory_source_resolution",
        prompt_style,
        variant_id,
        {"city": city, "timezone": timezone, "recipient": recipient, "query": query},
    )
    commands = [
        f"email search --query '{_quote(query)}'",
        f"email read --id {seed_id}",
        f"weather forecast --location '{_quote(city)}' --days 1",
        f"calendar today --timezone {timezone}",
        "calendar list --from 2026-03-01 --to 2026-03-01",
        "tasks list --status pending",
        f"tasks add --title '{_quote(city)} contradictory-source next step' --priority high --due {due}",
        f"openclaw cron add --name contradictory-source-{variant_id:02d} --cron '{cron}' --message 'Run {_quote(city)} daily contradiction check'",
    ]
    checks = [
        _exit_zero_check(),
        _task_created(),
        _cron_created(),
    ]
    if risky_weather or blocked_today:
        commands.append(
            f"email send --to {recipient} --subject '{_quote(city)} async update' --body 'I checked the latest {query} note, the forecast, and todays calendar, and {city} should shift async while keeping the next step and daily check in place.'"
        )
        checks.extend([_email_to(recipient), _calendar_not_created()])
    else:
        commands.append(
            f"calendar add-event --title '{_quote(city)} live review' --start {start}"
        )
        checks.append(_calendar_created())
    return HardDecisionSpec(
        task_id=task_id,
        scenario_slug="contradictory_source_resolution",
        variant_id=variant_id,
        prompt_style=prompt_style,
        instruction=bundle.instruction,
        commands=commands,
        checks=checks,
        canonical_instruction=bundle.canonical_instruction,
        instruction_variants=bundle.instruction_variants,
        initial_state_overrides=_contradictory_initial_state_overrides(city, blocked_today=blocked_today),
    )


def _core_specs() -> list[HardDecisionSpec]:
    specs: list[HardDecisionSpec] = []
    for i in range(6):
        city_tz = _CITY_TIMEZONE_BUNDLES[i]
        inbox = _INBOX_EMAILS[i % len(_INBOX_EMAILS)]
        recipient = _RECIPIENTS[i]
        schedule = _SCHEDULE_BUNDLES[i]
        specs.append(
            _build_inbox_spec(
                task_id=f"hard_decision_workflow_{len(specs) + 1}",
                variant_id=i + 1,
                ctx={
                    **city_tz,
                    **inbox,
                    "recipient": recipient,
                    **schedule,
                    "state_mode": "task_existing" if i % 2 == 0 else "task_missing",
                },
                core=True,
            )
        )
    for i in range(6):
        city_tz = _CITY_TIMEZONE_BUNDLES[i]
        schedule = _SCHEDULE_BUNDLES[i]
        specs.append(
            _build_release_spec(
                task_id=f"hard_decision_workflow_{len(specs) + 1}",
                variant_id=i + 1,
                ctx={
                    **city_tz,
                    **schedule,
                    "model": _MODELS[i],
                    "path": _RELEASE_FILE_PATHS[0],
                    "existing_piece": "decision_log" if i % 2 == 0 else "review_slot",
                },
                core=True,
            )
        )
    for i in range(6):
        bundle = _CHANNEL_TARGET_BUNDLES[i]
        schedule = _SCHEDULE_BUNDLES[i]
        specs.append(
            _build_incident_spec(
                task_id=f"hard_decision_workflow_{len(specs) + 1}",
                variant_id=i + 1,
                ctx={
                    **bundle,
                    **schedule,
                    "topic": _TOPICS[i],
                    "recipient": _RECIPIENTS[i],
                },
                core=True,
            )
        )
    for i in range(6):
        city_tz = _CITY_TIMEZONE_BUNDLES[i]
        schedule = _SCHEDULE_BUNDLES[i]
        specs.append(
            _build_daily_ops_spec(
                task_id=f"hard_decision_workflow_{len(specs) + 1}",
                variant_id=i + 1,
                ctx={
                    **city_tz,
                    **schedule,
                    "cron_name": f"hard-ops-{i + 1:02d}",
                    "state_mode": "task_existing" if i % 2 == 0 else "cron_existing",
                },
                core=True,
            )
        )
    return specs


def _sample_candidate_contexts(scenario_slug: str, count: int) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    if scenario_slug == "inbox_followthrough":
        for city_tz in _CITY_TIMEZONE_BUNDLES:
            for inbox in _INBOX_EMAILS:
                for recipient in _RECIPIENTS[:8]:
                    for schedule in _SCHEDULE_BUNDLES:
                        for state_mode in ("task_existing", "task_missing"):
                            candidates.append(
                                {
                                    **city_tz,
                                    **inbox,
                                    "recipient": recipient,
                                    **schedule,
                                    "state_mode": state_mode,
                                    "prompt_style": _scenario_prompt_style(len(candidates)),
                                }
                            )
    elif scenario_slug == "release_recovery_runbook":
        for city_tz in _CITY_TIMEZONE_BUNDLES:
            for model in _MODELS:
                for path in _RELEASE_FILE_PATHS:
                    for schedule in _SCHEDULE_BUNDLES:
                        for existing_piece in ("decision_log", "review_slot"):
                            candidates.append(
                                {
                                    **city_tz,
                                    "model": model,
                                    "path": path,
                                    "existing_piece": existing_piece,
                                    **schedule,
                                    "prompt_style": _scenario_prompt_style(len(candidates)),
                                }
                            )
    elif scenario_slug == "channel_incident_recovery":
        for bundle in _CHANNEL_TARGET_BUNDLES:
            for topic in _TOPICS:
                for recipient in _RECIPIENTS[:8]:
                    for schedule in _SCHEDULE_BUNDLES:
                        candidates.append(
                            {
                                **bundle,
                                "topic": topic,
                                "recipient": recipient,
                                **schedule,
                                "state_mode": "task_existing",
                                "prompt_style": _scenario_prompt_style(len(candidates)),
                            }
                        )
    elif scenario_slug == "daily_ops_commitment_loop":
        for city_tz in _CITY_TIMEZONE_BUNDLES:
            for schedule in _SCHEDULE_BUNDLES:
                for state_mode, task_title in (
                    ("task_existing", f"{city_tz['city']} ops next step"),
                    ("cron_existing", f"{city_tz['city']} ops review"),
                ):
                    candidates.append(
                        {
                            **city_tz,
                            **schedule,
                            "task_title": task_title,
                            "state_mode": state_mode,
                            "prompt_style": _scenario_prompt_style(len(candidates)),
                        }
                    )
    elif scenario_slug == "release_gate_followthrough":
        for city_tz in _CITY_TIMEZONE_BUNDLES:
            for model in _MODELS:
                for path in _RELEASE_FILE_PATHS:
                    for schedule in _SCHEDULE_BUNDLES:
                        candidates.append(
                            {
                                **city_tz,
                                "model": model,
                                "path": path,
                                **schedule,
                                "prompt_style": _scenario_prompt_style(len(candidates)),
                            }
                        )
    elif scenario_slug == "delivery_update_followthrough":
        for bundle in _CHANNEL_TARGET_BUNDLES:
            for topic in _TOPICS:
                for recipient in _RECIPIENTS[:8]:
                    for schedule in _SCHEDULE_BUNDLES:
                        for state_mode in ("task_existing", "task_missing"):
                            candidates.append(
                                {
                                    **bundle,
                                    "topic": topic,
                                    "recipient": recipient,
                                    **schedule,
                                    "requires_live_followup": str(bundle["target"]).startswith("#"),
                                    "state_mode": state_mode,
                                    "prompt_style": _scenario_prompt_style(len(candidates)),
                                }
                            )
    elif scenario_slug == "ops_review_followthrough":
        for city_tz in _CITY_TIMEZONE_BUNDLES:
            risky_weather = city_tz["city"] in {"Berlin", "London", "New York", "Sydney"}
            for schedule in _SCHEDULE_BUNDLES:
                for state_mode in ("task_existing", "cron_existing"):
                    candidates.append(
                        {
                            **city_tz,
                            **schedule,
                            "risky_weather": risky_weather,
                            "state_mode": state_mode,
                            "prompt_style": _scenario_prompt_style(len(candidates)),
                        }
                    )
    elif scenario_slug == "existing_state_followthrough":
        existing_bundles = (
            ("cron", "hard_existing_cron"),
            ("task", "hard_existing_task"),
            ("calendar", "hard_existing_calendar"),
        )
        for city_tz in _CITY_TIMEZONE_BUNDLES:
            for schedule in _SCHEDULE_BUNDLES:
                for recipient in _RECIPIENTS[:8]:
                    for existing_piece, initial_state in existing_bundles:
                        candidates.append(
                            {
                                **city_tz,
                                **schedule,
                                "existing_piece": existing_piece,
                                "initial_state": initial_state,
                                "recipient": recipient,
                                "prompt_style": _scenario_prompt_style(len(candidates)),
                            }
                        )
    elif scenario_slug == "duplicate_avoidance_followthrough":
        for city_tz in _CITY_TIMEZONE_BUNDLES:
            risky_weather = _forecast_is_risky(city_tz["city"])
            for recipient in _RECIPIENTS[:8]:
                for schedule in _SCHEDULE_BUNDLES:
                    candidates.append(
                        {
                            **city_tz,
                            **schedule,
                            "recipient": recipient,
                            "risky_weather": risky_weather,
                            "prompt_style": _scenario_prompt_style(len(candidates)),
                        }
                    )
    elif scenario_slug == "multi_source_decision_followthrough":
        for city_tz in _CITY_TIMEZONE_BUNDLES:
            risky_weather = city_tz["city"] in {"Berlin", "London", "New York", "Sydney"}
            for schedule in _SCHEDULE_BUNDLES:
                for recipient in _RECIPIENTS[:8]:
                    candidates.append(
                        {
                            **city_tz,
                            **schedule,
                            "recipient": recipient,
                            "risky_weather": risky_weather,
                            "prompt_style": _scenario_prompt_style(len(candidates)),
                        }
                    )
    elif scenario_slug == "state_repair_followthrough":
        repair_bundles = (
            ("model", "hard_wrong_model"),
            ("calendar", "hard_wrong_calendar"),
            ("task", "hard_wrong_task"),
        )
        for city_tz in _CITY_TIMEZONE_BUNDLES:
            for schedule in _SCHEDULE_BUNDLES:
                for repair_kind, initial_state in repair_bundles:
                    for model in _MODELS[:5]:
                        candidates.append(
                            {
                                **city_tz,
                                **schedule,
                                "repair_kind": repair_kind,
                                "initial_state": initial_state,
                                "model": model,
                                "path": _RELEASE_FILE_PATHS[0],
                                "prompt_style": _scenario_prompt_style(len(candidates)),
                            }
                        )
    elif scenario_slug == "completion_gap_followthrough":
        gap_bundles = (
            ("task_and_calendar", "hard_partial_release"),
            ("calendar_only", "hard_partial_release_task"),
            ("task_only", "hard_partial_release_calendar"),
        )
        for city_tz in _CITY_TIMEZONE_BUNDLES:
            for schedule in _SCHEDULE_BUNDLES:
                for recipient in _RECIPIENTS[:8]:
                    for gap_kind, initial_state in gap_bundles:
                        candidates.append(
                            {
                                **city_tz,
                                **schedule,
                                "gap_kind": gap_kind,
                                "initial_state": initial_state,
                                "model": _MODELS[(len(candidates)) % len(_MODELS)],
                                "path": _RELEASE_FILE_PATHS[0],
                                "recipient": recipient,
                                "prompt_style": _scenario_prompt_style(len(candidates)),
                            }
                        )
    elif scenario_slug == "branch_resolution_followthrough":
        for city_tz in _CITY_TIMEZONE_BUNDLES:
            backup_path = city_tz["city"] in {"Berlin", "London", "Sydney", "New York"}
            for schedule in _SCHEDULE_BUNDLES:
                for recipient in _RECIPIENTS[:8]:
                    candidates.append(
                        {
                            **city_tz,
                            **schedule,
                            "recipient": recipient,
                            "backup_path": backup_path,
                            "initial_state": "hard_partial_delivery",
                            "prompt_style": _scenario_prompt_style(len(candidates)),
                        }
                    )
    elif scenario_slug == "already_done_skip_followthrough":
        for city_tz in _CITY_TIMEZONE_BUNDLES:
            for recipient in _RECIPIENTS[:8]:
                candidates.append(
                    {
                        **city_tz,
                        "recipient": recipient,
                        "prompt_style": _scenario_prompt_style(len(candidates)),
                    }
                )
    elif scenario_slug == "wrong_state_replacement_followthrough":
        replace_bundles = (
            ("model", "hard_wrong_model"),
            ("calendar", "hard_wrong_calendar"),
            ("task", "hard_wrong_task"),
        )
        for city_tz in _CITY_TIMEZONE_BUNDLES:
            for schedule in _SCHEDULE_BUNDLES:
                for replace_kind, initial_state in replace_bundles:
                    for model in _MODELS[:5]:
                        candidates.append(
                            {
                                **city_tz,
                                **schedule,
                                "replace_kind": replace_kind,
                                "initial_state": initial_state,
                                "model": model,
                                "path": _RELEASE_FILE_PATHS[0],
                                "prompt_style": _scenario_prompt_style(len(candidates)),
                            }
                        )
    elif scenario_slug == "interrupted_workflow_resume":
        resume_kinds = (
            "ops_review_missing",
            "ops_task_missing",
            "release_handoff_missing",
        )
        for city_tz in _CITY_TIMEZONE_BUNDLES:
            for schedule in _SCHEDULE_BUNDLES:
                for recipient in _RECIPIENTS[:8]:
                    for resume_kind in resume_kinds:
                        candidates.append(
                            {
                                **city_tz,
                                **schedule,
                                "recipient": recipient,
                                "resume_kind": resume_kind,
                                "path": _RELEASE_FILE_PATHS[0],
                                "prompt_style": _scenario_prompt_style(len(candidates)),
                            }
                        )
    elif scenario_slug == "contradictory_source_resolution":
        conflict_queries = [item for item in _INBOX_EMAILS if item["query"] in {"review", "meeting"}]
        for city_tz in _CITY_TIMEZONE_BUNDLES:
            risky_weather = city_tz["city"] in {"Berlin", "London", "New York", "Sydney"}
            for schedule in _SCHEDULE_BUNDLES:
                for recipient in _RECIPIENTS[:8]:
                    for inbox in conflict_queries:
                        for blocked_today in (False, True):
                            candidates.append(
                                {
                                    **city_tz,
                                    **schedule,
                                    "recipient": recipient,
                                    "query": inbox["query"],
                                    "seed_id": inbox["seed_id"],
                                    "risky_weather": risky_weather,
                                    "blocked_today": blocked_today,
                                    "prompt_style": _scenario_prompt_style(len(candidates)),
                                }
                            )
    else:
        raise ValueError(f"unknown scenario: {scenario_slug}")
    rng = random.Random(f"hard-decision:{scenario_slug}:v2")
    rng.shuffle(candidates)
    return candidates[:count]


def _signature(spec: HardDecisionSpec) -> tuple[str, tuple[str, ...]]:
    return (spec.instruction, tuple(spec.commands))


_SCENARIO_ORDER = [
    "inbox_followthrough",
    "release_recovery_runbook",
    "channel_incident_recovery",
    "daily_ops_commitment_loop",
    "release_gate_followthrough",
    "delivery_update_followthrough",
    "ops_review_followthrough",
    "existing_state_followthrough",
    "duplicate_avoidance_followthrough",
    "multi_source_decision_followthrough",
    "state_repair_followthrough",
    "completion_gap_followthrough",
    "branch_resolution_followthrough",
    "already_done_skip_followthrough",
    "wrong_state_replacement_followthrough",
    "interrupted_workflow_resume",
    "contradictory_source_resolution",
]

_DEFAULT_HARD_SCENARIO_COUNTS = {
    "inbox_followthrough": 12,
    "release_recovery_runbook": 10,
    "channel_incident_recovery": 10,
    "daily_ops_commitment_loop": 10,
    "release_gate_followthrough": 30,
    "delivery_update_followthrough": 10,
    "ops_review_followthrough": 30,
    "existing_state_followthrough": 10,
    "duplicate_avoidance_followthrough": 10,
    "multi_source_decision_followthrough": 20,
    "state_repair_followthrough": 46,
    "completion_gap_followthrough": 12,
    "branch_resolution_followthrough": 40,
    "already_done_skip_followthrough": 10,
    "wrong_state_replacement_followthrough": 46,
    "interrupted_workflow_resume": 30,
    "contradictory_source_resolution": 26,
}


_SCENARIO_PRIMARY_ABILITIES = {
    "inbox_followthrough": "information_transfer",
    "release_recovery_runbook": "workflow_completion",
    "channel_incident_recovery": "information_transfer",
    "daily_ops_commitment_loop": "workflow_completion",
    "release_gate_followthrough": "workflow_completion",
    "delivery_update_followthrough": "information_transfer",
    "ops_review_followthrough": "workflow_completion",
    "existing_state_followthrough": "gap_completion",
    "duplicate_avoidance_followthrough": "duplicate_avoidance",
    "multi_source_decision_followthrough": "multi_source_reasoning",
    "state_repair_followthrough": "state_repair",
    "completion_gap_followthrough": "gap_completion",
    "branch_resolution_followthrough": "multi_source_reasoning",
    "already_done_skip_followthrough": "duplicate_avoidance",
    "wrong_state_replacement_followthrough": "state_repair",
    "interrupted_workflow_resume": "gap_completion",
    "contradictory_source_resolution": "multi_source_reasoning",
}

_SCENARIO_ABILITY_TAGS = {
    "inbox_followthrough": ["information_transfer", "workflow_completion"],
    "release_recovery_runbook": ["workflow_completion", "schedule_inference"],
    "channel_incident_recovery": ["information_transfer", "workflow_completion"],
    "daily_ops_commitment_loop": ["workflow_completion", "schedule_inference"],
    "release_gate_followthrough": ["workflow_completion", "state_inspection"],
    "delivery_update_followthrough": ["information_transfer", "workflow_completion"],
    "ops_review_followthrough": ["workflow_completion", "schedule_inference"],
    "existing_state_followthrough": ["gap_completion", "state_inspection", "duplicate_avoidance", "workflow_completion"],
    "duplicate_avoidance_followthrough": ["duplicate_avoidance", "completion_recognition"],
    "multi_source_decision_followthrough": ["multi_source_reasoning", "branch_resolution", "workflow_completion"],
    "state_repair_followthrough": ["state_repair", "state_inspection", "workflow_completion"],
    "completion_gap_followthrough": ["gap_completion", "state_inspection", "workflow_completion"],
    "branch_resolution_followthrough": ["multi_source_reasoning", "branch_resolution", "duplicate_avoidance"],
    "already_done_skip_followthrough": ["duplicate_avoidance", "completion_recognition", "information_transfer"],
    "wrong_state_replacement_followthrough": ["state_repair", "replacement_planning", "workflow_completion"],
    "interrupted_workflow_resume": ["gap_completion", "state_inspection", "duplicate_avoidance", "workflow_completion"],
    "contradictory_source_resolution": ["multi_source_reasoning", "branch_resolution", "workflow_completion", "state_inspection"],
}


def _scenario_primary_ability(scenario_slug: str) -> str:
    return _SCENARIO_PRIMARY_ABILITIES[scenario_slug]


def _scenario_ability_tags(scenario_slug: str) -> list[str]:
    return list(_SCENARIO_ABILITY_TAGS[scenario_slug])


def _normalize_scenario_count_overrides(
    scenario_count_overrides: tuple[tuple[str, int], ...],
) -> dict[str, int]:
    overrides = dict(scenario_count_overrides)
    unknown = sorted(set(overrides) - set(_SCENARIO_ORDER))
    if unknown:
        raise ValueError(
            f"Unknown hard-decision scenario count override(s): {', '.join(unknown)}"
        )
    return overrides


def _scenario_target_count(
    scenario_slug: str,
    variants_per_scenario: int,
    scenario_count_overrides: dict[str, int],
) -> int:
    if not scenario_count_overrides and variants_per_scenario == 16:
        return _DEFAULT_HARD_SCENARIO_COUNTS[scenario_slug]
    return scenario_count_overrides.get(scenario_slug, variants_per_scenario)


@lru_cache(maxsize=16)
def _build_specs(
    variants_per_scenario: int,
    scenario_count_overrides: tuple[tuple[str, int], ...] = (),
) -> tuple[HardDecisionSpec, ...]:
    specs: list[HardDecisionSpec] = []
    seen: set[tuple[str, tuple[str, ...]]] = set()
    core_specs = _core_specs()
    for spec in core_specs:
        specs.append(spec)
        seen.add(_signature(spec))

    override_counts = _normalize_scenario_count_overrides(scenario_count_overrides)

    scenario_builders = {
        "inbox_followthrough": _build_inbox_spec,
        "release_recovery_runbook": _build_release_spec,
        "channel_incident_recovery": _build_incident_spec,
        "daily_ops_commitment_loop": _build_daily_ops_spec,
        "release_gate_followthrough": _build_release_gate_followthrough_spec,
        "delivery_update_followthrough": _build_delivery_update_followthrough_spec,
        "ops_review_followthrough": _build_ops_review_followthrough_spec,
        "existing_state_followthrough": _build_existing_state_followthrough_spec,
        "duplicate_avoidance_followthrough": _build_duplicate_avoidance_followthrough_spec,
        "multi_source_decision_followthrough": _build_multi_source_decision_followthrough_spec,
        "state_repair_followthrough": _build_state_repair_followthrough_spec,
        "completion_gap_followthrough": _build_completion_gap_followthrough_spec,
        "branch_resolution_followthrough": _build_branch_resolution_followthrough_spec,
        "already_done_skip_followthrough": _build_already_done_skip_followthrough_spec,
        "wrong_state_replacement_followthrough": _build_wrong_state_replacement_followthrough_spec,
        "interrupted_workflow_resume": _build_interrupted_workflow_resume_spec,
        "contradictory_source_resolution": _build_contradictory_source_resolution_spec,
    }
    for scenario_index, scenario_slug in enumerate(_SCENARIO_ORDER):
        scenario_target = _scenario_target_count(
            scenario_slug, variants_per_scenario, override_counts
        )
        core_count = 6 if scenario_slug in {
            "inbox_followthrough",
            "release_recovery_runbook",
            "channel_incident_recovery",
            "daily_ops_commitment_loop",
        } else 0
        if scenario_target < 6:
            core_count = min(core_count, scenario_target)
        extra_needed = max(0, scenario_target - core_count)
        if extra_needed == 0:
            continue
        candidates = _sample_candidate_contexts(scenario_slug, extra_needed * 8)
        builder = scenario_builders[scenario_slug]
        scenario_variant = 7 if core_count else 1
        for ctx in candidates:
            task_id = f"hard_decision_workflow_{len(specs) + 1}"
            if scenario_slug in {"daily_ops_commitment_loop", "ops_review_followthrough"}:
                ctx = {**ctx, "cron_name": f"hard-ops-{scenario_index + 1:02d}-{scenario_variant:02d}"}
            spec = builder(
                task_id=task_id,
                variant_id=scenario_variant,
                ctx=ctx,
                core=False,
            )
            sig = _signature(spec)
            if sig in seen:
                continue
            specs.append(spec)
            seen.add(sig)
            scenario_variant += 1
            if scenario_variant > scenario_target:
                break
        if scenario_variant <= scenario_target:
            raise RuntimeError(
                f"Unable to build enough unique {scenario_slug} variants for count={scenario_target}."
            )

    truncated: list[HardDecisionSpec] = []
    scenario_counts = {scenario_slug: 0 for scenario_slug in _SCENARIO_ORDER}
    for spec in specs:
        if scenario_counts[spec.scenario_slug] >= _scenario_target_count(
            spec.scenario_slug, variants_per_scenario, override_counts
        ):
            continue
        scenario_counts[spec.scenario_slug] += 1
        truncated.append(spec)
    specs = truncated

    return tuple(specs)


@BaseTaskGenerator.register("hard_decision_workflow")
class HardDecisionWorkflowGenerator(BaseTaskGenerator):
    """Decision-heavy, underspecified workflows with bounded valid outcomes."""

    required_domains = (
        "composite",
        "monitoring",
        "tasks",
        "calendar",
        "email",
        "weather",
        "setup_config",
        "plugin_skill",
        "channel_mgmt",
        "messaging",
        "security",
        "file",
    )
    difficulty = 3

    @property
    def parameters(self) -> dict[str, list[Any]]:  # type: ignore[override]
        specs = self._specs()
        return {"workflow_index": list(range(len(specs)))}

    def _specs(self) -> tuple[HardDecisionSpec, ...]:
        options = get_generation_options()
        scenario_count_overrides = tuple(sorted(options.hard_decision_scenario_counts.items()))
        return _build_specs(
            options.hard_decision_variants_per_scenario, scenario_count_overrides
        )

    def _spec(self, params: dict[str, Any]) -> HardDecisionSpec:
        return self._specs()[int(params["workflow_index"])]

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        del initial_config
        idx = int(params["workflow_index"])
        specs = self._specs()
        if idx >= len(specs):
            yield Fail("workflow index outside hard decision pack"), TaskData()
            return
        spec = specs[idx]
        yield Pass(), TaskData(
            public={
                "hard_decision_scenario": spec.scenario_slug,
                "hard_decision_variant": spec.variant_id,
                "hard_decision_ability": _scenario_primary_ability(spec.scenario_slug),
                "hard_decision_ability_tags": _scenario_ability_tags(spec.scenario_slug),
                "prompt_style": spec.prompt_style,
                "step_count": len(spec.commands),
            },
            private={"initial_state_overrides": spec.initial_state_overrides},
        )

    def build_task_id(
        self, params: dict[str, Any], data: TaskData, task_counter: int
    ) -> str:
        del data, task_counter
        return self._spec(params).task_id

    def get_initial_state(self, params: dict[str, Any]) -> str:
        return self._spec(params).initial_state

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
        online_requirement = (
            "required"
            if any(cmd.startswith("openclaw channels login") for cmd in solution)
            else "optional"
        )
        availability_tier = (
            "flaky"
            if spec.scenario_slug == "channel_incident_recovery"
            else "external-risk"
        )
        _, hidden_constraints = _split_constraints(
            instruction, _extract_constraints(solution)
        )
        if spec.scenario_slug in {"release_recovery_runbook", "release_gate_followthrough"}:
            decision_requirements = ["infer_schedule", "infer_title", "infer_model"]
        elif spec.scenario_slug in {"daily_ops_commitment_loop", "ops_review_followthrough"}:
            decision_requirements = ["infer_schedule", "infer_title"]
        elif spec.scenario_slug == "existing_state_followthrough":
            decision_requirements = ["infer_missing_steps", "avoid_duplicate", "infer_schedule", "infer_message"]
        elif spec.scenario_slug == "multi_source_decision_followthrough":
            decision_requirements = ["infer_schedule", "infer_branch", "infer_message"]
        elif spec.scenario_slug == "branch_resolution_followthrough":
            decision_requirements = ["infer_branch", "avoid_duplicate", "infer_schedule"]
        elif spec.scenario_slug == "delivery_update_followthrough":
            decision_requirements = ["infer_missing_steps", "avoid_duplicate", "infer_target", "infer_message"]
        elif spec.scenario_slug == "duplicate_avoidance_followthrough":
            decision_requirements = ["infer_missing_steps", "avoid_duplicate", "infer_branch", "infer_schedule"]
        elif spec.scenario_slug == "state_repair_followthrough":
            decision_requirements = ["infer_repair", "infer_schedule", "infer_model"]
        elif spec.scenario_slug == "completion_gap_followthrough":
            decision_requirements = ["infer_missing_steps", "avoid_duplicate", "infer_schedule", "infer_message"]
        elif spec.scenario_slug == "already_done_skip_followthrough":
            decision_requirements = ["infer_completion", "avoid_duplicate", "infer_message"]
        elif spec.scenario_slug == "wrong_state_replacement_followthrough":
            decision_requirements = ["infer_replacement", "avoid_duplicate", "infer_schedule"]
        elif spec.scenario_slug == "interrupted_workflow_resume":
            decision_requirements = ["infer_missing_steps", "avoid_duplicate", "infer_completion"]
        elif spec.scenario_slug == "contradictory_source_resolution":
            decision_requirements = ["infer_branch", "infer_schedule", "infer_message"]
        elif spec.scenario_slug == "inbox_followthrough":
            decision_requirements = ["infer_missing_steps", "avoid_duplicate", "infer_message"]
        elif spec.scenario_slug == "channel_incident_recovery":
            decision_requirements = ["infer_missing_steps", "avoid_duplicate", "infer_target", "infer_message"]
        else:
            decision_requirements = ["infer_schedule", "infer_title", "infer_message"]
        return {
            "canonical_instruction": spec.canonical_instruction or spec.instruction,
            "instruction_variants": list(spec.instruction_variants),
            "hidden_constraints": [
                item
                for item in hidden_constraints
                if str(item.get("type", "")) not in {"datetime", "cron", "timezone"}
            ],
            "decision_requirements": decision_requirements,
            "realism_tags": ["challenge", "hard_decision", "underspecified"],
            "online_requirement": online_requirement,
            "availability_tier": availability_tier,
        }
