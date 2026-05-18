"""Skill registry for command-prefix routing."""

from __future__ import annotations

from openclaw_env.skills.base import Skill


class SkillRegistry:
    """Register and resolve skills by command prefix."""

    def __init__(self) -> None:
        self._prefix_to_skill: dict[str, Skill] = {}
        self._skills: list[Skill] = []

    def register(self, prefix: str, skill: Skill) -> None:
        if not prefix:
            raise ValueError("Prefix cannot be empty")
        existing = self._prefix_to_skill.get(prefix)
        if existing is not None and existing is not skill:
            raise ValueError(
                f"Prefix '{prefix}' already registered by {existing.__class__.__name__}"
            )
        self._prefix_to_skill[prefix] = skill
        if skill not in self._skills:
            self._skills.append(skill)

    def register_skill(self, skill: Skill) -> None:
        for prefix in skill.prefixes:
            self.register(prefix, skill)

    def resolve(self, prefix: str) -> Skill | None:
        return self._prefix_to_skill.get(prefix)

    def list_prefixes(self) -> list[str]:
        return sorted(self._prefix_to_skill)

    def iter_skills(self) -> list[Skill]:
        return list(self._skills)
