"""Infer pipeline — run agent on all tests."""

from __future__ import annotations

import asyncio
import json
import logging
import time
from pathlib import Path

from clawarena.adapters.base import FrameworkAdapter
from clawarena.adapters.registry import get_adapter
from clawarena.utils import framework_line
from clawarena.core.io import apply_overlay, load_questions, load_tests_config, write_json
from clawarena.core.provider import ModelConfig, resolve_model_config
from clawarena.core.types import RoundContext, TestContext, WorkCopy
from clawarena.prompts import standalone_feedback, with_feedback
from clawarena.utils import find_free_port, get_project_root

logger = logging.getLogger(__name__)

def normalize_alias(fw_name: str) -> str:
    if fw_name in ("claude", "claude-code", "claude_code"):
        return "claude-code"
    else:
        return fw_name

async def run_infer(
    tests_json_path: Path,
    framework: str,
    out_dir: Path,
    concurrency: int = 4,
    timeout: float = 300,
    retry: int = 1,
    cli_model: ModelConfig | None = None,
    overlay: str | None = None,
    test_ids: list[str] | None = None,
) -> None:
    """Main infer entry point.

    ``test_ids`` (if given) restricts execution to the listed test IDs from
    ``tests.json``. Unknown IDs raise ``ValueError`` so typos surface early
    instead of silently running everything.
    """
    base_dir = tests_json_path.parent
    tests_cfg = load_tests_config(tests_json_path)
    tests_cfg = apply_overlay(tests_cfg, overlay)

    if test_ids:
        wanted = set(test_ids)
        available = {t["id"] for t in tests_cfg["tests"]}
        unknown = wanted - available
        if unknown:
            raise ValueError(
                f"--test-id: unknown id(s) {sorted(unknown)}; "
                f"available: {sorted(available)}",
            )
        tests_cfg["tests"] = [t for t in tests_cfg["tests"] if t["id"] in wanted]

    framework = normalize_alias(framework)
    adapter = get_adapter(framework)

    manifest_rel = tests_cfg["frameworks"][framework]["manifest"]
    manifest_path = base_dir / manifest_rel
    manifest = adapter.data_handler.load_manifest(manifest_path)
    manifest_dir = manifest_path.parent

    eval_dir = (base_dir / tests_cfg["eval_dir"]).resolve()

    work_copy = adapter.data_handler.prepare_work_copy(
        manifest, manifest_dir, get_project_root(),
    )

    # ── MetaClaw ──────────────────────────────────────
    mc_raw = tests_cfg.get("metaclaw") or {}
    mc_manager = None
    proxy_pool = None
    mc_hooks = None

    mc_unmanaged = False  # deferred hooks creation after model resolution

    if mc_raw.get("enabled"):
        from clawarena.overlays.metaclaw.config import load_config, parse_trigger_config
        from clawarena.overlays.metaclaw.hooks import MetaClawHooks
        from clawarena.overlays.metaclaw.manager import MetaClawManager
        from clawarena.overlays.metaclaw.proxy import MetaClawProxyPool

        mem_trig, rl_trig = parse_trigger_config(mc_raw)

        # Resolve optional skills source directory from tests.json
        mc_skills_src: Path | None = None
        if mc_raw.get("skills_dir"):
            mc_skills_src = base_dir / mc_raw["skills_dir"]

        if mc_raw.get("managed", True):
            mc_cfg = load_config(base_dir / mc_raw["config_path"])
            # Sync upstream_model_id so as_provider_config() returns the correct
            # model; the actual llm.* override happens in _write_tmp_config.
            import os as _os_mc
            if (mid := _os_mc.environ.get("CLAWARENA_MODEL_ID", "")):
                mc_cfg.upstream_model_id = mid
            mc_work_dir = manifest_dir / "work"
            mc_work_dir.mkdir(exist_ok=True)
            if not mc_raw.get("per_scene_isolation", False):
                mc_manager = MetaClawManager(
                    mc_cfg, out_dir, mc_work_dir, work_copy,
                    skills_src=mc_skills_src,
                )
                await mc_manager.start()
                mc_hooks = MetaClawHooks(
                    proxy_url=mc_manager.proxy_url,
                    mc_config=mc_cfg,
                    memory_trigger=mem_trig,
                    rl_trigger=rl_trig,
                    per_scene_isolation=False,
                    total_scenes=len(tests_cfg["tests"]),
                )
                if concurrency != 1:
                    logger.warning("[warn] MetaClaw global mode — forcing concurrency=1")
                    concurrency = 1
            else:
                # Gateway-based engines cannot support per-invocation env override
                _GATEWAY_FRAMEWORKS = {"codex", "copaw"}
                if framework in _GATEWAY_FRAMEWORKS:
                    logger.warning(
                        "[warn] %s uses a gateway-based engine — "
                        "falling back to MetaClaw global mode (concurrency=1)",
                        framework,
                    )
                    mc_manager = MetaClawManager(
                        mc_cfg, out_dir, mc_work_dir, work_copy,
                        skills_src=mc_skills_src,
                    )
                    await mc_manager.start()
                    mc_hooks = MetaClawHooks(
                        proxy_url=mc_manager.proxy_url,
                        mc_config=mc_cfg,
                        memory_trigger=mem_trig,
                        rl_trigger=rl_trig,
                        per_scene_isolation=False,
                        total_scenes=len(tests_cfg["tests"]),
                    )
                    concurrency = 1
                else:
                    pool_size = min(concurrency, len(tests_cfg["tests"]))
                    proxy_pool = await MetaClawProxyPool.create(
                        mc_cfg, (mem_trig, rl_trig), pool_size,
                        mc_work_dir, work_copy,
                        skills_src=mc_skills_src,
                    )
        else:
            mc_unmanaged = True
            logger.info("[metaclaw] unmanaged mode — skipping proxy lifecycle")

    # ── mm-metaclaw overlay ───────────────────────────
    mmmc_raw = tests_cfg.get("mm_metaclaw") or {}
    mmmc_manager = None
    mmmc_hooks = None
    mmmc_extra_env: dict[str, str] | None = None

    # Mutual exclusion: mm_metaclaw and metaclaw cannot both be enabled
    if mmmc_raw.get("enabled") and mc_raw.get("enabled"):
        import warnings
        warnings.warn(
            "[clawarena] mm_metaclaw and metaclaw cannot both be enabled — "
            "disabling metaclaw automatically.",
            stacklevel=2,
        )
        mc_raw = {**mc_raw, "enabled": False}
        if mc_manager:
            await mc_manager.stop()
            mc_manager = None
        if proxy_pool:
            await proxy_pool.shutdown()
            proxy_pool = None
        mc_hooks = None

    if mmmc_raw.get("enabled"):
        from clawarena.overlays.mm_metaclaw.config import load_config as mmmc_load_config
        from clawarena.overlays.mm_metaclaw.config import parse_trigger_config as mmmc_parse_trigger
        from clawarena.overlays.mm_metaclaw.hooks import MmMetaClawHooks
        from clawarena.overlays.mm_metaclaw.manager import MmMetaClawManager

        mmmc_cfg = mmmc_load_config(mmmc_raw)
        if mmmc_cfg.transport_mode == "http_plugin" and framework != "openclaw":
            raise ValueError(
                "mm_metaclaw.transport_mode='http_plugin' is currently supported "
                "only for the openclaw framework"
            )
        mmmc_manager = MmMetaClawManager(mmmc_cfg, out_dir)
        if mmmc_cfg.managed:
            await mmmc_manager.start()

        if mmmc_cfg.transport_mode == "http_plugin":
            adapter.data_handler.configure_mm_metaclaw_plugin(
                work_copy,
                get_project_root() / "helpers" / "openclaw_customize" / "mm-metaclaw",
            )
            mmmc_extra_env = {
                "METACLAW_GATEWAY": mmmc_manager.gateway_url,
                "OPENCLAW_LOCAL_MODE": "1",
            }
        else:
            mem_trig_mm = mmmc_parse_trigger(mmmc_raw)
            mmmc_hooks = MmMetaClawHooks(
                gateway_url=mmmc_manager.gateway_url,
                config=mmmc_cfg,
                memory_trigger=mem_trig_mm,
                total_scenes=len(tests_cfg["tests"]),
            )

        if not mmmc_cfg.per_scene_isolation and concurrency != 1:
            logger.warning("[warn] mm_metaclaw global mode — forcing concurrency=1")
            concurrency = 1

    # ── Model config resolution ───────────────────────
    if mmmc_manager and mmmc_raw.get("enabled") and mmmc_raw.get("managed", True):
        if mmmc_cfg.transport_mode == "http_plugin":
            effective_model = mmmc_manager.as_upstream_model_config()
        else:
            effective_model = mmmc_manager.as_provider_config()
    elif mc_manager:
        effective_model = mc_manager.as_provider_config()
    elif proxy_pool:
        effective_model = None  # each scene gets its own via pool.acquire
    else:
        effective_model = resolve_model_config(tests_cfg, framework, cli_model)

    # Deferred hooks for unmanaged MetaClaw — needs effective_model.api_base
    if mc_unmanaged:
        mc_cfg = None
        if mc_raw.get("config_path"):
            mc_cfg = load_config(base_dir / mc_raw["config_path"])
        proxy_url = effective_model.api_base if effective_model and effective_model.api_base else ""
        if not proxy_url:
            logger.warning("[metaclaw] unmanaged mode but no api_base in model config — hooks disabled")
        else:
            mc_hooks = MetaClawHooks(
                proxy_url=proxy_url,
                mc_config=mc_cfg,
                memory_trigger=mem_trig,
                rl_trigger=rl_trig,
                per_scene_isolation=False,
                total_scenes=len(tests_cfg["tests"]),
            )

    if effective_model:
        adapter.data_handler.apply_model_config(work_copy, effective_model)

    port = find_free_port()
    gw = await adapter.engine.start_gateway(work_copy, port)
    await adapter.engine.wait_for_gateway(gw)

    try:
        semaphore = asyncio.Semaphore(concurrency)
        tasks = []
        for test in tests_cfg["tests"]:
            if proxy_pool:
                tasks.append(
                    _run_test_isolated(
                        adapter, test, eval_dir, work_copy, gw.port,
                        out_dir, semaphore, timeout, retry, framework,
                        proxy_pool=proxy_pool,
                    )
                )
            else:
                tasks.append(
                    _run_test(
                        adapter, test, eval_dir, work_copy, gw.port,
                        out_dir, semaphore, timeout, retry, framework,
                        mc_hooks=mc_hooks,
                        mmmc_hooks=mmmc_hooks,
                        extra_env=mmmc_extra_env,
                    )
                )
        await asyncio.gather(*tasks)
    finally:
        await adapter.engine.stop_gateway(gw)
        if mc_manager:
            await mc_manager.stop()
        if proxy_pool:
            await proxy_pool.shutdown()
        if mmmc_manager:
            await mmmc_manager.stop(
                hooks=mmmc_hooks,
                framework=framework,
                test_count=len(tests_cfg["tests"]),
            )
        print(framework_line("[done]", "Gateway stopped.", framework))


