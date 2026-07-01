"""Stats entry points: run_stats, generate_stats_report."""

from __future__ import annotations

from pathlib import Path

from clawarena.core.io import load_tests_config
from clawarena.stats.base import BenchmarkStats
from clawarena.stats.charts import render_charts
from clawarena.stats.collect import collect_benchmark
from clawarena.stats.render import render_markdown
from clawarena.stats.tokenizer import TokenCounter


def generate_stats_report(bench: BenchmarkStats, out_dir: Path) -> Path:
    """Render charts + STATS.md into out_dir; return STATS.md path."""
    out_dir.mkdir(parents=True, exist_ok=True)
    charts = render_charts(bench, out_dir)
    md = render_markdown(bench, charts)
    path = out_dir / "STATS.md"
    path.write_text(md, encoding="utf-8")
    return path


def run_stats(
    tests_json_path: Path, framework: str | None, out_dir: Path,
    tokenizer: str = "cl100k_base",
) -> None:
    """Generate stats reports.

    If `framework` is None, run for every framework registered in tests.json.
    Single-framework runs land in `out_dir`; multi-framework runs land under
    `out_dir/<fw>/`.
    """
    cfg = load_tests_config(tests_json_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    counter = TokenCounter(tokenizer)
    print(f"Tokenizer: {tokenizer}")

    fws = [framework] if framework else list(cfg["frameworks"].keys())
    for fw in fws:
        if fw not in cfg["frameworks"]:
            print(f"[warn] Framework '{fw}' not in tests.json, skipping")
            continue
        print(f"\n{'=' * 60}")
        print(f"Framework: {fw}")
        bench = collect_benchmark(tests_json_path, fw, counter)
        print(
            f"  Scenarios: {bench.total_scenarios}, "
            f"Rounds: {bench.total_rounds}, "
            f"Tokens: {bench.total_tokens:,}"
        )
        fw_out = out_dir / fw if len(fws) > 1 else out_dir
        path = generate_stats_report(bench, fw_out)
        print(f"  Report: {path}")
