"""装配工厂：把 vendored harness 的各部件组装成一个可运行的 main :class:`AgentHarness`。

参考 ArcBench ``runner/run_runner.py`` 的组装流程，但额外装配 clawarena-native 引入的
三件能力：``Workflow`` 工具（异步后台 + <task-notification>）、``SessionHistory`` 工具
（跨 session 历史读取）、以及对应的 ``BackgroundRegistry`` / ``SessionHistoryStore``。

ClawArena 的调度按 round 调用一次 ``engine.run_agent``；由于 :class:`SessionLog` 每次都
从磁盘重读，同一 session 的多 round 通过"每 round 用同一 active session jsonl 重建 harness"
自然续接。
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from .agent.background import BackgroundRegistry
from .agent.compaction import Compactor, Microcompactor, MicrocompactorConfig
from .agent.harness import AgentHarness, HarnessConfig
from .agent.session_history import SessionHistoryStore
from .agent.session_log import SessionLog
from .agent.subagent import SubagentManager
from .prompts import render_main_system_prompt
from .provider import build_provider
from .sandbox import AccessibleScope, ReadTracker
from .tokenizer import UnifiedTokenizer
from .tools import BASIC_TOOLS, BaseTool, schema_format_kwargs
from .tools.agent_tool import AgentTool
from .tools.ls import LSTool
from .tools.session_history import SessionHistoryTool
from .tools.workflow import WorkflowTool
from .types import ModelBundle


def build_tokenizer(config_dict: dict[str, Any]) -> UnifiedTokenizer:
    tok = config_dict.get("tokenizer", {}) or {}
    tmpl = config_dict.get("chat_template", {}) or {}
    return UnifiedTokenizer(
        tokenizer_source=str(tok.get("source", "qwen3")),
        template_source=str(tmpl.get("source", tok.get("source", "qwen3"))),
    )


def _make_reinjection_reader(config_dict: dict[str, Any]):
    cap = int((config_dict.get("read", {}) or {}).get("max_text_bytes", 524288))

    async def _reader(path: str) -> Optional[str]:
        try:
            p = Path(path)
            if not p.is_file():
                return None
            return p.read_bytes()[:cap].decode("utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            return None

    return _reader


def build_main_harness(
    *,
    bundle: ModelBundle,
    config_dict: dict[str, Any],
    workspace_root: Path,
    sessions_dir: Path,
    active_session_jsonl: Path,
    active_session_id: str,
    tokenizer: Optional[UnifiedTokenizer] = None,
    system_prompt: Optional[str] = None,
    env_reminder: Optional[str] = None,
    enable_workflow: bool = True,
    enable_session_history: bool = True,
    enable_compaction: bool = True,
) -> AgentHarness:
    """组装并返回 main :class:`AgentHarness`（已 wire background / session_history /
    workflow_script_dir / subagent_manager）。"""
    sessions_dir = Path(sessions_dir)
    workspace_root = Path(workspace_root)
    sessions_dir.mkdir(parents=True, exist_ok=True)
    workspace_root.mkdir(parents=True, exist_ok=True)

    if tokenizer is None:
        tokenizer = build_tokenizer(config_dict)

    main_provider = build_provider(bundle.main)
    subagent_provider = build_provider(bundle.subagent)
    compaction_provider = build_provider(bundle.compaction)

    usage_thresholds = list(
        (config_dict.get("usage_hint", {}) or {}).get(
            "thresholds_pct", [50, 60, 70, 80, 85, 90, 95]
        )
    )
    memory_thresholds = list(
        (config_dict.get("memory", {}) or {}).get(
            "persist_reminder_thresholds_pct", [80, 90]
        )
    )

    # ---- tools：基础 6 件 + LS + Agent + Workflow + SessionHistory ----
    schema_kwargs = schema_format_kwargs(config_dict, bundle.main.effective_modalities)
    tools_enabled = list(
        (config_dict.get("tools", {}) or {}).get("enabled") or list(BASIC_TOOLS)
    )
    tools: dict[str, BaseTool] = {}
    tool_schemas: list[dict[str, Any]] = []
    for name in tools_enabled:
        cls = BASIC_TOOLS.get(name)
        if cls is None:
            continue
        tools[name] = cls()
        tool_schemas.append(cls.schema(**schema_kwargs))
    # LS + Agent 始终装配（与 BASIC_TOOLS 平级）
    tools["LS"] = LSTool()
    tool_schemas.append(LSTool.schema(**schema_kwargs))
    tools["Agent"] = AgentTool()
    tool_schemas.append(AgentTool.schema())
    wf_cfg = config_dict.get("workflow", {}) or {}
    if enable_workflow:
        tools["Workflow"] = WorkflowTool()
        tool_schemas.append(
            WorkflowTool.schema(
                max_concurrency=int(wf_cfg.get("max_concurrency", 8)),
                max_agents=int(wf_cfg.get("max_agents", 1000)),
            )
        )
    if enable_session_history:
        tools["SessionHistory"] = SessionHistoryTool()
        tool_schemas.append(SessionHistoryTool.schema())

    scope = AccessibleScope(allowed=[workspace_root], workspace_root=workspace_root)
    read_tracker = ReadTracker()
    session_log = SessionLog(Path(active_session_jsonl))

    token_limit = int((config_dict.get("token_limits", {}) or {}).get("main_agent", 200000))

    compactor = None
    microcompactor = None
    if enable_compaction:
        comp_cfg = config_dict.get("compaction", {}) or {}
        reinj_cfg = config_dict.get("post_compact_reinjection", {}) or {}
        compactor = Compactor(
            provider=compaction_provider,
            tokenizer=tokenizer,
            token_limit=token_limit,
            auto_compact_buffer_tokens=int(comp_cfg.get("auto_compact_buffer_tokens", 13000)),
            reserved_summary_output_tokens=int(
                comp_cfg.get("reserved_summary_output_tokens", 20000)
            ),
            force_pct=int(comp_cfg.get("force_pct", 92)),
            max_consecutive_failures=int(comp_cfg.get("max_consecutive_failures", 3)),
            summarizer_max_output_tokens=int(comp_cfg.get("summarizer_max_output_tokens", 20000)),
            reinjection_enabled=bool(reinj_cfg.get("enabled", True)),
            reinjection_token_budget=int(reinj_cfg.get("token_budget", 50000)),
            reinjection_max_files=int(reinj_cfg.get("max_files", 5)),
            reinjection_max_tokens_per_file=int(reinj_cfg.get("max_tokens_per_file", 5000)),
            reinjection_reader=_make_reinjection_reader(config_dict),
            events_log_path=sessions_dir / "compaction_events.jsonl",
        )
        mc_cfg = config_dict.get("microcompact", {}) or {}
        microcompactor = Microcompactor(
            tokenizer=tokenizer,
            cfg=MicrocompactorConfig(
                enabled=bool(mc_cfg.get("enabled", True)),
                stale_after_messages=int(mc_cfg.get("stale_after_messages", 30)),
                size_threshold_tokens=int(mc_cfg.get("size_threshold_tokens", 800)),
                max_redactions_per_event=int(mc_cfg.get("max_redactions_per_event", 8)),
            ),
        )

    sub_cfg = config_dict.get("subagent", {}) or {}
    sub_manager = SubagentManager(
        provider=subagent_provider,
        tokenizer=tokenizer,
        workspace_root=workspace_root,
        sessions_dir=sessions_dir,
        config_dict=config_dict,
        agent_modalities=bundle.subagent.effective_modalities,
        token_limit=int(sub_cfg.get("token_limit", 100000)),
        max_iterations=int(sub_cfg.get("max_iterations", 30)),
        explore_enabled=bool(sub_cfg.get("explore_enabled", True)),
        general_purpose_enabled=bool(sub_cfg.get("general_purpose_enabled", True)),
    )

    h_cfg = HarnessConfig(
        token_limit=token_limit,
        usage_thresholds_pct=usage_thresholds,
        always_hint_on_real_user=bool(
            (config_dict.get("usage_hint", {}) or {}).get("always_on_real_user", True)
        ),
        max_iterations=int((config_dict.get("agent_loop", {}) or {}).get("max_iterations", 80)),
        memory_notification_enabled=bool(
            (config_dict.get("memory", {}) or {}).get("notification_enabled", True)
        ),
        memory_persist_thresholds=memory_thresholds,
    )

    harness = AgentHarness(
        agent_id="main",
        system_prompt=system_prompt
        or render_main_system_prompt(usage_thresholds_pct=usage_thresholds),
        provider=main_provider,
        tools=tools,
        tool_schemas=tool_schemas,
        scope=scope,
        read_tracker=read_tracker,
        cwd=workspace_root,
        tokenizer=tokenizer,
        cfg=h_cfg,
        config_dict=config_dict,
        session_log=session_log,
        compactor=compactor,
        microcompactor=microcompactor,
        agent_modalities=bundle.main.effective_modalities,
        subagent_manager=sub_manager,
    )

    # ---- wire clawarena-native 的三件能力 ----
    harness.background = BackgroundRegistry(harness.inject_background_user)
    if enable_workflow:
        wf_dir = sessions_dir / "workflows"
        harness.workflow_script_dir = wf_dir
    if enable_session_history:
        harness.session_history = SessionHistoryStore(sessions_dir, active_session_id)

    if env_reminder:
        harness.queue_system_reminder(env_reminder)

    return harness
