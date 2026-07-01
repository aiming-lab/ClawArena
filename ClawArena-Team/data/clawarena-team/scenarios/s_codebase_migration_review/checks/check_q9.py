"""check_q9.py — audit/final_review.json schema 完整 + decision 合法 + 跨轮值一致。

通过条件（全部满足，exit 0）：
  1. audit/final_review.json 存在且为合法 JSON
  2. 含必须字段：decision / services / risks / coverage_gap / rpc_diff_count
  3. decision ∈ {block_merge, staged_rollout, approve}；
     且若 coverage_gap 含 31.2（或 < 80），decision 不可为 'approve'
  4. rpc_diff_count 为正整数（>= 1）
  5. coverage_gap 字段含数字 31.2（或等价的 31.2% 字符串）
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root

REQUIRED_KEYS = {"decision", "services", "risks", "coverage_gap", "rpc_diff_count"}
VALID_DECISIONS = {"block_merge", "staged_rollout", "approve"}


def main() -> int:
    ws = workspace_root()
    p = ws / "audit" / "final_review.json"
    if not p.exists():
        fail("missing audit/final_review.json")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"final_review.json is not valid JSON: {e}")

    missing = REQUIRED_KEYS - set(data.keys())
    if missing:
        fail(f"final_review.json missing keys: {sorted(missing)}")

    # decision 合法值
    decision = str(data.get("decision", "")).lower().replace(" ", "_")
    if decision not in VALID_DECISIONS:
        fail(f"decision must be one of {sorted(VALID_DECISIONS)}, got {data['decision']!r}")

    # coverage_gap 含 31.2
    cg = str(data.get("coverage_gap", ""))
    if not re.search(r"\b31\.2\b", cg):
        fail(f"coverage_gap field must contain '31.2' (ledger coverage), got {cg!r}")

    # ledger 覆盖率 31.2% < 80%，不可 approve
    if decision == "approve":
        fail("ledger coverage is 31.2% (< 80% threshold); 'approve' is not a defensible decision")

    # rpc_diff_count 是正整数
    rdc = data.get("rpc_diff_count")
    try:
        rdc_int = int(rdc)
    except (TypeError, ValueError):
        fail(f"rpc_diff_count must be an integer, got {rdc!r}")
        return 1
    if rdc_int < 1:
        fail(f"rpc_diff_count must be >= 1 (at least 1 RPC incompatibility found), got {rdc_int}")

    # services 须含 4 个服务
    services = data.get("services", [])
    if isinstance(services, list):
        svc_str = " ".join(str(s).lower() for s in services)
    else:
        svc_str = str(services).lower()
    for svc in ("payments", "billing", "ledger", "reports"):
        if svc not in svc_str:
            fail(f"final_review.json 'services' field missing service: {svc!r}")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
