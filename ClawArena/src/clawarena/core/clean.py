"""Clean command — remove temporary work copies and logs."""

from __future__ import annotations

import shutil
from pathlib import Path


def run_clean(
    out_dir: Path,
    targets: list[str] | None = None,
) -> None:
    """Clean temporary files under out_dir.

    Targets: 'work' (work copies), 'logs' (LLM logs), 'all' (both).
    """
    targets = targets or ["all"]

    clean_work = "work" in targets or "all" in targets
    clean_logs = "logs" in targets or "all" in targets

    removed = 0

    if clean_work:
        for work_dir in out_dir.rglob("work"):
            if work_dir.is_dir():
                shutil.rmtree(work_dir)
                print(f"  Removed: {work_dir}")
                removed += 1

    if clean_logs:
        for log_dir in out_dir.rglob("llm_logs"):
            if log_dir.is_dir():
                shutil.rmtree(log_dir)
                print(f"  Removed: {log_dir}")
                removed += 1

    print(f"Clean complete: {removed} directories removed.")
