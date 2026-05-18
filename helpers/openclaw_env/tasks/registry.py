"""Task generator registry and base class."""

from __future__ import annotations

import itertools
import re
import uuid
from abc import ABC, abstractmethod
from typing import Any, Iterator

from openclaw_env.core.task import GroundTruth, Task, TaskData
from openclaw_env.tasks.generation_options import get_generation_options


class SetupResult:
    """Result of a task generator setup step."""

    def __init__(self, success: bool = True, reason: str = "") -> None:
        self.success = success
        self.reason = reason


class Pass(SetupResult):
    """Successful setup result."""

    def __init__(self) -> None:
        super().__init__(success=True)


class Fail(SetupResult):
    """Failed setup result."""

    def __init__(self, reason: str = "") -> None:
        super().__init__(success=False, reason=reason)


# Global registry of generators
_GENERATOR_REGISTRY: dict[str, type[BaseTaskGenerator]] = {}
_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_DATE_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2})?\b")
_CLI_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("location", re.compile(r"--location '([^']+)'")),
    ("timezone", re.compile(r"--timezone ([^\s]+)")),
    ("channel", re.compile(r"--channel ([^\s]+)")),
    ("target", re.compile(r"--target ([^\s]+)")),
    ("cron", re.compile(r"--cron '([^']+)'")),
    ("query", re.compile(r"--query '([^']+)'")),
    ("path", re.compile(r"--path '([^']+)'")),
    ("title", re.compile(r"--title '([^']+)'")),
    ("subject", re.compile(r"--subject '([^']+)'")),
    ("body", re.compile(r"--body '([^']+)'")),
    ("priority", re.compile(r"--priority ([^\s]+)")),
    ("model", re.compile(r"--model ([^\s]+)")),
)
_MODEL_SET_RE = re.compile(r"openclaw models set ([^\s]+)")
_VOLATILE_DOMAINS = {"messaging", "channel_mgmt", "plugin_skill"}


def _append_candidate(
    out: list[dict[str, Any]],
    seen: set[tuple[str, str]],
    slot_type: str,
    value: str,
) -> None:
    normalized = value.strip().strip("'\"")
    if not normalized:
        return
    key = (slot_type, normalized.lower())
    if key in seen:
        return
    seen.add(key)
    out.append({"type": slot_type, "value": normalized})


def _extract_constraints(commands: list[str]) -> list[dict[str, Any]]:
    joined = "\n".join(commands)
    out: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    for email in _EMAIL_RE.findall(joined):
        _append_candidate(out, seen, "email", email)
    for dt in _DATE_RE.findall(joined):
        _append_candidate(out, seen, "datetime", dt)
    for slot_type, pattern in _CLI_PATTERNS:
        for match in pattern.findall(joined):
            _append_candidate(out, seen, slot_type, match)
    for model in _MODEL_SET_RE.findall(joined):
        _append_candidate(out, seen, "model", model)
    return out


