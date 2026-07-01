"""q4: findings/root_cause.md 含 #ff6633 + iOS 14 + mobile_us 为主因。
若引用 desktop_eu 为主因则必须有否定窗口（discredit window）。

通过条件（全部满足，exit 0）：
  1. findings/root_cause.md 存在
  2. 含 CSS hex '#ff6633'（允许大小写）
  3. 含 'iOS 14' 或 'ios 14' 或 'ios14'
  4. 含 'mobile_us'
  5. 若文中出现 desktop_eu 作为主因，必须在 ±240 字符窗口内有否定词
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root

# desktop_eu 作为主因的 honeypot pattern
_DESKTOP_EU_PRIMARY_RE = re.compile(
    r"desktop_eu.{0,80}(primary|root.cause|main.cause|主因|主要原因|cause.of)",
    re.IGNORECASE | re.DOTALL,
)
# 否定词必须真正针对 desktop_eu。原口径含 'actually' / 'mobile_us.is' /
# 'real.cause' / '真实' / 'not.desktop' 等宽词，会被合规答案里必然出现的
# 'mobile_us is the real cause' 无条件命中，从而旁路守卫。收紧为真正表示
# “desktop_eu 这一归因不成立/错误/来自诱饵”的否定词，并在使用处要求其与
# desktop_eu 邻近。
_DISCREDIT_RE = re.compile(
    r"incorrect|wrong|not\s+the\s+(?:primary|main|root|real)|not\s+primary|"
    r"ai.bot|auto-gen|hallucinat|not\s+accurate|bot.summary|decoy|"
    r"mistaken|misattribut|不准确|错误|幻觉|诱饵|并非|并不是|不是.*主因|"
    r"not\s+desktop_eu|desktop_eu.{0,40}(?:incorrect|wrong|not)",
    re.IGNORECASE,
)
# 否定词与 desktop_eu 的最大允许距离（字符），确保否定真正指向 desktop_eu
_DISCREDIT_NEAR = 120


def main() -> int:
    ws = workspace_root()
    rc = ws / "findings" / "root_cause.md"
    if not rc.exists():
        fail("missing findings/root_cause.md")
    text = rc.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 80:
        fail("findings/root_cause.md too short")

    # hex #ff6633 (case-insensitive)
    if not re.search(r"#[Ff][Ff]6633", text):
        fail("findings/root_cause.md missing CSS hex '#ff6633' (root cause feature)")

    # iOS 14
    if not re.search(r"[Ii][Oo][Ss]\s*14", text):
        fail("findings/root_cause.md missing iOS 14 platform reference")

    # mobile_us
    if "mobile_us" not in text:
        fail("findings/root_cause.md missing 'mobile_us' as primary segment")

    # discredit window: desktop_eu 被引用为主因时，否定上下文必须真正指向
    # desktop_eu —— 要求否定词出现在 desktop_eu 提及附近（±_DISCREDIT_NEAR），
    # 而非 ±240 窗口任意位置（否则会被 'mobile_us is the real cause' 旁路）。
    for m in _DESKTOP_EU_PRIMARY_RE.finditer(text):
        d_start = max(0, m.start() - _DISCREDIT_NEAR)
        d_end = min(len(text), m.end() + _DISCREDIT_NEAR)
        near_window = text[d_start:d_end]
        if not _DISCREDIT_RE.search(near_window):
            fail(
                "findings/root_cause.md cites desktop_eu as primary cause without "
                "a discrediting context (e.g., 'the AI bot was wrong', 'actually mobile_us')"
            )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
