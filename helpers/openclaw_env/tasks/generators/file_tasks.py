"""Task generators for File system domain (D14)."""

from __future__ import annotations

from typing import Any, Iterator

from openclaw_env.core.task import TaskData
from openclaw_env.tasks.registry import BaseTaskGenerator, Pass, SetupResult

_PATHS = [
    "/notes/todo.txt",
    "/docs/readme.md",
    "/config/settings.json",
    "/reports/q1_summary.txt",
    "/workspace/scratch.py",
]

_CONTENTS = [
    "Hello, world!",
    "# My Notes\n- item 1\n- item 2",
    '{"key": "value", "enabled": true}',
    "Q1 Summary\nRevenue: +15%\nCosts: -5%",
    "# placeholder script\nprint('hello')",
]

_DST_PATHS = [
    "/archive/todo.txt",
    "/backup/readme.md",
    "/config/settings.bak.json",
    "/archive/q1_summary.txt",
    "/old/scratch.py",
]


@BaseTaskGenerator.register("file_create")
class CreateFileGenerator(BaseTaskGenerator):
    """Create a virtual file with content."""

    required_domains = ("file",)
    difficulty = 1
    parameters = {
        "path": _PATHS,
        "content": _CONTENTS,
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={"path": params["path"], "content": params["content"]},
            private={"expected_path": params["path"]},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"I need to save some data. "
            f"Create a file at '{params['path']}' and write this content: '{params['content']}'."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            f"file create --path '{params['path']}' --content '{params['content']}'",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "effect",
                "effect_type": "files_created",
                "condition": "count_gte",
                "expected": 1,
                "name": "file created",
            },
        ]


@BaseTaskGenerator.register("file_create_and_read")
class CreateAndReadFileGenerator(BaseTaskGenerator):
    """Create a file then verify its content by reading it."""

    required_domains = ("file",)
    difficulty = 2
    parameters = {
        "path": _PATHS[:3],
        "content": _CONTENTS[:3],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={"path": params["path"], "content": params["content"]},
            private={"expected_content": params["content"]},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"Please create a file at '{params['path']}' with content '{params['content']}', "
            f"then read it back to confirm it saved correctly."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            f"file create --path '{params['path']}' --content '{params['content']}'",
            f"file read --path '{params['path']}'",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "effect",
                "effect_type": "files_created",
                "condition": "count_gte",
                "expected": 1,
                "name": "file created",
            },
            {
                "type": "output",
                "condition": "contains",
                "expected": params["content"][:20],
                "name": "file content readable",
            },
        ]


@BaseTaskGenerator.register("file_move")
class MoveFileGenerator(BaseTaskGenerator):
    """Create a file and then move it to a new path."""

    required_domains = ("file",)
    difficulty = 2
    parameters = {
        "src": _PATHS[:4],
        "dst": _DST_PATHS[:4],
        "content": _CONTENTS[:2],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "src": params["src"],
                "dst": params["dst"],
                "content": params["content"],
            },
            private={"expected_dst": params["dst"]},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"I want to reorganize some files. "
            f"Create a file at '{params['src']}' with content '{params['content']}', "
            f"then move it to '{params['dst']}'."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            f"file create --path '{params['src']}' --content '{params['content']}'",
            f"file move --src '{params['src']}' --dst '{params['dst']}'",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "effect",
                "effect_type": "files_created",
                "condition": "count_gte",
                "expected": 1,
                "name": "file initially created",
            },
        ]


@BaseTaskGenerator.register("file_append")
class AppendToFileGenerator(BaseTaskGenerator):
    """Create a file then append additional content."""

    required_domains = ("file",)
    difficulty = 2
    parameters = {
        "path": _PATHS[:3],
        "initial_content": ["Line 1\n", "# Header\n", "Start of file\n"],
        "append_content": ["\nLine 2", "\n## Section 2", "\nMore content here"],
    }

    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        data = TaskData(
            public={
                "path": params["path"],
                "initial_content": params["initial_content"],
                "append_content": params["append_content"],
            },
            private={},
        )
        yield Pass(), data

    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        return (
            f"I'm adding to an existing note. "
            f"Create '{params['path']}' with '{params['initial_content']}', "
            f"then append '{params['append_content']}' to it."
        )

    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        return [
            f"file create --path '{params['path']}' --content '{params['initial_content']}'",
            f"file append --path '{params['path']}' --content '{params['append_content']}'",
        ]

    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        return [
            {
                "type": "effect",
                "effect_type": "files_created",
                "condition": "count_gte",
                "expected": 1,
                "name": "file created",
            },
        ]
