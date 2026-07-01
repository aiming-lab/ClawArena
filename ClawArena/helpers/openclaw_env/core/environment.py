"""Main environment class for CLI agent testing and training."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from openclaw_env.backend.base import BaseBackend
from openclaw_env.backend.mock_backend import MockBackend
from openclaw_env.backend.multi_app_backend import MultiAppBackend
from openclaw_env.core.observation import EvaluationResult, Observation
from openclaw_env.core.task import Task, load_task
from openclaw_env.evaluation.evaluator import EvaluatorComb, build_evaluator
from openclaw_env.utils.safety_guard import (
    SafetyViolation,
    check_command_safety,
    check_python_safety,
)
from openclaw_env.utils.state_manager import StateManager
from openclaw_env.utils.trajectory_recorder import TrajectoryRecorder
from openclaw_env.skills.state_merge import (
    as_named_mapping,
    merge_backend_state_into_eval,
    merge_named_entities,
)


class OpenClawEnv:
    """Main environment for CLI agent testing and training.

    Supports CLI and Python API dual-mode interaction with composable
    evaluation and state isolation.

    Usage:
        with OpenClawEnv(task_id="msg_send_basic_1") as env:
            obs = env.reset()
            while True:
                action = agent.act(obs)
                obs, reward, done, info = env.step(action)
                if done:
                    break
            result = env.evaluate()
    """

    def __init__(
        self,
        task_id: str,
        experiment_name: str = "default",
        backend: str = "mock",
        interface: str = "cli",
        max_steps: int = 50,
        timeout_seconds: int = 120,
        raise_on_safety_violation: bool = True,
        record_trajectory: bool = True,
        instruction_variant_mode: str = "canonical",
        backend_kwargs: dict | None = None,
        task_data_dir: str | Path | None = None,
    ) -> None:
        self.task_id = task_id
        self.experiment_name = experiment_name
        self.interface = interface
        self.max_steps = max_steps
        self.timeout_seconds = timeout_seconds
        self.raise_on_safety_violation = raise_on_safety_violation
        self.record_trajectory = record_trajectory
        if instruction_variant_mode not in {"canonical", "sampled"}:
            raise ValueError(
                "instruction_variant_mode must be 'canonical' or 'sampled'."
            )
        self.instruction_variant_mode = instruction_variant_mode
        self._task_data_dir = Path(task_data_dir) if task_data_dir else None

        self._task: Task | None = None
        self._backend: BaseBackend = _create_backend(backend, **(backend_kwargs or {}))
        self._state_manager: StateManager | None = None
        self._evaluator: EvaluatorComb | None = None
        self._recorder: TrajectoryRecorder | None = None

        self._step_count = 0
        self._done = False
        self._last_observation: Observation | None = None
        self._cumulative_reward = 0.0
        self._command_history: list[dict] = []
        self._active_instruction = ""

        # Track effects for evaluation
        self._effects: dict[str, list[dict[str, Any]]] = {
            "messages_sent": [],
            "agents_created": [],
            "agents_deleted": [],
            "channels_configured": [],
            "cron_jobs_created": [],
            "plugins_installed": [],
            "config_changes": [],
            # New app effects
            "calendar_events_created": [],
            "calendar_events_updated": [],
            "calendar_events_deleted": [],
            "emails_sent": [],
            "emails_moved": [],
            "files_created": [],
            "files_deleted": [],
            "tasks_created": [],
            "tasks_completed": [],
        }

    def __enter__(self) -> OpenClawEnv:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def reset(self) -> Observation:
        """Initialize environment to the task's initial state."""
        # Load task
        self._task = load_task(self.task_id, data_dir=self._task_data_dir)

        # Set up isolated state
        self._state_manager = StateManager(
            base_config_name=self._task.initial_state
        )
        self._state_manager.initialize()
        self._state_manager.apply_state_overrides(
            self._task.data.private.get("initial_state_overrides", {})
        )

        # Initialize backend
        env_vars = self._state_manager.get_env_vars()
        # Enable best-effort online external data for real/hybrid runs only.
        if isinstance(self._backend, MultiAppBackend) and self._backend.real_backend is not None:
            env_vars["OPENCLAW_ENV_ENABLE_ONLINE_DATA"] = "1"
        self._backend.initialize(str(self._state_manager.state_dir), env_vars)

        # Build evaluator from task ground truth
        if self._task.ground_truth:
            self._evaluator = build_evaluator(
                self._task.ground_truth.evaluation_checks
            )

        # Set up trajectory recorder
        if self.record_trajectory:
            self._recorder = TrajectoryRecorder(
                task_id=self.task_id,
                instruction=self._resolve_task_instruction(self._task),
            )
            self._recorder.set_metadata({
                "domains": self._task.domains,
                "difficulty": self._task.difficulty,
                "experiment": self.experiment_name,
                "interface": self.interface,
                "instruction_variant_mode": self.instruction_variant_mode,
                "canonical_instruction": self._task.canonical_instruction
                or self._task.instruction,
            })

        # Reset counters
        self._step_count = 0
        self._done = False
        self._cumulative_reward = 0.0
        self._command_history.clear()
        for k in self._effects:
            self._effects[k].clear()
        self._active_instruction = self._resolve_task_instruction(self._task)

        # Build initial observation
        obs = Observation(
            command_output="Environment initialized. Ready for commands.",
            task_instruction=self._active_instruction,
            current_config=self._backend.get_config(),
            gateway_status=self._backend.get_gateway_status(),
            available_commands=_get_available_commands(
                self._task.domains,
            ),
            step_number=0,
        )
        self._last_observation = obs
        return obs

    def step(self, action: str) -> tuple[Observation, float, bool, dict[str, Any]]:
        """Execute an action and return (observation, reward, done, info)."""
        if self._done:
            raise RuntimeError("Episode already done. Call reset() first.")
        if self._task is None:
            raise RuntimeError("No task loaded. Call reset() first.")

        self._step_count += 1
        info: dict[str, Any] = {"step": self._step_count}

        # Safety check
        is_real = (
            isinstance(self._backend, MultiAppBackend)
            and self._backend.real_backend is not None
        )
        try:
            if self.interface == "python":
                check_python_safety(action)
            else:
                check_command_safety(action, strict=not is_real)
        except SafetyViolation as e:
            obs = Observation(
                error_output=f"Safety violation: {e}",
                exit_code=1,
                task_instruction=self._active_instruction,
                step_number=self._step_count,
                current_config=self._backend.get_config(),
            )
            info["safety_violation"] = True
            if self.raise_on_safety_violation:
                self._done = True
            if self._recorder:
                self._recorder.record_step(obs, action, 0.0, self._done, info)
            self._last_observation = obs
            return obs, 0.0, self._done, info

        # Execute action
        if self.interface == "python":
            result = self._backend.execute_python(action)
        else:
            result = self._backend.execute_cli(action)
        command_meta: dict[str, Any] = dict(result.meta or {})
        if result.execution_trace:
            command_meta["execution_trace"] = result.execution_trace
        if command_meta:
            info["command_meta"] = command_meta

        # Record to command history (capped at 50 to bound memory)
        self._command_history.append({
            "action": action,
            "stdout": result.stdout[:500],
            "stderr": result.stderr[:200],
            "exit_code": result.exit_code,
        })
        if len(self._command_history) > 50:
            self._command_history.pop(0)

        # Track effects
        if result.state_changes:
            self._track_effects(result.state_changes)

        # Check if agent signaled completion
        if action.strip().lower() in ("done", "exit", "quit"):
            self._done = True

        # Check step limit
        if self._step_count >= self.max_steps:
            self._done = True
            info["truncated"] = True

        # Compute intermediate reward (0 unless done)
        reward = 0.0
        if self._done and self._evaluator:
            eval_result = self.evaluate()
            reward = eval_result.score

        self._cumulative_reward += reward

        obs = Observation(
            command_output=result.stdout,
            error_output=result.stderr if result.stderr else None,
            exit_code=result.exit_code,
            current_config=self._backend.get_config(),
            gateway_status=self._backend.get_gateway_status(),
            task_instruction=self._active_instruction,
            step_number=self._step_count,
        )
        self._last_observation = obs

        if self._recorder:
            self._recorder.record_step(obs, action, reward, self._done, info)

        return obs, reward, self._done, info

    def evaluate(self) -> EvaluationResult:
        """Evaluate the current state against task goals."""
        if self._evaluator is None:
            return EvaluationResult(success=False, score=0.0)

        env_state = self._get_evaluation_state()
        task_data = {}
        if self._task and self._task.data:
            task_data = {
                "public": self._task.data.public,
                "private": self._task.data.private,
            }

        result = self._evaluator(env_state, task_data)

        if self._recorder:
            self._recorder.set_evaluation(result)

        return result

    def save_state(self) -> str:
        """Save a snapshot of the current state. Returns snapshot ID."""
        if self._state_manager is None:
            raise RuntimeError("Environment not initialized.")
        return self._state_manager.save_snapshot()

    def load_state(self, state_id: str) -> None:
        """Restore state from a snapshot."""
        if self._state_manager is None:
            raise RuntimeError("Environment not initialized.")
        self._state_manager.load_snapshot(state_id)
        # Re-initialize backend with restored state
        env_vars = self._state_manager.get_env_vars()
        self._backend.initialize(str(self._state_manager.state_dir), env_vars)

    @property
    def task(self) -> Task | None:
        return self._task

    @property
    def trajectory(self):
        return self._recorder.trajectory if self._recorder else None

    def close(self) -> None:
        """Clean up resources."""
        self._backend.cleanup()
        if self._state_manager:
            self._state_manager.cleanup()

    def _get_evaluation_state(self) -> dict[str, Any]:
        """Build the state dict used for evaluation."""
        state: dict[str, Any] = {
            "config": self._backend.get_config(),
            "gateway_status": self._backend.get_gateway_status(),
            "effects": dict(self._effects),
            "step_count": self._step_count,
            "task_instruction": self._active_instruction,
            "canonical_instruction": (
                (self._task.canonical_instruction or self._task.instruction)
                if self._task
                else ""
            ),
            "command_history": list(self._command_history),
        }

        if self._last_observation:
            state["last_stdout"] = self._last_observation.command_output
            state["last_stderr"] = self._last_observation.error_output or ""
            state["last_exit_code"] = self._last_observation.exit_code

        backend_state = self._backend.get_state()

        # In real mode, ensure openclaw live state is still available even when
        # upstream backend returns sparse state.
        if isinstance(self._backend, MultiAppBackend) and self._backend.real_backend is not None:
            real_state = self._backend.real_backend.get_state()
            if "agents" not in backend_state and "agents" in real_state:
                backend_state["agents"] = real_state["agents"]
            if "channels" not in backend_state and "channels" in real_state:
                backend_state["channels"] = real_state["channels"]

        merge_backend_state_into_eval(state, state["effects"], backend_state)

        # Normalize possibly list-shaped live state and backfill from effects.
        state["agents"] = as_named_mapping(state.get("agents"))
        state["channels"] = as_named_mapping(state.get("channels"))
        merge_named_entities(state["agents"], state["effects"].get("agents_created", []))
        merge_named_entities(state["channels"], state["effects"].get("channels_configured", []))

        return state

    def _track_effects(self, changes: dict[str, Any]) -> None:
        """Track state changes as effects for evaluation."""
        if "agents" in changes:
            for name, agent_data in changes["agents"].items():
                self._effects["agents_created"].append(
                    {"name": name, **agent_data}
                )
        if "messages" in changes:
            self._effects["messages_sent"].extend(changes["messages"])
        if "config" in changes:
            self._effects["config_changes"].append(changes["config"])
        if "plugins" in changes:
            self._effects["plugins_installed"].extend(changes["plugins"])
        if "cron_jobs" in changes:
            self._effects["cron_jobs_created"].extend(changes["cron_jobs"])
        # New app effects
        if "calendar_events_created" in changes:
            self._effects["calendar_events_created"].extend(changes["calendar_events_created"])
        if "calendar_events_updated" in changes:
            self._effects["calendar_events_updated"].extend(changes["calendar_events_updated"])
        if "calendar_events_deleted" in changes:
            self._effects["calendar_events_deleted"].extend(changes["calendar_events_deleted"])
        if "emails_sent" in changes:
            self._effects["emails_sent"].extend(changes["emails_sent"])
        if "emails_moved" in changes:
            self._effects["emails_moved"].extend(changes["emails_moved"])
        if "files_created" in changes:
            self._effects["files_created"].extend(changes["files_created"])
        if "files_deleted" in changes:
            self._effects["files_deleted"].extend(changes["files_deleted"])
        if "tasks_created" in changes:
            self._effects["tasks_created"].extend(changes["tasks_created"])
        if "tasks_completed" in changes:
            self._effects["tasks_completed"].extend(changes["tasks_completed"])

    def _resolve_task_instruction(self, task: Task) -> str:
        """Resolve the instruction shown to the agent for this episode."""
        canonical = task.canonical_instruction or task.instruction
        if self.instruction_variant_mode != "sampled":
            return task.instruction

        variants = task.variant_texts()
        if not variants:
            return task.instruction

        seed_material = f"{task.task_id}:{self.experiment_name}:{canonical}"
        seed = int.from_bytes(
            hashlib.sha256(seed_material.encode("utf-8")).digest()[:8],
            "big",
        )
        return variants[seed % len(variants)]


