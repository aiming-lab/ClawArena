from __future__ import annotations

from openclaw_env.core.environment import OpenClawEnv
from openclaw_env.core.task import GroundTruth, Task, TaskData


def test_task_roundtrip_preserves_v2_fields():
    task = Task(
        task_id="demo_task",
        instruction="Do the thing.",
        domains=["composite", "monitoring"],
        difficulty=3,
        initial_state="default",
        ground_truth=GroundTruth(solution_commands=["openclaw status"], evaluation_checks=[]),
        data=TaskData(public={"prompt_style": "direct"}, private={}),
        canonical_instruction="Do the thing.",
        instruction_variants=[
            {"style": "brief", "text": "Handle it."},
            {"style": "underspecified", "text": "Take care of this."},
        ],
        visible_constraints=[{"type": "query", "value": "status"}],
        hidden_constraints=[{"type": "priority", "value": "high"}],
        decision_requirements=["infer_priority"],
        realism_tags=["multi_step", "underspecified"],
        online_requirement="optional",
        provider_dependencies=["google_calendar"],
        availability_tier="external-risk",
    )

    restored = Task.from_dict(task.to_dict())
    assert restored.canonical_instruction == "Do the thing."
    assert restored.variant_texts() == ["Handle it.", "Take care of this."]
    assert restored.visible_constraints == [{"type": "query", "value": "status"}]
    assert restored.hidden_constraints == [{"type": "priority", "value": "high"}]
    assert restored.decision_requirements == ["infer_priority"]
    assert restored.realism_tags == ["multi_step", "underspecified"]
    assert restored.online_requirement == "optional"
    assert restored.provider_dependencies == ["google_calendar"]
    assert restored.availability_tier == "external-risk"


def test_task_from_dict_keeps_legacy_specs_compatible():
    task = Task.from_dict(
        {
            "task_id": "legacy_task",
            "instruction": "Legacy instruction.",
            "domains": ["monitoring"],
            "difficulty": 1,
            "initial_state": "default",
            "ground_truth": {
                "solution_commands": ["openclaw status"],
                "evaluation_checks": [],
            },
            "data": {"public": {}, "private": {}},
        }
    )

    assert task.canonical_instruction == "Legacy instruction."
    assert task.instruction_variants == []
    assert task.visible_constraints == []
    assert task.hidden_constraints == []
    assert task.decision_requirements == []
    assert task.realism_tags == []
    assert task.online_requirement is None


def test_environment_can_show_sampled_instruction_variant():
    with OpenClawEnv(
        task_id="agent_create_1",
        backend="mock",
        instruction_variant_mode="sampled",
    ) as env:
        env.reset()
        assert env.task is not None
        env.task.instruction_variants = [
            {"style": "brief", "text": "Create the agent quickly."},
            {"style": "underspecified", "text": "Set up that agent."},
        ]
        env._active_instruction = env._resolve_task_instruction(env.task)
        assert env._active_instruction in {
            "Create the agent quickly.",
            "Set up that agent.",
        }
