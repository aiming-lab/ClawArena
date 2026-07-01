"""clawarena-team CLI entry point.

Subcommands: check / run / resume / stats / clean / test.

All commands accept ``-c/--config`` pointing to a yaml or json override file; for
priority see :mod:`clawarena_team.config`.
"""
from __future__ import annotations

import asyncio
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import click

from . import __version__
from .config import Config, PathsConfig, load_config
from .provider import build_pool_from_config, parse_model_json, probe_and_apply
from .runner import RunRunner, load_dataset, validate_dataset
from .tokenizer import UnifiedTokenizer
from .types import ModelBundle

# ---------------------------------------------------------------------------
# Common helpers
# ---------------------------------------------------------------------------


def config_option(f):
    """The ``--config`` option decorator shared by all subcommands.

    No short option is used, to avoid clashing with each subcommand's
    ``-c/--concurrency`` / ``-c/--scenario-id`` etc.
    """
    return click.option(
        "--config", "config_path",
        default=None, type=click.Path(path_type=Path, exists=True, dir_okay=False),
        help="YAML/JSON config file; merges between CLI args and env vars.",
    )(f)


def _explicit(ctx: click.Context, name: str) -> bool:
    """Whether the CLI explicitly passed this parameter (used to distinguish "not passed" from "equal to the default")."""
    src = ctx.get_parameter_source(name)
    return src is not None and src.name == "COMMANDLINE"


def _build_cli_overrides(ctx: click.Context, mapping: dict[str, str]) -> dict[str, Any]:
    """Collect explicit CLI parameters into a dotted-path dict for :func:`load_config` to merge.

    ``mapping``: ``click param name → dotted yaml path``.
    """
    out: dict[str, Any] = {}
    for click_name, dotted in mapping.items():
        if not _explicit(ctx, click_name):
            continue
        value = ctx.params.get(click_name)
        if value is None:
            continue
        # Path → str (stored in the dict to make it yaml-friendly)
        if isinstance(value, Path):
            value = str(value)
        keys = dotted.split(".")
        cur = out
        for k in keys[:-1]:
            cur = cur.setdefault(k, {})
        cur[keys[-1]] = value
    return out


def _ensure_dataset_dir(p: Path, tests_filename: str = "tests.json") -> Path:
    p = p.resolve()
    if not (p / tests_filename).exists():
        raise click.ClickException(f"missing {p}/{tests_filename}")
    return p


def _build_tokenizer(cfg: Config) -> UnifiedTokenizer:
    return UnifiedTokenizer(
        tokenizer_source=cfg.get("tokenizer.source", "qwen3"),
        template_source=cfg.get("chat_template.source", "qwen3"),
        base_dir=cfg.yaml_path.parent if cfg.yaml_path else None,
    )


def _resolve_model_json(arg: str | None) -> str | None:
    """``--model`` fallback: CLI > env ``CATEAM_MODEL_JSON``. Returning None means use the main from yaml/env."""
    if arg:
        return arg
    env = os.environ.get("CATEAM_MODEL_JSON")
    return env or None


def _build_bundle(model_arg: str | None, cfg: Config) -> ModelBundle:
    pool_warnings: list[str] = []
    pool_errors: list[str] = []
    defaults_pool = build_pool_from_config(
        cfg.get("model_pool", {}) or {},
        warnings=pool_warnings, errors=pool_errors,
    )
    main_defaults = cfg.get("main", {}) or {}
    model_str = _resolve_model_json(model_arg)
    if model_str is None and not main_defaults.get("provider"):
        raise click.ClickException(
            "--model JSON is required (or set main.* in config / CATEAM_MODEL_JSON env var)"
        )
    raw: dict[str, Any] | str = model_str if model_str else {}
    bundle = parse_model_json(
        raw, defaults_pool=defaults_pool,
        main_defaults=main_defaults,
        warnings=pool_warnings, errors=pool_errors,
    )
    for w in pool_warnings:
        click.echo(f"[warn] {w}", err=True)
    if pool_errors:
        for e in pool_errors:
            click.echo(f"[error] {e}", err=True)
        raise click.ClickException("model pool failed static validation; aborting")
    return bundle


