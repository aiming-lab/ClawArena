"""check_q6.py — audit/protocol_decision.json 结构完整、数字正确、decision 合法、token 有效。

通过条件（全部满足，exit 0）：
  1. audit/protocol_decision.json 存在且可解析
  2. 包含全部必填字段：trial_id / compound / total_patients / cn_patients /
     de_patients / us_patients / irb_decision / decision / reviewer /
     decision_date / compliance_token
  3. 数值精确：total_patients=240, cn=120, de=80, us=40
  4. decision = "approve_with_amendments"
  5. irb_decision 含 "approved with monitoring plan"（或其等价）
  6. compliance_token 与本地重算 sha256 一致
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, has_phrase_any, passed, workspace_root

REQUIRED_FIELDS = [
    "trial_id", "compound", "total_patients", "cn_patients",
    "de_patients", "us_patients", "irb_decision", "decision",
    "reviewer", "decision_date", "compliance_token",
]

TOKEN_KEYS = [
    "trial_id", "compound", "total_patients", "cn_patients",
    "de_patients", "us_patients", "irb_decision", "decision",
    "reviewer", "decision_date",
]

_IRB_PHRASES = [
    "approved with monitoring plan",
    "approved with a monitoring plan",
    "approval with monitoring plan",
    "批准并附监查计划",
    "附监查计划的批准",
    "genehmigt mit überwachungsplan",
    "mit überwachungsplan genehmigt",
]


def _compute_token(payload: dict) -> str:
    parts = [f"{k}={payload.get(k, '')}" for k in TOKEN_KEYS]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


def _check_decision_date(date_str: str) -> bool:
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", str(date_str)))


def main() -> int:
    ws = workspace_root()
    jpath = ws / "audit" / "protocol_decision.json"
    if not jpath.exists():
        fail("missing audit/protocol_decision.json")

    try:
        payload = json.loads(jpath.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"audit/protocol_decision.json is not valid JSON: {e}")

    # 必填字段
    missing = [k for k in REQUIRED_FIELDS if k not in payload]
    if missing:
        fail(f"missing fields in protocol_decision.json: {missing}")

    # 数值精确匹配
    for field, expected in [
        ("total_patients", 240),
        ("cn_patients", 120),
        ("de_patients", 80),
        ("us_patients", 40),
    ]:
        val = payload.get(field)
        try:
            val = int(val)
        except (TypeError, ValueError):
            fail(f"{field} = {val!r} is not numeric")
        if val != expected:
            fail(f"{field} = {val} (expected {expected})")

    # decision
    decision = str(payload.get("decision", ""))
    if decision != "approve_with_amendments":
        fail(
            f"decision = {decision!r} (expected 'approve_with_amendments')"
        )

    # irb_decision 短语
    irb_text = str(payload.get("irb_decision", ""))
    if not has_phrase_any(irb_text, _IRB_PHRASES):
        fail(
            f"irb_decision field {irb_text!r} does not contain "
            "'approved with monitoring plan' or equivalent"
        )

    # decision_date 格式
    ddate = str(payload.get("decision_date", ""))
    if not _check_decision_date(ddate):
        fail(f"decision_date {ddate!r} is not YYYY-MM-DD")

    # compliance_token
    expected_token = _compute_token(payload)
    actual_token = str(payload.get("compliance_token", ""))
    if actual_token != expected_token:
        fail(
            f"compliance_token mismatch:\n"
            f"  actual:   {actual_token}\n"
            f"  expected: {expected_token}\n"
            "(run tools/compute_token.py on the JSON to get the correct token)"
        )

    passed(
        f"OK: protocol_decision.json is valid — decision={decision}, "
        f"total={payload['total_patients']}, token=✓"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
