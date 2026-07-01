"""Cross-scenario run entry point: schedules several scenarios and aggregates the top-level report."""
from __future__ import annotations

import asyncio
import json
import logging
import os
import time
import uuid
from pathlib import Path
from typing import Any

from ..agent.harness import TokenLimitExceeded
from ..provider.base import NonRetryableProviderError
from ..tokenizer import UnifiedTokenizer
from ..types import DatasetManifests, ModelBundle, ScenarioManifest
from .scenario_runner import ScenarioRunner

log = logging.getLogger(__name__)


class RunRunner:
    def __init__(
        self,
        *,
        manifests: DatasetManifests,
        scenarios: dict[str, ScenarioManifest],
        model_bundle: ModelBundle,
        tokenizer: UnifiedTokenizer,
        config_dict: dict[str, Any],
        output_root: Path,
        concurrency: int = 1,
    ):
        self.manifests = manifests
        self.scenarios = scenarios
        self.model_bundle = model_bundle
        self.tokenizer = tokenizer
        self.config_dict = config_dict
        self.output_root = output_root
        self.concurrency = concurrency
        # retry: max attempts per scenario (including the first), from scenario.retry
        # (CLI --retry / CATEAM_SCENARIO_RETRY overrides already merged into
        # config_dict). Only execution-time exceptions (provider errors, etc.) are
        # retried; a check failure is a normal result and does not trigger a retry.
        # <1 is treated as 1.
        self.retry = max(1, int((config_dict.get("scenario") or {}).get("retry", 3)))
        # Per-scenario wall-clock hard timeout (seconds): when >0, wrap the whole
        # scenario execution with ``asyncio.wait_for``. On heavy / very long context
        # scenarios some models permanently hang at an **unbounded await point** —
        # slow provider streaming, in-turn ``asyncio.gather`` over parallel subagents,
        # ``wait_for_backgrounds``, etc. (GPU at 0%, runlog making zero progress, jsonl
        # silent) — which single-point timeouts (httpx per-chunk read-timeout, wait_all
        # only covering the background gather) cannot catch. This wall-clock fallback
        # does not depend on the exact hang point: on timeout it cancels the scenario
        # coroutine → since metadata.json is only written at the end of ``run()`` and is
        # not persisted on cancellation → a clean failure → can be re-run by
        # ``clawarena-team resume`` (the other scenarios complete as usual and feed into
        # the report). 0=disabled (default, preserving the original semantics). From
        # CATEAM_SCENARIO_TIMEOUT_SEC.
        self.scenario_timeout = max(
            0.0, float(os.environ.get("CATEAM_SCENARIO_TIMEOUT_SEC", "0") or "0")
        )

    async def _run_one(self, scenario: ScenarioManifest, run_dir: Path) -> dict[str, Any]:
        runner = ScenarioRunner(
            scenario=scenario,
            manifests=self.manifests,
            model_bundle=self.model_bundle,
            tokenizer=self.tokenizer,
            config_dict=self.config_dict,
            run_dir=run_dir,
        )
        return await runner.run()

    async def run(self) -> dict[str, Any]:
        run_id = f"run_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        run_dir = self.output_root / run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        sem = asyncio.Semaphore(self.concurrency)

        async def _guarded(sc: ScenarioManifest):
            async with sem:
                # A single scenario failure (provider error, assertion, etc.) must not
                # drag down the whole run: each scenario is attempted at most
                # self.retry times (including the first). Each retry has _run_one create
                # a fresh ScenarioRunner and _setup_workspace rebuild work/sessions/evals,
                # so re-runs are idempotent. If all attempts are exhausted and it still
                # fails, the exception is swallowed and metadata.json is not written; it
                # can be re-run later by ``clawarena-team resume``; the other scenarios
                # complete as usual and feed into the report.
                for attempt in range(1, self.retry + 1):
                    try:
                        if self.scenario_timeout > 0:
                            # Wall-clock fallback: a permanent hang anywhere is
                            # cancelled on timeout; metadata.json is not written.
                            return await asyncio.wait_for(
                                self._run_one(sc, run_dir), timeout=self.scenario_timeout
                            )
                        return await self._run_one(sc, run_dir)
                    except Exception as e:
                        # Exception routing:
                        # - wall-clock timeout (asyncio.TimeoutError): possibly transient
                        #   (rate slope backing off / a deadlock may clear next round),
                        #   retry.
                        # - NonRetryableProviderError (4xx other than 429): bad payload /
                        #   auth failure / context over model limit / model not found,
                        #   etc. A re-run will reproduce it, so give up immediately
                        #   without consuming the retry budget.
                        # - TokenLimitExceeded: the local tokenizer computes context over
                        #   token_limit; a re-run overflows the same way, so give up.
                        # - everything else (transient 5xx exhausted / transport /
                        #   business exception): retry.
                        timed_out = isinstance(e, asyncio.TimeoutError)
                        fatal = isinstance(e, (NonRetryableProviderError, TokenLimitExceeded))
                        if timed_out:
                            reason = f"wall-clock timeout {self.scenario_timeout:.0f}s"
                        elif fatal:
                            reason = f"non-retryable ({type(e).__name__}): {e}"
                        else:
                            reason = repr(e)
                        if fatal:
                            log.error(
                                "scenario %s fast-fail; not retrying: %s",
                                sc.scenario_id, reason,
                            )
                            return None
                        if attempt < self.retry:
                            log.warning(
                                "scenario %s attempt %d/%d failed; retrying: %s",
                                sc.scenario_id, attempt, self.retry, reason,
                            )
                        else:
                            log.error(
                                "scenario %s failed after %d attempt(s); skipping "
                                "(resume can retry): %s",
                                sc.scenario_id, self.retry, reason,
                            )
                return None

        raw_results = await asyncio.gather(
            *(_guarded(sc) for sc in self.scenarios.values())
        )
        results = [r for r in raw_results if r is not None]

        # report aggregation
        from ..scoring.report import build_run_report

        report_json, report_md = build_run_report(run_id, results)
        (run_dir / "report.json").write_text(
            json.dumps(report_json, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
        )
        (run_dir / "report.md").write_text(report_md, encoding="utf-8")
        return {"run_id": run_id, "run_dir": str(run_dir), "report": report_json}