def _create_backend(backend_type: str, **kwargs) -> BaseBackend:
    """Create a backend instance by type name.

    Extra keyword arguments are forwarded to the backend constructor
    (only meaningful for ``"hybrid"`` currently).
    """
    if backend_type == "mock":
        return MockBackend()
    if backend_type == "multi":
        return MultiAppBackend()
    if backend_type == "real":
        real_kwargs = dict(kwargs)
        fallback_to_mock = bool(real_kwargs.pop("fallback_openclaw_network_to_mock", False))
        strict_online_data = bool(real_kwargs.pop("strict_online_data", True))
        return MultiAppBackend(
            real_openclaw=True,
            real_openclaw_kwargs=real_kwargs,
            fallback_openclaw_network_to_mock=fallback_to_mock,
            strict_online_data=strict_online_data,
        )
    if backend_type == "hybrid":
        from openclaw_env.backend.hybrid_backend import HybridBackend
        return HybridBackend(**kwargs)
    raise ValueError(f"Unknown backend type: {backend_type}")


def make_env(
    task_id: str,
    task_data_dir: str | Path | None = None,
    mode: str = "mock",
    backend_kwargs: dict | None = None,
    **kwargs,
) -> OpenClawEnv:
    """Convenience factory for creating an OpenClawEnv.

    Args:
        task_id: Task identifier (e.g. ``"calendar_add_event_1"``).
        task_data_dir: Optional task-data root containing ``tasks/`` and
            ``datasets/``. Defaults to built-in ``openclaw_env/data``.
        mode: Backend mode — ``'mock'``, ``'multi'``, ``'real'``, or
            ``'hybrid'``.
        backend_kwargs: Extra keyword arguments forwarded to the backend
            constructor. Currently only used by ``'hybrid'`` mode
            (e.g. ``{"auto_start_gateway": True, "gateway_port": 19000}``).
        **kwargs: Forwarded to :class:`OpenClawEnv`.
    """
    _MODE_MAP = {"mock": "mock", "multi": "multi", "real": "real", "hybrid": "hybrid"}
    backend = _MODE_MAP.get(mode, "mock")
    return OpenClawEnv(
        task_id=task_id,
        task_data_dir=task_data_dir,
        backend=backend,
        backend_kwargs=backend_kwargs,
        **kwargs,
    )


