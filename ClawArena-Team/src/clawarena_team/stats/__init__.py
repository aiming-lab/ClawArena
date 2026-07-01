"""ClawArena-Team dataset statistics and visualization.

Public API:

- :func:`run_stats`: CLI entry point; generates ``<out>/STATS.md`` + ``chart_*.png`` from a dataset.
- :func:`generate_stats_report`: render ``BenchmarkStats`` in memory.
- :func:`collect_benchmark`: build ``BenchmarkStats`` from an already-loaded set of scenarios.

The module split mirrors ClawArena ``clawarena.stats``, making it easy to extend with custom categories or charts.
"""
from .base import (
    ALL_CATEGORIES,
    ALL_MODALITIES,
    CATEGORY_COLORS,
    CATEGORY_LABELS,
    MODALITY_COLORS,
    BenchmarkStats,
    FileFact,
    RoundFact,
    ScenarioStats,
    UpdateFact,
    WorkspaceFact,
)
from .charts import render_charts
from .collect import collect_benchmark
from .render import render_markdown
from .runner import generate_stats_report, run_stats
from .tokenizer import TokenCounter

__all__ = [
    "ALL_CATEGORIES",
    "ALL_MODALITIES",
    "BenchmarkStats",
    "CATEGORY_COLORS",
    "CATEGORY_LABELS",
    "FileFact",
    "MODALITY_COLORS",
    "RoundFact",
    "ScenarioStats",
    "TokenCounter",
    "UpdateFact",
    "WorkspaceFact",
    "collect_benchmark",
    "generate_stats_report",
    "render_charts",
    "render_markdown",
    "run_stats",
]