async def _run_test_isolated(
    adapter: FrameworkAdapter,
    test: dict,
    eval_dir: Path,
    work_copy: WorkCopy,
    gateway_port: int | None,
    out_dir: Path,
    semaphore: asyncio.Semaphore,
    timeout: float,
    retry: int,
    framework: str,
    proxy_pool: "MetaClawProxyPool",  # noqa: F821
) -> None:
    """Run a single test with per-scene MetaClaw isolation."""
    async with proxy_pool.acquire() as (mc_hooks, slot_provider_cfg):
        scene_env = adapter.data_handler.build_model_env(work_copy, slot_provider_cfg)
        await _run_test(
            adapter, test, eval_dir, work_copy, gateway_port,
            out_dir, semaphore, timeout, retry, framework,
            mc_hooks=mc_hooks, extra_env=scene_env,
        )


async def _run_test(
    adapter: FrameworkAdapter,
    test: dict,
    eval_dir: Path,
    work_copy: WorkCopy,
    gateway_port: int | None,
    out_dir: Path,
    semaphore: asyncio.Semaphore,
    timeout: float,
    retry: int,
    framework: str,
    completed_rounds: frozenset[str] = frozenset(),
    preloaded: dict[str, dict] | None = None,
    mc_hooks: "MetaClawHooks | None" = None,  # noqa: F821
    mmmc_hooks: "MmMetaClawHooks | None" = None,  # noqa: F821
    extra_env: dict[str, str] | None = None,
) -> None:
    """Run all rounds for a single test scenario."""
    async with semaphore:
        test_id = test["id"]
        eval_name = test.get("eval", test_id)

        session_id = adapter.data_handler.init_session(work_copy, test_id)
        workspace = adapter.data_handler.resolve_workspace(work_copy, test_id)
        manifest = work_copy.extra.get("manifest", {})

        ctx = TestContext(
            framework=framework,
            test_id=test_id,
            eval_dir=eval_dir,
            eval_name=eval_name,
            workspace=workspace,
            agent_id=test_id,
            session_id=session_id,
            history_sessions=manifest.get("agents", {}).get(test_id, {}).get(
                "history_sessions", []
            ),
            gateway_port=gateway_port,
            work_copy=work_copy,
        )

        questions = adapter.data_handler.load_questions(eval_dir, eval_name, test, work_copy)
        rounds = questions.get("rounds", [])
        if not rounds:
            print(framework_line("[warn]", f"No rounds for {test_id}", framework))
            return

        prev_inline_score: dict | None = None
        prev_round_record: dict | None = None
        override_feedback: str | None = None
        skip_standalone = False
        all_results: list[dict] = []
        all_inline_scores: list[dict] = []

        work_copy.extra["_is_resume"] = bool(completed_rounds)

        for ri, rnd in enumerate(rounds):
            round_id = rnd["id"]
            is_last = ri == len(rounds) - 1
            result_path = out_dir / test_id / round_id / "infer_result.json"

            # Resume: skip rounds that already have a result on disk
            if round_id in completed_rounds:
                existing = (preloaded or {}).get(round_id, {})
                prev_inline_score = existing.get("inline_score") or {}
                prev_round_record = rnd
                all_results.append(existing)
                all_inline_scores.append(prev_inline_score)
                passed = prev_inline_score.get("passed", False)
                print(framework_line(f"  [skip]", f"{test_id}/{round_id} ({'pass' if passed else 'fail'})", framework))
                continue

            # Execute updates
            for uid in rnd.get("update_ids", []):
                adapter.data_handler.execute_update(uid, work_copy, test_id, session_id)

            # Build query
            qtype = adapter.get_qtype(rnd.get("type", "multi_choice"))
            question_text = qtype.format_query(rnd, ctx)

            feedback_text: str | None = None
            if override_feedback is not None:
                feedback_text = override_feedback if override_feedback else None
                override_feedback = None
            elif prev_inline_score is not None and prev_round_record is not None:
                candidate = qtype.build_feedback(prev_round_record, prev_inline_score, ctx)
                if candidate:
                    feedback_text = candidate

            query = with_feedback(feedback_text, question_text) if feedback_text else question_text

            # mm-metaclaw before_round hook (http mode: explicit inject)
            if mmmc_hooks:
                inject_ctx = await mmmc_hooks.before_round(
                    session_id=session_id,
                    messages=[{"role": "user", "content": query}],
                    model="",
                )
                if inject_ctx:
                    logger.debug("[mm-metaclaw] before_round inject_ctx keys: %s", list(inject_ctx.keys()))

            # Run agent with retry
            ts_before = time.time()
            result = None
            last_error = ""
            for attempt in range(retry):
                result = await adapter.engine.run_agent(
                    session_id, query, work_copy,
                    agent_id=test_id, gateway_port=gateway_port, timeout=timeout,
                    extra_env=extra_env,
                )
                if result.status == "success":
                    break
                last_error = result.error or f"Attempt {attempt+1} failed"
                if result.error:
                    print(framework_line("  [stderr]", result.error, framework), flush=True)
                if attempt < retry - 1:
                    print(framework_line(f"  [retry {attempt+1}]", f"{test_id}/{round_id}", framework))
            ts_after = time.time()

            # Build infer_result
            llm_log = (
                result.llm_log
                if result and result.llm_log is not None
                else adapter.data_handler.read_llm_log(work_copy, session_id, ts_before)
            )
            inline_score = qtype.compute_inline_score(rnd, result.answer if result else "", ctx)

            infer_result = {
                "meta": {
                    "framework": ctx["framework"],
                    "test_id": test_id,
                    "round_id": round_id,
                    "question_type": rnd.get("type", "multi_choice"),
                    "agent_id": test_id,
                    "session_id": session_id,
                    "eval_question_path": str(eval_dir / eval_name / "questions.json"),
                },
                "question": query,
                "answer": {
                    "status": result.status if result else "failed",
                    "text": result.answer if result else "",
                    "error": result.error if result else last_error,
                },
                "timing": {
                    "started_at": ts_before,
                    "finished_at": ts_after,
                    "duration_ms": int((ts_after - ts_before) * 1000),
                    "retry_count": retry,
                },
                "llm_log": llm_log,
                "inline_score": inline_score,
            }

            write_json(result_path, infer_result)
            passed = inline_score.get("passed", False)
            print(framework_line(f"  [{'pass' if passed else 'fail'}]", f"{test_id}/{round_id}", framework))

            all_results.append(infer_result)
            all_inline_scores.append(inline_score)

            # Engine round hook
            hook_result = await adapter.engine.on_round_complete(RoundContext(
                framework=framework, test_id=test_id, round_id=round_id,
                round_index=ri, total_rounds=len(rounds), is_last_round=is_last,
                round_record=rnd, query=query, result=infer_result,
                inline_score=inline_score, prev_inline_score=prev_inline_score,
                all_results=all_results if is_last else None,
                all_inline_scores=all_inline_scores if is_last else None,
                result_path=result_path, workspace_path=workspace, out_dir=out_dir,
                session_id=session_id, work_copy=work_copy,
            ))

            if hook_result is not None:
                if hook_result.override_inline_score and "passed" in hook_result.override_inline_score:
                    inline_score = hook_result.override_inline_score
                    infer_result["inline_score"] = inline_score
                    write_json(result_path, infer_result)
                if hook_result.extra_data:
                    infer_result["hook_data"] = hook_result.extra_data
                    write_json(result_path, infer_result)
                if hook_result.override_feedback is not None:
                    override_feedback = hook_result.override_feedback
                if hook_result.skip_standalone_feedback:
                    skip_standalone = True
                if hook_result.skip_remaining and not is_last:
                    prev_inline_score = inline_score
                    prev_round_record = rnd
                    break

            # MetaClaw trigger (framework-independent)
            if mc_hooks:
                await mc_hooks.on_round_complete(
                    round_index=ri,
                    total_rounds=len(rounds),
                    is_last_round=is_last,
                )

            # mm-metaclaw on_round_complete hook
            if mmmc_hooks:
                trajectory = [
                    {"role": "user", "content": query},
                    {"role": "assistant", "content": result.answer if result else ""},
                ]
                await mmmc_hooks.on_round_complete(
                    round_index=ri,
                    total_rounds=len(rounds),
                    is_last_round=is_last,
                    session_id=session_id,
                    trajectory=trajectory,
                )

            prev_inline_score = inline_score
            prev_round_record = rnd

        # Standalone feedback after last round
        if not skip_standalone and prev_inline_score and prev_round_record:
            if override_feedback is not None:
                fb_text = override_feedback
            else:
                qtype = adapter.get_qtype(prev_round_record.get("type", "multi_choice"))
                fb_text = qtype.build_feedback(prev_round_record, prev_inline_score, ctx)
            if fb_text:
                await adapter.engine.run_agent(
                    session_id, standalone_feedback(fb_text), work_copy,
                    agent_id=test_id, gateway_port=gateway_port,
                    extra_env=extra_env,
                )


