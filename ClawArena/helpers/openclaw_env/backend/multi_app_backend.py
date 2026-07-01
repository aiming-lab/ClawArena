"""MultiAppBackend — routes CLI commands to per-app sub-backends."""

from __future__ import annotations

from typing import Any

from openclaw_env.backend.base import BaseBackend, CommandResult
from openclaw_env.backend.mock_backend import MockBackend
from openclaw_env.backend.calendar_backend import CalendarBackend
from openclaw_env.backend.email_backend import EmailBackend
from openclaw_env.backend.weather_backend import WeatherBackend
from openclaw_env.backend.file_backend import FileSystemBackend
from openclaw_env.backend.tasks_backend import TasksBackend
from openclaw_env.backend.http_backend import HttpBackend
from openclaw_env.skills.adapters import (
    FileSkillAdapter,
    HttpSkillAdapter,
    OpenClawSkillAdapter,
)
from openclaw_env.skills.impl import CalendarSkill, EmailSkill, TasksSkill, WeatherSkill
from openclaw_env.skills.policies.openclaw_fallback import should_fallback_to_mock
from openclaw_env.skills.registry import SkillRegistry
from openclaw_env.skills.runtime import SkillRuntime


class MultiAppBackend(BaseBackend):
    """Routing backend that delegates command execution to skills.

    Command routing is based on the first token of the command:
        openclaw * → MockBackend (or RealOpenClawBackend when real_openclaw=True)
        calendar *  → CalendarBackend
        gcalcli *   → CalendarBackend
        email *     → EmailBackend
        weather *   → WeatherBackend
        file *      → FileSystemBackend
        tasks *     → TasksBackend
        curl *      → HttpBackend (real subprocess in real/hybrid, mock in multi)
    """

    def __init__(
        self,
        real_openclaw: bool = False,
        real_openclaw_kwargs: dict[str, Any] | None = None,
        fallback_openclaw_network_to_mock: bool = False,
        strict_online_data: bool = True,
    ) -> None:
        self._fallback_openclaw_network_to_mock = fallback_openclaw_network_to_mock
        self._openclaw_mock_fallback: MockBackend | None = None
        self._strict_online_data = strict_online_data

        if real_openclaw:
            from openclaw_env.backend.real_openclaw_backend import RealOpenClawBackend

            self._openclaw_backend = RealOpenClawBackend(**(real_openclaw_kwargs or {}))
            self._mock: MockBackend | None = None
            self._real: BaseBackend | None = self._openclaw_backend
            if self._fallback_openclaw_network_to_mock:
                self._openclaw_mock_fallback = MockBackend()
        else:
            self._openclaw_backend = MockBackend()
            self._mock = self._openclaw_backend  # type: ignore[assignment]
            self._real = None

        self._email_skill = EmailSkill()
        self._email = EmailBackend(self._email_skill)
        self._file = FileSystemBackend()
        self._tasks_skill = TasksSkill()
        self._tasks = TasksBackend(self._tasks_skill)
        self._http = HttpBackend(real_http=real_openclaw)

        self._skill_registry = SkillRegistry()
        self._openclaw_skill = OpenClawSkillAdapter(
            primary_backend=self._openclaw_backend,
            mock_fallback_backend=self._openclaw_mock_fallback,
            fallback_enabled=self._fallback_openclaw_network_to_mock,
        )
        self._calendar_skill = CalendarSkill()
        self._weather_skill = WeatherSkill()
        # Compatibility wrappers expose legacy backend objects while delegating
        # implementation to skills.
        self._calendar = CalendarBackend(self._calendar_skill)
        self._weather = WeatherBackend(self._weather_skill)

        # Legacy compatibility map: keep concrete backend instances reachable.
        self._router: dict[str, BaseBackend] = {
            "openclaw": self._openclaw_backend,
            "calendar": self._calendar,
            "gcalcli": self._calendar,
            "email": self._email,
            "weather": self._weather,
            "file": self._file,
            "tasks": self._tasks,
            "curl": self._http,
        }
        self._skill_registry.register_skill(self._openclaw_skill)
        self._skill_registry.register_skill(self._calendar_skill)
        self._skill_registry.register_skill(self._email_skill)
        self._skill_registry.register_skill(self._weather_skill)
        self._skill_registry.register_skill(FileSkillAdapter(self._file))
        self._skill_registry.register_skill(self._tasks_skill)
        self._skill_registry.register_skill(HttpSkillAdapter(self._http))
        self._runtime = SkillRuntime(self._skill_registry)

    # ------------------------------------------------------------------ #
    # BaseBackend interface                                                 #
    # ------------------------------------------------------------------ #

    def initialize(self, state_dir: str, env_vars: dict[str, str]) -> None:
        merged_env = dict(env_vars)
        if self._strict_online_data:
            merged_env["OPENCLAW_ENV_STRICT_ONLINE_DATA"] = "1"
        self._runtime.initialize(state_dir, merged_env)

    def execute_cli(self, command: str) -> CommandResult:
        return self._runtime.execute_cli(command)

    def execute_python(self, code: str) -> CommandResult:
        # Delegate Python execution to the openclaw backend only.
        return self._openclaw_backend.execute_python(code)

    def get_gateway_status(self) -> dict[str, Any] | None:
        return self._openclaw_backend.get_gateway_status()

    def get_config(self) -> dict[str, Any]:
        return self._openclaw_backend.get_config()

    def cleanup(self) -> None:
        self._runtime.cleanup()

    # ------------------------------------------------------------------ #
    # Multi-app state access                                               #
    # ------------------------------------------------------------------ #

    def get_state(self) -> dict[str, Any]:
        """Merge state from all registered skills into one dict."""
        return self._runtime.get_state()

    # Legacy compatibility accessors for existing tests/callers.
    @property
    def calendar_backend(self) -> CalendarBackend:
        return self._calendar

    @property
    def email_backend(self) -> EmailBackend:
        return self._email

    @property
    def file_backend(self) -> FileSystemBackend:
        return self._file

    @property
    def tasks_backend(self) -> TasksBackend:
        return self._tasks

    @property
    def mock_backend(self) -> MockBackend | None:
        return self._mock

    @property
    def real_backend(self) -> BaseBackend | None:
        return self._real

    def _should_fallback_to_mock(self, command: str, result: CommandResult) -> bool:
        """Compatibility wrapper: fallback policy moved to skills layer."""
        return should_fallback_to_mock(
            enabled=self._fallback_openclaw_network_to_mock,
            command=command,
            result=result,
        )