def _run_probe(bundle: ModelBundle, cfg: Config) -> None:
    probe_cfg = cfg.get("probe", {}) or {}
    if not probe_cfg.get("enabled", True):
        click.echo("[probe] disabled via config", err=True)
        return
    warnings: list[str] = []
    errors: list[str] = []
    asyncio.run(probe_and_apply(
        bundle,
        timeout_sec=float(probe_cfg.get("timeout_sec", 20.0)),
        max_tokens=int(probe_cfg.get("max_tokens", 4)),
        warnings=warnings,
        errors=errors,
    ))
    for w in warnings:
        click.echo(f"[probe-warn] {w}", err=True)
    if errors:
        for e in errors:
            click.echo(f"[probe-error] {e}", err=True)
        raise click.ClickException("modality probe failed required modalities; aborting")


@click.group(help="ClawArena-Team — Subagent Management Benchmark.")
@click.version_option(__version__)
def main() -> None:  # pragma: no cover - click entry point
    pass


# ---------------------------------------------------------------------------
# check
# ---------------------------------------------------------------------------


_CHECK_CLI_MAP = {
    "data_dir": "paths.data",
    "scenario_filter": "paths.scenario_filter",
    "strict": "paths.strict",
}


@main.command(help="Validate the dataset structure (strict).")
@click.option("-d", "--data", "data_dir", default=None, type=click.Path(path_type=Path))
@click.option("-t", "--scenario-id", "scenario_filter", default=None,
              help="Comma-separated scenario_ids to limit the check to.")
@click.option("-s", "--strict", is_flag=True, default=False,
              help="Treat warnings as errors (non-zero exit on any warning).")
@config_option
@click.pass_context
def check(
    ctx: click.Context,
    data_dir: Path | None,
    scenario_filter: str | None,
    strict: bool,
    config_path: Path | None,
) -> None:
    cfg = load_config(
        config_file=config_path,
        cli_overrides=_build_cli_overrides(ctx, _CHECK_CLI_MAP),
    )
    paths = cfg.paths()
    if paths.data is None:
        raise click.ClickException("-d/--data is required (or set paths.data in config)")
    data_path = _ensure_dataset_dir(paths.data)

    report = validate_dataset(data_path)
    warnings, errors = report.warnings, report.errors

    if paths.scenario_filter:
        wanted = {x.strip() for x in paths.scenario_filter.split(",") if x.strip()}
        def _relevant(line: str) -> bool:
            return any(w in line for w in wanted)
        warnings = [w for w in warnings if _relevant(w)]
        errors = [e for e in errors if _relevant(e)]

    for w in warnings:
        click.echo(f"[warn] {w}")
    for e in errors:
        click.echo(f"[error] {e}", err=True)

    ok = not errors and (not paths.strict or not warnings)
    if not ok:
        click.echo(
            f"FAIL — {len(errors)} errors, {len(warnings)} warnings (strict={paths.strict})",
            err=True,
        )
        sys.exit(1)
    click.echo(f"OK — {len(warnings)} warnings")


# ---------------------------------------------------------------------------
# run
# ---------------------------------------------------------------------------


_RUN_CLI_MAP = {
    "data_dir": "paths.data",
    "out_dir": "paths.run_output",
    "scenario_filter": "paths.scenario_filter",
    "tests_ref": "paths.tests_ref",
    "concurrency": "paths.concurrency",
    "retry": "scenario.retry",
}


@main.command(help="Run the benchmark (infer + score + report).")
@click.option("-d", "--data", "data_dir", default=None, type=click.Path(path_type=Path))
@click.option("-o", "--out", "out_dir", default=None, type=click.Path(path_type=Path))
@click.option("-m", "--model", "model_json", default=None,
              help="JSON string defining main/llm/vlm/omni models.")
