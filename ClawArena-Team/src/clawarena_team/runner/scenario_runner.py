"""Single-scenario scheduling.

Flow:
1. Copy the workspace template to results/<run_id>/<scenario_id>/work/;
2. Instantiate the main agent's AgentHarness and SubagentManager;
3. For each round:
   - apply the file injections for the round's update_ids (new/replace);
   - take the round question (with feedback from the previous round prepended);
   - send it to the main agent and wait until the round's end condition is met;
   - run exec_check scoring and write evals/<round_id>.json;
4. End of scenario: wait for all background subagents to finish, then write metadata.json.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import shlex
import shutil
import time
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)

from ..agent import AgentHarness, SubagentManager, TokenLimitExceeded
from ..agent.background import BackgroundRegistry
from ..agent.harness import HarnessConfig
from ..persistence.session_io import write_session_jsonl
from ..persistence.session_md import write_session_md
from ..prompts import (
    ENVIRONMENT_REMINDER,
    WORKSPACE_UPDATE_REMINDER,
    WORKSPACE_UPDATE_USER_PREFIX,
    build_main_agent_system_prompt,
    render_feedback,
)
from ..provider import build_provider
from ..sandbox import AccessibleScope, ReadTracker
from ..scoring.exec_check import run_exec_check
from ..scoring.metrics import compute_scenario_metrics
from ..tokenizer import UnifiedTokenizer
from ..tools import BASIC_TOOLS, SUBAGENT_TOOLS, WORKFLOW_TOOLS
from ..tools.subagent import CreateSubagentTool
from ..tools.workflow import WorkflowTool
from ..types import (
    DatasetManifests,
    ModelBundle,
    RoundEval,
    ScenarioManifest,
)


_PLACEHOLDER_RE = re.compile(r"\$\{([a-zA-Z_][a-zA-Z0-9_]*)\}")


def _format_command(template: str, mapping: dict[str, str]) -> str:
    """Substitute path variables for ``${var}`` placeholders; path values are safely
    quoted via ``shlex.quote``.

    Supported placeholders:
    - ``${workspace}``: absolute path of this run's workspace copy (the check
      typically uses it as cwd).
    - ``${scripts}``: absolute path of the scenario's ``checks/`` directory, for
      invocations like ``python ${scripts}/check_q1.py``.
    - ``${scenario_dir}``: absolute path of the directory containing the scenario manifest.
    - ``${scenario_id}``: the scenario ID string.

    Unrecognized placeholders are kept verbatim, to allow the shell's own variable
    expansion.
    """

    def _replace(m: re.Match[str]) -> str:
        name = m.group(1)
        if name not in mapping:
            return m.group(0)
        return shlex.quote(str(mapping[name]))

    return _PLACEHOLDER_RE.sub(_replace, template)


def _apply_update(workspace_root: Path, op: str, src: Path, dst_rel: str) -> None:
    dst = workspace_root / dst_rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if op == "new":
        if dst.exists():
            raise FileExistsError(f"update 'new' but dst exists: {dst}")
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    elif op == "replace":
        if dst.exists():
            if dst.is_dir():
                shutil.rmtree(dst)
            else:
                dst.unlink()
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    else:
        raise ValueError(f"unknown update op: {op}")


class ScenarioRunner:
    def __init__(
        self,
        *,
        scenario: ScenarioManifest,
        manifests: DatasetManifests,
        model_bundle: ModelBundle,
        tokenizer: UnifiedTokenizer,
        config_dict: dict[str, Any],
        run_dir: Path,
    ):
        self.scenario = scenario
        self.manifests = manifests
        self.model_bundle = model_bundle
        self.tokenizer = tokenizer
        self.config_dict = config_dict
        self.run_dir = run_dir
        self.scenario_out = run_dir / scenario.scenario_id
        self.work_root = self.scenario_out / "work"
        self.sessions_dir = self.scenario_out / "sessions"
        self.evals_dir = self.scenario_out / "evals"
        self.round_evals: list[RoundEval] = []

    def _setup_workspace(self) -> None:
        if self.work_root.exists():
            shutil.rmtree(self.work_root)
        shutil.copytree(self.scenario.workspace_template, self.work_root)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        # The ${workspace} that check_*.py receives is work_root; they read
        # ${workspace}/sessions/main.jsonl. So the session stream must also be written
        # to work_root/sessions/, otherwise all session-dependent checks (delegation,
        # session reuse, over-scope scans) can never read it and either falsely fail or
        # silently skip (warn-only). The canonical copy is still kept in
        # scenario_out/sessions/ (results / inspection backward compatibility).
        self.work_sessions_dir = self.work_root / "sessions"
        self.work_sessions_dir.mkdir(parents=True, exist_ok=True)
        self.evals_dir.mkdir(parents=True, exist_ok=True)

    def _build_main_harness(self) -> tuple[AgentHarness, SubagentManager]:
        accessible = [self.work_root / sub for sub in self.scenario.main_agent_accessible_paths]
        main_scope = AccessibleScope(accessible, scenario_root=self.work_root)
        main_tracker = ReadTracker()
        delegable = [self.work_root / sub for sub in self.scenario.main_agent_delegable_paths]
        # Used to validate the subagent's accessible_paths: main's readable paths ∪
        # the delegable paths. delegable is only for authorization and does not enter
        # main's own scope (main itself is still out of scope for them).
        grant_scope = AccessibleScope(accessible + delegable, scenario_root=self.work_root)

        usage_thresholds = self.config_dict.get("usage_hint", {}).get(
            "thresholds_pct", [50, 60, 70, 80, 85, 90, 95]
        )
        sub_token_limit = int(self.config_dict.get("token_limits", {}).get("subagent", 100000))
        cfg = HarnessConfig(
            token_limit=int(self.config_dict.get("token_limits", {}).get("main_agent", 200000)),
            usage_thresholds_pct=usage_thresholds,
            always_hint_on_real_user=True,
            max_iterations=int(self.config_dict.get("agent_loop", {}).get("max_iterations", 80)),
        )

        manager = SubagentManager(
            scenario_root=self.work_root,
            creator_scope=grant_scope,
            model_bundle=self.model_bundle,
            tokenizer=self.tokenizer,
            config_dict=self.config_dict,
            sub_token_limit=sub_token_limit,
            usage_thresholds_pct=usage_thresholds,
            max_iterations=cfg.max_iterations,
        )

        # Tool set: the main agent has the basic + subagent families, then filtered by
        # the tools.enabled whitelist. When the whitelist is None there is no filtering
        # (all enabled); when it is a list, only tools in the list are kept.
        enabled_cfg = self.config_dict.get("tools", {}).get("enabled")
        if enabled_cfg is None:
            enabled_set: set[str] | None = None
        else:
            enabled_set = set(enabled_cfg)
            all_registered = set(BASIC_TOOLS) | set(SUBAGENT_TOOLS) | set(WORKFLOW_TOOLS)
            unknown = enabled_set - all_registered
            if unknown:
                raise ValueError(
                    f"tools.enabled contains unknown tool names: {sorted(unknown)}; "
                    f"valid names are {sorted(all_registered)}"
                )

        def _is_enabled(name: str) -> bool:
            return enabled_set is None or name in enabled_set

        tools_inst = {n: cls() for n, cls in BASIC_TOOLS.items() if _is_enabled(n)}
        tools_inst.update({n: cls() for n, cls in SUBAGENT_TOOLS.items() if _is_enabled(n)})
        tools_inst.update({n: cls() for n, cls in WORKFLOW_TOOLS.items() if _is_enabled(n)})

        # Build the pool listing description for the create_subagent schema (exposes key/name/effective_modalities)
        pool_lines = [
            f"  - key={k.value}  name={e.name}  modalities=[{', '.join(e.effective_modalities)}]"
            for k, e in self.model_bundle.pool.items()
        ]
        pool_listing = "\n".join(pool_lines) or "(empty)"
        pool_keys = "/".join(k.value for k in self.model_bundle.pool.keys())

        main_modalities = list(self.model_bundle.main.modalities)
        main_limits = dict(self.model_bundle.main.modality_limits)

        # Config-driven tool description parameters (ensures the prompt matches runtime; not hardcoded).
        read_cfg = self.config_dict.get("read", {})
        notice_bytes = int(read_cfg.get("notice_bytes", 32768))
        hard_bytes = int(read_cfg.get("hard_bytes", 262144))
        bash_default_ms = int(self.config_dict.get("bash", {}).get("default_timeout_ms", 120000))
        wf_cfg = self.config_dict.get("workflow", {})
        so_runsub = self.config_dict.get("structured_output", {}).get("runsubagent_enabled", False)
        basic_kwargs = dict(
            modalities=main_modalities,
            modality_limits=main_limits,
            notice_bytes=notice_bytes,
            hard_bytes=hard_bytes,
            default_timeout_ms=bash_default_ms,
        )

        schemas: list[dict[str, Any]] = []
        for n, cls in BASIC_TOOLS.items():
            if not _is_enabled(n):
                continue
            schemas.append(cls.schema(**basic_kwargs))
        for n, cls in SUBAGENT_TOOLS.items():
            if not _is_enabled(n):
                continue
            if n == CreateSubagentTool.name:
                schemas.append(cls.schema(
                    pool_keys=pool_keys,
                    pool_listing=pool_listing,
                    subagent_token_limit=sub_token_limit,
                ))
            else:
                schemas.append(cls.schema(structured_output_enabled=so_runsub))
        for n, cls in WORKFLOW_TOOLS.items():
            if not _is_enabled(n):
                continue
            if n == WorkflowTool.name:
                schemas.append(cls.schema(
                    pool_keys=pool_keys,
                    pool_listing=pool_listing,
                    max_concurrency=int(wf_cfg.get("max_concurrency", 8)),
                    max_agents=int(wf_cfg.get("max_agents", 1000)),
                ))
            else:
                schemas.append(cls.schema())

        # Dynamically assemble the main system prompt: varies with tools.enabled and the
        # usage thresholds / large-file thresholds.
        main_system_prompt = build_main_agent_system_prompt(
            enabled_tools=enabled_set,
            thresholds_pct=usage_thresholds,
            delegate_notice_kib=notice_bytes // 1024,
        )

        provider = build_provider(self.model_bundle.main)
        harness = AgentHarness(
            agent_id="main",
            system_prompt=main_system_prompt,
            provider=provider,
            tools=tools_inst,
            tool_schemas=schemas,
            scope=main_scope,
            read_tracker=main_tracker,
            cwd=self.work_root,
            tokenizer=self.tokenizer,
            cfg=cfg,
            config_dict=self.config_dict,
            agent_modalities=main_modalities,
            modality_limits=main_limits,
            subagent_manager=manager,
        )
        # The unified background-task registry is attached to the main harness;
        # attach_main uses it so the manager goes through the same registry.
        harness.background = BackgroundRegistry(harness.queue_task_notification)
        # Workflow script backup directory: workflows/ alongside the scenario's sessions/.
        wf_dirname = self.config_dict.get("workflow", {}).get("script_dirname", "workflows")
        harness.workflow_script_dir = self.scenario_out / wf_dirname
        manager.attach_main(harness)

        # Inject the Environment <system-reminder> before the first round's entry. The
        # text is assembled from the enabled tools to avoid hardcoding.
        subagent_on = _is_enabled(CreateSubagentTool.name) and _is_enabled("RunSubagent")
        workflow_on = _is_enabled(WorkflowTool.name)
        accessible_tools = "/".join(
            t for t in ("Read", "Edit", "Write", "Grep", "Glob") if _is_enabled(t)
        ) or "(no direct file tools)"
        if subagent_on and workflow_on:
            delegate_hint = "grant them to a subagent (CreateSubagent) or a Workflow agent (defineAgent)"
        elif subagent_on:
            delegate_hint = "only grant them to a subagent in CreateSubagent.accessible_paths"
        elif workflow_on:
            delegate_hint = "only reach them through a Workflow agent (defineAgent.accessible_paths)"
        else:
            delegate_hint = "they are not reachable in this configuration"
        env_body = ENVIRONMENT_REMINDER.format(
            scenario_id=self.scenario.scenario_id,
            cwd=str(self.work_root),
            accessible_tools=accessible_tools,
            accessible_paths="\n".join(f"    - {p}" for p in accessible) or "    (none)",
            delegate_hint=delegate_hint,
            delegable_paths="\n".join(f"    - {p}" for p in delegable) or "    (none)",
            modalities=", ".join(main_modalities),
            token_limit=f"{cfg.token_limit:,}",
            subagent_token_limit=f"{sub_token_limit:,}",
            pool_keys=pool_keys or "(empty)",
        )
        harness.queue_system_reminder(env_body)
        return harness, manager

    def _flush_sessions(self, harness, manager) -> None:
        """Write the session jsonl of main + each sub to two places: the canonical
        scenario_out/sessions/ (results / inspection) and work_root/sessions/ (the
        ${workspace}/sessions/ that the check actually reads).
        """
        for base in (self.sessions_dir, self.work_sessions_dir):
            write_session_jsonl(base / "main.jsonl", harness.turns, owner="main")
            for sub_id, rec in manager.records.items():
                for sid, h in rec.harnesses.items():
                    write_session_jsonl(
                        base / f"sub_{sub_id}_{sid}.jsonl",
                        h.turns,
                        owner=f"{sub_id}:{sid}",
                    )

    @staticmethod
    def _seal_dangling_tool_uses(harness: AgentHarness) -> int:
        """When a round is cancelled by the outer ``wait_for``, the ``tool_calls`` the
        assistant already emitted may not all have received their corresponding
        ``tool_result`` (the execution coro was cancelled mid-way). When a later round
        resends the message to Anthropic, it is rejected with a 4xx (``messages.N:
        tool_use ids were found without tool_result blocks immediately after``),
        causing an L2 fast-fail and killing the whole scenario.

        This function scans the tail of the last ``assistant + tool_calls`` group and,
        for each tool_call_id that did not receive a ``tool_result``, injects a
        synthetic ``tool_result`` (marking the cancellation reason), so the provider
        call payload of a later round is valid.
        Returns the number of injected entries (0=clean, >0=had dangling).
        """
        from ..agent.harness import HarnessTurn
        turns = harness.turns
        # Walk back from the tail to find the most recent ``assistant + tool_calls`` group
        target_idx = None
        for i in range(len(turns) - 1, -1, -1):
            if turns[i].role == "assistant":
                if turns[i].tool_calls:
                    target_idx = i
                break  # any assistant terminates the scan: only handle the most recent assistant's dangling
        if target_idx is None:
            return 0
        asst = turns[target_idx]
        following = turns[target_idx + 1 :]
        seen_ids: set[str] = {
            t.tool_call_id for t in following
            if t.role == "tool_result" and t.tool_call_id
        }
        injected = 0
        for tc in asst.tool_calls:
            tc_id = (tc.get("id") if isinstance(tc, dict) else getattr(tc, "id", "")) or ""
            if tc_id and tc_id not in seen_ids:
                turns.append(
                    HarnessTurn(
                        role="tool_result",
                        content=(
                            "[round cancelled by CATEAM_ROUND_TIMEOUT_SEC; "
                            "tool execution did not complete in time]"
                        ),
                        tool_call_id=tc_id,
                        timestamp=time.time(),
                    )
                )
                injected += 1
        return injected

    async def _run_round_body(
        self,
        harness: AgentHarness,
        manager: SubagentManager,
        question_body: str,
    ) -> None:
        """The await body of a single round: push the user message → run the agent →
        wait for backgrounds to finish.

        Extracted as a separate coroutine so that when ``CATEAM_ROUND_TIMEOUT_SEC>0`` the
        whole thing is wrapped by ``asyncio.wait_for``; a permanent hang anywhere
        (provider silently dropping the socket, a background subagent deadlock, some
        await inside send_user) will be cancelled.
        """
        await harness.send_user(question_body, is_real_question=True)
        await manager.wait_for_backgrounds()

    def _exec_check(self, round_id: str, eval_spec, started_at: float) -> RoundEval:
        cmd = _format_command(
            eval_spec.command,
            {
                "workspace": str(self.work_root),
                "scripts": str(self.scenario.scripts_dir),
                "scenario_dir": str(self.scenario.scenario_dir),
                "scenario_id": self.scenario.scenario_id,
            },
        )
        result = run_exec_check(
            command=cmd,
            cwd=self.work_root,
            expect_exit=eval_spec.expect_exit,
            timeout=eval_spec.timeout,
            expect_stdout=eval_spec.expect_stdout,
            regex=eval_spec.expect_stdout_regex,
        )
        re_obj = RoundEval(
            round_id=round_id,
            passed=result["passed"],
            exit_code=result["exit_code"],
            stdout=result["stdout"],
            stderr=result["stderr"],
            duration_sec=time.time() - started_at,
        )
        (self.evals_dir / f"{round_id}.json").write_text(
            json.dumps(
                {
                    "round_id": re_obj.round_id,
                    "passed": re_obj.passed,
                    "exit_code": re_obj.exit_code,
                    "stdout": re_obj.stdout,
                    "stderr": re_obj.stderr,
                    "duration_sec": re_obj.duration_sec,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        return re_obj

    async def run(self) -> dict[str, Any]:
        self._setup_workspace()
        harness, manager = self._build_main_harness()

        prev_feedback: tuple[str, str, str] | None = None  # (prev_round_id, verdict, text)
        final_feedback_mode = self.config_dict.get("scenario", {}).get("final_feedback_mode", "skip")

        for idx, rnd in enumerate(self.scenario.rounds):
            # apply updates — collect the per-op change list so we can both
            # inject a workspace-update <system-reminder> for the agent and
            # prepend an explicit "I've updated some files" line to the user
            # turn (so the agent cannot miss it even if it ignores reminders).
            update_new_files: list[str] = []
            update_replaced_files: list[str] = []
            for uid in rnd.update_ids:
                ug = self.scenario.updates.get(uid)
                if ug is None:
                    raise KeyError(f"update_id {uid} not defined in manifest")
                for uf in ug.files:
                    _apply_update(self.work_root, ug.op, uf.src, uf.dst_rel)
                    if ug.op == "new":
                        update_new_files.append(uf.dst_rel)
                    elif ug.op == "replace":
                        update_replaced_files.append(uf.dst_rel)

            if update_new_files or update_replaced_files:
                reminder_body = WORKSPACE_UPDATE_REMINDER.format(
                    new_files="\n".join(f"    - {p}" for p in update_new_files) or "    (none)",
                    replaced_files="\n".join(f"    - {p}" for p in update_replaced_files) or "    (none)",
                )
                harness.queue_system_reminder(reminder_body)

            question_body = rnd.question
            if prev_feedback is not None:
                _prev_id, verdict, text = prev_feedback
                question_body = render_feedback(
                    verdict=verdict,
                    feedback_text=text,
                    question=rnd.question,
                )
            if update_new_files or update_replaced_files:
                question_body = WORKSPACE_UPDATE_USER_PREFIX + question_body

            started_at = time.time()
            # Per-round wall-clock fallback: when any await within a round (send_user/
            # _run_loop/chat/wait_for_backgrounds, etc.) hangs permanently, do not let
            # that single round burn the whole scenario budget.
            # ``CATEAM_ROUND_TIMEOUT_SEC=0`` (default) disables it; when >0, a round that
            # times out is marked failed and the next round continues — finer-grained
            # than the scenario-level wall-clock fallback, and can rescue scenarios where
            # one round deadlocks but the other rounds are healthy (e.g.
            # s_security_pcap_triage).
            round_timeout_sec = float(
                os.environ.get("CATEAM_ROUND_TIMEOUT_SEC", "0") or "0"
            )
            try:
                if round_timeout_sec > 0:
                    await asyncio.wait_for(
                        self._run_round_body(harness, manager, question_body),
                        timeout=round_timeout_sec,
                    )
                else:
                    await harness.send_user(question_body, is_real_question=True)
                    # Wait for all unfinished backgrounds to complete (the round's end condition)
                    await manager.wait_for_backgrounds()
            except asyncio.TimeoutError:
                # Clean up dangling tool_use left after cancellation (the execution coro
                # being cancelled mid-way leaves tool_result missing); otherwise a later
                # round's chat() is rejected by Anthropic with a 4xx for invalid history,
                # an L2 fast-fail kills the whole scenario.
                sealed = self._seal_dangling_tool_uses(harness)
                log.warning(
                    "scenario %s round %s exceeded CATEAM_ROUND_TIMEOUT_SEC=%.0fs; "
                    "sealed %d dangling tool_use(s); marking round failed and continuing",
                    self.scenario.scenario_id, rnd.id, round_timeout_sec, sealed,
                )
                self.round_evals.append(
                    RoundEval(
                        round_id=rnd.id,
                        passed=False,
                        exit_code=-1,
                        stdout="",
                        stderr=f"round timeout {round_timeout_sec:.0f}s "
                               f"(CATEAM_ROUND_TIMEOUT_SEC);"
                               f"sealed {sealed} dangling tool_use; later rounds continue",
                        duration_sec=time.time() - started_at,
                    )
                )
                # This round counts as failed; continue to the next round (prev_feedback
                # is still assembled with the failure verdict).
                prev_feedback = (rnd.id, "incorrect", rnd.feedback.incorrect)
                continue
            except TokenLimitExceeded:
                # All remaining rounds of this scenario are scored 0
                for remaining in self.scenario.rounds[idx:]:
                    self.round_evals.append(
                        RoundEval(
                            round_id=remaining.id,
                            passed=False,
                            exit_code=-1,
                            stdout="",
                            stderr="main agent token limit exceeded",
                            duration_sec=0.0,
                        )
                    )
                break

            # Flush main + sub session jsonl BEFORE running the round's exec_check.
            # check_*.py decoy guards (e.g. CreateSubagent over-grant scans) and
            # session-reuse checks inspect ${workspace}/sessions/main.jsonl; flushing
            # to work_root/sessions/ here makes per-round evals actually see subagent
            # provisioning instead of being blind to it.
            self._flush_sessions(harness, manager)

            # Fix (fix/audit-top10 #2): _exec_check internally uses a blocking
            # subprocess.run; awaiting it directly would freeze the entire asyncio event
            # loop for up to timeout seconds, making --concurrency effectively useless.
            # Wrapping it in asyncio.to_thread gives true IO parallelism.
            round_eval = await asyncio.to_thread(self._exec_check, rnd.id, rnd.eval, started_at)
            self.round_evals.append(round_eval)

            verdict = "correct" if round_eval.passed else "incorrect"
            text = rnd.feedback.correct if round_eval.passed else rnd.feedback.incorrect
            is_last = idx == len(self.scenario.rounds) - 1
            if is_last:
                if final_feedback_mode == "extra_turn":
                    lead = (
                        "Nice — that one checked out. "
                        if verdict == "correct"
                        else "Hmm, the previous answer didn't quite land. "
                    )
                    closing = (
                        f"{lead}{text}\n\n"
                        "That's it for this scenario; any closing thoughts?"
                    )
                    try:
                        await harness.send_user(closing, is_real_question=True)
                        await manager.wait_for_backgrounds()
                    except TokenLimitExceeded:
                        pass
                prev_feedback = None
            else:
                prev_feedback = (rnd.id, verdict, text)

        # Write session jsonl (raw stream) — written to both scenario_out/sessions/ and work_root/sessions/
        self._flush_sessions(harness, manager)

        # Write session md (human-readable timeline; the session accumulates across rounds, not into round subdirectories)
        write_session_md(
            self.scenario_out / "session_main.md",
            owner="main",
            turns=harness.turns,
            system_prompt=harness.system_prompt,
            header_meta={
                "scenario_id": self.scenario.scenario_id,
                "model_id": self.model_bundle.main.model_id,
                "provider": self.model_bundle.main.provider,
                "modalities": list(harness.agent_modalities),
                "token_limit": harness.cfg.token_limit,
                "context_size_max": harness.context_size_max,
            },
        )
        for sub_id, rec in manager.records.items():
            for sid, h in rec.harnesses.items():
                pool_entry = self.model_bundle.pool.get(rec.spec.model_key)
                model_id = pool_entry.config.model_id if pool_entry else "?"
                provider = pool_entry.config.provider if pool_entry else "?"
                write_session_md(
                    self.scenario_out / f"session_{sub_id}_{sid}.md",
                    owner=f"{sub_id}:{sid}",
                    turns=h.turns,
                    system_prompt=h.system_prompt,
                    header_meta={
                        "subagent_id": sub_id,
                        "subagent_name": rec.spec.name,
                        "session_id": sid,
                        "model_key": rec.spec.model_key.value,
                        "model_id": model_id,
                        "provider": provider,
                        "tools_granted": list(rec.spec.tools),
                        "accessible_paths": [str(p) for p in rec.spec.accessible_paths],
                        "context_size_max": h.context_size_max,
                    },
                )

        metrics = compute_scenario_metrics(
            scenario_id=self.scenario.scenario_id,
            round_evals=self.round_evals,
            manager=manager,
            main_harness=harness,
        )

        metadata = self._assemble_metadata(harness=harness, metrics=metrics)
        (self.scenario_out / "metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
        )
        return metadata

    def _assemble_metadata(self, *, harness, metrics) -> dict[str, Any]:
        """Assemble this scenario's metadata dict (identical to what is persisted in
        metadata.json).

        ``harness`` is this scenario's main agent :class:`AgentHarness` (a local
        variable in ``run``, **not** a ``self`` attribute); ``token_limit`` must be
        taken from its ``cfg``, for ``report.py`` to compute the MCU% denominator.
        Extracted into a standalone method so unit tests can cover this assembly logic.
        """
        return {
            "scenario_id": self.scenario.scenario_id,
            "started_at": getattr(self, "_started_at", None),
            "finished_at": time.time(),
            # Fix (fix/audit-top10 #3): write this scenario's actual token_limit into
            # metadata, so report.py's MCU% denominator no longer always falls back to
            # 200000.
            "token_limit": getattr(harness.cfg, "token_limit", None),
            "rounds": [
                {"id": re_.round_id, "passed": re_.passed, "exit_code": re_.exit_code}
                for re_ in self.round_evals
            ],
            "metrics": metrics.__dict__,
            "models": {
                "main": {
                    "provider": self.model_bundle.main.provider,
                    "model_id": self.model_bundle.main.model_id,
                    "api_base": self.model_bundle.main.api_base,
                    "modalities": list(self.model_bundle.main.modalities),
                    "extra": dict(self.model_bundle.main.extra),
                },
                "pool": {k.value: e.info_for_metadata() for k, e in self.model_bundle.pool.items()},
            },
        }
