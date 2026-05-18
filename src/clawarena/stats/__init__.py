"""Stats package — comprehensive benchmark structural & token analysis.

Public API:

- :func:`run_stats` — CLI entry point.
- :func:`generate_stats_report` — render an in-memory BenchmarkStats.
- :func:`collect_benchmark` — build a BenchmarkStats from tests.json.
- :class:`FrameworkLayout` — per-framework session layout protocol.
- :func:`get_layout`, :func:`register_layout` — layout registry.
"""

from clawarena.stats.base import (
    ALL_CATEGORIES,
    CATEGORY_LABELS,
    BenchmarkStats,
    FrameworkLayout,
    RoundFact,
    ScenarioStats,
    UpdateFact,
)
from clawarena.stats.charts import render_charts
from clawarena.stats.collect import collect_benchmark
from clawarena.stats.registry import (
    get_layout,
    register_layout,
    registered_frameworks,
)
from clawarena.stats.render import render_markdown
from clawarena.stats.runner import generate_stats_report, run_stats
from clawarena.stats.tokenizer import TokenCounter

__all__ = [
    "ALL_CATEGORIES",
    "CATEGORY_LABELS",
    "BenchmarkStats",
    "FrameworkLayout",
    "RoundFact",
    "ScenarioStats",
    "TokenCounter",
    "UpdateFact",
    "collect_benchmark",
    "generate_stats_report",
    "get_layout",
    "register_layout",
    "registered_frameworks",
    "render_charts",
    "render_markdown",
    "run_stats",
]
