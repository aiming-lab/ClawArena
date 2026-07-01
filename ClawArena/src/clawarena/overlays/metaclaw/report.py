"""MetaClaw report collection and generation — covers all modes."""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field
from pathlib import Path

from clawarena.overlays.metaclaw.config import MetaClawConfig
from clawarena.overlays.metaclaw.hooks import MetaClawHooks
from clawarena.overlays.metaclaw.run_dir import MetaClawRunDir

logger = logging.getLogger(__name__)


@dataclass
class MetaClawRunReport:
    run_id: str = ""
    started_at: str = ""
    elapsed_seconds: float = 0.0
    framework: str = ""
    test_count: int = 0
    mode_flags: dict = field(default_factory=dict)
    proxy_url: str = ""
    config_summary: dict = field(default_factory=dict)
    triggers: dict = field(default_factory=dict)
    memory_stats: dict | None = None
    memory_health: dict | None = None
    memory_summary: dict | None = None
    memory_operator_report: dict | None = None
    memory_feedback_analysis: dict | None = None
    skills_snapshot: dict | None = None
    rl_summary: dict | None = None


class MetaClawCollector:
    def __init__(
        self,
        proxy_url: str,
        config: MetaClawConfig,
        hooks: MetaClawHooks,
        run_dir: MetaClawRunDir,
    ):
        self._url = proxy_url
        self._config = config
        self._hooks = hooks
        self._run_dir = run_dir

    async def collect(
        self,
        elapsed_seconds: float,
        framework: str = "",
        test_count: int = 0,
    ) -> MetaClawRunReport:
        report = MetaClawRunReport(
            run_id=self._run_dir.run_id,
            elapsed_seconds=elapsed_seconds,
            framework=framework,
            test_count=test_count,
            mode_flags={
                "memory": self._config.memory.enabled,
                "skills": self._config.skills.enabled,
                "rl": self._config.rl.enabled,
            },
            proxy_url=self._url,
            config_summary={
                "served_model_name": self._config.served_model_name,
                "max_context_tokens": self._config.max_context_tokens,
            },
            triggers={
                "memory_ingest": self._hooks.memory_ingest_count,
                "rl_train": self._hooks.rl_train_count,
                "scenes_completed": self._hooks.completed_scenes,
            },
        )

        if self._config.memory.enabled:
            report.memory_stats = await self._get_json("/v1/memory/stats")
            report.memory_health = await self._get_json("/v1/memory/health")
            report.memory_summary = await self._get_json("/v1/memory/summary")
            report.memory_operator_report = await self._get_json("/v1/memory/operator-report")
            report.memory_feedback_analysis = await self._get_json("/v1/memory/feedback-analysis")

        if self._config.skills.enabled and self._run_dir.skills_snapshot_dir:
            count_after = sum(
                1 for f in self._run_dir.skills_snapshot_dir.rglob("*") if f.is_file()
            )
            meta_path = self._run_dir.root / "skills_meta.json"
            count_before = 0
            if meta_path.exists():
                count_before = json.loads(meta_path.read_text()).get("count_before", 0)
            report.skills_snapshot = {
                "skills_dir": str(self._run_dir.skills_snapshot_dir),
                "count_before": count_before,
                "count_after": count_after,
                "evolved_count": count_after - count_before,
                "auto_evolve": self._config.skills.auto_evolve,
                "top_k": self._config.skills.top_k,
            }

        if self._config.rl.enabled:
            report.rl_summary = {
                "scene_per_train": self._config.rl.scene_per_train,
                "total_scenes": self._hooks.completed_scenes,
                "train_triggers": self._hooks.rl_train_count,
                "estimated_steps": self._hooks.rl_train_count * self._config.rl.batch_size,
                "lora_rank": self._config.rl.lora_rank,
                "batch_size": self._config.rl.batch_size,
                "model": self._config.rl.model,
            }

        return report

    async def _get_json(self, path: str) -> dict | None:
        try:
            import aiohttp
            async with aiohttp.ClientSession() as s:
                async with s.get(
                    f"{self._url}{path}",
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as r:
                    if r.status == 200:
                        return await r.json()
        except Exception as e:
            logger.debug("Failed to GET %s%s: %s", self._url, path, e)
        return None


def write_report(report: MetaClawRunReport, out_dir: Path) -> None:
    """Write metaclaw_report.json and metaclaw_report.md to out_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)

    # JSON
    json_path = out_dir / "metaclaw_report.json"
    json_path.write_text(json.dumps(asdict(report), indent=2, ensure_ascii=False))

    # Markdown
    md_path = out_dir / "metaclaw_report.md"
    md_path.write_text(_render_markdown(report))


def _render_markdown(r: MetaClawRunReport) -> str:
    lines = [
        "# MetaClaw Run Report",
        f"Generated: {r.started_at} | Duration: {r.elapsed_seconds:.1f}s | Framework: {r.framework}",
        "",
        "## Run Configuration",
        "| Field | Value |",
        "|---|---|",
    ]
    for k, v in r.config_summary.items():
        lines.append(f"| {k} | {v} |")
    modes = "+".join(k for k, v in r.mode_flags.items() if v) or "baseline"
    lines.append(f"| mode | {modes} |")
    lines.append(f"| test_count | {r.test_count} |")

    lines += [
        "",
        "## Trigger Summary",
        "| Event | Count |",
        "|---|---|",
    ]
    for k, v in r.triggers.items():
        lines.append(f"| {k} | {v} |")

    if r.memory_stats:
        lines += ["", "## Memory Report"]
        lines += ["### Stats", f"```json\n{json.dumps(r.memory_stats, indent=2)}\n```"]
    if r.memory_health:
        lines += ["### Health", f"```json\n{json.dumps(r.memory_health, indent=2)}\n```"]
    if r.memory_summary:
        lines += ["### Summary", f"```json\n{json.dumps(r.memory_summary, indent=2)}\n```"]

    if r.skills_snapshot:
        lines += [
            "", "## Skills Report",
            "| Metric | Value |",
            "|---|---|",
        ]
        for k, v in r.skills_snapshot.items():
            lines.append(f"| {k} | {v} |")

    if r.rl_summary:
        lines += [
            "", "## RL Training Report",
            "| Metric | Value |",
            "|---|---|",
        ]
        for k, v in r.rl_summary.items():
            lines.append(f"| {k} | {v} |")

    return "\n".join(lines) + "\n"