@click.option("-c", "--concurrency", default=None, type=int)
@click.option("-t", "--scenario-id", "scenario_filter", default=None)
@click.option("--retry", default=None, type=int,
              help="Max attempts per scenario incl. first try; only execution errors "
                   "are retried, not check failures (default 3 from config).")
@click.option("--tests", "tests_ref", default=None,
              help="Tests file inside the dataset dir (default tests.json). "
                   "To run a custom subset, author your own tests-*.json alongside it; "
                   "to run individual scenarios, use -t/--scenario-id instead.")
@click.option("--skip-probe", is_flag=True, default=False,
              help="Skip the init-time modality probe (debug only).")
@config_option
@click.pass_context
def run(
    ctx: click.Context,
    data_dir: Path | None,
    out_dir: Path | None,
    model_json: str | None,
    concurrency: int | None,
    scenario_filter: str | None,
    retry: int | None,
    tests_ref: str | None,
    skip_probe: bool,
    config_path: Path | None,
) -> None:
    cfg = load_config(
        config_file=config_path,
        cli_overrides=_build_cli_overrides(ctx, _RUN_CLI_MAP),
    )
    paths = cfg.paths()
    if paths.data is None:
        raise click.ClickException("-d/--data is required")
    if paths.run_output is None:
        raise click.ClickException("-o/--out is required")
    data_path = _ensure_dataset_dir(paths.data, paths.tests_ref)
    out_path = paths.run_output
    out_path.mkdir(parents=True, exist_ok=True)

    _, manifests, scenarios = load_dataset(data_path, tests_filename=paths.tests_ref)
    if paths.scenario_filter:
        # ``-t`` supports comma-separated multiple ids (consistent with the check
        # subcommand's help behaviour); an unknown id immediately raises a
        # ClickException, to catch typos early.
        wanted = [s.strip() for s in paths.scenario_filter.split(",") if s.strip()]
        missing = [s for s in wanted if s not in scenarios]
        if missing:
            raise click.ClickException(
                f"scenario_id not found in dataset: {missing}"
            )
        scenarios = {s: scenarios[s] for s in wanted}

    bundle = _build_bundle(model_json, cfg)
    if not skip_probe:
        _run_probe(bundle, cfg)

    tokenizer = _build_tokenizer(cfg)
    runner = RunRunner(
        manifests=manifests,
        scenarios=scenarios,
        model_bundle=bundle,
        tokenizer=tokenizer,
        config_dict=cfg.as_dict(),
        output_root=out_path,
        concurrency=paths.concurrency,
    )
    result = asyncio.run(runner.run())
    click.echo(json.dumps(result, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------------------
# resume
# ---------------------------------------------------------------------------


_RESUME_CLI_MAP = {
    "data_dir": "paths.data",
    "old_out": "paths.resume_old",
    "new_out": "paths.resume_output",
    "tests_ref": "paths.tests_ref",
    "concurrency": "paths.concurrency",
    "retry": "scenario.retry",
}


@main.command("resume", help="Re-run scenarios that did not finish in a previous results dir.")
@click.option("-d", "--data", "data_dir", default=None, type=click.Path(path_type=Path))
@click.option("-O", "--old", "old_out", default=None, type=click.Path(path_type=Path),
              help="Path to the previous run's output directory (not run id).")
@click.option("-o", "--out", "new_out", default=None, type=click.Path(path_type=Path),
              help="New output directory; must not exist.")
@click.option("-m", "--model", "model_json", default=None)
@click.option("-c", "--concurrency", default=None, type=int)
@click.option("--retry", default=None, type=int,
              help="Max attempts per scenario incl. first try (default 3 from config).")
@click.option("--tests", "tests_ref", default=None,
              help="Tests file inside the dataset dir (default tests.json).")
@click.option("--skip-probe", is_flag=True, default=False)
@config_option
@click.pass_context
def resume(
    ctx: click.Context,
    data_dir: Path | None,
    old_out: Path | None,
    new_out: Path | None,
    model_json: str | None,
    concurrency: int | None,
    retry: int | None,
    tests_ref: str | None,
    skip_probe: bool,
    config_path: Path | None,
) -> None:
    cfg = load_config(
        config_file=config_path,
        cli_overrides=_build_cli_overrides(ctx, _RESUME_CLI_MAP),
    )
    paths = cfg.paths()
    if paths.data is None:
        raise click.ClickException("-d/--data is required")
    if paths.resume_old is None or paths.resume_output is None:
        raise click.ClickException("-O/--old and -o/--out are required")

    data_path = _ensure_dataset_dir(paths.data, paths.tests_ref)
    old_path = paths.resume_old
    new_path = paths.resume_output
    if new_path.exists():
        raise click.ClickException(f"new output dir already exists: {new_path}")
    new_path.mkdir(parents=True, exist_ok=False)

    _, manifests, scenarios = load_dataset(data_path, tests_filename=paths.tests_ref)

    completed: set[str] = set()
    if old_path.exists():
        for run_subdir in old_path.iterdir():
            if not run_subdir.is_dir():
                continue
            for sc_dir in run_subdir.iterdir():
                if (sc_dir / "metadata.json").exists():
                    completed.add(sc_dir.name)
                    target_run = new_path / run_subdir.name
                    target_run.mkdir(parents=True, exist_ok=True)
                    if not (target_run / sc_dir.name).exists():
                        shutil.copytree(sc_dir, target_run / sc_dir.name)

    todo = {sid: sc for sid, sc in scenarios.items() if sid not in completed}
    if not todo:
        click.echo("nothing to resume; all scenarios completed.")
        return

    bundle = _build_bundle(model_json, cfg)
    if not skip_probe:
        _run_probe(bundle, cfg)

    tokenizer = _build_tokenizer(cfg)
    runner = RunRunner(
        manifests=manifests,
        scenarios=todo,
        model_bundle=bundle,
        tokenizer=tokenizer,
        config_dict=cfg.as_dict(),
        output_root=new_path,
        concurrency=paths.concurrency,
    )
    result = asyncio.run(runner.run())
    click.echo(json.dumps(result, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


_STATS_CLI_MAP = {
    "data_dir": "paths.data",
    "out_dir": "paths.stats_output",
    "tokenizer_override": "paths.tokenizer_override",
    "tests_ref": "paths.tests_ref",
}


@main.command(help="Dataset statistics; with --out, write STATS.md + chart_*.png to a directory.")
@click.option("-d", "--data", "data_dir", default=None, type=click.Path(path_type=Path))
@click.option("-o", "--out", "out_dir", default=None, type=click.Path(path_type=Path),
              help="Output directory. When omitted, prints a short summary to stdout.")
@click.option("-t", "--tokenizer", "tokenizer_override", default=None,
              help="Override tokenizer source (default: configs/default.yaml `tokenizer.source`).")
@click.option("--tests", "tests_ref", default=None,
              help="Tests file inside the dataset dir (default tests.json).")
@config_option
@click.pass_context
def stats(
    ctx: click.Context,
    data_dir: Path | None,
    out_dir: Path | None,
    tokenizer_override: str | None,
    tests_ref: str | None,
    config_path: Path | None,
) -> None:
    from .stats import run_stats

    cfg = load_config(
        config_file=config_path,
        cli_overrides=_build_cli_overrides(ctx, _STATS_CLI_MAP),
    )
    paths = cfg.paths()
    if paths.data is None:
        raise click.ClickException("-d/--data is required")
    data_path = _ensure_dataset_dir(paths.data, paths.tests_ref)

    tok_source = paths.tokenizer_override or cfg.get("tokenizer.source", "qwen3")

    if paths.stats_output is None:
        _, _, scenarios = load_dataset(data_path, tests_filename=paths.tests_ref)
        total_rounds = sum(len(sc.rounds) for sc in scenarios.values())
        click.echo(f"scenarios: {len(scenarios)}")
        click.echo(f"total rounds: {total_rounds}")
        for sid, sc in scenarios.items():
            click.echo(f"  {sid}: {len(sc.rounds)} rounds, updates={len(sc.updates)}")
        return

    out_path = paths.stats_output
    path = run_stats(data_path, out_path, tokenizer=tok_source, tests_filename=paths.tests_ref)
    click.echo(f"stats report: {path}")
    click.echo(f"chart files:  {out_path}/chart_*.png")


# ---------------------------------------------------------------------------
# clean
# ---------------------------------------------------------------------------


_CLEAN_TARGET_DIRS: dict[str, list[str]] = {
    "work": ["work"],
    "logs": ["logs", "llm_logs"],
    "sessions": ["sessions"],
}

_CLEAN_CLI_MAP = {
    "out_dir": "paths.clean_output",
    "targets": "paths.clean_targets",
}


@main.command(help="Remove transient files under a results dir; choose targets via -t.")
@click.option("-o", "--out", "out_dir", default=None, type=click.Path(path_type=Path))
@click.option("-t", "--targets", default=None,
              help="Comma-separated: work,logs,sessions,all (default: work).")
@config_option
@click.pass_context
def clean(
    ctx: click.Context,
    out_dir: Path | None,
    targets: str | None,
    config_path: Path | None,
) -> None:
    cfg = load_config(
        config_file=config_path,
        cli_overrides=_build_cli_overrides(ctx, _CLEAN_CLI_MAP),
    )
    paths = cfg.paths()
    if paths.clean_output is None:
        raise click.ClickException("-o/--out is required")
    out_path = paths.clean_output
    if not out_path.exists():
        click.echo("(nothing to clean)")
        return
    selected = {x.strip() for x in paths.clean_targets.split(",") if x.strip()}
    if "all" in selected:
        selected = set(_CLEAN_TARGET_DIRS.keys())
    unknown = selected - set(_CLEAN_TARGET_DIRS.keys())
    if unknown:
        raise click.ClickException(
            f"unknown clean targets: {sorted(unknown)}; "
            f"allowed: {sorted(_CLEAN_TARGET_DIRS.keys()) + ['all']}"
        )
    dir_names: set[str] = set()
    for t in selected:
        dir_names.update(_CLEAN_TARGET_DIRS[t])
    removed = 0
    for p in out_path.rglob("*"):
        if p.is_dir() and p.name in dir_names:
            shutil.rmtree(p)
            click.echo(f"  removed: {p}")
            removed += 1
    click.echo(f"clean complete: removed {removed} dirs (targets={sorted(selected)})")


# ---------------------------------------------------------------------------
# compare
# ---------------------------------------------------------------------------


_COMPARE_CLI_MAP = {
    "out_dir": "paths.compare_output",
}


@main.command("compare", help="Cross-run comparison of report.json files (≥2).")
@click.option(
    "-r", "--report", "reports", multiple=True,
    type=click.Path(path_type=Path, exists=True, dir_okay=False),
    help="Path to a run's report.json; repeat -r for each run (≥2 required).",
)
@click.option(
    "-o", "--out", "out_dir", default=None, type=click.Path(path_type=Path),
    help="Output directory; writes comparison.json + comparison.md.",
)
@config_option
@click.pass_context
def compare(
    ctx: click.Context,
    reports: tuple[Path, ...],
    out_dir: Path | None,
    config_path: Path | None,
) -> None:
    cfg = load_config(
        config_file=config_path,
        cli_overrides=_build_cli_overrides(ctx, _COMPARE_CLI_MAP),
    )
    paths = cfg.paths()
    if len(reports) < 2:
        raise click.ClickException("at least 2 -r/--report paths required")
    target_dir = paths.compare_output or out_dir
    if target_dir is None:
        raise click.ClickException("-o/--out is required (or set paths.compare_output)")
    target = Path(target_dir).resolve()
    target.mkdir(parents=True, exist_ok=True)

    from .scoring.compare import build_comparison

    try:
        data, md_text = build_comparison(list(reports))
    except ValueError as e:
        raise click.ClickException(str(e))

    (target / "comparison.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (target / "comparison.md").write_text(md_text, encoding="utf-8")
    click.echo(f"comparison written to: {target}")


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------


@main.command(
    "report",
    help="Regenerate report.json/report.md from completed scenarios' metadata.json "
    "(stitch across one or more runs).",
)
@click.option(
    "-i", "--input", "inputs", multiple=True, required=True,
    type=click.Path(path_type=Path, exists=True, file_okay=False),
    help="Results dir to scan for scenario metadata.json (recursive); repeat -i to "
    "stitch completed scenarios across multiple runs.",
)
@click.option(
    "-o", "--out", "out_dir", required=True, type=click.Path(path_type=Path),
    help="Output directory; writes report.json + report.md.",
)
@click.option(
    "--run-id", "run_id", default="stitched", show_default=True,
    help="run_id label embedded in the regenerated report.",
)
@click.option(
    "-d", "--data", "data_path", default=None,
    type=click.Path(path_type=Path, exists=True, file_okay=False),
    help="Dataset dir; if given, report scenario coverage vs the full set (lists missing).",
)
def report(
    inputs: tuple[Path, ...],
    out_dir: Path,
    run_id: str,
    data_path: Path | None,
) -> None:
    """Regenerate the report by stitching together metadata.json of completed scenarios across runs.

    Completion criterion = metadata.json exists in the scenario's root directory
    (only written after scenario_runner finishes up). Because scenarios are
    independent, completed scenarios from different runs can be stitched into one
    full test pass. When a scenario appears multiple times, the one with the latest
    finished_at is kept. Note: this command does not judge whether the API errored;
    that must be checked manually elsewhere.
    """
    from .scoring.report import build_run_report, collect_scenario_metadata

    metadata, info = collect_scenario_metadata([Path(p) for p in inputs])
    if not metadata:
        raise click.ClickException(
            "no completed scenarios (metadata.json) found under the given -i input(s)"
        )

    report_json, report_md = build_run_report(run_id, metadata)
    target = Path(out_dir).resolve()
    target.mkdir(parents=True, exist_ok=True)
    (target / "report.json").write_text(
        json.dumps(report_json, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    (target / "report.md").write_text(report_md, encoding="utf-8")

    click.echo(
        f"stitched {info['unique']} unique scenario(s) from "
        f"{info['scanned']} metadata.json file(s)"
    )
    if info["duplicates"]:
        dups = sorted(info["duplicates"])
        click.echo(
            f"  {len(dups)} scenario(s) found in multiple runs "
            f"(kept latest finished_at): {', '.join(dups)}"
        )
    if data_path is not None:
        from .runner import load_dataset

        _, _, scenarios = load_dataset(Path(data_path))
        full = set(scenarios)
        have = {m.get("scenario_id") for m in metadata}
        click.echo(f"  coverage: {len(have & full)}/{len(full)} scenarios")
        missing = sorted(full - have)
        if missing:
            click.echo(f"  MISSING ({len(missing)}): {', '.join(missing)}")
    click.echo(f"report written to: {target}")


# ---------------------------------------------------------------------------
# test
# ---------------------------------------------------------------------------


@main.command(help="Equivalent to running 'pytest tests/' in the project root.")
@click.argument("pytest_args", nargs=-1)
def test(pytest_args: tuple[str, ...]) -> None:
    cmd = [sys.executable, "-m", "pytest", *pytest_args]
    rc = subprocess.call(cmd)
    sys.exit(rc)


if __name__ == "__main__":  # pragma: no cover
    main()
