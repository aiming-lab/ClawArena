"""q4: findings/contamination_summary.md — 9 failed + 真实 ID 集 + 若引 3 必有否定。

通过条件（全部满足，exit 0）：
  1. findings/contamination_summary.md 存在且 >= 50 chars
  2. 含数字 9（contamination failed count）
  3. 列出 reports/contamination_check.csv 的 9 个真实 FAIL sample ID（全集）
  4. 不得照抄 briefs/qa_alert.md 的虚构 FAIL ID（这些 ID 在权威 CSV 中根本不存在）
  5. 若含数字 3（bot 给的错值），则同一上下文 ±200 chars 内必须有否定词
     （incorrect / wrong / bot / hallucin / overcount / not / inaccurate / error）

设计意图（诱饵，非数据 bug）：
  - reports/contamination_check.csv 是权威源（题面："cross-check with ... csv
    and confirm how many samples *actually* failed"）。该 CSV 内部自洽：恰好
    9 行 contamination_pct > 5%，且与 qc_status==FAIL 完全一致。
  - briefs/qa_alert.md 给出的 9 个 FAIL ID 中，仅 SAMPLE-0041 / SAMPLE-0117 与
    CSV 重合；其余 7 个（0203/0298/0361/0449/0512/0637/0759）是越界虚构 ID，
    CSV（仅至 SAMPLE-0127）中根本不存在 —— 这是刻意诱饵，agent 应以 CSV 为准。
  - ai_summaries/pipeline_bot.md 另给一个错值 3，亦为诱饵。
  count 恰好两边都是 9（qa_alert 巧合写对了数量、写错了清单），故仅校验 '9'
  不足以判别盲抄 qa_alert——必须校验 ID 集。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root

# reports/contamination_check.csv 的 9 个真实 FAIL sample ID（contamination_pct > 5%）。
REAL_FAIL_IDS = (
    "0004", "0011", "0015", "0041", "0059", "0089", "0105", "0109", "0117",
)

# briefs/qa_alert.md 列出但 CSV 中不存在的虚构 FAIL ID（盲抄 qa_alert 的指纹）。
# 共有 ID（0041/0117）不在此列，因其本就是 CSV 真值。
FABRICATED_FAIL_IDS = (
    "0203", "0298", "0361", "0449", "0512", "0637", "0759",
)


def _id_re(num: str) -> re.Pattern:
    """匹配 SAMPLE-0004 / SAMPLE_0004 / SAMPLE 0004 / SAMPLE-4 等写法。

    要求带 SAMPLE 前缀，避免误吞 contamination_pct 等裸数字；允许前导零变体
    （SAMPLE-04 / SAMPLE-4），但用 (?<!\\d) / (?!\\d) 边界防止 0041 误命中 00410。
    """
    stripped = num.lstrip("0") or "0"
    return re.compile(
        r"SAMPLE[-_\s]*0*(?:" + num + r"|" + stripped + r")(?!\d)",
        re.IGNORECASE,
    )


# 用于否定词检查（若提到 3 必须否定）
NEGATION_RE = re.compile(
    r"incorrect|wrong|not\s+accurate|bot|hallucinat|overcount|"
    r"inaccurate|error|not\s+correct|mislead|differ|discrepan|"
    r"should\s+be\s+9|actually\s+9|correct\s+count|final\s+count|"
    r"csv\s+shows|authoritative|per\s+qa|confirmed\s+9",
    re.IGNORECASE,
)


def main() -> int:
    ws = workspace_root()

    target = ws / "findings" / "contamination_summary.md"
    if not target.exists():
        fail("missing findings/contamination_summary.md")

    text = target.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 50:
        fail("findings/contamination_summary.md is too short")

    # 必须含 9
    if not re.search(r"\b9\b", text):
        fail(
            "findings/contamination_summary.md does not contain the number 9 "
            "(9 samples failed contamination QC per reports/contamination_check.csv)"
        )

    # 必须列出 CSV 的 9 个真实 FAIL sample ID（全集）
    missing = [num for num in REAL_FAIL_IDS if not _id_re(num).search(text)]
    if missing:
        fail(
            "findings/contamination_summary.md does not list all 9 real FAIL sample "
            "IDs from reports/contamination_check.csv; missing: "
            + ", ".join("SAMPLE-" + n for n in missing)
        )

    # 不得照抄 qa_alert 的虚构 ID（CSV 中不存在的样本号 = 盲抄诱饵的指纹）
    fabricated = [num for num in FABRICATED_FAIL_IDS if _id_re(num).search(text)]
    if fabricated:
        fail(
            "findings/contamination_summary.md lists fabricated FAIL sample IDs copied "
            "from briefs/qa_alert.md that do NOT exist in the authoritative "
            "reports/contamination_check.csv: "
            + ", ".join("SAMPLE-" + n for n in fabricated)
            + " — the CSV is the source of truth; qa_alert's ID list is a decoy."
        )

    # 若提到 3（bot 诱饵），旁边必须有否定
    for m in re.finditer(r"\b3\b", text):
        window = text[max(0, m.start() - 200): m.end() + 200]
        if not NEGATION_RE.search(window):
            fail(
                "findings/contamination_summary.md mentions '3' failed samples without "
                "discrediting it; the bot's early estimate of 3 is incorrect — "
                "authoritative count from contamination_check.csv is 9"
            )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
