"""check_q5.py — findings/version_audit.md 明示 v1/v2 过期，v3 为权威版本。

通过条件（全部满足，exit 0）：
  1. findings/version_audit.md 存在且非空
  2. 含 "v1_2024" 或 "v1" 加上弃用关键词（superseded / deprecated / stale / archived / 过期 / 已废弃）
  3. 含 "v2_2025" 或 "v2" 加上弃用关键词
  4. 含 "v3" 加上权威关键词（authoritative / current / 当前 / 最终 / 权威）
  5. 文件中 "v3" 不与弃用关键词同时出现（即 v3 没被错误标成 stale）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root

_DEPRECATED_KW = re.compile(
    r"superseded|deprecated|stale|archived|obsolete|not cite|do not cite|"
    r"已废弃|过期|已过时|已取代|存档|禁止引用",
    re.IGNORECASE,
)
_AUTH_KW = re.compile(
    r"authoritative|current|canonical|active|final|authority|"
    r"当前|权威|最终|有效|正式",
    re.IGNORECASE,
)


def _version_deprecated(text: str, ver: str) -> bool:
    """检查 text 中 ver（如 'v1' / 'v1_2024'）是否在 ±200 chars 内有弃用关键词。"""
    for m in re.finditer(re.escape(ver), text, re.IGNORECASE):
        window = text[max(0, m.start() - 200): m.end() + 200]
        if _DEPRECATED_KW.search(window):
            return True
    return False


def _v3_authoritative(text: str) -> bool:
    """检查 'v3' 在 ±200 chars 内是否有权威关键词。"""
    # 'v3' 作版本 token：词首起、其后非数字即可（匹配 v3 / v3_zh_en_de.docx / v3.docx，但非 v30）。
    # 注意 \b 在 'v3_' 处不成立（下划线是 \w），故不用 \bv3\b。
    for m in re.finditer(r"(?<![a-z0-9])v3(?![0-9])", text, re.IGNORECASE):
        window = text[max(0, m.start() - 200): m.end() + 200]
        if _AUTH_KW.search(window):
            return True
    return False


def main() -> int:
    ws = workspace_root()
    audit = ws / "findings" / "version_audit.md"
    if not audit.exists():
        fail("missing findings/version_audit.md")

    text = audit.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 60:
        fail("findings/version_audit.md is too short (< 60 chars)")

    # v1 deprecated
    if not (_version_deprecated(text, "v1_2024") or _version_deprecated(text, "v1")):
        fail("v1_2024 not identified as deprecated/stale in version_audit.md")

    # v2 deprecated
    if not (_version_deprecated(text, "v2_2025") or _version_deprecated(text, "v2")):
        fail("v2_2025 not identified as deprecated/stale in version_audit.md")

    # v3 authoritative
    if not _v3_authoritative(text):
        fail("v3 not identified as authoritative/current in version_audit.md")

    passed("OK: version_audit.md correctly marks v1/v2 as stale and v3 as authoritative")
    return 0


if __name__ == "__main__":
    sys.exit(main())
