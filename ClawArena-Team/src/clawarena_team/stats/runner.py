"""``clawarena-team stats`` entry point.

Output layout:
- ``<out>/STATS.md`` — main report
- ``<out>/chart_*.png`` — charts (skipped when matplotlib is unavailable)
"""
from __future__ import annotations

from pathlib import Path

from ..runner.dataset import load_dataset
from .base import BenchmarkStats
from .charts import render_charts
from .collect import collect_benchmark
from .render import render_markdown
from .tokenizer import TokenCounter


def generate_stats_report(bench: BenchmarkStats, out_dir: Path) -> Path:
    """Render charts + STATS.md into ``out_dir`` and return the STATS.md path."""
    out_dir.mkdir(parents=True, exist_ok=True)
    charts = render_charts(bench, out_dir)
    md = render_markdown(bench, charts)
    path = out_dir / "STATS.md"
    path.write_text(md, encoding="utf-8")
    return path


def run_stats(
    data_dir: Path,
    out_dir: Path,
    *,
    tokenizer: str = "qwen3",
    name: str | None = None,
    tests_filename: str = "tests.json",
) -> Path:
    """Collect dataset statistics → write charts + STATS.md. Return the STATS.md path."""
    tests, _, scenarios = load_dataset(data_dir, tests_filename=tests_filename)
    counter = TokenCounter(tokenizer)
    bench = collect_benchmark(
        scenarios, counter=counter, name=name or tests.name,
    )
    return generate_stats_report(bench, out_dir)