def _split_constraints(
    instruction: str, constraints: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    instruction_lc = instruction.lower()
    visible: list[dict[str, Any]] = []
    hidden: list[dict[str, Any]] = []
    for item in constraints:
        value = str(item.get("value", "")).lower()
        if value and value in instruction_lc:
            visible.append(item)
        else:
            hidden.append(item)
    return visible, hidden


def _derive_decision_requirements(
    hidden_constraints: list[dict[str, Any]],
) -> list[str]:
    reqs: list[str] = []
    hidden_types = {str(item.get("type", "")) for item in hidden_constraints}
    mapping = (
        ("infer_priority", {"priority"}),
        ("infer_title", {"title"}),
        ("infer_schedule", {"datetime", "timezone", "cron"}),
        ("infer_target", {"target", "channel", "email"}),
        ("infer_message", {"subject", "body"}),
        ("infer_model", {"model"}),
    )
    for name, slot_types in mapping:
        if hidden_types & slot_types:
            reqs.append(name)
    return reqs


def _derive_provider_dependencies(commands: list[str]) -> list[str]:
    deps: list[str] = []
    joined = "\n".join(commands)
    if any(cmd.startswith("calendar ") for cmd in commands):
        deps.append("google_calendar")
    if any(cmd.startswith("email ") for cmd in commands):
        deps.append("email_provider")
    if any(cmd.startswith("tasks ") for cmd in commands):
        deps.append("google_tasks")
    if any(cmd.startswith("weather ") for cmd in commands):
        deps.append("weather_provider")
    if "--channel " in joined or any(cmd.startswith("openclaw message ") for cmd in commands):
        deps.append("channel_provider")
    return deps


def _derive_online_requirement(
    provider_dependencies: list[str],
    commands: list[str],
) -> str:
    if not provider_dependencies:
        return "none"
    if any("--online" in cmd for cmd in commands):
        return "required"
    return "optional"


def _derive_availability_tier(provider_dependencies: list[str]) -> str:
    if not provider_dependencies:
        return "stable"
    if "channel_provider" in provider_dependencies:
        return "flaky"
    return "external-risk"


def _merge_unique_strings(*groups: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for group in groups:
        for item in group:
            normalized = str(item).strip()
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            out.append(normalized)
    return out


class BaseTaskGenerator(ABC):
    """Base class for task generators.

    Subclasses define:
    - required_domains: which domains this generator covers
    - difficulty: task difficulty level (1-3)
    - parameters: dict of parameter lists for combinatorial expansion
    - setup(): yields task variations
    - solution(): provides expert solution commands
    - evaluation_checks(): provides evaluation specifications
    """

    required_domains: tuple[str, ...] = ()
    difficulty: int = 1
    parameters: dict[str, list[Any]] = {}

    @classmethod
    def register(cls, generator_id: str):
        """Decorator to register a generator class."""
        def decorator(subcls: type[BaseTaskGenerator]):
            subcls._generator_id = generator_id
            _GENERATOR_REGISTRY[generator_id] = subcls
            return subcls
        return decorator

    @property
    def generator_id(self) -> str:
        return getattr(self, "_generator_id", self.__class__.__name__)

    @abstractmethod
    def setup(
        self, params: dict[str, Any], initial_config: dict[str, Any]
    ) -> Iterator[tuple[SetupResult, TaskData]]:
        """Generate task variations.

        Args:
            params: A specific parameter combination from self.parameters
            initial_config: The base configuration state

        Yields:
            (SetupResult, TaskData) pairs for each task variation
        """

    @abstractmethod
    def get_instruction(self, params: dict[str, Any], data: TaskData) -> str:
        """Generate the natural language instruction for the agent."""

    @abstractmethod
    def get_solution(self, params: dict[str, Any], data: TaskData) -> list[str]:
        """Provide the expert solution as a list of CLI commands."""

    @abstractmethod
    def get_evaluation_checks(
        self, params: dict[str, Any], data: TaskData
    ) -> list[dict[str, Any]]:
        """Provide evaluation check specifications."""

    def get_initial_state(self, params: dict[str, Any]) -> str:
        """Return the name of the base config to use. Override for custom states."""
        return "default"

    def build_task_id(
        self, params: dict[str, Any], data: TaskData, task_counter: int
    ) -> str:
        """Build task_id for a generated task.

        Override in specific generators when task IDs need custom naming.
        """
        del params, data
        return f"{self.generator_id}_{task_counter}"

    def get_task_schema_metadata(
        self,
        params: dict[str, Any],
        data: TaskData,
        instruction: str,
        solution: list[str],
        checks: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Return optional top-level benchmark metadata for a task."""
        del params, data, instruction, solution, checks
        return {}

    def generate_tasks(
        self, initial_config: dict[str, Any] | None = None
    ) -> list[Task]:
        """Generate all task variations from this generator."""
        if initial_config is None:
            initial_config = {}

        tasks: list[Task] = []
        task_counter = 0

        # Generate all parameter combinations
        param_combinations = _expand_parameters(self.parameters)

        for params in param_combinations:
            for result, data in self.setup(params, initial_config):
                if not result.success:
                    continue

                task_counter += 1
                task_id = self.build_task_id(params, data, task_counter)

                instruction = self.get_instruction(params, data)
                solution = self.get_solution(params, data)
                checks = self.get_evaluation_checks(params, data)
                data.public.setdefault("prompt_style", "direct")

                derived_constraints = _extract_constraints(solution)
                visible_constraints, hidden_constraints = _split_constraints(
                    instruction, derived_constraints
                )
                provider_dependencies = _derive_provider_dependencies(solution)
                availability_tier = _derive_availability_tier(provider_dependencies)
                online_requirement = _derive_online_requirement(
                    provider_dependencies,
                    solution,
                )
                realism_tags = [
                    "multi_step" if len(solution) > 1 else "single_step",
                ]
                if len(self.required_domains) > 1:
                    realism_tags.append("cross_domain")
                if hidden_constraints:
                    realism_tags.append("underspecified")
                if set(self.required_domains) & _VOLATILE_DOMAINS:
                    realism_tags.append("high_volatility")
                if online_requirement == "required":
                    realism_tags.append("online_required")

                extra = self.get_task_schema_metadata(
                    params=params,
                    data=data,
                    instruction=instruction,
                    solution=solution,
                    checks=checks,
                )
                instruction_variants = list(extra.get("instruction_variants", []))
                visible_constraints = list(
                    extra.get("visible_constraints", visible_constraints)
                )
                hidden_constraints = list(
                    extra.get("hidden_constraints", hidden_constraints)
                )
                decision_requirements = _merge_unique_strings(
                    _derive_decision_requirements(hidden_constraints),
                    list(extra.get("decision_requirements", [])),
                )
                realism_tags = _merge_unique_strings(
                    realism_tags,
                    list(extra.get("realism_tags", [])),
                )
                provider_dependencies = _merge_unique_strings(
                    provider_dependencies,
                    list(extra.get("provider_dependencies", [])),
                )
                availability_tier = str(
                    extra.get("availability_tier", availability_tier)
                )
                online_requirement = str(
                    extra.get("online_requirement", online_requirement)
                )
                canonical_instruction = str(
                    extra.get("canonical_instruction", instruction)
                )

                task = Task(
                    task_id=task_id,
                    instruction=instruction,
                    canonical_instruction=canonical_instruction,
                    instruction_variants=instruction_variants,
                    visible_constraints=visible_constraints,
                    hidden_constraints=hidden_constraints,
                    decision_requirements=decision_requirements,
                    realism_tags=realism_tags,
                    online_requirement=online_requirement,
                    provider_dependencies=provider_dependencies,
                    availability_tier=availability_tier,
                    domains=list(self.required_domains),
                    difficulty=self.difficulty,
                    initial_state=self.get_initial_state(params),
                    ground_truth=GroundTruth(
                        solution_commands=solution,
                        evaluation_checks=checks,
                        metadata={
                            "generator_id": self.generator_id,
                            "params": params,
                            "generation_options": get_generation_options().to_dict(),
                        },
                    ),
                    data=data,
                    template_id=self.generator_id,
                    generator_id=self.generator_id,
                )
                tasks.append(task)

        return tasks


def get_all_generators() -> dict[str, type[BaseTaskGenerator]]:
    """Get all registered generators."""
    return dict(_GENERATOR_REGISTRY)


def get_generator(generator_id: str) -> BaseTaskGenerator:
    """Instantiate a generator by ID."""
    cls = _GENERATOR_REGISTRY.get(generator_id)
    if cls is None:
        raise ValueError(
            f"Unknown generator: {generator_id}. "
            f"Available: {list(_GENERATOR_REGISTRY.keys())}"
        )
    return cls()


def generate_all_tasks(
    initial_config: dict[str, Any] | None = None,
    generator_ids: list[str] | None = None,
) -> list[Task]:
    """Generate tasks from all (or specified) generators."""
    all_tasks: list[Task] = []
    gen_ids = generator_ids or list(_GENERATOR_REGISTRY.keys())

    for gid in gen_ids:
        gen = get_generator(gid)
        tasks = gen.generate_tasks(initial_config)
        all_tasks.extend(tasks)

    return all_tasks


def _expand_parameters(parameters: dict[str, list[Any]]) -> list[dict[str, Any]]:
    """Expand parameter dict into list of all combinations."""
    if not parameters:
        return [{}]

    keys = list(parameters.keys())
    values = [parameters[k] for k in keys]

    combinations = []
    for combo in itertools.product(*values):
        combinations.append(dict(zip(keys, combo)))

    return combinations
