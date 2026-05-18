"""Task generators for Tasks domain (D15)."""

from __future__ import annotations

from typing import Any, Iterator

from openclaw_env.core.task import TaskData
from openclaw_env.tasks.registry import BaseTaskGenerator, Pass, SetupResult

_TASK_TITLES = [
    "Write weekly report",
    "Review pull requests",
    "Update project documentation",
    "Prepare slide deck",
    "Schedule team retrospective",
]

_DUE_DATES = [
    "2026-03-05",
    "2026-03-08",
    "2026-03-10",
    "2026-03-15",
]

_PRIORITIES = ["high", "medium", "low"]

# Seeded task IDs (matches TasksBackend seeds)
_SEED_IDS = ["task_seed_1", "task_seed_2", "task_seed_3"]
_SEED_TITLES = [
    "Review project proposal",
    "Write quarterly report",
    "Schedule team standup",
]

_SEARCH_QUERIES = ["project", "quarterly", "standup", "report"]


@BaseTaskGenerator.register("tasks_add")
class AddTaskGenerator(BaseTaskGenerator):
    """Add a new task with a title."""

    required_domains = ("tasks",)
    difficulty = 1
    parameters = {
        "title": _TASK_TITLES,
        "due": _DUE_DATES[:3],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={"title": params["title"], "due": params["due"]},
            private={"expected_title": params["title"]},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"I've been meaning to track this — "
            f"add '{params['title']}' to my task list, due {params['due']}."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            f"tasks add --title '{params['title']}' --due {params['due']}",
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
        ]


@BaseTaskGenerator.register("tasks_add_with_priority")
class AddTaskWithPriorityGenerator(BaseTaskGenerator):
    """Add a task with priority and due date."""

    required_domains = ("tasks",)
    difficulty = 1
    parameters = {
        "title": _TASK_TITLES[:3],
        "priority": _PRIORITIES,
        "due": _DUE_DATES,
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "title": params["title"],
                "priority": params["priority"],
                "due": params["due"],
            },
            private={
                "expected_title": params["title"],
                "expected_priority": params["priority"],
            },
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"I need to stay on top of a {params['priority']}-priority item. "
            f"Add '{params['title']}' to my list, due {params['due']}."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            f"tasks add --title '{params['title']}' "
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
                "name": "task created with priority",
            },
        ]


@BaseTaskGenerator.register("tasks_complete")
class CompleteTaskGenerator(BaseTaskGenerator):
    """Mark a seeded task as complete."""

    required_domains = ("tasks",)
    difficulty = 2
    parameters = {
        "seed_id": _SEED_IDS,
        "seed_title": _SEED_TITLES,
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "task_id": params["seed_id"],
                "task_title": params["seed_title"],
            },
            private={"expected_completed_id": params["seed_id"]},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"I just finished the '{params['seed_title']}' task. "
            f"Find it in my task list and mark it as done."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            f"tasks complete --id {params['seed_id']}",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "effect",
                "effect_type": "tasks_completed",
                "condition": "count_gte",
                "expected": 1,
                "name": "task marked as done",
            },
        ]


@BaseTaskGenerator.register("tasks_search")
class SearchTasksGenerator(BaseTaskGenerator):
    """Search tasks by keyword."""

    required_domains = ("tasks",)
    difficulty = 1
    parameters = {
        "query": _SEARCH_QUERIES,
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={"query": params["query"]},
            private={},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"I'm looking for a specific task. "
            f"Search my list for anything related to '{params['query']}'."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            f"tasks search --query '{params['query']}'",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "output",
                "condition": "exit_code_zero",
                "expected": None,
                "name": "search succeeds",
            },
        ]


@BaseTaskGenerator.register("tasks_list_filtered")
class ListTasksFilteredGenerator(BaseTaskGenerator):
    """List tasks filtered by status and/or priority."""

    required_domains = ("tasks",)
    difficulty = 1
    parameters = {
        "status": ["pending", "all", "done"],
        "priority": _PRIORITIES,
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={"status": params["status"], "priority": params["priority"]},
            private={},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"Let me see what's on my plate. "
            f"Show me all {params['status']} tasks with {params['priority']} priority."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            f"tasks list --status {params['status']} --priority {params['priority']}",
        ]

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
