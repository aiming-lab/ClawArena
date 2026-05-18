"""MmMetaClawManager — full lifecycle orchestration for a mm-metaclaw gateway."""

from __future__ import annotations

import os
import dataclasses
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

from clawarena.core.provider import ModelConfig
from clawarena.overlays.mm_metaclaw.config import MmMetaClawConfig
from clawarena.overlays.mm_metaclaw.proxy import GatewayProcess
from clawarena.overlays.mm_metaclaw.run_dir import MmMetaClawRunDir
from clawarena.utils import find_free_port

logger = logging.getLogger(__name__)


class MmMetaClawManager:
    """Manages the full lifecycle of a single mm-metaclaw gateway instance.

    Responsibilities:
    * Write a ``config.yaml`` to ``gateway_dir`` with correct upstream
      credentials and ``enabled_modules``.
    * Start the gateway daemon (``python3 -m mm_metaclaw start --daemon``).
    * Wait until ``/v1/health`` returns 200.
    * On stop: collect stats, write report, terminate the daemon.
    """

    def __init__(
        self,
        config: MmMetaClawConfig,
        out_dir: Path,
        skills_src: Path | None = None,
    ):
        self.config = config
        self.out_dir = out_dir
        # Default to the bundled skills_init/ directory so the skill module
        # starts with the 43 pre-built starter skills rather than an empty dir.
        self._skills_src = skills_src or (config.gateway_dir / "skills_init")

        self._gateway: GatewayProcess | None = None
        self._run_dir: MmMetaClawRunDir | None = None
        self._start_time: float = 0.0
        self._started_at: str = ""

    @property
    def gateway_url(self) -> str:
        if self._gateway:
            return self._gateway.url
        return f"http://{self.config.proxy_host}:{self.config.proxy_port}"

    async def start(self) -> None:
        """Write config, start daemon, wait for health."""
        # Resolve port *before* writing config.yaml so the daemon binds on
        # the correct address (mirrors how the metaclaw overlay works).
        port = (
            find_free_port()
            if self.config.proxy_port == 0
            else self.config.proxy_port
        )
        resolved_config = dataclasses.replace(self.config, proxy_port=port)

        run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + f"_{os.getpid()}"
        self._run_dir = MmMetaClawRunDir.create(
            resolved_config,
            self.out_dir,
            run_id,
            skills_src_override=self._skills_src,
        )

        self._gateway = GatewayProcess(
            host=self.config.proxy_host,
            port=port,
            gateway_dir=self.config.gateway_dir,
        )
        await self._gateway.start(log_path=self._run_dir.log_path)

        self._start_time = time.time()
        self._started_at = datetime.now(timezone.utc).isoformat()
        logger.info(
            "mm-metaclaw gateway started: %s  modules=%s  transport=%s  hook_mode=%s  (run_id=%s)",
            self._gateway.url,
            self.config.enabled_modules,
            self.config.transport_mode,
            self.config.hook_mode,
            run_id,
        )

    async def stop(
        self,
        hooks: "MmMetaClawHooks | None" = None,  # noqa: F821
        framework: str = "",
        test_count: int = 0,
    ) -> None:
        """Collect stats, write report, terminate daemon, clean up."""
        elapsed = time.time() - self._start_time if self._start_time else 0.0

        if hooks and self._gateway:
            from clawarena.overlays.mm_metaclaw.report import MmMetaClawCollector, write_report
            collector = MmMetaClawCollector(
                self._gateway.url, hooks, self.config.enabled_modules,
            )
            report = await collector.collect(elapsed, framework, test_count)
            report.started_at = self._started_at
            write_report(report, self.out_dir)

        if self._gateway:
            await self._gateway.stop()
        if self._run_dir:
            self._run_dir.cleanup()

    def as_provider_config(self) -> ModelConfig:
        """Return a ModelConfig that points the benchmark agent at this gateway."""
        return ModelConfig(
            provider="openai",
            api_base=f"{self.gateway_url}/v1",
            api_key="clawarena",
            model_id=self.config.upstream_model or self.config.served_model_name,
        )

    def as_upstream_model_config(self) -> ModelConfig:
        """Return the upstream provider config for plugin-driven HTTP mode."""
        return ModelConfig(
            provider="openai",
            api_base=self.config.upstream_api_base,
            api_key=self.config.upstream_api_key,
            model_id=self.config.upstream_model or self.config.served_model_name,
        )
