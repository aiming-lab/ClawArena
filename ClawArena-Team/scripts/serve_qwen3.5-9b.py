"""Serve Qwen3.5-9B with vLLM as an **optional alternative** llm + vlm pool endpoint.

This is a lighter-weight stand-in for the default gemma llm/vlm pool
(``serve_gemma-4-31b.py``); use it only if you want a different subagent backbone.

Features:
- vision + text + video (native multimodal)
- ``--enable-auto-tool-choice --tool-call-parser qwen3_coder``
- ``--speculative-config '{"method":"qwen3_next_mtp","num_speculative_tokens":2}'``
- ``--max-model-len 100000`` (within the native 262K limit)
- Defaults: GPUs 4,5, TP=2, port 8901

Configuration via environment variables:
- ``CATEAM_VLLM_BIN``    : path to the ``vllm`` binary (default: ``vllm`` on PATH).
- ``CATEAM_MODELS_ROOT`` : root dir holding model weights (default: ``~/models``).
  Weights are expected at ``<MODELS_ROOT>/Qwen/Qwen3.5-9B``.

Reference: https://huggingface.co/Qwen/Qwen3.5-9B
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
from pathlib import Path

VLLM_BIN = os.environ.get("CATEAM_VLLM_BIN", "vllm")
MODELS_ROOT = Path(os.environ.get("CATEAM_MODELS_ROOT", str(Path.home() / "models")))
MODEL_DIR = MODELS_ROOT / "Qwen" / "Qwen3.5-9B"
SERVED_NAME = "qwen3.5-9b"
DEFAULT_PORT = 8901
DEFAULT_GPUS = "4,5"
DEFAULT_TP = 2
DEFAULT_MAX_LEN = 100_000
DEFAULT_SPEC_TOKENS = 2


def build_command(args: argparse.Namespace) -> list[str]:
    spec_cfg = json.dumps(
        {"method": "qwen3_next_mtp", "num_speculative_tokens": args.spec_tokens}
    )
    cmd = [
        VLLM_BIN,
        "serve",
        str(MODEL_DIR),
        "--served-model-name",
        SERVED_NAME,
        "--host",
        args.host,
        "--port",
        str(args.port),
        "--tensor-parallel-size",
        str(args.tp),
        "--max-model-len",
        str(args.max_model_len),
        "--reasoning-parser",
        "qwen3",
        "--enable-auto-tool-choice",
        "--tool-call-parser",
        "qwen3_coder",
        "--speculative-config",
        spec_cfg,
        "--gpu-memory-utilization",
        str(args.gpu_mem_util),
        "--trust-remote-code",
    ]
    if args.extra:
        cmd.extend(shlex.split(args.extra))
    return cmd


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=DEFAULT_PORT)
    p.add_argument("--gpus", default=DEFAULT_GPUS, help="CUDA_VISIBLE_DEVICES, comma-separated")
    p.add_argument("--tp", type=int, default=DEFAULT_TP)
    p.add_argument("--max-model-len", type=int, default=DEFAULT_MAX_LEN)
    p.add_argument("--spec-tokens", type=int, default=DEFAULT_SPEC_TOKENS)
    p.add_argument("--gpu-mem-util", type=float, default=0.90)
    p.add_argument("--extra", default="", help="extra vllm flags as a string (shlex-parsed)")
    p.add_argument("--dry-run", action="store_true", help="print the command but do not run it")
    args = p.parse_args()

    if not MODEL_DIR.exists() or not any(MODEL_DIR.iterdir()):
        sys.exit(f"weights not ready: {MODEL_DIR} (set CATEAM_MODELS_ROOT or download the weights)")

    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = args.gpus
    cmd = build_command(args)

    print("CUDA_VISIBLE_DEVICES=" + args.gpus + " \\\n  " + " ".join(shlex.quote(c) for c in cmd))
    if args.dry_run:
        return 0

    os.execvpe(cmd[0], cmd, env)


if __name__ == "__main__":
    raise SystemExit(main())
