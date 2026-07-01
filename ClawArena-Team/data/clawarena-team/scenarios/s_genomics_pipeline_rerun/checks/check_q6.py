"""q6: audit/rerun_plan.json — JSON schema + decision + sha token 一致。

通过条件（全部满足，exit 0）：
  1. audit/rerun_plan.json 存在且 JSON 可解析
  2. 必填字段齐备：pipeline / ref_genome / decision / samples_to_rerun /
     failed_samples_excluded / analyst / plan_date / compliance_token
  3. pipeline 含 "varcall-2026q2"
  4. ref_genome 含 "GRCh38.p15" 或 "p15"
  5. decision 含 "partial_rerun" 语义（含 partial + rerun/re-run 相关词）
  6. samples_to_rerun 为整数，范围 [115, 120]（允许 ±3 余量，锚点 118）
  7. failed_samples_excluded 为整数，值 = 9
  8. compliance_token 与 verify_rerun.py 本地重算结果一致（sha256）
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root

PIPELINE = "varcall-2026q2"
FAILED_COUNT = 9
SAMPLES_TO_RERUN_MIN = 115
SAMPLES_TO_RERUN_MAX = 120

TOKEN_KEYS = [
    "pipeline",
    "ref_genome",
    "decision",
    "samples_to_rerun",
    "failed_samples_excluded",
    "analyst",
    "plan_date",
]


def compute_token(payload: dict) -> str:
    parts = [f"{k}={payload.get(k, '')}" for k in TOKEN_KEYS]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


def _is_partial_rerun(decision: str) -> bool:
    low = decision.lower().replace("-", "_").replace(" ", "_")
    return "partial" in low and ("rerun" in low or "re_run" in low)


def main() -> int:
    ws = workspace_root()

    plan_path = ws / "audit" / "rerun_plan.json"
    if not plan_path.exists():
        fail("missing audit/rerun_plan.json")

    try:
        payload = json.loads(plan_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"audit/rerun_plan.json is not valid JSON: {e}")

    # 必填字段检查
    required = list(TOKEN_KEYS) + ["compliance_token"]
    missing = [k for k in required if k not in payload]
    if missing:
        fail(f"audit/rerun_plan.json missing required fields: {missing}")

    # pipeline
    pipeline_val = str(payload.get("pipeline", ""))
    if PIPELINE not in pipeline_val:
        fail(f"pipeline field should contain '{PIPELINE}', got: {pipeline_val!r}")

    # ref_genome
    ref_val = str(payload.get("ref_genome", ""))
    if not re.search(r"p15|GRCh38\.p15", ref_val, re.IGNORECASE):
        fail(f"ref_genome should reference GRCh38.p15, got: {ref_val!r}")

    # decision
    decision_val = str(payload.get("decision", ""))
    if not _is_partial_rerun(decision_val):
        fail(
            f"decision should reflect 'partial_rerun_excluding_failed' semantics, "
            f"got: {decision_val!r}"
        )

    # samples_to_rerun
    try:
        samples_count = int(payload["samples_to_rerun"])
    except (ValueError, TypeError):
        fail(f"samples_to_rerun must be an integer, got: {payload.get('samples_to_rerun')!r}")
    if not (SAMPLES_TO_RERUN_MIN <= samples_count <= SAMPLES_TO_RERUN_MAX):
        fail(
            f"samples_to_rerun={samples_count} out of expected range "
            f"[{SAMPLES_TO_RERUN_MIN}, {SAMPLES_TO_RERUN_MAX}] "
            f"(127 total - 9 failed = 118)"
        )

    # failed_samples_excluded
    try:
        failed_val = int(payload["failed_samples_excluded"])
    except (ValueError, TypeError):
        fail(f"failed_samples_excluded must be an integer, got: {payload.get('failed_samples_excluded')!r}")
    if failed_val != FAILED_COUNT:
        fail(
            f"failed_samples_excluded={failed_val} should be {FAILED_COUNT} "
            "(9 samples failed contamination QC)"
        )

    # compliance_token 重算
    expected_token = compute_token(payload)
    actual_token = str(payload.get("compliance_token", ""))
    if actual_token != expected_token:
        fail(
            f"compliance_token mismatch:\n"
            f"  stored:   {actual_token!r}\n"
            f"  expected: {expected_token!r}\n"
            f"Run: python tools/verify_rerun.py audit/rerun_plan.json"
        )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
