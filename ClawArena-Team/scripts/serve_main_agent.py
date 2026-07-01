"""Serve the ClawArena-Team **main agent** (the model under test) with vLLM -- single card, long context.

Unlike ``serve_gemma-4-31b.py`` (main/llm/vlm subagent pool) and ``serve_gemma-4-omni.py``
(omni subagent pool), this script serves only the "model under test" endpoint, defaulting to
one dedicated GPU (the subagent pools occupy the other cards). Pick one of the candidate main
models; each uses its native context limit (all >200k):

  +---------------+----------------------------+---------+------------------------------+
  | --model       | architecture               | ctx     | notes                        |
  +---------------+----------------------------+---------+------------------------------+
  | gemma-31b     | gemma4 dense multimodal    | 216000  | fp8 KV + assistant MTP       |
  | qwen3.6-27b   | qwen3_5 hybrid(linear)+vision| 216000 | multimodal; qwen3_next_mtp   |
  | glm-4.7-flash | glm4_moe_lite MoE+MLA text  | 202752  | 30B-A3B; built-in mtp        |
  +---------------+----------------------------+---------+------------------------------+

Single-card ~96GB feasibility (each including spec/MTP):
- gemma-31b: 62.5GB weights + 216k fp8 KV (~19GB) + draft ~1GB ~= 82GB (util 0.90 leaves room).
- qwen3.6-27b: ~54GB weights; the hybrid linear attention keeps KV small, so 216k is comfortable.
- glm-4.7-flash: ~62GB weights (full MoE experts resident on one card) + MLA (kv_lora_rank 512) -> tiny KV.

Port defaults to 8910 (subagents use 8900/8902, no conflict). On the ClawArena-Team side, set
``main.api_base`` to ``http://127.0.0.1:8910/v1`` and ``main.model_id`` to the matching served-name.

Dependencies: vllm nightly (glm47 tool parser / qwen3_5 / the various MTP paths all need a
recent nightly).

Configuration via environment variables:
- ``CATEAM_VLLM_BIN``    : path to the ``vllm`` binary (default: ``vllm`` on PATH).
- ``CATEAM_MODELS_ROOT`` : root dir holding model weights (default: ``~/models``).

References (per-model official vllm commands):
- https://huggingface.co/google/gemma-4-31B-it
- https://huggingface.co/Qwen/Qwen3.6-27B
- https://huggingface.co/zai-org/GLM-4.7-Flash
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

# vllm parameter set per candidate main model (taken from each model card's recommended command).
# spec=None means no MTP/spec; a dict spec is passed verbatim as the --speculative-config JSON.
MODELS: dict[str, dict] = {
    "gemma-31b": {
        "model_dir": MODELS_ROOT / "google/gemma-4-31B-it",
        "served": "gemma-4-31b-it-main",
        "max_len": 216_000,
        "tool_parser": "gemma4",
        "reasoning_parser": "gemma4",
        "kv_cache_dtype": "fp8",  # 31B needs fp8 KV to fit 216k on one card
        "limit_mm": {"image": 48, "video": 8},  # dense multimodal (no audio)
        "spec": {
            "model": str(MODELS_ROOT / "google/gemma-4-31B-it-assistant"),
            "num_speculative_tokens": 4,
        },
    },
    "qwen3.6-27b": {
        "model_dir": MODELS_ROOT / "Qwen/Qwen3.6-27B",
        "served": "qwen3.6-27b",
        "max_len": 216_000,
        "tool_parser": "qwen3_coder",
        "reasoning_parser": "qwen3",
        "kv_cache_dtype": None,  # hybrid linear attention already keeps KV small; bf16 is fine
        "limit_mm": {"image": 48, "video": 8},  # multimodal (image/video, no audio)
        "spec": {"method": "qwen3_next_mtp", "num_speculative_tokens": 2},
        # Qwen3.6 is a Mamba/linear-attention hybrid: each decode sequence uses one Mamba
        # cache block; the default max_num_seqs=1024 exceeds the available block count
        # (~478) and breaks cudagraph capture. Cap at 256.
        # --enable-prefix-caching: Mamba hybrids disable APC by default; enabling it makes
        # the Mamba layers use mamba-cache-mode=all (block-aligned state) so the long
        # prefixes of multi-turn agent conversations can be reused, avoiding repeat prefill
        # (supported by the official Qwen3.x recipe).
        "extra_args": ["--max-num-seqs", "256", "--enable-prefix-caching"],
    },
    "glm-4.7-flash": {
        "model_dir": MODELS_ROOT / "zai-org/GLM-4.7-Flash",
        "served": "glm-4.7-flash",
        "max_len": 202_752,  # native limit (rope_scaling=null, no extrapolation)
        "tool_parser": "glm47",
        "reasoning_parser": "glm45",
        "kv_cache_dtype": None,  # MLA compresses KV, no fp8 needed
        "limit_mm": None,  # text-only model
        # MTP disabled by default: on some vllm versions GLM's MLA + spec + cudagraph
        # capture conflict (mla_attention.build_for_cudagraph_capture: assert
        # max_query_len <= reorder_batch_threshold fails). Restore {"method":"mtp",...}
        # once a newer vllm fixes this.
        "spec": None,
    },
}

DEFAULT_PORT = 8910
DEFAULT_GPUS = "7"  # subagents occupy the other cards; the main agent gets the last one
DEFAULT_TP = 1
DEFAULT_DP = 1


def build_command(args: argparse.Namespace, spec: dict) -> list[str]:
    cmd = [
        VLLM_BIN,
        "serve",
        str(spec["model_dir"]),
        "--served-model-name",
        spec["served"],
        "--host",
        args.host,
        "--port",
        str(args.port),
        "--tensor-parallel-size",
        str(args.tp),
        "--data-parallel-size",
        str(args.dp),
        "--max-model-len",
        str(args.max_model_len if args.max_model_len else spec["max_len"]),
        "--tool-call-parser",
        spec["tool_parser"],
        "--reasoning-parser",
        spec["reasoning_parser"],
        "--enable-auto-tool-choice",
        "--gpu-memory-utilization",
        str(args.gpu_mem_util),
        "--trust-remote-code",
    ]
    if spec.get("kv_cache_dtype"):
        cmd += ["--kv-cache-dtype", spec["kv_cache_dtype"]]
    if spec.get("limit_mm"):
        cmd += ["--limit-mm-per-prompt", json.dumps(spec["limit_mm"])]
    if args.async_scheduling:
        cmd += ["--async-scheduling"]
    if not args.no_spec and spec.get("spec"):
        cmd += ["--speculative-config", json.dumps(spec["spec"])]
    if spec.get("extra_args"):  # per-model fixed extra flags (e.g. Qwen's --max-num-seqs)
        cmd += spec["extra_args"]
    if args.extra:
        cmd.extend(shlex.split(args.extra))
    return cmd


def main() -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--model", required=True, choices=sorted(MODELS),
                   help="pick one candidate main model")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=DEFAULT_PORT)
    p.add_argument("--gpus", default=DEFAULT_GPUS, help="CUDA_VISIBLE_DEVICES, comma-separated")
    p.add_argument("--tp", type=int, default=DEFAULT_TP)
    p.add_argument("--dp", type=int, default=DEFAULT_DP,
                   help="data-parallel replicas (requires len(--gpus)==tp*dp)")
    p.add_argument("--max-model-len", type=int, default=0,
                   help="override this model's default ctx (0 = use the model default)")
    p.add_argument("--gpu-mem-util", type=float, default=0.90)
    p.add_argument("--no-spec", action="store_true",
                   help="disable this model's MTP/spec (for ablations or debugging)")
    p.add_argument("--no-async-scheduling", dest="async_scheduling",
                   action="store_false", default=True)
    p.add_argument("--extra", default="", help="extra vllm flags as a string (shlex-parsed)")
    p.add_argument("--dry-run", action="store_true", help="print the command but do not run it")
    args = p.parse_args()

    spec = MODELS[args.model]

    ngpu = len([g for g in args.gpus.split(",") if g.strip()])
    if ngpu != args.tp * args.dp:
        sys.exit(f"GPU count ({ngpu}) must equal tp*dp ({args.tp}*{args.dp}={args.tp * args.dp}): --gpus {args.gpus}")

    model_dir = spec["model_dir"]
    if not args.dry_run:  # dry-run only prints the command, weights need not be present
        if not model_dir.exists() or not any(model_dir.iterdir()):
            sys.exit(f"weights not ready: {model_dir}\n"
                     f"  download example: hf download <repo> --local-dir {model_dir}")
        if not args.no_spec and "model" in (spec.get("spec") or {}):
            draft = Path(spec["spec"]["model"])
            if not draft.exists() or not any(draft.iterdir()):
                sys.exit(f"MTP draft not ready: {draft} (or pass --no-spec to disable MTP)")

    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = args.gpus
    vllm_bin_dir = os.path.dirname(os.path.realpath(VLLM_BIN)) if os.path.sep in VLLM_BIN else ""
    if vllm_bin_dir:
        env["PATH"] = f"{vllm_bin_dir}:{env.get('PATH', '')}"
    env.setdefault("VLLM_WORKER_MULTIPROC_METHOD", "spawn")

    cmd = build_command(args, spec)

    print("CUDA_VISIBLE_DEVICES=" + args.gpus + " \\\n  " + " ".join(shlex.quote(c) for c in cmd))
    if args.dry_run:
        return 0

    os.execvpe(cmd[0], cmd, env)


if __name__ == "__main__":
    raise SystemExit(main())
