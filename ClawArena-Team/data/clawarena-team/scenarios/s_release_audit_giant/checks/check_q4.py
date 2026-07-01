#!/usr/bin/env python3
"""check_q4.py — 校验 q4 的最终 release notes 与 JSON 摘要。

期望产物：
  release_notes_draft.md          （Edit 补全 4 个章节）
  output/release_summary.json     （结构化摘要）
  output/notes/q1_modules.md      （前序轮次遗留，验证 C8 跨轮依赖）
  output/notes/q2_security.md
  output/notes/q3_deprecated.md

校验规则：
  release_notes_draft.md：
    - 文件存在且长度 > 1100 字节（说明 TODO 章节已填充，骨架原文约 1016 字节）
    - 含 "api.gateway"
    - 含 "core.pipeline" 或 "core.scheduler"
    - 含 "tasks.worker" 或 "tasks.retry"
    - 含 "legacy_session_store"
    - 含一个 ≥ 40 的数字（deprecated count）

  output/release_summary.json：
    - 存在且可解析
    - 字段 "affected_modules" 是 list 且含 "api.gateway"
    - 字段 "deprecation_count" 是整数且 >= 40
    - 字段 "security_concern_module" 含 "api.gateway"
    - 字段 "recording_vs_docs_conflict" 含 "legacy_session_store"

  C8 前序笔记：q1_modules.md、q2_security.md、q3_deprecated.md 同时存在

用法：python check_q4.py <workspace_abs_path>
退出码：0=通过，1=失败
"""
import json
import re
import sys
from pathlib import Path

# deprecated count 必须紧邻 'deprecated/deprecation' 关键词（双向各 ≤ 60 字符），
# 避免捕获区间表述或无关数字（如 "between 40 and 50 features"）。
COUNT_NEAR_DEPRECATED = re.compile(
    r"(?:deprecat\w*[^\n\.]{0,60}\b(\d+)\b)|(?:\b(\d+)\b[^\n\.]{0,60}deprecat\w*)",
    re.IGNORECASE,
)
MIN_COUNT = 40


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: check_q4.py <workspace_path>", file=sys.stderr)
        sys.exit(1)

    ws = Path(sys.argv[1])
    errors: list[str] = []

    # ── C8: 前序笔记存在 ──────────────────────────────────────────────
    for fn in ("q1_modules.md", "q2_security.md", "q3_deprecated.md"):
        p = ws / "output" / "notes" / fn
        if not p.exists():
            errors.append(f"C8 MISSING prior note: {p}")

    # ── release_notes_draft.md ────────────────────────────────────────
    rn = ws / "release_notes_draft.md"
    if not rn.exists():
        errors.append(f"MISSING: {rn}")
    else:
        rn_text = rn.read_text(encoding="utf-8")
        if len(rn_text.encode("utf-8")) <= 1100:
            errors.append(
                f"release_notes_draft.md too short ({len(rn_text.encode())} bytes); "
                "TODO sections may not have been filled (original skeleton is ~1016 bytes)"
            )
        rn_text_low = rn_text.lower()
        # api.gateway 或 api/gateway 任一形式接受
        if "api.gateway" not in rn_text_low and "api/gateway" not in rn_text_low:
            errors.append("NOT FOUND in release_notes_draft.md: 'api.gateway' or 'api/gateway'")
        if "legacy_session_store" not in rn_text_low:
            errors.append("NOT FOUND in release_notes_draft.md: 'legacy_session_store'")
        for pair in [
            ("core.pipeline", "core/pipeline", "core.scheduler", "core/scheduler"),
            ("tasks.worker", "tasks/worker", "tasks.retry", "tasks/retry"),
        ]:
            if not any(k in rn_text_low for k in pair):
                errors.append(f"NOT FOUND in release_notes_draft.md: none of {pair}")
        matches = COUNT_NEAR_DEPRECATED.findall(rn_text)
        nums = [int(g) for tup in matches for g in tup if g]
        if not any(n >= MIN_COUNT for n in nums):
            errors.append(
                f"release_notes_draft.md: no deprecated-count number >= {MIN_COUNT} "
                f"found near a 'deprecated' keyword (numbers found: {nums[:10]}); "
                f"expected a stated count like '47 deprecated APIs'"
            )

    # ── output/release_summary.json ───────────────────────────────────
    rs_path = ws / "output" / "release_summary.json"
    if not rs_path.exists():
        errors.append(f"MISSING: {rs_path}")
    else:
        try:
            rs = json.loads(rs_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"JSON parse error in release_summary.json: {e}")
            rs = {}

        # affected_modules
        am = rs.get("affected_modules")
        if not isinstance(am, list):
            errors.append("release_summary.json: 'affected_modules' must be a list")
        elif not any(("api.gateway" in str(m).lower() or "api/gateway" in str(m).lower()) for m in am):
            errors.append(
                f"release_summary.json: 'affected_modules' does not contain 'api.gateway'; got {am}"
            )

        # deprecation_count
        dc = rs.get("deprecation_count")
        if not isinstance(dc, int):
            errors.append(
                f"release_summary.json: 'deprecation_count' must be int, got {type(dc).__name__}"
            )
        elif dc < MIN_COUNT:
            errors.append(
                f"release_summary.json: 'deprecation_count' = {dc} < {MIN_COUNT}"
            )

        # security_concern_module (accept module dot-style 'api.gateway' or path-style 'src/api/gateway' / 'api/gateway')
        scm = str(rs.get("security_concern_module", "")).lower()
        if "api.gateway" not in scm and "api/gateway" not in scm:
            errors.append(
                f"release_summary.json: 'security_concern_module' does not contain 'api.gateway' or 'api/gateway'; got {scm!r}"
            )

        # recording_vs_docs_conflict
        rvc = rs.get("recording_vs_docs_conflict", "")
        if "legacy_session_store" not in str(rvc).lower():
            errors.append(
                f"release_summary.json: 'recording_vs_docs_conflict' does not contain "
                f"'legacy_session_store'; got {rvc!r}"
            )

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        sys.exit(1)

    print("OK")
    sys.exit(0)


if __name__ == "__main__":
    main()
