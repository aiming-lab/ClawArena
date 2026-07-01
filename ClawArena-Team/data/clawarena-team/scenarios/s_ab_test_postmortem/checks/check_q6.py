"""q6: audit/decision.json schema + sha_token 与本地重算 sha256 一致。

通过条件（全部满足，exit 0）：
  1. audit/decision.json 存在且 JSON 合法
  2. 含字段：decision / experiment_id / primary_segment / root_cause_hex / decision_date
  3. decision ∈ {rollback_to_A, partial_rollback_mobile_us}
  4. experiment_id == 'EXP-2421'
  5. primary_segment == 'mobile_us'
  6. root_cause_hex 含 '#ff6633'（case-insensitive）
  7. sha_token 字段存在且与工具重算 sha256 前缀一致（≥ 16 hex chars）
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root

REQUIRED_KEYS = {"decision", "experiment_id", "primary_segment", "root_cause_hex", "decision_date"}
VALID_DECISIONS = {"rollback_to_A", "partial_rollback_mobile_us"}
SHA_TOKEN_KEYS = ["decision", "experiment_id", "primary_segment", "root_cause_hex", "decision_date"]


def _compute_token(payload: dict) -> str:
    parts = [f"{k}={payload.get(k, '')}" for k in SHA_TOKEN_KEYS]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


def main() -> int:
    ws = workspace_root()
    p = ws / "audit" / "decision.json"
    if not p.exists():
        fail("missing audit/decision.json")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"audit/decision.json not valid JSON: {e}")
    if not isinstance(data, dict):
        fail("audit/decision.json must be a JSON object")

    # 必填字段
    missing = REQUIRED_KEYS - set(data.keys())
    if missing:
        fail(f"audit/decision.json missing keys: {sorted(missing)}")

    # decision 合法值
    if data["decision"] not in VALID_DECISIONS:
        fail(f"decision must be one of {sorted(VALID_DECISIONS)}, got {data['decision']!r}")

    # experiment_id
    if str(data.get("experiment_id", "")).strip() != "EXP-2421":
        fail(f"experiment_id expected 'EXP-2421', got {data.get('experiment_id')!r}")

    # primary_segment
    if str(data.get("primary_segment", "")).strip() != "mobile_us":
        fail(f"primary_segment expected 'mobile_us', got {data.get('primary_segment')!r}")

    # root_cause_hex
    hex_val = str(data.get("root_cause_hex", "")).strip()
    if not re.match(r"#[Ff][Ff]6633", hex_val):
        fail(f"root_cause_hex expected '#ff6633', got {hex_val!r}")

    # sha_token
    token = data.get("sha_token") or data.get("compliance_token")
    if not isinstance(token, str) or not token:
        fail("sha_token (or compliance_token) missing or not a string")
    expected = _compute_token(data)
    given = str(token).strip().lower()
    if not given.startswith(expected[:16]):
        fail(
            f"sha_token does not match recomputed sha256 "
            f"(expected prefix {expected[:16]}, got {given[:16]})"
        )
    if len(given) < 16:
        fail(f"sha_token too short ({len(given)} hex chars; need >= 16)")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
