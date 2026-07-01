"""Run command — infer + score + report (+ compare) pipeline."""

from __future__ import annotations

import os
import asyncio
from datetime import datetime
from pathlib import Path

from clawarena.core.compare import generate_comparison
from clawarena.core.infer import run_infer
from clawarena.core.provider import ModelConfig
from clawarena.core.report import generate_report
from clawarena.core.scoring import run_scoring


async def _run_one_framework(
    fw: str,
    tests_json_path: Path,
    out_dir: Path,
    concurrency: int,
    timeout: float,
    retry: int,
    cli_model: ModelConfig | None = None,
    overlay: str | None = None,
    test_ids: list[str] | None = None,
) -> Path | None:
    """Single-framework pipeline: infer -> scoring -> report. Returns report.json path."""
    fw_dir = out_dir / fw
    infer_dir = fw_dir / "infer"
    scoring_dir = fw_dir / "scoring"
    report_dir = fw_dir / "report"

    infer_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"[{fw}] Starting Infer")
    print(f"{'='*60}")

    await run_infer(
        tests_json_path, fw, infer_dir,
        concurrency=concurrency, timeout=timeout, retry=retry,
        cli_model=cli_model,
        overlay=overlay,
        test_ids=test_ids,
    )

    print(f"\n[{fw}] --- Scoring ---")
    await asyncio.to_thread(run_scoring, infer_dir, scoring_dir)

    print(f"\n[{fw}] --- Report ---")
    await asyncio.to_thread(generate_report, scoring_dir, report_dir, tests_json_path)

    report_json = report_dir / "report.json"
    return report_json if report_json.exists() else None


async def _run_all_async(
    tests_json_path: Path,
    frameworks: list[str],
    out_dir: Path,
    concurrency: int,
    timeout: float,
    retry: int,
    cli_model: ModelConfig | None = None,
    overlay: str | None = None,
    test_ids: list[str] | None = None,
) -> None:
    """Run all frameworks concurrently, then generate a comparison report."""
    tasks = [
        _run_one_framework(fw, tests_json_path, out_dir, concurrency, timeout, retry,
                           cli_model=cli_model, overlay=overlay,
                           test_ids=test_ids)
        for fw in frameworks
    ]
    results = await asyncio.gather(*tasks)

    report_paths = [r for r in results if r is not None]
    if len(report_paths) >= 2:
        print(f"\n--- Comparison ---")
        generate_comparison(report_paths, out_dir / "comparison")


def run_all(
    tests_json_path: Path,
    frameworks: list[str],
    out_dir: Path,
    concurrency: int = 4,
    timeout: float = 300,
    retry: int = 1,
    clean_temp: bool = False,
    cli_model: ModelConfig | None = None,
    overlay: str | None = None,
    test_ids: list[str] | None = None,
) -> None:
    """Run the full pipeline: infer -> score -> report (-> compare)."""
    if out_dir.exists() and any(out_dir.iterdir()):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + f"_{os.getpid()}"
        out_dir = out_dir / f"run_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    asyncio.run(_run_all_async(
        tests_json_path, frameworks, out_dir, concurrency, timeout, retry,
        cli_model=cli_model,
        overlay=overlay,
        test_ids=test_ids,
    ))

    print(f"\nRun complete. Results in: {out_dir}")
