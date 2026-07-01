"""Serve Gemma-4-E4B-it with vLLM (the omni role), using -assistant as the MTP draft.

In the ClawArena-Team endpoint topology this endpoint plays the ``omni`` role
(text + image + video + audio, all modalities). The main / llm / vlm roles share the
31B endpoint in ``serve_gemma-4-31b.py``.

Features:
- text + image + video + audio (gemma-4 dense omni, all modalities)
- ``--enable-auto-tool-choice --tool-call-parser gemma4 --reasoning-parser gemma4``
- **MTP/spec disabled by default** (``--spec`` enables it explicitly). Reason: E4B has
  heterogeneous head layers (sliding-window heads=4 vs full-attention heads=8). Even on a
  vllm nightly that carries the per-group block-table runtime fix, the startup-time
  ``determine_available_memory`` -> attention-group build still trips the
  ``All layers in one attention group must share num_heads; got {8, 4}`` assertion. The
  31B model has uniform heads per layer so it is unaffected and keeps MTP on by default.
  Once vLLM fixes the startup-time group validation, ``--spec`` restores E4B MTP:
  the ``gemma-4-E4B-it-assistant`` draft with ``num_speculative_tokens=4`` (nightly
  rewrites the draft model_type gemma4_assistant -> gemma4_mtp, hitting the allowlist).
- ``--limit-mm-per-prompt``: audio=4, image=24, video=4
- ``--async-scheduling``: recommended by vLLM
- ``--data-parallel-size``: DP replicas (intra-endpoint round-robin); each uses 1 GPU.
- ``--max-model-len 128000`` (E4B native limit 131072)
- Defaults: GPU 4, TP=1, DP=1, port 8902, gpu-mem-util 0.45. omni/audio call volume is
  small, so a single GPU with dp=1 is enough; util 0.45 leaves room to co-locate other
  small models on that card.

Configuration via environment variables:
- ``CATEAM_VLLM_BIN``    : path to the ``vllm`` binary (default: ``vllm`` on PATH).
- ``CATEAM_MODELS_ROOT`` : root dir holding model weights (default: ``~/models``).
  Weights are expected at ``<MODELS_ROOT>/google/gemma-4-E4B-it`` and
  ``<MODELS_ROOT>/google/gemma-4-E4B-it-assistant``.

Dependencies:
- vllm **nightly** (same as the 31B endpoint; MTP needs nightly to auto-recognize gemma4_assistant)
- transformers >= 5.9.0 (for ``gemma4_assistant`` architecture recognition)

References:
- https://docs.vllm.ai/projects/recipes/en/latest/Google/Gemma4.html
- https://huggingface.co/google/gemma-4-E4B-it
- https://huggingface.co/google/gemma-4-E4B-it-assistant
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
MODEL_DIR = MODELS_ROOT / "google" / "gemma-4-E4B-it"
DRAFT_DIR = MODELS_ROOT / "google" / "gemma-4-E4B-it-assistant"
SERVED_NAME = "gemma-4-e4b-it"
DEFAULT_PORT = 8902
DEFAULT_GPUS = "4"
DEFAULT_TP = 1
DEFAULT_DP = 1
DEFAULT_MAX_LEN = 128_000  # 128k; omni subagents need >100k, leave headroom (E4B native limit 131072)
DEFAULT_SPEC_TOKENS = 4
# See the matching note in serve_gemma-4-31b.py: the per-prompt attachment count equals
# everything this subagent context has accumulated so far. audio/image/video = 1 is too
# strict (omni subagents often compare several images / audio clips) and would be 400'd by
# vLLM ("At most 1 image(s)"). Relax to cover the worst single-scenario accumulation; E4B
# single-card memory is tighter, so keep relatively conservative caps.
DEFAULT_LIMIT_MM = {"audio": 4, "image": 24, "video": 4}


def build_command(args: argparse.Namespace) -> list[str]:
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
        "--data-parallel-size",
        str(args.dp),
        "--max-model-len",
        str(args.max_model_len),
        "--tool-call-parser",
        "gemma4",
        "--reasoning-parser",
        "gemma4",
        "--enable-auto-tool-choice",
        "--limit-mm-per-prompt",
        json.dumps(DEFAULT_LIMIT_MM),
        "--gpu-memory-utilization",
        str(args.gpu_mem_util),
        "--trust-remote-code",
    ]
    if args.async_scheduling:
        cmd += ["--async-scheduling"]
    if args.enable_spec:
        # See module docstring: vllm nightly rewrites gemma4_assistant -> gemma4_mtp.
        spec_cfg = json.dumps(
            {"model": str(DRAFT_DIR), "num_speculative_tokens": args.spec_tokens}
        )
        cmd += ["--speculative-config", spec_cfg]
    if args.extra:
        cmd.extend(shlex.split(args.extra))
    return cmd


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=DEFAULT_PORT)
    p.add_argument("--gpus", default=DEFAULT_GPUS, help="CUDA_VISIBLE_DEVICES, comma-separated")
    p.add_argument("--tp", type=int, default=DEFAULT_TP)
    p.add_argument("--dp", type=int, default=DEFAULT_DP,
                   help="data-parallel replicas; each uses 1 GPU (requires len(--gpus)==tp*dp)")
    p.add_argument("--max-model-len", type=int, default=DEFAULT_MAX_LEN)
    p.add_argument("--gpu-mem-util", type=float, default=0.45)
    p.add_argument("--spec-tokens", type=int, default=DEFAULT_SPEC_TOKENS,
                   help="MTP draft steps (only used when --spec is given)")
    p.add_argument("--spec", action="store_true",
                   help="explicitly enable MTP / spec-dec (disabled by default; see the "
                        "E4B heterogeneous-head assertion note in the module docstring)")
    p.add_argument("--no-spec", action="store_true",
                   help="(already the default) disable MTP / spec-dec; wins if given with --spec")
    p.add_argument("--no-async-scheduling", dest="async_scheduling",
                   action="store_false", default=True,
                   help="disable vLLM async scheduling (fallback if scheduling misbehaves)")
    p.add_argument("--extra", default="", help="extra vllm flags as a string (shlex-parsed)")
    p.add_argument("--dry-run", action="store_true", help="print the command but do not run it")
    args = p.parse_args()
    # MTP/spec disabled by default (see module docstring: E4B heterogeneous heads + the
    # local nightly's startup-time assertion). Enabled only when --spec is given and --no-spec is not.
    args.enable_spec = args.spec and not args.no_spec

    ngpu = len([g for g in args.gpus.split(",") if g.strip()])
    if ngpu != args.tp * args.dp:
        sys.exit(f"GPU count ({ngpu}) must equal tp*dp ({args.tp}*{args.dp}={args.tp * args.dp}): --gpus {args.gpus}")

    if not MODEL_DIR.exists() or not any(MODEL_DIR.iterdir()):
        sys.exit(f"main weights not ready: {MODEL_DIR} (set CATEAM_MODELS_ROOT or download the weights)")
    if args.enable_spec and (not DRAFT_DIR.exists() or not any(DRAFT_DIR.iterdir())):
        sys.exit(f"MTP draft weights not ready: {DRAFT_DIR} (or drop --spec to disable MTP)")

    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = args.gpus
    # See serve_gemma-4-31b.py: flashinfer's JIT needs ninja on PATH.
    vllm_bin_dir = os.path.dirname(os.path.realpath(VLLM_BIN)) if os.path.sep in VLLM_BIN else ""
    if vllm_bin_dir:
        env["PATH"] = f"{vllm_bin_dir}:{env.get('PATH', '')}"
    env.setdefault("VLLM_WORKER_MULTIPROC_METHOD", "spawn")

    cmd = build_command(args)

    print("CUDA_VISIBLE_DEVICES=" + args.gpus + " \\\n  " + " ".join(shlex.quote(c) for c in cmd))
    if args.dry_run:
        return 0

    os.execvpe(cmd[0], cmd, env)


if __name__ == "__main__":
    raise SystemExit(main())
