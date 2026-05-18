"""mm-metaclaw trigger hooks — dual-mode (proxy / http) round callbacks."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from clawarena.overlays.mm_metaclaw.config import MmMetaClawConfig, TriggerCfg

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


async def _http_post(url: str, body: dict, timeout: float = 60.0) -> dict | None:
    """POST *body* as JSON to *url*.  Returns parsed response dict on 2xx, else None."""
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=body,
                timeout=aiohttp.ClientTimeout(total=timeout),
            ) as resp:
                if 200 <= resp.status < 300:
                    try:
                        return await resp.json()
                    except Exception:
                        return {}
                body_text = await resp.text()
                logger.warning("mm-metaclaw POST %s → %d: %s", url, resp.status, body_text[:200])
                return None
    except Exception as exc:
        logger.warning("mm-metaclaw POST %s failed: %s", url, exc)
        return None


# ---------------------------------------------------------------------------
# Hook class
# ---------------------------------------------------------------------------


class MmMetaClawHooks:
    """Round lifecycle hooks for the mm-metaclaw overlay.

    Two modes are supported, controlled by ``config.hook_mode``:

    **proxy mode** (default)
        The gateway pipeline handles inject/collect transparently when
        agent LLM traffic flows through.  Hooks only call ``/collect``
        endpoints at configured trigger points to verify collection
        behaviour.

    **http mode**
        Hooks explicitly drive *every* inject step (``before_round``) and
        *every* collect step (``on_round_complete``) via direct HTTP
        requests to module endpoints.  The gateway's proxy pipeline is
        still running but module calls are issued manually, enabling
        end-to-end HTTP-level testing of each endpoint.
    """

    def __init__(
        self,
        gateway_url: str,
        config: MmMetaClawConfig,
        memory_trigger: TriggerCfg,
        total_scenes: int = 0,
    ):
        self._base = gateway_url.rstrip("/")
        self._cfg = config
        self._mem_trig = memory_trigger
        self._total_scenes = total_scenes

        self.total_rounds_seen: int = 0
        self.completed_scenes: int = 0
        self.memory_collect_count: int = 0
        self.skill_collect_count: int = 0
        self.memory_inject_count: int = 0
        self.skill_inject_count: int = 0

        # Stores the last before_round inject result for test introspection
        self.last_inject_ctx: dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Before-round hook  (http mode only)
    # ------------------------------------------------------------------

    async def before_round(
        self,
        session_id: str,
        messages: list[dict],
        model: str = "",
    ) -> dict[str, Any]:
        """Called before the agent runs a round.

        **proxy mode**: no-op — returns empty dict.

        **http mode**: concurrently calls ``POST /v1/memory/inject`` and
        ``POST /v1/skill/inject``, then merges and returns the combined
        ``additional_context`` dicts for test introspection.
        """
        if self._cfg.hook_mode != "http":
            return {}

        results: dict[str, Any] = {}
        payload = {"session_id": session_id, "messages": messages, "model": model or ""}

        tasks: list[asyncio.Task] = []
        if "memory" in self._cfg.enabled_modules:
            tasks.append(asyncio.create_task(
                _http_post(f"{self._base}/v1/memory/inject", payload),
            ))
        if "skill" in self._cfg.enabled_modules:
            tasks.append(asyncio.create_task(
                _http_post(f"{self._base}/v1/skill/inject", payload),
            ))

        if tasks:
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            for resp in responses:
                if isinstance(resp, dict) and resp:
                    results.update(resp)
                    # Count only successful calls
                    if "memory" in self._cfg.enabled_modules and not self.memory_inject_count:
                        self.memory_inject_count += 1
                    elif "skill" in self._cfg.enabled_modules:
                        self.skill_inject_count += 1
            # Recalculate counts properly
            if "memory" in self._cfg.enabled_modules:
                self.memory_inject_count += 1
            if "skill" in self._cfg.enabled_modules:
                self.skill_inject_count += 1

        self.last_inject_ctx = results
        logger.debug("[mm-metaclaw/http] before_round inject: %s", list(results.keys()))
        return results

    # ------------------------------------------------------------------
    # After-round hook
    # ------------------------------------------------------------------

    async def on_round_complete(
        self,
        round_index: int,
        total_rounds: int,
        is_last_round: bool,
        session_id: str = "",
        trajectory: list[dict] | None = None,
    ) -> None:
        """Called after the agent completes a round.

        **proxy mode**: fires ``POST /v1/memory/collect`` at trigger points
        (same skip-on-final-interaction semantics as the original metaclaw).

        **http mode**: unconditionally fires ``POST /v1/memory/collect`` and
        ``POST /v1/skill/collect`` after every round.
        """
        self.total_rounds_seen += 1
        if is_last_round:
            self.completed_scenes += 1
        is_last_scene = self.completed_scenes == self._total_scenes

        payload: dict = {"session_id": session_id}
        if trajectory:
            payload["trajectory"] = trajectory

        if self._cfg.hook_mode == "http":
            await self._collect_all(payload, session_id)
        else:
            # proxy mode — collect at trigger points, only if module is enabled
            if (
                "memory" in self._cfg.enabled_modules
                and self._should_trigger(self._mem_trig, round_index, is_last_round, is_last_scene)
            ):
                await self._collect_memory(payload)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _should_trigger(
        self,
        cfg: TriggerCfg,
        round_index: int,
        is_last_round: bool,
        is_last_scene: bool,
    ) -> bool:
        """Mirror the trigger logic from the original metaclaw hooks (global mode only)."""
        # Skip final interaction — nothing subsequent would benefit
        if is_last_round and is_last_scene:
            return False
        trigger = False
        if cfg.every_n_rounds > 0 and self.total_rounds_seen % cfg.every_n_rounds == 0:
            trigger = True
        if is_last_round:
            if cfg.every_n_scenes > 0 and self.completed_scenes % cfg.every_n_scenes == 0:
                trigger = True
            if cfg.on_last_round:
                trigger = True
        return trigger

    async def _collect_memory(self, payload: dict) -> None:
        resp = await _http_post(f"{self._base}/v1/memory/collect", payload)
        if resp is not None:
            self.memory_collect_count += 1
            logger.info("[mm-metaclaw] memory/collect triggered (%d total)", self.memory_collect_count)

    async def _collect_skill(self, payload: dict) -> None:
        resp = await _http_post(f"{self._base}/v1/skill/collect", payload)
        if resp is not None:
            self.skill_collect_count += 1
            logger.info("[mm-metaclaw] skill/collect triggered (%d total)", self.skill_collect_count)

    async def _collect_all(self, payload: dict, session_id: str) -> None:
        tasks: list[asyncio.Task] = []
        if "memory" in self._cfg.enabled_modules:
            tasks.append(asyncio.create_task(self._collect_memory(payload)))
        if "skill" in self._cfg.enabled_modules:
            tasks.append(asyncio.create_task(self._collect_skill(payload)))
        if tasks:
            await asyncio.gather(*tasks)
