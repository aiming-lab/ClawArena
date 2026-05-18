"""Task generators for Email domain (D12)."""

from __future__ import annotations

from typing import Any, Iterator

from openclaw_env.core.task import TaskData
from openclaw_env.tasks.registry import BaseTaskGenerator, Pass, SetupResult

_RECIPIENTS = [
    "alice@example.com",
    "bob@example.com",
    "carol@example.com",
    "team@example.com",
    "manager@example.com",
]

_SUBJECTS = [
    "Project update",
    "Meeting request",
    "Action items",
    "Follow-up",
    "Quick question",
]

_BODIES = [
    "Hi, just wanted to give you a quick update on the project.",
    "Can we schedule a meeting for next week?",
    "Please review the attached action items.",
    "Following up on our previous conversation.",
    "I have a quick question about the roadmap.",
]

_FOLDERS = ["archive", "work", "personal", "important"]

# Seeded email IDs (matches EmailBackend seeds)
_SEED_IDS = ["email_seed_1", "email_seed_2", "email_seed_3", "email_seed_4", "email_seed_5"]
_SEED_SUBJECTS = [
    "Project proposal",
    "Meeting notes",
    "Budget report",
    "Follow-up on hackathon",
    "Quarterly review",
]
_SEED_SENDERS = [
    "alice@example.com",
    "bob@example.com",
    "carol@example.com",
    "dave@example.com",
    "eve@example.com",
]
_SEED_BODIES = [
    "Hi, I wanted to share the project proposal for Q2. Please review.",
    "Attached are the notes from today's standup meeting.",
    "Please find the budget report for this quarter attached.",
    "Just following up on the hackathon registration. Did you sign up?",
    "The quarterly review is scheduled for next Friday at 2pm.",
]

# Maps seed ID → (subject, sender) for natural-language instructions
_SEED_META: dict[str, tuple[str, str]] = dict(
    zip(_SEED_IDS, zip(_SEED_SUBJECTS, _SEED_SENDERS))
)
_QUERY_TO_SEED = {
    "proposal": ("email_seed_1", "Project proposal", "project proposal for Q2"),
    "meeting": ("email_seed_2", "Meeting notes", "notes from today's standup"),
    "budget": ("email_seed_3", "Budget report", "budget report for this quarter"),
    "hackathon": ("email_seed_4", "Follow-up on hackathon", "hackathon registration"),
    "review": ("email_seed_5", "Quarterly review", "quarterly review is scheduled"),
}


@BaseTaskGenerator.register("email_send")
class SendEmailGenerator(BaseTaskGenerator):
    """Send an email to a recipient."""

    required_domains = ("email",)
    difficulty = 1
    parameters = {
        "recipient": _RECIPIENTS,
        "subject": _SUBJECTS[:3],
        "body": _BODIES[:3],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "recipient": params["recipient"],
                "subject": params["subject"],
                "body": params["body"],
            },
            private={
                "expected_to": params["recipient"],
                "expected_subject": params["subject"],
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"Draft and send an email to {params['recipient']} — "
            f"subject: '{params['subject']}', body: '{params['body']}'."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            f"email send --to {params['recipient']} "
            f"--subject '{params['subject']}' "
            f"--body '{params['body']}'",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "effect",
                "effect_type": "emails_sent",
                "condition": "count_gte",
                "expected": 1,
                "name": "email sent",
            },
            {
                "type": "effect",
                "effect_type": "emails_sent",
                "condition": "field_equals",
                "expected": {"field": "to", "value": params["recipient"]},
                "name": f"email sent to {params['recipient']}",
            },
        ]


