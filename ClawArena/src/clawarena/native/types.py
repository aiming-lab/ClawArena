"""统一的接口与数据类型定义。

所有跨模块的数据结构集中于此，便于他人接手开发。落盘 JSON/YAML 中的相对路径在
解析后立即转换为绝对 ``Path`` 在内存中流转。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, Optional, Protocol

# ---------------------------------------------------------------------------
# Modality / Model
# ---------------------------------------------------------------------------

ALLOWED_MODALITY_NAMES: frozenset[str] = frozenset({"text", "image", "audio", "video"})


@dataclass
class ModelConfig:
    """单个被调用模型的访问配置。

    ``modalities``：该模型声明可直接消费的内容类型，至少含 ``"text"``。可选项：
    ``"image"`` / ``"audio"`` / ``"video"``。
    """

    provider: str
    model_id: str
    api_base: Optional[str] = None
    api_key: Optional[str] = None
    modalities: list[str] = field(default_factory=lambda: ["text"])
    declared_modalities: list[str] = field(default_factory=lambda: ["text"])
    effective_modalities: list[str] = field(default_factory=lambda: ["text"])
    extra: dict[str, Any] = field(default_factory=dict)

    def sanitized(self) -> dict[str, Any]:
        d = {
            "provider": self.provider,
            "model_id": self.model_id,
            "api_base": self.api_base,
            "modalities": list(self.modalities),
            "declared_modalities": list(self.declared_modalities),
            "effective_modalities": list(self.effective_modalities),
        }
        if self.extra:
            d["extra"] = self.extra
        return d


@dataclass
class ModelBundle:
    """一次 run 所用的三 role 模型。

    - ``main``：主 agent 的 provider 配置（``provider`` / ``model_id`` 必填）
    - ``subagent``：``Agent`` 工具 spawn 子代理时使用的 provider；缺省时整段从
      ``main`` 继承（field-by-field，详见
      :func:`arcbench.provider.registry.parse_model_json`）
    - ``compaction``：主 agent 自压缩时使用的 provider；缺省时整段从 ``main`` 继承。
      其 ``modalities`` 强制 ``["text"]``（claude-code 同款约束：summary 不留 image
      token），不可由配置改动

    三者均为 :class:`ModelConfig` 实例。具体 provider 实例由
    :func:`arcbench.provider.registry.build_provider` 按需构造。
    """

    main: ModelConfig
    subagent: ModelConfig
    compaction: ModelConfig


# ---------------------------------------------------------------------------
# Update / Patch
# ---------------------------------------------------------------------------


UpdateOp = Literal["add", "modify", "delete", "rename"]


@dataclass
class UpdateFileOp:
    """patch_spec 中的单条 op。

    - ``add``：``path`` 是目标路径，``content_ref`` 指向数据集内的源文件
    - ``modify``：``path`` 是目标路径，``diff`` 是 unified diff 文本
    - ``delete``：``path`` 是被删除的目标路径
    - ``rename``：``from_path`` → ``to_path``
    """

    op: UpdateOp
    path: Optional[str] = None
    from_path: Optional[str] = None
    to_path: Optional[str] = None
    diff: Optional[str] = None
    content_ref: Optional[str] = None


@dataclass
class UpdateSpec:
    """scenarios/<sid>/updates/<update_id>/patch_spec.json 在内存中的形态。"""

    update_id: str
    ops: list[UpdateFileOp]
    reminder_summary: str
    expected_reflections: list[str] = field(default_factory=list)
    # 该 update 在 patch 编译时的源根目录（含 files/ 等附属资产）
    base_dir: Optional[Path] = None


# ---------------------------------------------------------------------------
# Round / Day / Arc
# ---------------------------------------------------------------------------


@dataclass
class EvalSpec:
    command: str
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
    """questions.json 中的单题。

    ``type`` 在 ArcBench v1 一律为 ``exec_check`` —— arc_audit / scenario_audit 通过
    ``eval.command`` 不同来区分，不再单列 round 类型。
    """

    id: str
    type: Literal["exec_check"]
    update_ids: list[str]
    question: str
    eval: EvalSpec
    feedback: Feedback
    # 偏好是 round 级属性：本轮显式声明要考察的偏好 tag（引用代码注册表）。
    # 不是所有 round 都考察偏好——只有打了 tag 的轮次才核对。
    preference_tags: list[str] = field(default_factory=list)
    # 受控词表见 docs/handbook/question-tags.md；具体值任意但必须 list[str]。
    # 特殊保留命名空间：``update:<update_id>`` 用于标记"该题考察某次 update 的反映"，
    # 由 adaptation 评分模块识别并匹配 expected_reflections。
    tags: list[str] = field(default_factory=list)
    # 跨弧 callback 提示：声明本题引用了哪些前置 day 的产物路径或事实，
    # 供 oracle 生成器 / callback 评分使用。
    callbacks: list[str] = field(default_factory=list)


@dataclass
class ScenarioManifest:
    """test_samples/<ts_id>/arcs/<arc_id>/scenarios/<scenario_id>/scenario.json。

    一个 scenario 即弧内一个工作日，在 agent 端透过 ``day_idx`` 形态曝光为 ``day{n}``；
    ``scenario_id`` 是数据侧稳定 id，**不对 agent 暴露**。所有子资源目录（checks /
    updates / oracles）由各自字段显式声明、加载时解析为绝对路径——不在代码内硬编码。
    """

    scenario_id: str               # e.g. "s1"
    arc_seq: int                   # scenario 在所属 arc 内的序号（由 arc.scenarios 位置隐式确定）
    desc: str
    rounds: list[Round]
    scenario_audit: Optional[EvalSpec]   # 该 scenario 末尾的 self-audit（可选）
    scenario_dir: Path             # 解析后的绝对路径
    scripts_dir: Path              # check 脚本目录（scenario.json.scripts，缺省 checks/）
    updates_dir: Path              # update 根目录（scenario.json.updates_dir，缺省 updates/）
    oracles_dir: Path              # oracle 根目录（scenario.json.oracles_dir，缺省 oracles/）
    # 本 scenario 内被 round 引用的 update（update_id -> 已加载 UpdateSpec）
    updates: dict[str, "UpdateSpec"] = field(default_factory=dict)


@dataclass
class ArcManifest:
    """test_samples/<ts_id>/arcs/<arc_id>/arc.json。"""

    arc_id: str
    test_sample_id: str
    version: str                   # base/pro 等版本轴（原 project_version）；可空
    desc: str                      # 面向人类
    select_prompt: str             # 面向 agent 的英文一句话（agent_choice 菜单用）
    unlock: list[dict[str, Any]]   # unlock 谓词（原始 dict，由 arc_scheduler 解析求值）
    scenarios: list[ScenarioManifest]    # 已加载并排序的 scenario 列表（弧内严格保序）
    arc_audit: Optional[ScenarioManifest]  # 弧尾 self-audit（复用 scenario 结构，可选）
    arc_dir: Path


@dataclass
class TestSampleManifest:
    """test_samples/<ts_id>/manifest.json 在内存中的形态。

    一个 test_sample 是独立隔离的大型项目：独立 workspace / session / MEMORY.md。
    """

    test_sample_id: str
    desc: str
    manifest_path: Path
    ts_dir: Path
    workspace_template: Optional[Path]            # 绝对路径；None → 无初始模板（由 arc1 首轮 update 铺设）
    arcs: dict[str, ArcManifest]                  # arc_id -> 已加载 ArcManifest（保持声明顺序）
    first_arc: str
    completion_criterion: Literal["visited", "passed"]


@dataclass
class TestsConfig:
    tests_path: Path
    name: str
    test_samples: dict[str, Path]                 # ts_id -> manifest.json 绝对路径（保持声明顺序）
    mode: Literal["cascade", "oracle"]
    seed: int
    extras: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Oracle
# ---------------------------------------------------------------------------


@dataclass
class OracleProduct:
    """scenarios/<sid>/oracles/<round_id>.json 中描述的预期产物。

    简单实现：path → 文件内容（utf-8）。binary / 大体量产物可后续加 content_ref。
    """

    round_id: str
    files: dict[str, str]                         # workspace 相对路径 → utf-8 内容


# ---------------------------------------------------------------------------
# Preferences
# ---------------------------------------------------------------------------


@dataclass
class PreferenceResult:
    """偏好类 check() 返回值。"""

    satisfied: bool
    hint: str = ""                                # 反馈给 agent 的简短提示
    detail: dict[str, Any] = field(default_factory=dict)


@dataclass
class PreferenceExposure:
    """单次 exposure 的事件记录，供 adherence curve / 报告使用。

    粒度参考：``test_sample → arc → scenario → round``。``scenario_id`` 是数据侧稳定
    标识，``day_idx`` 是该 scenario 在 test_sample 内累计出现的序号（agent 端看到
    ``day{n}``）。scheduler 每个 test_sample 一份，故 exposure_index 是该 test_sample 内累计。
    """

    tag: str
    round_id: str
    scenario_id: str                              # 数据侧 id（== ScenarioManifest.scenario_id）
    day_idx: int                                  # test_sample 内累计 scenario 序号（agent 侧 day{n}）
    arc_id: str
    test_sample_id: str
    exposure_index: int                           # 该 tag 在本 test_sample 内第几次 exposure（从 1 起）
    satisfied: bool
    skipped_due_to_user_override: bool = False
    in_explicit_period: bool = True
    hint: str = ""
    # 仅 ema mode 填充：本次 check 之后该 tag 的 EMA 值；fixed mode 下也维护（诊断用）
    adherence_ema: Optional[float] = None
    # 仅 ema mode 填充：本次 check 之后该 EMA 落在哪个 band（'low'/'mid'/'high'）
    band: Optional[str] = None


# ---------------------------------------------------------------------------
# Persona (v2 hook only)
# ---------------------------------------------------------------------------


@dataclass
class Persona:
    """v2 多人格 user。v1 仅作为 hook 占位。"""

    persona_id: str
    name: str
    role: str
    tone: str
    preference_scope_overrides: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


@dataclass
class RoundEval:
    """单 round 评分（最细粒度）。

    - ``scenario_id``：数据侧稳定 id；
    - ``day_idx``：该 scenario 在 test_sample 内累计出现的序号（agent 侧只看到 ``day{n}``）；
    - ``test_sample_id`` / ``arc_id``：所属上层。
    """

    round_id: str
    scenario_id: str
    day_idx: int
    arc_id: str
    test_sample_id: str
    passed: bool
    raw_score: float                              # exec_check 给的原始分数（0 或 1）
    final_score: float                            # 偏好静默期扣分后的最终分数
    exit_code: int
    stdout: str
    stderr: str
    duration_sec: float
    violated_preferences: list[str] = field(default_factory=list)
    # 数据源相对路径（相对 data_root）—— 便于结果反查源题
    source_round_ref: Optional[str] = None        # e.g. "test_samples/ts_webapp/arcs/arc1/scenarios/s1/scenario.json#rounds[0]"


@dataclass
class ScenarioResult:
    """单 scenario（== 一个 questions.json / scenario.json）的聚合结果。"""

    scenario_id: str                              # 数据侧 id（== ScenarioManifest.scenario_id）
    day_idx: int                                  # 该 scenario 在 test_sample 内的序号
    test_sample_id: str
    version: str                                  # 所在 arc 的版本（base/pro 等）
    arc_id: str
    arc_seq: int                                  # scenario 在 arc 内的序号（弧内固定序）
    rounds: list[RoundEval]
    # —— 聚合 ——
    tcr: float = 0.0
    final_score_mean: float = 0.0
    scenario_audit_passed: Optional[bool] = None   # 仅当 scenario.json 定义了 scenario_audit 才非 None
    passed: bool = False                           # scenario_audit 不 fail + 全 round.passed
    # —— 局部偏好观测 ——
    adherence_in_scenario: dict[str, float] = field(default_factory=dict)
    violated_preferences_count: dict[str, int] = field(default_factory=dict)
    # —— 局部状态信号 ——
    had_silent_failure: bool = False
    # —— update / callback 局部 ——
    update_reflections: dict[str, dict] = field(default_factory=dict)  # uid -> {checked, passed, rate}
    callback_rate: Optional[float] = None
    # 数据源相对路径
    source_scenario_ref: Optional[str] = None      # e.g. "scenarios/sprint8__1/scenario.json"


@dataclass
class ArcResult:
    arc_id: str
    test_sample_id: str
    version: str
    scenarios: list[ScenarioResult]
    rounds: list[RoundEval]                       # 扁平镜像（含 scenario_audit / arc_audit 衍生 round），向后兼容
    arc_audit_passed: Optional[bool]              # 弧尾 self-audit 通过与否
    visited: bool = True                          # cascade 无覆盖下"经过即视为完成"
    passed: bool = False                          # arc_audit + rounds 全过才算 pass
    # 'continuous' scheduling 模式额外消费的字段（由 session_runner 在弧结束时填）
    had_silent_failure: bool = False
    adherence_snapshot: dict[str, float] = field(default_factory=dict)
    # 数据源相对路径
    source_arc_ref: Optional[str] = None          # e.g. "test_samples/ts_webapp/arcs/arc1/arc.json"


@dataclass
class TestSampleResult:
    """跨 arc 同 test_sample 的 rollup（run-level 才能拼出来）。"""

    test_sample_id: str
    arc_ids: list[str]
    versions: list[str]                           # 与 arc_ids 一一对应的 arc.version
    scenario_ids: list[str]
    rounds_total: int = 0
    rounds_passed: int = 0
    tcr: float = 0.0
    scenarios_total: int = 0
    scenarios_passed: int = 0
    scenario_pass_rate: float = 0.0
    # path-dependence 视图：每个 version / arc 的 tcr 序列（按 arc 完成时序）
    version_progression: list[dict] = field(default_factory=list)  # [{arc_id, version, tcr, passed}]
    # agent 在 arc DAG 上的推进轨迹
    arc_progression: dict[str, Any] = field(default_factory=dict)  # {visited:[...], depth:int, reached_audit:bool}
    adherence_rollup: dict[str, float] = field(default_factory=dict)
    had_silent_failure_arcs: int = 0


# ---------------------------------------------------------------------------
# Message type registry (agent.messages 详细定义；此处仅暴露符号常量)
# ---------------------------------------------------------------------------


# 消息 role/type 全集；session.jsonl 反序列化 / harness 组装 messages 时统一使用。
MSG_ROLE_SYSTEM = "system"
MSG_ROLE_USER = "user"
MSG_ROLE_ASSISTANT = "assistant"
MSG_ROLE_TOOL_RESULT = "tool_result"
# 特殊系统子类型（参考 claude-code）：边界标记，不参与 provider messages 拼装的内容部分，
# 但 transcript 重建时遇到它即对前面的内容做截断 + 拼接其 summary。
MSG_SUBTYPE_COMPACT_BOUNDARY = "compact_boundary"


# ---------------------------------------------------------------------------
# Provider Protocol
# ---------------------------------------------------------------------------


class Provider(Protocol):
    """所有 provider 须实现该接口。"""

    name: str

    async def chat(
        self,
        *,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
        **kwargs: Any,
    ) -> dict[str, Any]:
        """返回标准化 ``{content, tool_calls, raw_usage, usage_normalized, finish_reason}``。"""
        ...
