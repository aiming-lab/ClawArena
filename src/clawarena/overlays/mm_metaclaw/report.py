"""mm-metaclaw run report — collect gateway stats and render markdown/JSON."""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from clawarena.overlays.mm_metaclaw.hooks import MmMetaClawHooks

logger = logging.getLogger(__name__)


@dataclass
class ModuleStats:
    """Stats for a single gateway module."""
    name: str
    enabled: bool = False
    extra: dict = field(default_factory=dict)


@dataclass
class MmMetaClawRunReport:
    """Aggregate report for a mm-metaclaw benchmark run."""
    started_at: str = ""
    elapsed_sec: float = 0.0
    framework: str = ""
    test_count: int = 0
    hook_mode: str = "proxy"
    enabled_modules: list[str] = field(default_factory=list)
    memory_collect_count: int = 0
    skill_collect_count: int = 0
    memory_inject_count: int = 0
    skill_inject_count: int = 0
    module_stats: list[ModuleStats] = field(default_factory=list)


def _render_markdown(report: MmMetaClawRunReport) -> str:
    lines = [
        "# mm-metaclaw Run Report",
        "",
        f"**Started**: {report.started_at}",
        f"**Framework**: {report.framework}",
        f"**Tests**: {report.test_count}",
        f"**Hook mode**: `{report.hook_mode}`",
        f"**Enabled modules**: {', '.join(report.enabled_modules) or '(none)'}",
        f"**Elapsed**: {report.elapsed_sec:.1f}s",
        "",
        "## Hook Counters",
        "",
        "| Event | Count |",
        "|---|---|",
        f"| memory/collect | {report.memory_collect_count} |",
        f"| skill/collect | {report.skill_collect_count} |",
        f"| memory/inject (http mode) | {report.memory_inject_count} |",
        f"| skill/inject (http mode) | {report.skill_inject_count} |",
    ]
    if report.module_stats:
        lines += ["", "## Module Stats", ""]
        for ms in report.module_stats:
            lines.append(f"### {ms.name}")
            if ms.extra:
                for k, v in ms.extra.items():
                    lines.append(f"- **{k}**: {v}")
            else:
                lines.append("*(no stats available)*")
    return "\n".join(lines) + "\n"


def write_report(report: MmMetaClawRunReport, out_dir: Path) -> None:
    """Write ``mm_metaclaw_report.json`` and ``mm_metaclaw_report.md`` to *out_dir*."""
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "mm_metaclaw_report.json"
    md_path = out_dir / "mm_metaclaw_report.md"

    json_path.write_text(
        json.dumps(asdict(report), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    md_path.write_text(_render_markdown(report), encoding="utf-8")
    logger.info("mm-metaclaw report written to %s", out_dir)


class MmMetaClawCollector:
    """Fetches live stats from gateway endpoints and builds a run report."""

    _STAT_ENDPOINTS: list[tuple[str, str]] = [
        ("memory", "/v1/memory/stats"),
        ("skill", "/v1/skill/status"),
    ]

    def __init__(
        self,
        gateway_url: str,
        hooks: "MmMetaClawHooks",
        enabled_modules: list[str],
    ):
        self._base = gateway_url.rstrip("/")
        self._hooks = hooks
        self._enabled = set(enabled_modules)

    async def collect(
        self,
        elapsed_sec: float,
        framework: str,
        test_count: int,
    ) -> MmMetaClawRunReport:
        module_stats: list[ModuleStats] = []
        for mod_name, endpoint in self._STAT_ENDPOINTS:
            if mod_name not in self._enabled:
                continue
            extra = await self._fetch_stats(endpoint)
            module_stats.append(ModuleStats(name=mod_name, enabled=True, extra=extra))

        return MmMetaClawRunReport(
            elapsed_sec=elapsed_sec,
            framework=framework,
            test_count=test_count,
            hook_mode=self._hooks._cfg.hook_mode,
            enabled_modules=list(self._hooks._cfg.enabled_modules),
            memory_collect_count=self._hooks.memory_collect_count,
            skill_collect_count=self._hooks.skill_collect_count,
            memory_inject_count=self._hooks.memory_inject_count,
            skill_inject_count=self._hooks.skill_inject_count,
            module_stats=module_stats,
        )

    async def _fetch_stats(self, endpoint: str) -> dict:
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self._base}{endpoint}",
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as resp:
                    if resp.status == 200:
                        return await resp.json()
        except Exception as exc:
            logger.debug("mm-metaclaw stats %s failed: %s", endpoint, exc)
        return {}
