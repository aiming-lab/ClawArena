"""Sequentially validate / evaluate main-agent target models (registry: scripts/eval_targets.json).

For each target: use the fixed local gemma subagent pool from ``configs/eval_base.yaml``
as the background, inject the target as the ``main`` agent via ``-m``, and run
ClawArena-Team on a "minimal-token scenario". **Validation mode (default) treats the run
as PASS as soon as the first round (q1) completes** -- once
``<out>/<run_id>/<scenario>/evals/q1.json`` appears the process is killed and PASS is
recorded, saving time and money; ``--full`` runs the whole scenario.

Dependent services (by group):
- gemini / openrouter   : direct cloud access (keys are read from the environment).
- codex                 : needs a ChatMock-style proxy ``... serve --port 8920``.
- bedrock               : needs litellm ``scripts/serve_litellm.sh`` (:4000).
- local                 : needs ``scripts/serve_main_agent.py`` (:8910).
- all groups            : need the local gemma subagent pool (:8900 / :8902).

API keys are taken straight from the environment (e.g. ``GEMINI_API_KEY``,
``OPENROUTER_API_KEY``, ``ANTHROPIC_API_KEY``). Export them before running, e.g.::

    export GEMINI_API_KEY=...   OPENROUTER_API_KEY=...   ANTHROPIC_API_KEY=...

Configuration via environment variables:
- ``CATEAM_HOME``           : project root (default: parent dir of this script).
- ``CATEAM_BIN``            : path to the ``clawarena-team`` CLI (default: found on PATH).

Usage::

    python scripts/run_eval_targets.py --list
    python scripts/run_eval_targets.py --target gemini-3.5-flash
    python scripts/run_eval_targets.py --group openrouter
    python scripts/run_eval_targets.py --all                 # all targets, q1 validation
    python scripts/run_eval_targets.py --all --full          # run full scenarios
    python scripts/run_eval_targets.py --target codex-gpt-5.5 --full-bench  # full 41-scenario run
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import signal
import subprocess
import time
from pathlib import Path

ROOT = Path(os.environ.get("CATEAM_HOME", Path(__file__).resolve().parents[1]))
# Locate the CLI: honor CATEAM_BIN, else look on PATH, else fall back to the name.
CLI = os.environ.get("CATEAM_BIN") or shutil.which("clawarena-team") or "clawarena-team"
REGISTRY = ROOT / "scripts" / "eval_targets.json"
EVAL_BASE = ROOT / "configs" / "eval_base.yaml"
DATA = ROOT / "data" / "clawarena-team"
DEFAULT_SCENARIO = "s_finance_options_pricing"  # smallest-token scenario in the full set (~15.2k)
OUT_ROOT = ROOT / "results" / "eval"


def load_keys_into_env() -> dict[str, str]:
    """Return a child env with cloud API keys.

    Keys are taken from the current process environment (export them beforehand).
    This is just a copy of ``os.environ`` so the target main's ``api_key_env`` can
    resolve them in the subprocess.
    """
    return os.environ.copy()


def load_targets() -> list[dict]:
    return json.loads(REGISTRY.read_text())["targets"]


def run_one(target: dict, scenario: str, timeout: int, full: bool, env: dict,
            *, full_bench: bool = False, out_root: Path | None = None) -> dict:
    tid = target["id"]
    out_dir = (out_root or OUT_ROOT) / tid
    model_json = json.dumps({"main": target["main"]}, ensure_ascii=False)
    # main only declares the text modality; non-text inputs are handled by the
    # vlm / omni subagents in the pool (ClawArena-Team design).
    cmd = [CLI, "run", "-d", str(DATA),
           "--config", str(EVAL_BASE), "-m", model_json,
           "-o", str(out_dir), "--retry", "3" if full_bench else "1"]
    if not full_bench:  # validation mode: only run the minimal scenario
        cmd += ["-t", scenario]
    log_path = out_dir / "run.log"
    out_dir.mkdir(parents=True, exist_ok=True)
    result = {"id": tid, "group": target.get("group"), "model": target["main"]["model_id"]}
    started = time.time()

    with open(log_path, "w") as logf:
        proc = subprocess.Popen(cmd, cwd=str(ROOT), env=env, stdout=logf,
                                stderr=subprocess.STDOUT, start_new_session=True)
        try:
            if full_bench:
                return _wait_full_bench(proc, out_dir, log_path, timeout, started, result)
            return _wait_q1(proc, out_dir, scenario, full, log_path, timeout, started, result)
        finally:
            _kill(proc)


def _wait_full_bench(proc, out_dir, log_path, timeout, started, result) -> dict:
    """Full benchmark: run to natural completion, read pass stats from report.json."""
    while True:
        rc = proc.poll()
        if rc is not None:
            # Take the newest run's report (results are never deleted, so out_dir may
            # hold several historical run_* dirs; picking the first arbitrarily could
            # read a stale report and give a false summary).
            reps = sorted(out_dir.glob("*/report.json"),
                          key=lambda p: p.stat().st_mtime, reverse=True)
            if reps:
                rep = json.loads(reps[0].read_text())
                result.update(
                    status="DONE" if rc == 0 else "DONE?",
                    reason=(f"scenarios={len(rep.get('scenarios', []))} "
                            f"task_succ={rep.get('avg_task_success_rate')} "
                            f"scen_full_pass={rep.get('avg_scenario_full_pass_rate')}"),
                    elapsed=round(time.time() - started, 1),
                    report=str(reps[0]))
            else:
                result.update(status="FAIL", reason=f"process exited rc={rc}, no report",
                              elapsed=round(time.time() - started, 1), log_tail=_tail(log_path))
            return result
        if time.time() - started > timeout:
            _kill(proc)
            result.update(status="TIMEOUT", reason=f"timed out after {timeout}s (resume with `clawarena-team resume`)",
                          elapsed=round(time.time() - started, 1), log_tail=_tail(log_path))
            return result
        time.sleep(10)


def _wait_q1(proc, out_dir, scenario, full, log_path, timeout, started, result) -> dict:
    """Validation mode: mark PASS as soon as evals/q1.json appears, then kill."""
    q1_glob = f"*/{scenario}/evals/q1.json"
    while True:
        if not full and list(out_dir.glob(q1_glob)):
            _kill(proc)
            result.update(status="PASS", reason="q1 complete", elapsed=round(time.time() - started, 1))
            return result
        rc = proc.poll()
        if rc is not None:
            if list(out_dir.glob(q1_glob)):
                result.update(status="PASS", reason="run finished and q1 exists",
                              elapsed=round(time.time() - started, 1))
            else:
                result.update(status="FAIL", reason=f"process exited rc={rc}, no q1",
                              elapsed=round(time.time() - started, 1), log_tail=_tail(log_path))
            return result
        if time.time() - started > timeout:
            _kill(proc)
            result.update(status="FAIL", reason=f"timed out after {timeout}s",
                          elapsed=round(time.time() - started, 1), log_tail=_tail(log_path))
            return result
        time.sleep(2)


def _kill(proc: subprocess.Popen) -> None:
    if proc.poll() is None:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            time.sleep(3)
            if proc.poll() is None:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except ProcessLookupError:
            pass


def _tail(path: Path, n: int = 12) -> list[str]:
    try:
        return path.read_text(errors="replace").splitlines()[-n:]
    except OSError:
        return []


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--target", help="single target id")
    g.add_argument("--group", help="run by group (gemini/openrouter/openrouter-free/codex/bedrock/anthropic/local)")
    g.add_argument("--all", action="store_true", help="run every target")
    p.add_argument("--list", action="store_true", help="only list targets")
    p.add_argument("--scenario", default=DEFAULT_SCENARIO)
    p.add_argument("--timeout", type=int, default=600)
    p.add_argument("--full", action="store_true", help="in validation mode, run the full scenario (default stops at q1)")
    p.add_argument("--full-bench", action="store_true",
                   help="formal experiment: run the full set (no -t), summarize from report.json")
    p.add_argument("--out-root", default=None,
                   help="output root (default: results/eval for validation, results/exp for full-bench)")
    args = p.parse_args()

    targets = load_targets()
    if args.list:
        for t in targets:
            print(f"  {t['id']:28s} [{t.get('group')}] {t['main']['model_id']}")
        return 0

    if args.target:
        sel = [t for t in targets if t["id"] == args.target]
    elif args.group:
        sel = [t for t in targets if t.get("group") == args.group]
    elif args.all:
        sel = targets
    else:
        p.error("specify one of --target / --group / --all / --list")
    if not sel:
        print("no matching target"); return 1

    # full-bench: enlarge the default timeout (the full set runs scenarios serially and
    # can take hours); override with --timeout.
    if args.full_bench and args.timeout == 600:
        args.timeout = 36_000
    out_root = Path(args.out_root) if args.out_root else (ROOT / "results" / ("exp" if args.full_bench else "eval"))

    env = load_keys_into_env()
    out_root.mkdir(parents=True, exist_ok=True)
    results = []
    for t in sel:
        mode = "full-bench (full set)" if args.full_bench else ("full" if args.full else "q1")
        print(f"\n>>> [{t['id']}] {t['main']['model_id']} ({mode}) ...", flush=True)
        r = run_one(t, args.scenario, args.timeout, args.full, env,
                    full_bench=args.full_bench, out_root=out_root)
        results.append(r)
        print(f"    {r['status']}  {r['reason']}  ({r['elapsed']}s)")
        if r["status"] in ("FAIL", "TIMEOUT"):
            for ln in r.get("log_tail", []):
                print(f"      | {ln}")

    summary_path = out_root / ("exp_summary.json" if args.full_bench else "eval_summary.json")
    summary_path.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    ok = sum(1 for r in results if r["status"] in ("PASS", "DONE"))
    print(f"\n=== summary: {ok}/{len(results)} complete ===  -> {summary_path}")
    for r in results:
        print(f"  {('[OK]' if r['status'] in ('PASS', 'DONE') else '[FAIL]')} {r['id']:28s} {r['reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
