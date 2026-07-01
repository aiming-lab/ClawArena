"""check_q6.py — audit/ui_decision.json: json_schema + decision + a11y + locales + token.

通过条件（全部满足，exit 0）：
  1. audit/ui_decision.json 存在且可解析为 JSON
  2. decision 字段 == 'approve_v7_with_a11y_fixes'（schema_by_shape: 找含该字符串的值）
  3. a11y_fix_required 字段为 true（布尔 true 或字符串 'true'）
  4. localization 包含全部 4 种 locale: en, zh-CN, ja, de
  5. compliance_token == sha256('merchant-portal-v7:approve_v7_with_a11y_fixes:en,zh-CN,ja,de')[:16]
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root

EXPECTED_TOKEN_SRC = "merchant-portal-v7:approve_v7_with_a11y_fixes:en,zh-CN,ja,de"
EXPECTED_TOKEN = hashlib.sha256(EXPECTED_TOKEN_SRC.encode()).hexdigest()[:16]
REQUIRED_LOCALES = {"en", "zh-CN", "ja", "de"}
EXPECTED_DECISION = "approve_v7_with_a11y_fixes"


def _flatten_values(obj, depth: int = 0) -> list:
    """递归提取 JSON 对象或列表中的所有叶子值。"""
    if depth > 5:
        return []
    results = []
    if isinstance(obj, dict):
        for v in obj.values():
            results.extend(_flatten_values(v, depth + 1))
    elif isinstance(obj, list):
        for v in obj:
            results.extend(_flatten_values(v, depth + 1))
    else:
        results.append(obj)
    return results


def _find_locales(data: dict) -> set[str]:
    """从任意 JSON 结构中找出 locale 字符串集合。"""
    found = set()
    for v in _flatten_values(data):
        if isinstance(v, str):
            for loc in REQUIRED_LOCALES:
                if loc in v:
                    found.add(loc)
    return found


def main() -> int:
    ws = workspace_root()

    # 结构层
    out_path = ws / "audit" / "ui_decision.json"
    if not out_path.exists():
        fail("missing audit/ui_decision.json")

    raw = out_path.read_text(encoding="utf-8", errors="ignore")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail(f"audit/ui_decision.json is not valid JSON: {exc}")

    if not isinstance(data, dict):
        fail("audit/ui_decision.json must be a JSON object")

    all_values = _flatten_values(data)
    str_values = [v for v in all_values if isinstance(v, str)]

    # 字段层：decision == 'approve_v7_with_a11y_fixes'
    decision_found = any(EXPECTED_DECISION in v for v in str_values)
    if not decision_found:
        fail(
            f"audit/ui_decision.json: decision value '{EXPECTED_DECISION}' not found. "
            f"Found string values: {str_values[:10]}"
        )

    # 字段层：a11y_fix_required == true
    # 只认真正的 a11y_fix_required（含同义键）键值，不再把 JSON 中任意位置的
    # 布尔 true 当作满足——否则显式写成 false 的 a11y_fix_required 会被别处无关
    # 的 true 兜底误判为满足（over-loose）。
    a11y_key_found = False
    a11y_required = False
    low_keys = {k.lower(): v for k, v in data.items()}
    for key in ("a11y_fix_required", "a11y_required", "accessibility_fix_required",
                "fix_required", "a11y_fixes_required"):
        if key in low_keys:
            a11y_key_found = True
            val = low_keys[key]
            if val is True or str(val).lower() in ("true", "yes", "1"):
                a11y_required = True
            break
    if not a11y_key_found:
        fail("audit/ui_decision.json: a11y_fix_required field not found")
    if not a11y_required:
        fail("audit/ui_decision.json: a11y_fix_required present but not true")

    # 字段层：4 个 locale 全覆盖
    found_locales = _find_locales(data)
    missing_locales = REQUIRED_LOCALES - found_locales
    if missing_locales:
        fail(
            f"audit/ui_decision.json: missing locales {missing_locales}. "
            f"Found: {found_locales}. Required: {REQUIRED_LOCALES}"
        )

    # 字段层：compliance_token
    token_found = None
    for key in ("compliance_token", "token", "audit_token", "compliance_hash"):
        if key in low_keys:
            token_found = str(low_keys[key]).strip()
            break
    if token_found is None:
        for v in str_values:
            if re.match(r"^[0-9a-f]{16}$", v.strip()):
                token_found = v.strip()
                break
    if token_found != EXPECTED_TOKEN:
        fail(
            f"audit/ui_decision.json: compliance_token mismatch. "
            f"Expected: {EXPECTED_TOKEN!r}, got: {token_found!r}. "
            f"Token source: sha256('{EXPECTED_TOKEN_SRC}')[:16]"
        )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
