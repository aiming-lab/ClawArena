"""MetaClaw trigger hooks — memory ingest and RL train triggers."""

from __future__ import annotations

import asyncio
import logging
from urllib.parse import urlparse

from clawarena.overlays.metaclaw.config import MetaClawConfig, TriggerCfg

logger = logging.getLogger(__name__)


async def _http_post_json(url: str, timeout: float = 60) -> bool:
    """POST JSON ``{}`` to *url*, return True on 2xx."""
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json={},
                timeout=aiohttp.ClientTimeout(total=timeout),
            ) as resp:
                if 200 <= resp.status < 300:
                    return True
                body = await resp.text()
                logger.warning("MetaClaw POST %s → %d: %s", url, resp.status, body[:200])
                return False
    except Exception as e:
        logger.warning("MetaClaw POST %s failed: %s", url, e)
        return False


async def _run_train_step(port: int, timeout: float = 660) -> bool:
    """Run ``metaclaw train-step --port <port>`` as a subprocess."""
    try:
        proc = await asyncio.create_subprocess_exec(
            "metaclaw", "train-step", "--port", str(port),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        if proc.returncode == 0:
            if stdout:
                logger.info("[train-step] %s", stdout.decode().strip())
            return True
        logger.warning(
            "[train-step] exited %d: %s", proc.returncode,
            stderr.decode().strip() if stderr else "(no stderr)",
        )
        return False
    except FileNotFoundError:
        logger.error("[train-step] 'metaclaw' command not found in PATH")
        return False
    except asyncio.TimeoutError:
        logger.error("[train-step] timed out (%.0fs)", timeout)
        return False
    except Exception as e:
        logger.error("[train-step] %s", e)
        return False


class MetaClawHooks:
    """Trigger hooks called after each round to fire memory ingest / RL train.

    Follows the original MetaClaw benchmark convention: triggers are **skipped**
    on the final interaction of a run because no subsequent rounds would benefit
    from the updated state.  Concretely:

    * **Global mode** — skip all triggers on the last round of the last scene.
    * **Isolation mode** — skip all triggers on each scene's last round (scenes
      are independent; nothing follows after the last round).
    """

    def __init__(
        self,
        proxy_url: str,
        mc_config: MetaClawConfig | None,
        memory_trigger: TriggerCfg,
        rl_trigger: TriggerCfg,
        per_scene_isolation: bool,
        total_scenes: int = 0,
    ):
        self._proxy_url = proxy_url.rstrip("/")
        self._proxy_port = urlparse(proxy_url).port or 30000
        self._mc = mc_config
        self._mem = memory_trigger
        self._rl = rl_trigger
        self._isolation = per_scene_isolation
        self._total_scenes = total_scenes

        self.total_rounds_seen: int = 0
        self.completed_scenes: int = 0
        self.memory_ingest_count: int = 0
        self.rl_train_count: int = 0

    async def on_round_complete(
        self,
        round_index: int,
        total_rounds: int,
        is_last_round: bool,
    ) -> None:
        self.total_rounds_seen += 1
        if is_last_round:
            self.completed_scenes += 1
        is_last_scene = self.completed_scenes == self._total_scenes

        mem_enabled = (self._mc.memory.enabled and self._mc.memory.manual_trigger) if self._mc else True
        rl_enabled = (self._mc.rl.enabled and self._mc.rl.manual_train_trigger) if self._mc else True

        if mem_enabled:
            if self._should_trigger(self._mem, round_index, is_last_round, is_last_scene):
                await self._trigger_memory_ingest()

        if rl_enabled:
            if self._should_trigger(self._rl, round_index, is_last_round, is_last_scene):
                await self._trigger_rl_train()

    # ------------------------------------------------------------------

    def _should_trigger(
        self,
        cfg: TriggerCfg,
        round_index: int,
        is_last_round: bool,
        is_last_scene: bool,
    ) -> bool:
        # Nothing follows after the final interaction — skip all triggers.
        if self._isolation and is_last_round:
            return False
        if not self._isolation and is_last_round and is_last_scene:
            return False

        if self._isolation:
            n = cfg.every_n_rounds
            if n > 0 and (round_index + 1) % n == 0:
                return True
            return False

        # Global mode
        trigger = False
        if cfg.every_n_rounds > 0 and self.total_rounds_seen % cfg.every_n_rounds == 0:
            trigger = True
        if is_last_round:
            if cfg.every_n_scenes > 0 and self.completed_scenes % cfg.every_n_scenes == 0:
                trigger = True
            if cfg.on_last_round:
                trigger = True
        return trigger

    # ------------------------------------------------------------------

    async def _trigger_memory_ingest(self) -> None:
        url = f"{self._proxy_url}/v1/memory/ingest"
        if await _http_post_json(url):
            self.memory_ingest_count += 1
            logger.info("[memory] ingest triggered (%d total)", self.memory_ingest_count)

    async def _trigger_rl_train(self) -> None:
        if await _run_train_step(self._proxy_port):
            self.rl_train_count += 1
            logger.info("[rl] train-step triggered (%d total)", self.rl_train_count)
