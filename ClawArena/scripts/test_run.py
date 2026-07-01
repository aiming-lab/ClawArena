import json
import os
import pty
import select
import sys
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path


# ===================== Configuration =====================
class cfg:
    # Log file path (auto-suffixes _1/_2 if exists)
    LOG_FILE = "logs/run.log"

    # clawarena executable (use "clawarena" if installed, or full path)
    CLAWARENA_BIN = "clawarena"

    # Path to tests.json
    DATA = "data/clawarena/tests.json"

    # Frameworks (comma-separated)
    FRAMEWORKS = "openclaw"

    # Output directory
    OUT = "results/run"

    # Concurrency
    CONCURRENCY = 1

    # Per-task timeout (seconds)
    TIMEOUT = 300

    # Retry count on failure
    RETRY = 2

    # External plugin paths (.py files), leave empty if not needed
    PLUGIN = []

    # Optional JSON overlay forwarded via `--overlay` to `clawarena run`.
    # Used to toggle MetaClaw without editing tests.json, e.g.:
    #   OVERLAY = '{"metaclaw":{"enabled":true,"managed":true,' \
    #             '"config_path":"metaclaw/skills-only.yaml",' \
    #             '"skills_dir":"metaclaw/skills","per_scene_isolation":false}}'
    # Leave as None (default) to skip.
    OVERLAY = None

    # Shell script to source API keys (set to None to skip)
    API_KEY_SCRIPT = "scripts/env_example.sh"
# ==========================================================


def resolve_log_path(log_file: str) -> Path:
    """If the target path exists, try _1/_2/... suffixes until a free slot is found."""
    p = Path(log_file)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        return p
    stem, suffix = p.stem, p.suffix
    n = 1
    while True:
        candidate = p.parent / f"{stem}_{n}{suffix}"
        if not candidate.exists():
            return candidate
        n += 1


def load_env_from_shell(script_path: str) -> dict:
    """Source a shell script and capture the resulting environment variables."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        tmp_path = f.name
    try:
        result = subprocess.run(
            ["bash", "-c",
             f"source {script_path} && "
             "python3 -c 'import os,json; json.dump(dict(os.environ),open(os.environ[\"__TMP_ENV\"],\"w\"))'"],
            env={**os.environ, "__TMP_ENV": tmp_path},
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"Failed to load env script: {script_path}")
        with open(tmp_path) as f:
            return json.load(f)
    finally:
        os.unlink(tmp_path)


def run_command(cmd: list, log_path: Path, env: dict = None) -> int:
    """Run a command with real-time output to both terminal and log file via PTY."""
    master_fd, slave_fd = pty.openpty()
    proc = subprocess.Popen(
        cmd,
        stdout=slave_fd,
        stderr=slave_fd,
        env=env,
        close_fds=True,
    )
    os.close(slave_fd)

    with open(log_path, "a", encoding="utf-8") as log_f:
        while True:
            try:
                r, _, _ = select.select([master_fd], [], [], 1.0)
                if r:
                    chunk = os.read(master_fd, 4096)
                    if not chunk:
                        break
                    text = chunk.decode("utf-8", errors="replace")
                    sys.stdout.write(text)
                    sys.stdout.flush()
                    log_f.write(text)
                    log_f.flush()
                elif proc.poll() is not None:
                    break
            except OSError:
                break

    os.close(master_fd)
    proc.wait()
    return proc.returncode


def append_timing(log_path: Path, start: datetime, end: datetime):
    """Append timing summary to the log and print to terminal."""
    elapsed = (end - start).total_seconds()
    lines = [
        "",
        "----------------------------------------",
        "Command finished.",
        f"Start time: {start.strftime('%Y-%m-%d %H:%M:%S')}",
        f"End time:   {end.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Elapsed:    {elapsed:.3f}s",
        "========================================",
        "",
    ]
    with open(log_path, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("----------------------------------------")
    print(f"Command finished. Elapsed: {elapsed:.3f}s")
    print(f"Full log written to: {log_path}")


def main():
    os.system("clear")

    log_path = resolve_log_path(cfg.LOG_FILE)

    env = None
    if cfg.API_KEY_SCRIPT:
        env = load_env_from_shell(cfg.API_KEY_SCRIPT)

    cmd = [
        cfg.CLAWARENA_BIN, "run",
        "--data", cfg.DATA,
        "--frameworks", cfg.FRAMEWORKS,
        "--out", cfg.OUT,
        "--concurrency", str(cfg.CONCURRENCY),
        "--timeout", str(cfg.TIMEOUT),
        "--retry", str(cfg.RETRY),
    ]
    for p in cfg.PLUGIN:
        cmd += ["--plugin", p]
    if getattr(cfg, "OVERLAY", None):
        cmd += ["--overlay", cfg.OVERLAY]

    start = datetime.now()
    run_command(cmd, log_path, env=env)
    end = datetime.now()

    append_timing(log_path, start, end)


if __name__ == "__main__":
    main()
