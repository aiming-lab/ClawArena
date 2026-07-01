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
import sys


# ---------------------------------------------------------------------------
# Command handlers
#
# CLI 命令统一经 SDK（``clawarena.ClawArena``）落地，保证 CLI 与 SDK 行为一致、
# 逻辑不重复。CLI 仅负责参数解析与 ModelConfig 构造。
# ---------------------------------------------------------------------------


def _cli_model(args: argparse.Namespace):
    """从 CLI 模型参数构造 ModelConfig（无 --model-id 时返回 None）。"""
    from clawarena.core.provider import ModelConfig
    return ModelConfig.from_cli(
        getattr(args, "provider", None),
        getattr(args, "model_id", None),
        getattr(args, "api_base", None),
        getattr(args, "api_key", None),
        getattr(args, "model_config", None),
    )


def _sdk(args: argparse.Namespace):
    """由 CLI 参数构造一个 ClawArena（含 --plugin 加载）。"""
    from clawarena import ClawArena
    return ClawArena(plugins=getattr(args, "plugin", None))


def cmd_check(args: argparse.Namespace) -> None:
    ok = _sdk(args).check(
        framework=args.framework, test_id=args.test_id, strict=args.strict,
        data=args.data,
    )
    if not ok:
        sys.exit(1)


def cmd_infer(args: argparse.Namespace) -> None:
    _sdk(args).infer(
        args.framework,
        out=args.out, test_id=args.test_id,
        concurrency=args.concurrency, timeout=args.timeout, retry=args.retry,
        model=_cli_model(args), overlay=getattr(args, "overlay", None),
        data=args.data,
    )


def cmd_resume_infer(args: argparse.Namespace) -> None:
    _sdk(args).resume_infer(
        args.framework, args.out, args.state_dir,
        workspace_dir=args.workspace_dir or None,
        concurrency=args.concurrency, timeout=args.timeout, retry=args.retry,
        inplace=args.inplace, data=args.data,
    )


def cmd_score(args: argparse.Namespace) -> None:
    _sdk(args).score(args.infer_dir, out=args.out or None)


def cmd_report(args: argparse.Namespace) -> None:
    _sdk(args).report(args.score_dir, out=args.out, data=args.data)


def cmd_compare(args: argparse.Namespace) -> None:
    _sdk(args).compare(args.reports, out=args.out)


def cmd_run(args: argparse.Namespace) -> None:
    _sdk(args).run(
        args.frameworks,
        out=args.out, test_id=getattr(args, "test_id", None),
        concurrency=args.concurrency, timeout=args.timeout, retry=args.retry,
        clean_temp=args.clean_temp,
        model=_cli_model(args), overlay=getattr(args, "overlay", None),
        data=args.data,
    )


def cmd_clean(args: argparse.Namespace) -> None:
    _sdk(args).clean(out=args.out, targets=args.targets)


def cmd_stats(args: argparse.Namespace) -> None:
    _sdk(args).stats(
        framework=args.framework, out=args.out, tokenizer=args.tokenizer,
        data=args.data,
    )


def cmd_fetch_data(args: argparse.Namespace) -> None:
    from clawarena.datafetch import DEFAULT_REPO, download_data, list_remote_datasets
    repo = args.repo or DEFAULT_REPO
    if args.list:
        for name in list_remote_datasets(repo=repo, ref=args.ref):
            print(name)
        return
    datasets = args.dataset.split(",") if args.dataset else None
    dest = download_data(
        datasets, repo=repo, ref=args.ref,
        dest=args.dest or None, force=args.force,
    )
    print(f"Data ready in: {dest}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


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

    # ---- fetch-data ----
    p = sub.add_parser("fetch-data", help="Download benchmark datasets to local cache")
    p.add_argument("-D", "--dataset", default=None,
                   help="Comma-separated dataset names (default: all). e.g. clawarena-real")
    p.add_argument("--dest", default=None,
                   help="Destination root (default: ~/.cache/clawarena/data)")
    p.add_argument("--repo", default=None,
                   help="Source repo URL (default: built-in DEFAULT_REPO)")
    p.add_argument("--ref", default="main", help="Branch/tag to fetch (default: main)")
    p.add_argument("--force", action="store_true", help="Overwrite existing datasets")
    p.add_argument("--list", action="store_true",
                   help="List remote dataset names instead of downloading")

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
        "fetch-data": cmd_fetch_data,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
