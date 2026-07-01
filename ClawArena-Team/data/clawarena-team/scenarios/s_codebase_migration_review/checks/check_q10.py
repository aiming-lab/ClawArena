"""check_q10.py — audit/final_review.json["compliance_token"] 与本地重算 sha256 一致。

通过条件（全部满足，exit 0）：
  1. audit/final_review.json 存在且包含 compliance_token 字段
  2. token 长度 >= 16 hex 字符
  3. token 前缀与本地 sha256(canonical) 的前 16 位一致
     canonical = decision|services|risks|coverage_gap|rpc_diff_count（逐字段 key=value 串联）
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root

KEYS = ["decision", "services", "risks", "coverage_gap", "rpc_diff_count"]


def _compute_token(payload: dict) -> str:
    parts = []
    for k in KEYS:
        v = payload.get(k, "")
        # normalise list/dict to stable string
        if isinstance(v, (list, dict)):
            v = json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        parts.append(f"{k}={v}")
    canonical = "|".join(parts)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def main() -> int:
    ws = workspace_root()
    p = ws / "audit" / "final_review.json"
    if not p.exists():
        fail("missing audit/final_review.json")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"final_review.json is not valid JSON: {e}")

    token = data.get("compliance_token")
    if not isinstance(token, str) or not token:
        fail("compliance_token missing or not a string")

    expected = _compute_token(data)
    given = token.strip().lower()

    if len(given) < 16:
        fail(f"compliance_token too short ({len(given)} hex chars; need >= 16)")

    if not given.startswith(expected[:16]):
        fail(
            f"compliance_token does not match recomputed sha256; "
            f"expected prefix: {expected[:16]}, got: {given[:16]}"
        )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
