"""MetaClawManager — lifecycle orchestration for a single MetaClaw proxy."""

from __future__ import annotations

import os
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

from clawarena.core.provider import ModelConfig
from clawarena.core.types import WorkCopy
from clawarena.overlays.metaclaw.config import MetaClawConfig
from clawarena.overlays.metaclaw.proxy import ProxyProcess, _write_tmp_config
from clawarena.overlays.metaclaw.run_dir import MetaClawRunDir
from clawarena.utils import find_free_port

logger = logging.getLogger(__name__)


class MetaClawManager:
    """Manages the full lifecycle of a single MetaClaw proxy instance."""

    def __init__(
        self,
        config: MetaClawConfig,
        out_dir: Path,
        work_root: Path,
        work_copy: WorkCopy,
        skills_src: Path | None = None,
    ):
        self.config = config
        self.out_dir = out_dir
        self._work_root = work_root
        self._work_copy = work_copy
        self._skills_src = skills_src

        self._proxy: ProxyProcess | None = None
        self._run_dir: MetaClawRunDir | None = None
        self._start_time: float = 0.0
        self._started_at: str = ""

    @property
    def proxy_url(self) -> str:
        if self._proxy:
            return self._proxy.url
        return ""

    async def start(self) -> None:
        run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + f"_{os.getpid()}"
        self._run_dir = MetaClawRunDir.create(
            self.config, self._work_root, run_id,
            skills_src_override=self._skills_src,
        )

        port = find_free_port()
        self._proxy = ProxyProcess(host=self.config.proxy_host, port=port)

        _write_tmp_config(self.config, self._run_dir, port)
        log_path = self._run_dir.root / "metaclaw.log"
        await self._proxy.start(self._run_dir.tmp_config_path, log_path=log_path)

        self._start_time = time.time()
        self._started_at = datetime.now(timezone.utc).isoformat()
        logger.info("MetaClaw started: %s (run_id=%s)", self._proxy.url, run_id)

    async def stop(self, hooks=None, framework: str = "", test_count: int = 0) -> None:
        elapsed = time.time() - self._start_time if self._start_time else 0

        if hooks and self._proxy and self._run_dir:
            from clawarena.overlays.metaclaw.report import MetaClawCollector, write_report
            collector = MetaClawCollector(
                self._proxy.url, self.config, hooks, self._run_dir,
            )
            report = await collector.collect(elapsed, framework, test_count)
            report.started_at = self._started_at
            write_report(report, self.out_dir)

        if self._proxy:
            await self._proxy.stop()
        if self._run_dir:
            self._run_dir.cleanup_tmp()

    def as_provider_config(self) -> ModelConfig:
        """Return a ModelConfig pointing to this proxy (OpenAI-compatible)."""
        return ModelConfig(
            provider="openai",
            api_base=f"{self.proxy_url}/v1",
            api_key="clawarena",
            model_id=self.config.upstream_model_id or self.config.served_model_name,
        )
