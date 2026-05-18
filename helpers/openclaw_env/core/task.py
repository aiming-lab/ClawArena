"""Task data structures and loading utilities."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).parent.parent / "data"


class Difficulty(IntEnum):
    SINGLE_STEP = 1
    MULTI_STEP = 2
    REASONING = 3


class Domain(str):
    """Task domain identifier (D1-D10)."""

    SETUP_CONFIG = "setup_config"
    MESSAGING = "messaging"
    AGENT_MGMT = "agent_mgmt"
    CHANNEL_MGMT = "channel_mgmt"
    MONITORING = "monitoring"
    PLUGIN_SKILL = "plugin_skill"
    CRON_WEBHOOK = "cron_webhook"
    SECURITY = "security"
    DEVICE_NODE = "device_node"
    COMPOSITE = "composite"


ALL_DOMAINS = [
    Domain.SETUP_CONFIG,
    Domain.MESSAGING,
    Domain.AGENT_MGMT,
    Domain.CHANNEL_MGMT,
    Domain.MONITORING,
    Domain.PLUGIN_SKILL,
    Domain.CRON_WEBHOOK,
    Domain.SECURITY,
    Domain.DEVICE_NODE,
    Domain.COMPOSITE,
]


@dataclass
class TaskData:
    """Public and private data associated with a task.

    Public data is visible to the agent (included in instructions).
    Private data is only used for evaluation.
    """

    public: dict[str, Any] = field(default_factory=dict)
    private: dict[str, Any] = field(default_factory=dict)


@dataclass
class GroundTruth:
    """Ground truth for task evaluation."""

    solution_commands: list[str]
    evaluation_checks: list[dict[str, Any]]
    answer: Any | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Task:
    """A single task instance."""

    task_id: str
    instruction: str
    domains: list[str]
    difficulty: int
    initial_state: str  # name of base config to use
    ground_truth: GroundTruth | None = None
    data: TaskData = field(default_factory=TaskData)
    template_id: str | None = None
    generator_id: str | None = None
    weight: float = 1.0
    canonical_instruction: str | None = None
    instruction_variants: list[dict[str, Any] | str] = field(default_factory=list)
    visible_constraints: list[dict[str, Any]] = field(default_factory=list)
    hidden_constraints: list[dict[str, Any]] = field(default_factory=list)
    decision_requirements: list[str] = field(default_factory=list)
    realism_tags: list[str] = field(default_factory=list)
    online_requirement: str | None = None
    provider_dependencies: list[str] = field(default_factory=list)
    availability_tier: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "instruction": self.instruction,
            "canonical_instruction": self.canonical_instruction or self.instruction,
            "instruction_variants": self.instruction_variants,
            "visible_constraints": self.visible_constraints,
            "hidden_constraints": self.hidden_constraints,
            "decision_requirements": self.decision_requirements,
            "realism_tags": self.realism_tags,
            "online_requirement": self.online_requirement,
            "provider_dependencies": self.provider_dependencies,
            "availability_tier": self.availability_tier,
            "domains": self.domains,
            "difficulty": self.difficulty,
            "initial_state": self.initial_state,
            "template_id": self.template_id,
            "generator_id": self.generator_id,
            "weight": self.weight,
            "data": {"public": self.data.public, "private": self.data.private},
            "ground_truth": {
                "solution_commands": self.ground_truth.solution_commands,
                "evaluation_checks": self.ground_truth.evaluation_checks,
                "answer": self.ground_truth.answer,
                "metadata": self.ground_truth.metadata,
            }
            if self.ground_truth
            else None,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Task:
        gt_data = d.get("ground_truth")
        ground_truth = None
        if gt_data:
            ground_truth = GroundTruth(
                solution_commands=gt_data["solution_commands"],
                evaluation_checks=gt_data["evaluation_checks"],
                answer=gt_data.get("answer"),
                metadata=gt_data.get("metadata", {}),
            )
        task_data = d.get("data", {})
        return cls(
            task_id=d["task_id"],
            instruction=d["instruction"],
            canonical_instruction=d.get("canonical_instruction") or d["instruction"],
            instruction_variants=d.get("instruction_variants", []),
            visible_constraints=d.get("visible_constraints", []),
            hidden_constraints=d.get("hidden_constraints", []),
            decision_requirements=d.get("decision_requirements", []),
            realism_tags=d.get("realism_tags", []),
            online_requirement=d.get("online_requirement"),
            provider_dependencies=d.get("provider_dependencies", []),
            availability_tier=d.get("availability_tier"),
            domains=d["domains"],
            difficulty=d["difficulty"],
            initial_state=d["initial_state"],
            ground_truth=ground_truth,
            data=TaskData(
                public=task_data.get("public", {}),
                private=task_data.get("private", {}),
            ),
            template_id=d.get("template_id"),
            generator_id=d.get("generator_id"),
            weight=d.get("weight", 1.0),
        )

    def variant_texts(self) -> list[str]:
        """Return normalized instruction variant texts."""
        texts: list[str] = []
        for item in self.instruction_variants:
            if isinstance(item, str):
                text = item.strip()
            elif isinstance(item, dict):
                text = str(item.get("text", "")).strip()
            else:
                text = ""
            if text:
                texts.append(text)
        return texts


def load_task(task_id: str, data_dir: Path | None = None) -> Task:
    """Load a single task by ID."""
    base = data_dir or DATA_DIR
    task_path = base / "tasks" / task_id / "specs.json"
    with open(task_path) as f:
        return Task.from_dict(json.load(f))


def load_task_ids(
    split: str = "train",
    data_dir: Path | None = None,
    difficulty: int | None = None,
    domain: str | None = None,
) -> list[str]:
    """Load task IDs for a given split, optionally filtered."""
    base = data_dir or DATA_DIR
    split_path = base / "datasets" / f"{split}.txt"
    if not split_path.exists():
        return []
    task_ids = split_path.read_text().strip().splitlines()
    if difficulty is not None or domain is not None:
        filtered = []
        for tid in task_ids:
            task = load_task(tid, data_dir=base)
            if difficulty is not None and task.difficulty != difficulty:
                continue
            if domain is not None and domain not in task.domains:
                continue
            filtered.append(tid)
        task_ids = filtered
    return task_ids


def save_task(task: Task, data_dir: Path | None = None) -> Path:
    """Save a task to disk."""
    base = data_dir or DATA_DIR
    task_dir = base / "tasks" / task.task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    specs_path = task_dir / "specs.json"
    with open(specs_path, "w") as f:
        json.dump(task.to_dict(), f, indent=2, ensure_ascii=False)
    return specs_path
