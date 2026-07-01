"""Serve Gemma-4-31B-it with vLLM (30.7B dense, native 256K ctx, multimodal text/image/video).

In the ClawArena-Team endpoint topology this single endpoint plays three roles at once:
main agent / llm pool / vlm pool. The logical split is done in the eval config via the
``modality`` fields (main/vlm use text+image+video; llm is text-only). The omni (audio)
role is served separately by ``serve_gemma-4-omni.py``.

**Audio note**: Gemma-4-31B does **not** support audio (only the E4B omni endpoint does,
per the official recipe). So ``--limit-mm-per-prompt`` here omits audio; any audio input
must be routed to the E4B endpoint in ``serve_gemma-4-omni.py``.

Features:
- ``--enable-auto-tool-choice --tool-call-parser gemma4 --reasoning-parser gemma4``
- ``--kv-cache-dtype fp8`` (a 30B model on 4x48GB needs fp8 KV)
- ``--speculative-config``: use ``gemma-4-31B-it-assistant`` as the MTP draft with
  ``num_speculative_tokens=4`` (``--no-spec`` disables it for an ablation)
- ``--limit-mm-per-prompt``: image=48, video=8 (31B has no audio)
- ``--async-scheduling``: overlaps scheduling with decoding (recommended by vLLM)
- ``--data-parallel-size``: DP replicas (intra-endpoint round-robin load balancing). A
  single GPU with ~96GB can hold 30.7B (bf16 ~62GB) + 128k fp8 KV + MTP draft, so TP=1
  is enough; use **DP rather than TP** to scale llm/vlm subagent throughput (subagent API
  requests are the benchmark bottleneck). Each DP replica uses 1 GPU; to add concurrency,
  raise ``--dp`` and grow ``--gpus`` accordingly.
- Defaults: GPUs 0,1,2,3, TP=1, DP=4, port 8900, max-model-len 128000.

Configuration via environment variables:
- ``CATEAM_VLLM_BIN``    : path to the ``vllm`` binary (default: ``vllm`` on PATH).
- ``CATEAM_MODELS_ROOT`` : root dir holding model weights (default: ``~/models``).
  Weights are expected at ``<MODELS_ROOT>/google/gemma-4-31B-it`` and
  ``<MODELS_ROOT>/google/gemma-4-31B-it-assistant``.

Dependencies:
- vllm **nightly** (stable releases may not support the gemma4_assistant MTP path; nightly
  auto-aliases the draft model_type during ``_rewrite_hf_config``)
- transformers >= 5.9.0 (for ``gemma4_assistant`` architecture recognition)

References:
- https://docs.vllm.ai/projects/recipes/en/latest/Google/Gemma4.html
- https://huggingface.co/google/gemma-4-31B-it
- https://huggingface.co/google/gemma-4-31B-it-assistant
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
MODEL_DIR = MODELS_ROOT / "google" / "gemma-4-31B-it"
DRAFT_DIR = MODELS_ROOT / "google" / "gemma-4-31B-it-assistant"
SERVED_NAME = "gemma-4-31b-it"
DEFAULT_PORT = 8900
DEFAULT_GPUS = "0,1,2,3"
DEFAULT_TP = 1
DEFAULT_DP = 4
DEFAULT_MAX_LEN = 128_000  # 128k; subagents need >100k, leave headroom. A separately-served main agent may need >200k.
DEFAULT_SPEC_TOKENS = 4
# limit-mm-per-prompt must cover the worst-case attachment count accumulated across a
# single agent/subagent context over many turns: every image-bearing tool_result appends
# an image message to the history, and each turn resends the whole history, so the per-prompt
# image count = total images this context has read so far. The largest single scenario carries
# 37 images; image=4 would be hard-400'd by vLLM ("At most 4 image(s)"), failing the turn for
# non-model reasons. Relax to 48 (~280 soft tokens/image, 48 images ~= 13k tokens, far below
# the ctx limit; GPU memory impact negligible). video relaxed to 8 for the same reason.
# The harness also enforces per-modality context caps (the eval config's vlm image=48/video=8
# match these), stripping the oldest attachments so the in-context count stays <= the cap;
# as long as the agent's modality caps are <= this limit-mm-per-prompt there are no 400s.
DEFAULT_LIMIT_MM = {"image": 48, "video": 8}


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
        "--kv-cache-dtype",
        "fp8",
        "--limit-mm-per-prompt",
        json.dumps(DEFAULT_LIMIT_MM),
        "--gpu-memory-utilization",
        str(args.gpu_mem_util),
        "--trust-remote-code",
    ]
    if args.async_scheduling:
        cmd += ["--async-scheduling"]
    if not args.no_spec:
        # On vllm nightly, SpeculativeConfig._rewrite_hf_config rewrites the draft's
        # model_type='gemma4_assistant' to 'gemma4_mtp', which hits the MTPModelTypes
        # allowlist and auto-selects method='mtp'. Do not pass method explicitly here.
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
    p.add_argument("--gpu-mem-util", type=float, default=0.92)
    p.add_argument("--spec-tokens", type=int, default=DEFAULT_SPEC_TOKENS,
                   help="MTP draft steps (only used when --no-spec is not given)")
    p.add_argument("--no-spec", action="store_true",
                   help="disable MTP / spec-dec (for debugging or ablations)")
    p.add_argument("--no-async-scheduling", dest="async_scheduling",
                   action="store_false", default=True,
                   help="disable vLLM async scheduling (fallback if scheduling misbehaves)")
    p.add_argument("--extra", default="", help="extra vllm flags as a string (shlex-parsed)")
    p.add_argument("--dry-run", action="store_true", help="print the command but do not run it")
    args = p.parse_args()

    ngpu = len([g for g in args.gpus.split(",") if g.strip()])
    if ngpu != args.tp * args.dp:
        sys.exit(f"GPU count ({ngpu}) must equal tp*dp ({args.tp}*{args.dp}={args.tp * args.dp}): --gpus {args.gpus}")

    if not MODEL_DIR.exists() or not any(MODEL_DIR.iterdir()):
        sys.exit(f"main weights not ready: {MODEL_DIR} (set CATEAM_MODELS_ROOT or download the weights)")
    if not args.no_spec and (not DRAFT_DIR.exists() or not any(DRAFT_DIR.iterdir())):
        sys.exit(f"MTP draft weights not ready: {DRAFT_DIR} (or pass --no-spec to disable MTP)")

    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = args.gpus
    # Make sure the vllm binary's directory is on PATH: flashinfer's JIT runs
    # subprocess.run('ninja') inside the worker via PATH, and a bare nohup/base shell
    # may not have the right dir (causing "ninja installed but not found").
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
