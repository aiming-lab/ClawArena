"""Unified interface and data type definitions.

All cross-module data structures are centralized here for ease of handover.
Relative paths in persisted JSON/YAML are converted to absolute ``Path`` objects
immediately after parsing and flow through memory as such.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Literal, Optional, Protocol

# ---------------------------------------------------------------------------
# Modality / Model
# ---------------------------------------------------------------------------


class Modality(str, Enum):
    LLM = "llm"
    VLM = "vlm"
    OMNI = "omni"


# "Required / allowed" declarations per pool type. Validation and pruning rules
# are documented in :mod:`clawarena_team.provider.registry`.
POOL_REQUIRED_MODALITIES: dict[Modality, frozenset[str]] = {
    Modality.LLM: frozenset({"text"}),
    Modality.VLM: frozenset({"text", "image"}),
    Modality.OMNI: frozenset({"text", "audio"}),
}
POOL_USABLE_MODALITIES: dict[Modality, frozenset[str]] = {
    Modality.LLM: frozenset({"text"}),
    Modality.VLM: frozenset({"text", "image", "video"}),
    Modality.OMNI: frozenset({"text", "image", "audio", "video"}),
}

ALLOWED_MODALITY_NAMES: frozenset[str] = frozenset({"text", "image", "audio", "video"})


@dataclass
class ModelConfig:
    """Access configuration for a single model to be invoked.

    ``modalities``: the content types this model declares it can directly consume;
    must contain at least ``"text"``. Optional values: ``"image"`` / ``"audio"`` /
    ``"video"``.
    ``modality_limits``: per non-``text`` modality, the **upper bound on the number
    of most-recent attachments retained in context** (e.g. ``{"image": 4, "video": 1}``).
    When exceeded, the oldest attachments are stripped into text placeholders while the
    most recent N are kept (matching the strip-oldest-first behavior of mainstream
    harnesses, and staying ≤ vLLM ``--limit-mm-per-prompt``).
    """

    provider: str
    model_id: str
    api_base: Optional[str] = None
    api_key: Optional[str] = None
    modalities: list[str] = field(default_factory=lambda: ["text"])
    modality_limits: dict[str, int] = field(default_factory=dict)
    extra: dict[str, Any] = field(default_factory=dict)

    def sanitized(self) -> dict[str, Any]:
        d = {
            "provider": self.provider,
            "model_id": self.model_id,
            "api_base": self.api_base,
            "modalities": list(self.modalities),
        }
        if self.modality_limits:
            d["modality_limits"] = dict(self.modality_limits)
        if self.extra:
            d["extra"] = self.extra
        return d


@dataclass
class ModelPoolEntry:
    """A single entry in the candidate subagent model pool.

    ``declared_modalities``: the set **declared** by the user in yaml/JSON/env.
    ``effective_modalities``: the set that is **actually in effect** after being pruned
    by pool rules and validated via init probing; this is what is actually presented to
    the agent in the Read tool description and the create_subagent tool description.
    """

    key: Modality
    name: str
    config: ModelConfig
    declared_modalities: list[str] = field(default_factory=lambda: ["text"])
    effective_modalities: list[str] = field(default_factory=lambda: ["text"])

    def public_view(self) -> dict[str, Any]:
        """Safe view exposed to the main agent; excludes api_key/api_base."""
        return {
            "key": self.key.value,
            "name": self.name,
            "modalities": list(self.effective_modalities),
        }

    def info_for_metadata(self) -> dict[str, Any]:
        """Fields persisted to metadata.json (excludes api_key)."""
        return {
            "key": self.key.value,
            "name": self.name,
            "provider": self.config.provider,
            "model_id": self.config.model_id,
            "api_base": self.config.api_base,
            "declared_modalities": list(self.declared_modalities),
            "effective_modalities": list(self.effective_modalities),
            "modality_limits": dict(self.config.modality_limits),
            "extra": dict(self.config.extra),
        }


@dataclass
class ModelBundle:
    """All models used in a single run: main + three categories of subagent candidates."""

    main: ModelConfig
    pool: dict[Modality, ModelPoolEntry]


# ---------------------------------------------------------------------------
# Tool messages
# ---------------------------------------------------------------------------


Role = Literal["system", "user", "assistant", "tool_result"]


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class ToolResult:
    tool_call_id: str
    content: str
    is_error: bool = False
    # Multimodal attachments: path + modality label ("text"/"image"/"audio"/"video")
    attachments: list[tuple[str, str]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Scenario / Dataset
# ---------------------------------------------------------------------------


UpdateOp = Literal["new", "replace"]


@dataclass
class UpdateFile:
    src: Path  # resolved to an absolute path relative to the manifest
    dst_rel: str  # target path relative to the workspace root


@dataclass
class UpdateGroup:
    update_id: str
    op: UpdateOp
    files: list[UpdateFile]


@dataclass
class EvalSpec:
    command: str  # placeholders and relative paths already resolved
    expect_exit: int = 0
    timeout: int = 60
    expect_stdout: Optional[str] = None
    expect_stdout_regex: bool = False


@dataclass
class Feedback:
    correct: str = ""
    incorrect: str = ""


@dataclass
class Round:
    id: str
    type: Literal["exec_check"]
    update_ids: list[str]
    question: str
    eval: EvalSpec
    feedback: Feedback
    # The capability dimensions assessed in this round (controlled vocabulary in
    # src/clawarena_team/stats/tag_vocab.py).
    # Used only for metadata / feedback analysis (aggregating pass rate by tag,
    # finding blank dimensions to author new data); does not affect runtime
    # scheduling or scoring. Optional field.
    tags: list[str] = field(default_factory=list)


@dataclass
class ScenarioManifest:
    scenario_id: str
    desc: str
    scenario_dir: Path  # absolute path to the directory containing this manifest
    workspace_template: Path  # absolute path
    scripts_dir: Path  # absolute path; resolved from the ``scripts`` field in manifest.json
    main_agent_accessible_paths: list[str]  # subpaths relative to the workspace root
    # Paths that may only be granted to subagents (the main agent's own
    # Read/Edit/Write/Grep/Glob cannot reach them, but the main agent may include them
    # in a subagent's accessible_paths when calling CreateSubagent).
    # Used to enforce delegation: the main agent must use a subagent to handle large
    # files, multimodal content, and red-herring directories.
    main_agent_delegable_paths: list[str]
    updates: dict[str, UpdateGroup]
    rounds: list[Round]


@dataclass
class DatasetManifests:
    manifests_path: Path
    scenarios: dict[str, Path]  # scenario_id -> absolute path to that scenario's manifest.json


@dataclass
class TestsConfig:
    tests_path: Path
    name: str
    desc: str
    manifests_ref: Path  # absolute path
    scenario_ids: list[str]
    extras: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Subagent / Session
# ---------------------------------------------------------------------------


RunMode = Literal["runtime", "background"]


@dataclass
class SubagentSpec:
    subagent_id: str
    name: str
    system_prompt: str
    model_key: Modality
    tools: list[str]
    accessible_paths: list[Path]  # absolute paths


@dataclass
class SessionMeta:
    session_id: str
    owner_id: str  # "main" or subagent_id
    started_at: float
    ended_at: Optional[float] = None
    mode: Optional[RunMode] = None
    # Peak context occupancy after adding the last turn (computed by the local
    # tokenizer); under monotonically increasing context this equals the total context
    # length at scenario end, which is the basis for comparison against token_limit.
    context_size_max: int = 0
    # Three cumulative components per model call (= per assistant turn), as a local view
    # that is comparable across providers:
    #   input  ─ content newly added to context between the previous assistant turn and this call
    #   output ─ this assistant turn itself
    #   cache_read ─ tokens already present in context before this call (in theory eligible for prompt cache hits)
    input_token_total: int = 0
    output_token_total: int = 0
    cache_read_total: int = 0


# ---------------------------------------------------------------------------
# Scoring / Metrics
# ---------------------------------------------------------------------------


@dataclass
class RoundEval:
    round_id: str
    passed: bool
    exit_code: int
    stdout: str
    stderr: str
    duration_sec: float


@dataclass
class SubagentLifecycleStat:
    subagent_id: str
    name: str
    model_key: Modality
    tools_granted: list[str]
    tools_used: set[str]
    accessible_paths: list[Path]
    files_accessible_total: int = 0
    files_accessed: set[Path] = field(default_factory=set)
    modality_usage: dict[str, int] = field(default_factory=dict)
    forbidden_count: int = 0
    sessions: list[SessionMeta] = field(default_factory=list)


@dataclass
class ScenarioMetrics:
    scenario_id: str
    task_success_rate: float
    rounds_passed: int
    rounds_total: int
    tool_permission_score: float
    readonly_subagent_score: float
    workspace_permission_score: float
    model_choice_score: float
    main_agent_forbidden_count: int
    subagent_forbidden_total: int
    subagent_forbidden_avg: float
    subagent_create_count: int
    model_key_distribution: dict[str, int]
    # Subagent invocation-mode counts, flattened into five categories
    # {"new+runtime", "new+background", "continue+runtime", "continue+background", "workflow"}.
    invocation_distribution: dict[str, int]
    tools_grant_counts: dict[str, int]
    # Token metrics (comparison against token_limit uses context_size_max):
    main_agent_context_size_max: int  # MCM
    main_agent_input_total: int       # MIT — cumulative new input
    main_agent_output_total: int      # MOT — cumulative output
    main_agent_cache_read_total: int  # MCR — cumulative cache-read (sum of per-round hittable portions)
    subagent_system_tokens: int            # SST — total subagent system prompt tokens (static)
    subagent_context_size_max_sum: int     # SCM — sum of context_size_max across subagent sessions
    subagent_input_total: int              # SIT
    subagent_output_total: int             # SOT
    subagent_cache_read_total: int         # SCR
    # Bash invocation-mode counts {"runtime": n, "background": m} (main + all subagents combined).
    bash_mode_distribution: dict[str, int] = field(default_factory=dict)  # BSH
    # Number of subagent calls with schema-enforced structured output (Workflow agent({schema}) + RunSubagent when enabled).
    structured_output_count: int = 0       # SOC


@dataclass
class RunReport:
    run_id: str
    scenarios: list[ScenarioMetrics]
    avg_task_success_rate: float
    avg_scenario_success_rate: float
    avg_scenario_full_pass_rate: float
    # Composite scoring (added in handbook v2):
    #   SMS = 0.5·TCS + 0.5·MQS  — Subagent Management Score
    #   TCS = (TCR + SCR + SFR) / 3        — Task Correctness Subscore
    #   MQS = mean over scenarios of mean(TPS, ROS, WPS, MCS)
    #         — Management Quality Subscore
    subagent_management_score: float = 0.0
    task_correctness_subscore: float = 0.0
    management_quality_subscore: float = 0.0


# ---------------------------------------------------------------------------
# Provider Protocol
# ---------------------------------------------------------------------------


class Provider(Protocol):
    """All providers must implement this interface."""

    name: str

    async def chat(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Return a normalized {content, tool_calls, usage} dict."""
        ...
