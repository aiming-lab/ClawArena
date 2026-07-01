"""Task generators for Calendar domain (D11)."""

from __future__ import annotations

from typing import Any, Iterator

from openclaw_env.core.task import TaskData
from openclaw_env.tasks.generation_options import get_generation_options
from openclaw_env.tasks.registry import BaseTaskGenerator, Pass, SetupResult

_TITLES = [
    "Team standup",
    "Product review",
    "1-on-1 with manager",
    "Design brainstorm",
    "Sprint planning",
]

_TIMES = [
    "2026-03-10T09:00",
    "2026-03-11T14:00",
    "2026-03-12T11:00",
]

_LOCATIONS = ["Conference Room A", "Zoom", "Office", "Google Meet"]

_ATTENDEE_LISTS = [
    "alice@example.com,bob@example.com",
    "carol@example.com,dave@example.com,eve@example.com",
    "team@example.com",
    "manager@example.com,alice@example.com",
]
_TIMEZONES = ["UTC", "America/New_York", "Asia/Shanghai"]


def _is_universal_profile() -> bool:
    return get_generation_options().command_profile == "universal"


def _calendar_add_command(
    title: str,
    start: str,
    location: str | None = None,
    attendees: str | None = None,
) -> str:
    if _is_universal_profile():
        cmd = f"gcalcli add --title '{title}' --when {start}"
        if location:
            cmd += f" --where '{location}'"
        if attendees:
            cmd += f" --who {attendees}"
        return cmd

    cmd = f"calendar add-event --title '{title}' --start {start}"
    if location:
        cmd += f" --location '{location}'"
    if attendees:
        cmd += f" --attendees {attendees}"
    return cmd


def _calendar_list_command(from_date: str, to_date: str) -> str:
    if _is_universal_profile():
        return f"gcalcli agenda {from_date} {to_date}"
    return f"calendar list --from {from_date} --to {to_date}"


def _calendar_update_command(event_id: str, new_start: str) -> str:
    if _is_universal_profile():
        return f"gcalcli edit --id {event_id} --when {new_start}"
    return f"calendar update-event --id {event_id} --start {new_start}"


def _calendar_today_online_command(timezone: str) -> str:
    if _is_universal_profile():
        return f"gcalcli now --timezone {timezone}"
    return f"calendar today --timezone {timezone}"


@BaseTaskGenerator.register("calendar_add_event")
class AddCalendarEventGenerator(BaseTaskGenerator):
    """Add a calendar event with title and start time."""

    required_domains = ("calendar",)
    difficulty = 1
    parameters = {
        "title": _TITLES,
        "start": _TIMES,
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={"title": params["title"], "start": params["start"]},
            private={"expected_title": params["title"], "expected_start": params["start"]},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"I'd like to block some time on my calendar. "
            f"Please add an event titled '{params['title']}' starting at {params['start']}."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [_calendar_add_command(params["title"], params["start"])]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "effect",
                "effect_type": "calendar_events_created",
                "condition": "count_gte",
                "expected": 1,
                "name": "calendar event created",
            },
        ]

    def get_initial_state(self, params: dict[str, Any]) -> str:
        return "default"


@BaseTaskGenerator.register("calendar_list_events")
class ListCalendarEventsGenerator(BaseTaskGenerator):
    """List calendar events for a date range."""

    required_domains = ("calendar",)
    difficulty = 1
    parameters = {
        "from_date": ["2026-03-01", "2026-03-10", "2026-03-15"],
        "to_date": ["2026-03-07", "2026-03-14", "2026-03-31"],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        # Only yield when from <= to
        if params["from_date"] > params["to_date"]:
            return
        data = TaskData(
            public={"from_date": params["from_date"], "to_date": params["to_date"]},
            private={},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"I want to review my schedule. "
            f"Show me all calendar events between {params['from_date']} and {params['to_date']}."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [_calendar_list_command(params["from_date"], params["to_date"])]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "output",
                "condition": "exit_code_zero",
                "expected": None,
                "name": "list command succeeds",
            },
        ]


@BaseTaskGenerator.register("calendar_reschedule_event")
class RescheduleEventGenerator(BaseTaskGenerator):
    """Reschedule an existing seeded event to a new time."""

    required_domains = ("calendar",)
    difficulty = 2
    parameters = {
        "original_title": ["Team standup", "Design brainstorm"],
        "original_start": ["2026-03-10T09:00", "2026-03-11T14:00"],
        "new_start": ["2026-03-13T10:00", "2026-03-14T15:00"],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "title": params["original_title"],
                "original_start": params["original_start"],
                "new_start": params["new_start"],
            },
            private={"expected_new_start": params["new_start"]},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"Plans changed - I need to move '{params['original_title']}'. "
            f"First add it at {params['original_start']}, then update it to {params['new_start']}."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        if _is_universal_profile():
            list_cmd = "gcalcli agenda"
        else:
            list_cmd = "calendar list"
        return [
            _calendar_add_command(params["original_title"], params["original_start"]),
            list_cmd,
            _calendar_update_command("evt_0001", params["new_start"]),
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
                "name": "event created",
            },
        ]


@BaseTaskGenerator.register("calendar_add_event_with_attendees")
class AddEventWithAttendeesGenerator(BaseTaskGenerator):
    """Add a calendar event with location and attendees."""

    required_domains = ("calendar",)
    difficulty = 2
    parameters = {
        "title": ["Quarterly review", "All-hands meeting", "Workshop", "Retrospective"],
        "start": ["2026-03-15T10:00", "2026-03-16T14:00"],
        "location": _LOCATIONS[:2],
        "attendees": _ATTENDEE_LISTS[:2],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "title": params["title"],
                "start": params["start"],
                "location": params["location"],
                "attendees": params["attendees"],
            },
            private={
                "expected_title": params["title"],
                "expected_attendees": params["attendees"].split(","),
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"I'm organizing a group event. Set up '{params['title']}' on the calendar "
            f"at {params['start']} in {params['location']}, and invite {params['attendees']}."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            _calendar_add_command(
                params["title"],
                params["start"],
                location=params["location"],
                attendees=params["attendees"],
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
                "name": "event with attendees created",
            },
        ]


@BaseTaskGenerator.register("calendar_today_online")
class CalendarTodayOnlineGenerator(BaseTaskGenerator):
    """Get current date-time with online option."""

    required_domains = ("calendar",)
    difficulty = 1
    parameters = {
        "timezone": _TIMEZONES,
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(public={"timezone": params["timezone"]}, private={})
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"I need the current date and time in {params['timezone']} right now. "
            "Please look it up and report it."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [_calendar_today_online_command(params["timezone"])]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "output",
                "condition": "exit_code_zero",
                "expected": None,
                "name": "calendar today online succeeds",
            },
            {
                "type": "output",
                "condition": "contains",
                "expected": f"Current date-time for {params['timezone']}:",
                "name": "output contains requested timezone",
            },
            {
                "type": "output",
                "condition": "contains",
                "expected": "Source:",
                "name": "output includes data source",
            },
        ]
