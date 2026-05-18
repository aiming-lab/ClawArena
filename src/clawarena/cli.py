"""clawarena CLI — entry point for the multi-framework benchmark platform.

Commands:
  check         Validate data integrity
  infer         Run agent inference
  resume-infer  Resume an interrupted inference run
  score         Score infer results
  report        Generate report from scoring
  compare       Compare multiple framework reports
  run           Full pipeline: infer + score + report (+ compare)
  clean         Remove temporary files
  stats         Token counting and statistics
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------


def cmd_check(args: argparse.Namespace) -> None:
    from clawarena.core.check import run_check
    _load_plugins(args)
    fws = args.framework.split(",") if args.framework else None
    tids = args.test_id.split(",") if args.test_id else None
    ok = run_check(
        Path(args.data), frameworks=fws, test_ids=tids, strict=args.strict,
    )
    if not ok:
        sys.exit(1)


def cmd_infer(args: argparse.Namespace) -> None:
    from clawarena.core.infer import run_infer
    from clawarena.core.provider import ModelConfig
    _load_plugins(args)
    out_dir = _prepare_infer_out(args.out)
    cli_model = ModelConfig.from_cli(
        getattr(args, "provider", None),
        getattr(args, "model_id", None),
        getattr(args, "api_base", None),
        getattr(args, "api_key", None),
        getattr(args, "model_config", None),
    )
    tids = args.test_id.split(",") if args.test_id else None
    asyncio.run(run_infer(
        Path(args.data), args.framework, out_dir,
        concurrency=args.concurrency,
        timeout=args.timeout, retry=args.retry,
        cli_model=cli_model,
        overlay=getattr(args, "overlay", None),
        test_ids=tids,
    ))


def cmd_resume_infer(args: argparse.Namespace) -> None:
    from clawarena.core.infer import resume_infer
    _load_plugins(args)
    asyncio.run(resume_infer(
        Path(args.data), args.framework, Path(args.out),
        state_dir=Path(args.state_dir),
        workspace_dir=Path(args.workspace_dir) if args.workspace_dir else None,
        concurrency=args.concurrency,
        timeout=args.timeout,
        retry=args.retry,
        inplace=args.inplace,
    ))


def cmd_score(args: argparse.Namespace) -> None:
    from clawarena.core.scoring import run_scoring
    out = Path(args.out) if args.out else None
    run_scoring(Path(args.infer_dir), out)


def cmd_report(args: argparse.Namespace) -> None:
    from clawarena.core.report import generate_report
    generate_report(Path(args.score_dir), Path(args.out), Path(args.data))


def cmd_compare(args: argparse.Namespace) -> None:
    from clawarena.core.compare import generate_comparison
    paths = [Path(p) for p in args.reports]
    generate_comparison(paths, Path(args.out))


def cmd_run(args: argparse.Namespace) -> None:
    from clawarena.core.provider import ModelConfig
    from clawarena.core.run import run_all
    _load_plugins(args)
    fws = args.frameworks.split(",")
    cli_model = ModelConfig.from_cli(
        getattr(args, "provider", None),
        getattr(args, "model_id", None),
        getattr(args, "api_base", None),
        getattr(args, "api_key", None),
        getattr(args, "model_config", None),
    )
    tids = args.test_id.split(",") if getattr(args, "test_id", None) else None
    run_all(
        Path(args.data), fws, Path(args.out),
        concurrency=args.concurrency, timeout=args.timeout,
        retry=args.retry, clean_temp=args.clean_temp,
        cli_model=cli_model,
        overlay=getattr(args, "overlay", None),
        test_ids=tids,
    )


def cmd_clean(args: argparse.Namespace) -> None:
    from clawarena.core.clean import run_clean
    targets = args.targets.split(",") if args.targets else None
    run_clean(Path(args.out), targets)


def cmd_stats(args: argparse.Namespace) -> None:
    from clawarena.stats import run_stats
    run_stats(
        Path(args.data), args.framework, Path(args.out),
        tokenizer=args.tokenizer,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_plugins(args: argparse.Namespace) -> None:
    """Load external adapter plugins if --plugin is specified."""
    plugin_paths = getattr(args, "plugin", None) or []
    if plugin_paths:
        from clawarena.plugins.loader import load_plugins
        load_plugins(plugin_paths)


def _add_model_args(p: argparse.ArgumentParser) -> None:
    """Add --provider / --model-id / --api-base / --api-key / --model-config to a subparser."""
    g = p.add_argument_group("model override")
    g.add_argument("--provider", default=None,
                   help="LLM provider (openai/anthropic/claude/bedrock/google/ollama/azure"
                        "/openrouter/groq/mistral/xai/qwen/moonshot/glm/minimax/copilot/telnyx)")
    g.add_argument("--model-id", default=None, help="Model name, e.g. gpt-4o")
    g.add_argument("--api-base", default=None, help="API endpoint URL")
    g.add_argument("--api-key", default=None, help="API key (prefer env vars)")
    g.add_argument(
        "--model-config", default=None, metavar="JSON",
        help=(
            "JSON object with extra model-entry fields forwarded to framework config. "
            "Example: '{\"reasoning\": true, \"contextWindow\": 200000}'"
        ),
    )


def _prepare_infer_out(out_arg: str) -> Path:
    import uuid
    out = Path(out_arg)
    if out.exists() and any(out.iterdir()):
        sub = f"infer_{uuid.uuid4().hex[:8]}"
        out = out / sub
    out.mkdir(parents=True, exist_ok=True)
    return out


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="clawarena",
        description="Multi-framework AI Agent benchmark evaluation platform",
    )
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # ---- check ----
    p = sub.add_parser("check", help="Validate data integrity")
    p.add_argument("-d", "--data", required=True, help="Path to tests.json")
    p.add_argument("-f", "--framework", default=None, help="Comma-separated framework names")
    p.add_argument("-t", "--test-id", default=None, help="Comma-separated test IDs")
    p.add_argument("-s", "--strict", action="store_true", help="Treat warnings as errors")
    p.add_argument("-p", "--plugin", nargs="+", default=None, metavar="PATH",
                   help="External adapter plugin .py files (loaded before validation "
                        "so framework-specific checks register)")

    # ---- infer ----
    p = sub.add_parser("infer", help="Run agent inference")
    p.add_argument("-d", "--data", required=True, help="Path to tests.json")
    p.add_argument("-f", "--framework", required=True, help="Framework name")
    p.add_argument("-o", "--out", required=True, help="Output directory")
    p.add_argument("-t", "--test-id", default=None, help="Comma-separated test IDs")
    p.add_argument("-c", "--concurrency", type=int, default=4)
    p.add_argument("-T", "--timeout", type=float, default=300)
    p.add_argument("-r", "--retry", type=int, default=1)
    p.add_argument("-p", "--plugin", nargs="+", default=None, metavar="PATH",
                    help="External adapter plugin .py files")
    p.add_argument(
        "--overlay", default=None, metavar="JSON",
        help=(
            "JSON string to override 'metaclaw' and/or 'mm_metaclaw' fields "
            "from tests.json (shallow merge per section). "
            "Example: '{\"mm_metaclaw\":{\"enabled\":true,\"hook_mode\":\"http\"}}'"
        ),
    )
    _add_model_args(p)

    # ---- resume-infer ----
    p = sub.add_parser("resume-infer", help="Resume interrupted inference")
    p.add_argument("-d", "--data", required=True, help="Path to tests.json")
    p.add_argument("-f", "--framework", required=True, help="Framework name")
    p.add_argument("-o", "--out", required=True, help="Existing infer results directory")
    p.add_argument("-S", "--state-dir", required=True, help="Existing state directory")
    p.add_argument("-W", "--workspace-dir", default=None, help="Existing workspace directory")
    p.add_argument("-c", "--concurrency", type=int, default=4)
    p.add_argument("-T", "--timeout", type=float, default=300)
    p.add_argument("-r", "--retry", type=int, default=1)
    p.add_argument("-i", "--inplace", action="store_true", default=False,
                   help="Use original state/workspace dirs in-place (backup first)")
    p.add_argument("-p", "--plugin", nargs="+", default=None, metavar="PATH",
                   help="External adapter plugin .py files")

    # ---- score ----
    p = sub.add_parser("score", help="Score infer results")
    p.add_argument("-d", "--infer-dir", required=True, help="Infer results directory")
    p.add_argument("-o", "--out", default=None, help="Output directory (default: in-place)")

    # ---- report ----
    p = sub.add_parser("report", help="Generate report from scoring")
    p.add_argument("-d", "--data", required=True, help="Path to tests.json (for round ordering)")
    p.add_argument("-s", "--score-dir", required=True, help="Scoring results directory")
    p.add_argument("-o", "--out", required=True, help="Report output directory")

    # ---- compare ----
    p = sub.add_parser("compare", help="Compare framework reports")
    p.add_argument("-r", "--reports", nargs="+", required=True, help="report.json paths (>=2)")
    p.add_argument("-o", "--out", required=True, help="Comparison output directory")

    # ---- run ----
    p = sub.add_parser("run", help="Full pipeline: infer + score + report")
    p.add_argument("-d", "--data", required=True, help="Path to tests.json")
    p.add_argument("-f", "--frameworks", required=True, help="Comma-separated framework names")
    p.add_argument("-o", "--out", required=True, help="Top-level output directory")
    p.add_argument("-t", "--test-id", default=None, help="Comma-separated test IDs")
    p.add_argument("-c", "--concurrency", type=int, default=4)
    p.add_argument("-T", "--timeout", type=float, default=300)
    p.add_argument("-r", "--retry", type=int, default=1)
    p.add_argument("-p", "--plugin", nargs="+", default=None, metavar="PATH",
                    help="External adapter plugin .py files")
    p.add_argument("--clean-temp", action="store_true")
    p.add_argument(
        "--overlay", default=None, metavar="JSON",
        help=(
            "JSON string to override 'metaclaw' and/or 'mm_metaclaw' fields "
            "from tests.json (shallow merge per section). "
            "Example: '{\"mm_metaclaw\":{\"enabled\":true,\"enabled_modules\":[\"proxy\",\"memory\"]}}'"
        ),
    )
    _add_model_args(p)

    # ---- clean ----
    p = sub.add_parser("clean", help="Remove temporary files")
    p.add_argument("-o", "--out", required=True, help="Target output directory")
    p.add_argument("-t", "--targets", default=None, help="Comma-separated: work,logs,all")

    # ---- stats ----
    p = sub.add_parser("stats", help="Token counting and statistics")
    p.add_argument("-d", "--data", required=True, help="Path to tests.json")
    p.add_argument("-f", "--framework", default=None, help="Framework name (default: all)")
    p.add_argument("-o", "--out", required=True, help="Output directory")
    p.add_argument("-t", "--tokenizer", default="cl100k_base")

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(0)

    commands = {
        "check": cmd_check,
        "infer": cmd_infer,
        "resume-infer": cmd_resume_infer,
        "score": cmd_score,
        "report": cmd_report,
        "compare": cmd_compare,
        "run": cmd_run,
        "clean": cmd_clean,
        "stats": cmd_stats,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
