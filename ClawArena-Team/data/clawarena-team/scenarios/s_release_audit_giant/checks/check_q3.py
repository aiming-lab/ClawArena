#!/usr/bin/env python3
"""check_q3.py — 校验 q3 落盘的 deprecated 扫描 + 冲突检测笔记。

期望产物：
  output/notes/q3_deprecated.md  （main agent 落盘）

校验规则：
  - 文件存在
  - deprecated 总数为整数且 >= 40（u1 apply 后大幅增加，精确值 47，允许 ±5 误差，即 ≥ 40）
  - 含 "legacy_session_store"（冲突 API 名）
  - 含关键词表明文档与视频冲突：
    "conflict" 或 "inconsistent" 或 "discrepancy"（不区分大小写）
  - 含证明已看 .mp4 录像的证据：视频文件名 design_meeting_2026-04-12 /
    .mp4 后缀 / "recording" / "video" / 录像内时间戳（mm:ss）。
    注意：裸 "meeting" 不算——该词在 docs/deprecations.md 中多次出现，
    单凭文本文档即可满足，不能证明看了录像。

用法：python check_q3.py <workspace_abs_path>
退出码：0=通过，1=失败
"""
import re
import sys
from pathlib import Path


CONFLICT_API = "legacy_session_store"
# deprecated count 必须紧邻 'deprecated/deprecation' 关键词（双向各 ≤ 60 字符），
# 避免捕获诸如 'between 40 and 50' 的区间表述或无关数字。
COUNT_NEAR_DEPRECATED = re.compile(
    r"(?:deprecat\w*[^\n\.]{0,60}\b(\d+)\b)|(?:\b(\d+)\b[^\n\.]{0,60}deprecat\w*)",
    re.IGNORECASE,
)
CONFLICT_WORD_PATTERN = re.compile(r"conflict|inconsisten\w*|discrepan\w*|mismatch", re.IGNORECASE)
# Bare 'meeting' is NOT evidence that the .mp4 recording was viewed — the word
# 'meeting' appears many times in docs/deprecations.md ('UPDATED POST-MEETING',
# '2026-04-12 meeting …') after the u1 hotfix, so it can be satisfied purely by
# the text doc. Require evidence of the recording itself: the video file name,
# the .mp4 extension, an explicit 'recording'/'video' reference, or a timestamp
# citation into the recording (e.g. 'at 12:34' / 'minute 5').
VIDEO_PATTERN = re.compile(
    r"design_meeting_2026-04-12"
    r"|\.mp4\b"
    r"|recording"
    r"|\bvideo\b"
    r"|(?:meeting\s+)?recording"
    r"|\b\d{1,2}:\d{2}\b"  # timestamp into the recording (mm:ss / h:mm)
    r"|\bminute\s+\d+\b",
    re.IGNORECASE,
)
MIN_DEPRECATED_COUNT = 40


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: check_q3.py <workspace_path>", file=sys.stderr)
        sys.exit(1)

    ws = Path(sys.argv[1])
    notes = ws / "output" / "notes" / "q3_deprecated.md"

    if not notes.exists():
        print(f"MISSING: {notes}", file=sys.stderr)
        sys.exit(1)

    text = notes.read_text(encoding="utf-8")

    # Check: legacy_session_store mentioned
    if CONFLICT_API.lower() not in text.lower():
        print(f"NOT FOUND: '{CONFLICT_API}' not mentioned in q3_deprecated.md", file=sys.stderr)
        sys.exit(1)

    # Check: conflict keyword present
    if not CONFLICT_WORD_PATTERN.search(text):
        print(
            "NOT FOUND: no conflict keyword (conflict/inconsistent/discrepancy/mismatch) "
            "in q3_deprecated.md",
            file=sys.stderr,
        )
        sys.exit(1)

    # Check: video/recording keyword present
    if not VIDEO_PATTERN.search(text):
        print(
            "NOT FOUND: no video/recording keyword in q3_deprecated.md — "
            "agent may not have read the meeting recording",
            file=sys.stderr,
        )
        sys.exit(1)

    # Check: deprecated count >= MIN_DEPRECATED_COUNT（数字必须紧邻 deprecated/deprecation）
    matches = COUNT_NEAR_DEPRECATED.findall(text)
    numbers = [int(g) for tup in matches for g in tup if g]
    if not any(n >= MIN_DEPRECATED_COUNT for n in numbers):
        print(
            f"FAIL: no deprecated-count number >= {MIN_DEPRECATED_COUNT} found near a "
            f"'deprecated' keyword in q3_deprecated.md (numbers found: {numbers[:10]}); "
            f"expected a stated count ~47 after u1 hotfix, e.g. '47 deprecated APIs'",
            file=sys.stderr,
        )
        sys.exit(1)

    print("OK")
    sys.exit(0)


if __name__ == "__main__":
    main()
