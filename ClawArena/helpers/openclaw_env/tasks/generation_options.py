"""Runtime options for task generation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class GenerationOptions:
    """Task-generation toggles controlled by the generation script."""

    message_dry_run: bool = False
    plugin_install_mode: Literal["stable", "mixed"] = "mixed"
    command_profile: Literal["local_skill"] = "local_skill"
    complex_task_pack: Literal["off", "standard"] = "standard"
    complex_scenario_profile: Literal["legacy", "life_work"] = "life_work"
    complex_min_steps: int = 3
    complex_max_steps: int = 5
    hard_decision_variants_per_scenario: int = 16
    hard_decision_scenario_counts: dict[str, int] = field(default_factory=dict)
    include_branch_sensitive: bool = False
    branch_sensitive_variants_per_scenario: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "message_dry_run": self.message_dry_run,
            "plugin_install_mode": self.plugin_install_mode,
            "command_profile": self.command_profile,
            "complex_task_pack": self.complex_task_pack,
            "complex_scenario_profile": self.complex_scenario_profile,
            "complex_min_steps": self.complex_min_steps,
            "complex_max_steps": self.complex_max_steps,
            "hard_decision_variants_per_scenario": self.hard_decision_variants_per_scenario,
            "hard_decision_scenario_counts": dict(sorted(self.hard_decision_scenario_counts.items())),
            "include_branch_sensitive": self.include_branch_sensitive,
            "branch_sensitive_variants_per_scenario": self.branch_sensitive_variants_per_scenario,
        }


_OPTIONS = GenerationOptions()


def set_generation_options(
    *,
    message_dry_run: bool = False,
    plugin_install_mode: Literal["stable", "mixed"] = "mixed",
    command_profile: str = "local_skill",
    complex_task_pack: str = "standard",
    complex_scenario_profile: str = "life_work",
    complex_min_steps: int = 3,
    complex_max_steps: int = 5,
    hard_decision_variants_per_scenario: int = 16,
    hard_decision_scenario_counts: dict[str, int] | None = None,
    include_branch_sensitive: bool = False,
    branch_sensitive_variants_per_scenario: int = 0,
) -> None:
    """Set global options used by generators in this process."""
    if plugin_install_mode not in {"stable", "mixed"}:
        raise ValueError(
            f"Invalid plugin_install_mode: {plugin_install_mode}. "
            "Expected one of: stable, mixed."
        )
    if command_profile != "local_skill":
        raise ValueError(
            f"Invalid command_profile: {command_profile}. "
            "Only 'local_skill' is supported."
        )
    if complex_task_pack not in {"off", "standard"}:
        raise ValueError(
            f"Invalid complex_task_pack: {complex_task_pack}. "
            "Expected one of: off, standard."
        )
    if complex_scenario_profile not in {"legacy", "life_work"}:
        raise ValueError(
            f"Invalid complex_scenario_profile: {complex_scenario_profile}. "
            "Expected one of: legacy, life_work."
        )
    if complex_min_steps < 1:
        raise ValueError("complex_min_steps must be >= 1.")
    if complex_max_steps < complex_min_steps:
        raise ValueError("complex_max_steps must be >= complex_min_steps.")
    if complex_max_steps > 5:
        raise ValueError("complex_max_steps must be <= 5 in v1.")
    if hard_decision_variants_per_scenario < 1:
        raise ValueError("hard_decision_variants_per_scenario must be >= 1.")
    scenario_counts = dict(hard_decision_scenario_counts or {})
    for scenario_slug, count in scenario_counts.items():
        if not isinstance(scenario_slug, str) or not scenario_slug:
            raise ValueError("hard_decision_scenario_counts keys must be non-empty strings.")
        if count < 1:
            raise ValueError("hard_decision_scenario_counts values must be >= 1.")
    if branch_sensitive_variants_per_scenario < 0:
        raise ValueError("branch_sensitive_variants_per_scenario must be >= 0.")
    if include_branch_sensitive and branch_sensitive_variants_per_scenario < 1:
        raise ValueError(
            "branch_sensitive_variants_per_scenario must be >= 1 when include_branch_sensitive is enabled."
        )
    global _OPTIONS
    _OPTIONS = GenerationOptions(
        message_dry_run=message_dry_run,
        plugin_install_mode=plugin_install_mode,
        command_profile=command_profile,
        complex_task_pack=complex_task_pack,
        complex_scenario_profile=complex_scenario_profile,
        complex_min_steps=complex_min_steps,
        complex_max_steps=complex_max_steps,
        hard_decision_variants_per_scenario=hard_decision_variants_per_scenario,
        hard_decision_scenario_counts=scenario_counts,
        include_branch_sensitive=include_branch_sensitive,
        branch_sensitive_variants_per_scenario=branch_sensitive_variants_per_scenario,
    )


def get_generation_options() -> GenerationOptions:
    """Read current generation options."""
    return _OPTIONS