@BaseTaskGenerator.register("email_search_and_read")
class SearchAndReadEmailGenerator(BaseTaskGenerator):
    """Search for an email by keyword and read the matching message."""

    required_domains = ("email",)
    difficulty = 1
    parameters = {
        "query": ["proposal", "meeting", "budget", "hackathon", "review"],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        seed_id, subject, body_snippet = _QUERY_TO_SEED[params["query"]]
        data = TaskData(
            public={"query": params["query"], "seed_id": seed_id},
            private={
                "expected_query": params["query"],
                "expected_seed_id": seed_id,
                "expected_subject": subject,
                "expected_body_snippet": body_snippet,
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"I'm trying to find something in my inbox. "
            f"Search for emails mentioning '{params['query']}' and read the matching email."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        seed_id = data.private["expected_seed_id"]
        return [
            f"email search --query '{params['query']}'",
            f"email read --id {seed_id}",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "output",
                "condition": "exit_code_zero",
                "expected": None,
                "name": "read command succeeds",
            },
            {
                "type": "output",
                "condition": "contains",
                "expected": data.private["expected_subject"],
                "output_field": "last_stdout",
                "name": "read output includes expected subject",
            },
            {
                "type": "output",
                "condition": "contains",
                "expected": data.private["expected_body_snippet"],
                "output_field": "last_stdout",
                "name": "read output includes expected body",
            },
        ]


@BaseTaskGenerator.register("email_reply")
class ReplyToEmailGenerator(BaseTaskGenerator):
    """Reply to a seeded email."""

    required_domains = ("email",)
    difficulty = 2
    parameters = {
        "seed_id": _SEED_IDS[:3],
        "seed_subject": _SEED_SUBJECTS[:3],
        "reply_body": [
            "Thanks for reaching out! I will review and get back to you.",
            "Understood, I will take care of this.",
            "Great, let me follow up on this shortly.",
        ],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "email_id": params["seed_id"],
                "subject": params["seed_subject"],
                "reply_body": params["reply_body"],
            },
            private={
                "expected_in_reply_to": params["seed_id"],
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"I need to respond to an email about '{params['seed_subject']}'. "
            f"Find it in my inbox and send this reply: '{params['reply_body']}'."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            f"email reply --id {params['seed_id']} --body '{params['reply_body']}'",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "effect",
                "effect_type": "emails_sent",
                "condition": "count_gte",
                "expected": 1,
                "name": "reply sent",
            },
        ]


@BaseTaskGenerator.register("email_move")
class MoveEmailGenerator(BaseTaskGenerator):
    """Move a seeded email to a different folder."""

    required_domains = ("email",)
    difficulty = 2
    parameters = {
        "seed_id": _SEED_IDS,
        "target_folder": _FOLDERS,
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "email_id": params["seed_id"],
                "folder": params["target_folder"],
            },
            private={
                "expected_email_id": params["seed_id"],
                "expected_folder": params["target_folder"],
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        subject, sender = _SEED_META[params["seed_id"]]
        return (
            f"I've processed the '{subject}' email from {sender}. "
            f"Move it to the '{params['target_folder']}' folder."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            f"email move --id {params['seed_id']} --folder {params['target_folder']}",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "effect",
                "effect_type": "emails_moved",
                "condition": "field_equals",
                "expected": {"field": "folder", "value": params["target_folder"]},
                "name": f"email moved to {params['target_folder']}",
            },
        ]


@BaseTaskGenerator.register("email_mark_read")
class MarkEmailsReadGenerator(BaseTaskGenerator):
    """Mark a seeded email as read."""

    required_domains = ("email",)
    difficulty = 1
    parameters = {
        "seed_id": _SEED_IDS[:3],
        "flag": ["read", "starred"],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={"email_id": params["seed_id"], "flag": params["flag"]},
            private={},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        subject, _ = _SEED_META[params["seed_id"]]
        return (
            f"I've already seen the '{subject}' email. "
            f"Mark it as {params['flag']}."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            f"email mark --id {params['seed_id']} --flag {params['flag']}",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "output",
                "condition": "exit_code_zero",
                "expected": None,
                "name": f"mark as {params['flag']} succeeds",
            },
        ]
