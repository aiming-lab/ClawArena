"""Concrete built-in skills."""

from openclaw_env.skills.impl.calendar_skill import CalendarSkill
from openclaw_env.skills.impl.email_skill import EmailSkill
from openclaw_env.skills.impl.tasks_skill import TasksSkill
from openclaw_env.skills.impl.weather_skill import WeatherSkill

__all__ = ["CalendarSkill", "EmailSkill", "TasksSkill", "WeatherSkill"]
