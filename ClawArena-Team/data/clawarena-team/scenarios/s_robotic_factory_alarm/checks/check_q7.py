"""check_q7.py — final audit ticket JSON + compliance token + power_supply decoy negated.

通过条件（全部满足，exit 0）：
  1. audit/maintenance_ticket.json 存在且 JSON 可解析
  2. 含字段 decision = "schedule_maintenance_24h"（或含 schedule 和 maintenance 和 24）
  3. 含字段 root_cause 含 "gripper" 或 "joint"
  4. 含字段 compliance_token，且其值等于按 tools/verify_decision.py 算法对本票据
     KEYS 字段（decision|alarm_code|robot_id|root_cause|dispatcher|ticket_date）
     重算出的 sha256 —— 不再只判长度，必须真正复算并比对
  5. 含字段 alarm_code = "E-0211"
  6. 若文件中出现 "power_supply" 或 "电源"，须在 ±200 chars 窗口内有否定词
     （否则视为采纳了 AI 幻觉摘要的错误根因）

compliance_token 口径说明：
  题面要求 "run tools/verify_decision.py to get the compliance token"。该脚本的
  token 不是路径绑定的，而是对票据自身 KEYS 字段值做 canonical "k=v" join 后取
  sha256。故复算只依赖票据内容本身，确定且无路径写法歧义——正确 token PASS，
  任一被哈希字段被篡改 / 占位 token 均 FAIL。
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, has_phrase_any, passed, workspace_root

# verify_decision.py 的 canonical 算法（与 workspace/tools/verify_decision.py 保持一致）：
#   token = sha256("|".join(f"{k}={payload.get(k, '')}" for k in _TOKEN_KEYS))
_TOKEN_KEYS = ["decision", "alarm_code", "robot_id", "root_cause", "dispatcher", "ticket_date"]


def _expected_token(ticket: dict) -> str:
    parts = [f"{k}={ticket.get(k, '')}" for k in _TOKEN_KEYS]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()

_PS_RE = re.compile(r"power[_\s]?supply|电源故障|电源问题", re.IGNORECASE)
_NEGATE_RE = re.compile(
    r"not the cause|incorrect|wrong|ruled out|not confirmed|not supported|"
    r"decoy|hallucin|不是根因|排除|错误|不正确|AI 生成|幻觉|unsupported",
    re.IGNORECASE,
)


def _power_supply_without_negation(text: str) -> bool:
    for m in _PS_RE.finditer(text):
        window = text[max(0, m.start() - 200): m.end() + 200]
        if not _NEGATE_RE.search(window):
            return True
    return False


def main() -> int:
    ws = workspace_root()
    ticket_path = ws / "audit" / "maintenance_ticket.json"
    if not ticket_path.exists():
        fail("missing audit/maintenance_ticket.json")
    try:
        ticket = json.loads(ticket_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"audit/maintenance_ticket.json is not valid JSON: {exc}")

    # decision 字段
    decision = str(ticket.get("decision", "")).lower()
    if not (
        "schedule_maintenance_24h" in decision
        or ("schedule" in decision and "maintenance" in decision and "24" in decision)
        or ("schedule" in decision and "24" in decision)
    ):
        fail(
            f"decision field does not indicate 'schedule_maintenance_24h': {ticket.get('decision')!r}"
        )

    # root_cause
    root_cause = str(ticket.get("root_cause", "")).lower()
    if not any(kw in root_cause for kw in ("gripper", "joint", "关节", "夹爪", "wear", "磨损")):
        fail(f"root_cause does not mention gripper/joint wear: {ticket.get('root_cause')!r}")

    # alarm_code
    alarm_code = str(ticket.get("alarm_code", ""))
    if not re.search(r"E[_\-]?0211", alarm_code, re.IGNORECASE):
        fail(f"alarm_code field does not match E-0211: {alarm_code!r}")

    # compliance_token —— 真正按 verify_decision.py 算法重算并比对（收紧）
    token = str(ticket.get("compliance_token", "")).strip().lower()
    if not token:
        fail("compliance_token field is missing or empty")
    # 去掉可能的 "COMPLIANCE_TOKEN:" 前缀（题面脚本输出形如 COMPLIANCE_TOKEN:<sha>）
    m = re.search(r"([0-9a-f]{64})", token)
    if not m:
        fail(
            "compliance_token does not contain a 64-hex sha256 digest — "
            "must run tools/verify_decision.py on the ticket and embed its token"
        )
    token_hex = m.group(1)
    expected = _expected_token(ticket)
    if token_hex != expected:
        fail(
            "compliance_token sha mismatch — the token does not match a recomputation "
            "over the ticket's own fields (decision|alarm_code|robot_id|root_cause|"
            f"dispatcher|ticket_date) per tools/verify_decision.py; "
            f"got {token_hex[:12]}…, expected {expected[:12]}…"
        )

    # power_supply decoy — full text check
    full_text = ticket_path.read_text(encoding="utf-8")
    if _power_supply_without_negation(full_text):
        fail(
            "power_supply cited as root cause without negation — AI decoy adopted. "
            "Must explicitly rule out power_supply with a negation phrase."
        )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