def _get_available_commands(
    domains: list[str],
) -> list[str]:
    """Get command hints based on task domains."""
    domain_commands: dict[str, list[str]] = {
        "setup_config": [
            "openclaw setup",
            "openclaw config set <path> <value>",
            "openclaw onboard",
        ],
        "messaging": [
            "openclaw message send --target <target> --message <text>",
            "openclaw message broadcast --targets <t1> <t2> --message <text>",
            "openclaw message poll --target <target> --poll-question <q> --poll-option <o1> --poll-option <o2>",
            "openclaw message search --channel discord --guild-id <gid> --channel-id <cid> --query <text>",
        ],
        "agent_mgmt": [
            "openclaw agents add <name> --model <model>",
            "openclaw agents list",
            "openclaw agents delete --name <name>",
            "openclaw agents set-identity --agent <name> --emoji <emoji>",
        ],
        "channel_mgmt": [
            "openclaw channels login --channel <name>",
            "openclaw channels list",
            "openclaw config set channels.<name>.config.<key> <value>",
        ],
        "monitoring": [
            "openclaw status",
            "openclaw status --json",
            "openclaw health",
            "openclaw logs",
            "openclaw doctor",
            "openclaw sessions",
        ],
        "plugin_skill": [
            "openclaw plugins enable <name>",
            "openclaw plugins disable <name>",
            "openclaw plugins list",
            "openclaw skills info <name>",
            "openclaw skills list",
        ],
        "cron_webhook": [
            "openclaw cron add --name <job> --cron <expr> --message <text>",
            "openclaw cron list",
            "openclaw config set integrations.webhooks.primary.url <url>",
        ],
        "security": [
            "openclaw security",
            "openclaw config set gateway.auth.token <token>",
        ],
        "device_node": [
            "openclaw devices pair",
            "openclaw devices list",
        ],
        "calendar": [
            "calendar list [--from DATE] [--to DATE]",
            "calendar add-event --title TITLE --start DATETIME [--location LOC] [--attendees A,B]",
            "calendar update-event --id ID [--title TITLE] [--start DATETIME] [--location LOC]",
            "calendar delete-event --id ID",
            "calendar search --query QUERY",
            "calendar today [--timezone TZ]",
        ],
        "email": [
            "email list [--folder FOLDER] [--unread] [--from SENDER]",
            "email read --id ID",
            "email send --to ADDR --subject SUBJ --body BODY",
            "email reply --id ID --body BODY",
            "email search --query QUERY",
            "email move --id ID --folder FOLDER",
            "email mark --id ID --flag {read,unread,starred}",
        ],
        "weather": [
            "weather get --location LOC [--date DATE]",
            "weather forecast --location LOC [--days N]",
            "weather alerts --location LOC",
        ],
        "file": [
            "file create --path PATH --content CONTENT",
            "file read --path PATH",
            "file delete --path PATH",
            "file list [--path PATH]",
            "file move --src SRC --dst DST",
            "file append --path PATH --content CONTENT",
        ],
        "tasks": [
            "tasks list [--status {all,pending,done}] [--priority {high,medium,low}]",
            "tasks add --title TITLE [--due DATE] [--priority PRIORITY]",
            "tasks complete --id ID",
            "tasks delete --id ID",
            "tasks search --query QUERY",
        ],
    }

    commands: list[str] = []
    for domain in domains:
        commands.extend(domain_commands.get(domain, []))
    # Always include general commands
    commands.extend([
        "openclaw status",
        "openclaw status --json",
        "done  # signal task completion",
    ])
    return list(dict.fromkeys(commands))  # deduplicate preserving order


def _as_named_mapping(raw: Any) -> dict[str, Any]:
    """Normalize backend entity containers to ``{name: payload}`` mappings."""
    return as_named_mapping(raw)


def _merge_named_entities(dst: dict[str, Any], entries: Any) -> None:
    """Merge effect entries that carry a ``name`` field into ``dst``."""
    merge_named_entities(dst, entries)
