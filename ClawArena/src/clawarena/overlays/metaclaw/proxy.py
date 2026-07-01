"""MetaClaw proxy process management and pool for per-scene isolation."""

from __future__ import annotations

import os
import asyncio
import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import AsyncIterator

from clawarena.core.provider import ModelConfig
from clawarena.core.types import WorkCopy
from clawarena.overlays.metaclaw.config import MetaClawConfig, TriggerCfg
from clawarena.overlays.metaclaw.run_dir import MetaClawRunDir
from clawarena.utils import find_free_port

logger = logging.getLogger(__name__)


@dataclass
class ProxyProcess:
    """Manages a single MetaClaw proxy subprocess."""

    host: str
    port: int
    _process: asyncio.subprocess.Process | None = None
    _log_file: "open | None" = None

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"

    async def start(self, config_path: Path, log_path: Path | None = None) -> None:
        """Start `metaclaw start --config <path>` and poll /healthz."""
        stdout_sink = asyncio.subprocess.PIPE
        stderr_sink = asyncio.subprocess.PIPE
        if log_path:
            self._log_file = open(log_path, "w")
            stdout_sink = self._log_file
            stderr_sink = self._log_file
            logger.info("MetaClaw proxy log → %s", log_path)
        self._process = await asyncio.create_subprocess_exec(
            "metaclaw", "start", "--config", str(config_path),
            stdout=stdout_sink,
            stderr=stderr_sink,
            start_new_session=True,
        )
        await self._wait_healthy()

    async def _wait_healthy(self, timeout: float = 60.0) -> None:
        """Poll /healthz until 200 or timeout."""
        import aiohttp

        deadline = asyncio.get_event_loop().time() + timeout
        while asyncio.get_event_loop().time() < deadline:
            try:
                async with aiohttp.ClientSession() as s:
                    async with s.get(f"{self.url}/healthz", timeout=aiohttp.ClientTimeout(total=2)) as r:
                        if r.status == 200:
                            logger.info("MetaClaw proxy ready at %s", self.url)
                            return
            except Exception:
                pass
            await asyncio.sleep(0.5)
        raise RuntimeError(
            f"MetaClaw proxy at {self.url} did not become healthy in {timeout:.0f}s"
        )

    async def stop(self) -> None:
        """SIGTERM → wait 10s → SIGKILL."""
        if self._process is None:
            return
        try:
            self._process.terminate()
            await asyncio.wait_for(self._process.wait(), timeout=10)
        except asyncio.TimeoutError:
            self._process.kill()
            await self._process.wait()
        except ProcessLookupError:
            pass
        self._process = None
        if self._log_file:
            self._log_file.close()
            self._log_file = None


# ---------------------------------------------------------------------------
# Proxy pool for per-scene isolation
# ---------------------------------------------------------------------------


@dataclass
class ProxySlot:
    slot_id: int
    proxy: ProxyProcess
    run_dir: MetaClawRunDir
    mc_config: MetaClawConfig


class MetaClawProxyPool:
    """Pool of pre-warmed MetaClaw proxy instances for per-scene isolation."""

    def __init__(self, slots: list[ProxySlot], trigger_cfgs: tuple[TriggerCfg, TriggerCfg]):
        self._slots = slots
        self._trigger_cfgs = trigger_cfgs
        self._queue: asyncio.Queue[ProxySlot] = asyncio.Queue()
        for s in slots:
            self._queue.put_nowait(s)

    @classmethod
    async def create(
        cls,
        mc_config: MetaClawConfig,
        trigger_cfgs: tuple[TriggerCfg, TriggerCfg],
        pool_size: int,
        work_root: Path,
        work_copy: WorkCopy,
        skills_src: Path | None = None,
    ) -> MetaClawProxyPool:
        from datetime import datetime
        base_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + f"_{os.getpid()}"

        async def _create_one(i: int) -> ProxySlot:
            run_id = f"{base_id}_slot{i}"
            run_dir = MetaClawRunDir.create(
                mc_config, work_root, run_id,
                skills_src_override=skills_src,
            )
            port = find_free_port()
            proxy = ProxyProcess(host=mc_config.proxy_host, port=port)
            _write_tmp_config(mc_config, run_dir, port)
            log_path = run_dir.root / "metaclaw.log"
            await proxy.start(run_dir.tmp_config_path, log_path=log_path)
            return ProxySlot(slot_id=i, proxy=proxy, run_dir=run_dir, mc_config=mc_config)

        slots = await asyncio.gather(*[_create_one(i) for i in range(pool_size)])
        return cls(list(slots), trigger_cfgs)

    @asynccontextmanager
    async def acquire(self) -> AsyncIterator[tuple["MetaClawHooks", ModelConfig]]:  # noqa: F821
        from clawarena.overlays.metaclaw.hooks import MetaClawHooks
        slot = await self._queue.get()
        hooks = MetaClawHooks(
            proxy_url=slot.proxy.url,
            mc_config=slot.mc_config,
            memory_trigger=self._trigger_cfgs[0],
            rl_trigger=self._trigger_cfgs[1],
            per_scene_isolation=True,
        )
        provider_cfg = ModelConfig(
            provider="openai",
            api_base=f"{slot.proxy.url}/v1",
            api_key="clawarena",
            model_id=slot.mc_config.upstream_model_id or slot.mc_config.served_model_name,
        )
        try:
            yield hooks, provider_cfg
        finally:
            self._queue.put_nowait(slot)

    async def shutdown(self) -> None:
        for slot in self._slots:
            await slot.proxy.stop()
            slot.run_dir.cleanup_tmp()


def _write_tmp_config(config: MetaClawConfig, run_dir: MetaClawRunDir, port: int) -> None:
    """Write a temporary YAML config for the proxy with injected port and dirs."""
    import copy
    import os
    try:
        import yaml
    except ImportError:
        return

    cfg = copy.deepcopy(config.raw_yaml)

    # Inject LLM connection settings from CLAWARENA_* env vars so users only
    # need to configure the unified provider platform; the YAML's llm section
    # (which may contain ${HBENCH_*} placeholders) is overridden here.
    llm = cfg.setdefault("llm", {})
    for env_var, llm_key in (
        ("CLAWARENA_API_BASE", "api_base"),
        ("CLAWARENA_API_KEY",  "api_key"),
        ("CLAWARENA_MODEL_ID", "model_id"),
    ):
        val = os.environ.get(env_var, "")
        if val:
            llm[llm_key] = val

    # Proxy: override host/port in the proxy sub-dict
    proxy_sect = cfg.setdefault("proxy", {})
    proxy_sect["host"] = config.proxy_host
    proxy_sect["port"] = port

    # Memory: redirect all path fields to the run dir
    if run_dir.memory_store_dir:
        mem = cfg.setdefault("memory", {})
        store_dir = str(run_dir.memory_store_dir)
        mem["dir"] = store_dir
        mem["store_path"] = str(run_dir.memory_store_dir / "memory.db")
        mem["policy_path"] = str(run_dir.memory_store_dir / "policy.json")
        mem["telemetry_path"] = str(run_dir.memory_store_dir / "telemetry.jsonl")

    # Skills: redirect dir and evolution_history_path
    if run_dir.skills_snapshot_dir:
        sk = cfg.setdefault("skills", {})
        sk["dir"] = str(run_dir.skills_snapshot_dir)
        sk["evolution_history_path"] = str(run_dir.skills_snapshot_dir / "evolution_history.jsonl")

    run_dir.tmp_config_path.write_text(yaml.dump(cfg, default_flow_style=False))
