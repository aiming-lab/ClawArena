"""Skill adapters mapping prefixes to existing backend implementations."""

from openclaw_env.skills.adapters.calendar import CalendarSkillAdapter
from openclaw_env.skills.adapters.email import EmailSkillAdapter
from openclaw_env.skills.adapters.file import FileSkillAdapter
from openclaw_env.skills.adapters.http import HttpSkillAdapter
from openclaw_env.skills.adapters.openclaw import OpenClawSkillAdapter
from openclaw_env.skills.adapters.tasks import TasksSkillAdapter
from openclaw_env.skills.adapters.weather import WeatherSkillAdapter

__all__ = [
    "OpenClawSkillAdapter",
    "CalendarSkillAdapter",
    "EmailSkillAdapter",
    "WeatherSkillAdapter",
    "FileSkillAdapter",
    "TasksSkillAdapter",
    "HttpSkillAdapter",
]
