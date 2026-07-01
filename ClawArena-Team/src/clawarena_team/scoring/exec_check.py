"""exec_check execution for a single round.

Returns a standard dict: ``{passed, exit_code, stdout, stderr}``; ``passed`` is
determined by combining expect_exit with the optional expect_stdout.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any


def run_exec_check(
    *,
    command: str,
    cwd: Path,
    expect_exit: int = 0,
    timeout: int = 60,
    expect_stdout: str | None = None,
    regex: bool = False,
) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            command,
            shell=True,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        exit_code = proc.returncode
        stdout = proc.stdout
        stderr = proc.stderr
    except subprocess.TimeoutExpired as e:
        # Fix (fix/audit-top10 W2 F6 / v1#7): the former exit_code=-1 timeout sentinel
        # was semantically confused with being killed by SIGHUP (returncode=-1) and the
        # token-breaker sentinel (scenario_runner writes -1); if a task sets
        # expect_exit=-1, the timeout and "expected signal termination" become entirely
        # entangled. We now use a dedicated -101 exit code plus an explicit
        # timed_out=True field, so downstream can precisely distinguish the failure cause.
        return {
            "passed": False,
            "exit_code": -101,
            "timed_out": True,
            "stdout": e.stdout or "",
            "stderr": (e.stderr or "") + f"\nTIMEOUT after {timeout}s",
        }

    ok = exit_code == expect_exit
    if ok and expect_stdout:
        if regex:
            ok = bool(re.search(expect_stdout, stdout))
        else:
            ok = expect_stdout in stdout
    return {"passed": ok, "exit_code": exit_code, "timed_out": False,
            "stdout": stdout, "stderr": stderr}