# ---------------------------------------------------------------------------
# Resume helpers
# ---------------------------------------------------------------------------


def _resolve_infer_out_dir(out_dir: Path) -> Path:
    """If out_dir looks like a ``clawarena run`` framework dir (has an infer/
    subdirectory with content), return ``out_dir / "infer"``.  Otherwise
    return out_dir unchanged."""
    infer_subdir = out_dir / "infer"
    if infer_subdir.is_dir() and any(infer_subdir.iterdir()):
        print(f"  [info] detected clawarena-run layout, using {infer_subdir}")
        return infer_subdir
    return out_dir


def _find_completed_rounds(
    out_dir: Path,
    test_id: str,
    round_ids: list[str],
) -> tuple[frozenset[str], dict[str, dict]]:
    """Scan out_dir for rounds that already have infer_result.json.

    Returns (completed_round_ids, preloaded_results).
    Malformed JSON is treated as incomplete.
    """
    completed: set[str] = set()
    preloaded: dict[str, dict] = {}
    for rid in round_ids:
        p = out_dir / test_id / rid / "infer_result.json"
        if p.exists():
            try:
                preloaded[rid] = json.loads(p.read_text(encoding="utf-8"))
                completed.add(rid)
            except Exception:
                pass
    return frozenset(completed), preloaded


