"""q8: audit/final_decision.json["compliance_token"] 与本地重算 sha256 一致."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root


KEYS = [
    "decision", "v3_mean", "v4_mean", "delta",
    "failed_test_name", "failed_test_line",
    "reward_variance", "reviewer", "decision_date",
]


def main() -> int:
    ws = workspace_root()
    p = ws / "audit" / "final_decision.json"
    if not p.exists():
        fail("missing audit/final_decision.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    token = data.get("compliance_token")
    if not isinstance(token, str) or not token:
        fail("compliance_token missing or not a string")
    # 重算 (排除 compliance_token 本身)
    parts = []
    for k in KEYS:
        v = data.get(k, "")
        parts.append(f"{k}={v}")
    canonical = "|".join(parts)
    expected = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    given = token.strip().lower()
    if not given.startswith(expected[:16]):
        # 容差：作者可能只复制前 16 / 32 / 64 hex；要求至少 16 hex 与重算前缀一致
        fail(f"compliance_token does not match recomputed sha256 (expected prefix {expected[:16]}, got {given[:16]})")
    if len(given) < 16:
        fail(f"compliance_token too short ({len(given)} hex chars; need >= 16)")
    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
