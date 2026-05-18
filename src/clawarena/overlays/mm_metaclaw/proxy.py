"""mm-metaclaw gateway process management."""

from __future__ import annotations

import asyncio
import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)

_HEALTH_ENDPOINT = "/v1/health"
_HEALTH_TIMEOUT_S = 60.0
_HEALTH_POLL_INTERVAL_S = 0.5


@dataclass
class GatewayProcess:
    """Manages a single mm-metaclaw gateway daemon subprocess."""

    host: str
    port: int
    gateway_dir: Path
    _process: asyncio.subprocess.Process | None = field(default=None, repr=False)
    _log_fh: "object | None" = field(default=None, repr=False)

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"

    async def start(self, log_path: Path | None = None) -> None:
        """Launch ``python3 -m mm_metaclaw start --daemon`` from gateway_dir."""
        stdout_sink = asyncio.subprocess.DEVNULL
        stderr_sink = asyncio.subprocess.DEVNULL
        if log_path:
            self._log_fh = open(log_path, "w")
            stdout_sink = self._log_fh
            stderr_sink = self._log_fh
            logger.info("mm-metaclaw gateway log → %s", log_path)

        self._process = await asyncio.create_subprocess_exec(
            sys.executable, "-m", "mm_metaclaw", "start", "--daemon",
            "--log-file", str(log_path or "/tmp/mm_metaclaw.log"),
            stdout=stdout_sink,
            stderr=stderr_sink,
            cwd=str(self.gateway_dir),
        )
        await self._wait_healthy()

    async def _wait_healthy(self, timeout: float = _HEALTH_TIMEOUT_S) -> None:
        """Poll ``/v1/health`` until HTTP 200 or timeout."""
        import aiohttp

        deadline = asyncio.get_event_loop().time() + timeout
        while asyncio.get_event_loop().time() < deadline:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{self.url}{_HEALTH_ENDPOINT}",
                        timeout=aiohttp.ClientTimeout(total=2),
                    ) as resp:
                        if resp.status == 200:
                            logger.info("mm-metaclaw gateway ready at %s", self.url)
                            return
            except Exception:
                pass
            await asyncio.sleep(_HEALTH_POLL_INTERVAL_S)
        raise RuntimeError(
            f"mm-metaclaw gateway at {self.url} did not become healthy "
            f"within {timeout:.0f}s"
        )

    async def stop(self) -> None:
        """Stop the gateway daemon gracefully, then force-kill if needed."""
        # Try the CLI stop command first (cleanly shuts down via PID file)
        try:
            stop_proc = await asyncio.create_subprocess_exec(
                sys.executable, "-m", "mm_metaclaw", "stop",
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
                cwd=str(self.gateway_dir),
            )
            await asyncio.wait_for(stop_proc.wait(), timeout=10)
        except Exception as exc:
            logger.warning("mm-metaclaw stop command failed (%s); falling back to SIGTERM", exc)

        # Fall back: terminate the subprocess we spawned directly
        if self._process is not None:
            try:
                self._process.terminate()
                await asyncio.wait_for(self._process.wait(), timeout=10)
            except asyncio.TimeoutError:
                self._process.kill()
                await self._process.wait()
            except ProcessLookupError:
                pass
            self._process = None

        if self._log_fh:
            self._log_fh.close()
            self._log_fh = None