async def resume_infer(
    tests_json_path: Path,
    framework: str,
    out_dir: Path,
    state_dir: Path,
    workspace_dir: Path | None,
    concurrency: int = 4,
    timeout: float = 300,
    retry: int = 1,
    inplace: bool = False,
) -> None:
    """Resume an interrupted infer run using existing results/state/workspace dirs."""
    base_dir = tests_json_path.parent
    tests_cfg = load_tests_config(tests_json_path)

    framework = normalize_alias(framework)
    adapter = get_adapter(framework)

    manifest_rel = tests_cfg["frameworks"][framework]["manifest"]
    manifest_path = base_dir / manifest_rel
    manifest = adapter.data_handler.load_manifest(manifest_path)
    manifest_dir = manifest_path.parent

    eval_dir = (base_dir / tests_cfg["eval_dir"]).resolve()
    project_root = get_project_root()

    # Auto-detect: if out_dir is a `clawarena run` framework dir, drill into infer/
    out_dir = _resolve_infer_out_dir(out_dir)

    work_copy: WorkCopy = adapter.data_handler.rebuild_work_copy(
        manifest, manifest_dir, project_root, state_dir, workspace_dir,
        inplace=inplace,
    )

    port = find_free_port()
    gw = await adapter.engine.start_gateway(work_copy, port)
    await adapter.engine.wait_for_gateway(gw)

    try:
        semaphore = asyncio.Semaphore(concurrency)
        tasks = []
        for test in tests_cfg["tests"]:
            test_id = test["id"]
            eval_name = test.get("eval", test_id)
            questions = load_questions(eval_dir, eval_name)
            round_ids = [r["id"] for r in questions.get("rounds", [])]

            completed, preloaded = _find_completed_rounds(out_dir, test_id, round_ids)
            if completed >= set(round_ids):
                print(framework_line("  [skip]", f"{test_id} (all {len(round_ids)} rounds complete)", framework))
                continue

            tasks.append(
                _run_test(
                    adapter, test, eval_dir, work_copy, gw.port,
                    out_dir, semaphore, timeout, retry, framework,
                    completed_rounds=completed,
                    preloaded=preloaded,
                )
            )

        await asyncio.gather(*tasks)
    finally:
        await adapter.engine.stop_gateway(gw)
        print(framework_line("[done]", "Gateway stopped.", framework))
