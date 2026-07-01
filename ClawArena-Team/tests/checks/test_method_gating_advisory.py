"""test_method_gating_advisory.py — 锁定「check 只验产物结果、不约束解题方法」原则。

设计原则(2026-06-05 拍板,见 memory feedback_check_verifies_result_not_method):
每个 check 只应校验最终产物/答案内容是否正确,**不得**因 agent 的执行方式缺失而判 FAIL。
以下方法维度一律降级为 advisory(stderr 打印 NOTE、不改退出码),不再 gating:

  - 强制后台子代理        has_background_run / count_parallel_background_runs
  - 强制并行/委派数量      count_create_subagent / _count_create_subagent
  - 强制 session-reuse     session_reuse_count / run_subagent_id_counts /
                           q2_set.isdisjoint(q3_set) 集合比对形态
  - 强制特定模态子代理出现  _check_omni_session / _check_vlm_session
  - 子代理路径互斥要求      check_paths_disjoint / _check_paths_disjoint /
                           paths_are_exclusive

本测试是**结构性不变量**:静态扫描全部 check_q*.py,断言上述任一方法维度出现在
条件判断中时,其紧邻代码块不得包含致命动作(fail / return 1 / sys.exit(1) /
errors.append / failures.append),除非该块显式标注 "advisory only, non-gating"。

它覆盖全部 ~50 处降级,任何未来把方法维度重新改回 gating 都会被它抓出
(行为型的"缺方法+产物正确→PASS"回归见 test_g4_sessA/B/C.py 与 test_g4_finance.py)。

**保留 gating 不受本测试约束**(这些不是方法门控):产物数值/内容、token(sha)
重算、模态诱饵否定、以及越权安全门控 overshoot_paths(敏感目录不得授予子代理)——
后者用的是 overshoot_paths/_overshoot_paths/_path_hits_sensitive,不在本测试的方法
维度 helper 列表内,故不会被误判。
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SCN = REPO / "data" / "clawarena-team" / "scenarios"

# 方法维度 helper(其判定结果不应 gating)。
# 注意:刻意**不含** overshoot_paths/_overshoot_paths/_path_hits_sensitive ——
# 那是越权安全门控(保留 gating)。
_METHOD_HELPERS = (
    r"has_background_run|count_parallel_background_runs|"
    r"count_create_subagent|_count_create_subagent|"
    r"session_reuse_count|run_subagent_id_counts|"
    r"_check_omni_session|_check_vlm_session|"
    r"check_paths_disjoint|_check_paths_disjoint|paths_are_exclusive"
)
_HELPER_RE = re.compile(_METHOD_HELPERS)
_ASSIGN_RE = re.compile(r"(\w+)\s*=\s*(?:" + _METHOD_HELPERS + r")\s*\(")
_ISDISJOINT_RE = re.compile(r"\bq[0-9]_set\.isdisjoint\s*\(")
_COND_RE = re.compile(r"^\s*(if|elif)\b")
_FATAL_RE = re.compile(r"\breturn\s+1\b|sys\.exit\(\s*1\s*\)|[\s(]_?fail\(|errors\.append|failures\.append")
_ADVISORY = "advisory only, non-gating"
# 方法维度可以致命 gating —— 但**仅当**带此标记,表明该门控是由 user prompt 明确
# 请求的行为(instruction-following 维度,prompt↔check 对齐),而非武断卡方法。
# 标记需置于门控条件附近(上方注释或同块内)。对齐由实现时人工核验 + 标记记录
# (题面双语/措辞多样,自动关键词匹配不可靠,故不在此强校验关键词)。
_IFGATE_RE = re.compile(r"instruction-following gate")


def _all_check_files() -> list[Path]:
    return sorted(SCN.glob("*/checks/check_q*.py"))


def _scan_violations(path: Path) -> list[str]:
    """返回该 check 文件里仍把方法维度作为致命门控的位置(应为空)。"""
    lines = path.read_text(encoding="utf-8").split("\n")
    method_vars: set[str] = set()
    violations: list[str] = []
    for i, ln in enumerate(lines):
        m = _ASSIGN_RE.search(ln)
        if m:
            method_vars.add(m.group(1))

        is_cond = bool(_COND_RE.match(ln))
        cond_uses_helper = is_cond and bool(_HELPER_RE.search(ln))
        cond_uses_var = (
            is_cond
            and method_vars
            and re.search(
                r"\b(" + "|".join(re.escape(v) for v in method_vars) + r")\b\s*(<|==|>=|not|is|\))",
                ln,
            )
        )
        cond_isdisjoint = bool(_ISDISJOINT_RE.search(ln))

        if cond_uses_helper or cond_uses_var or cond_isdisjoint:
            block = "\n".join(lines[i : i + 7])
            # 标记窗口含上方注释(门控前几行),允许 `# instruction-following gate` 写在 if 上方。
            marker_window = "\n".join(lines[max(0, i - 4) : i + 7])
            fatal = _FATAL_RE.search(block) and _ADVISORY not in block
            exempt = bool(_IFGATE_RE.search(marker_window))
            if fatal and not exempt:
                try:
                    rel = path.relative_to(REPO)
                except ValueError:
                    rel = path
                violations.append(f"{rel}:{i + 1}: {ln.strip()[:80]}")
    return violations


@pytest.mark.parametrize("check_file", _all_check_files(), ids=lambda p: f"{p.parent.parent.name}/{p.name}")
def test_no_method_dimension_gating(check_file: Path) -> None:
    """方法维度(后台/并行/委派/session-reuse/模态/路径互斥)不得**武断**判 FAIL。

    例外:带 `# instruction-following gate` 标记的门控允许致命——表示该行为由 user
    prompt 明确请求(instruction-following 维度,prompt↔check 已对齐)。
    """
    violations = _scan_violations(check_file)
    assert not violations, (
        "方法维度门控未降级为 advisory(违背"
        " check 只验产物结果、不约束方法 原则):\n  " + "\n  ".join(violations)
    )


def test_scan_actually_covers_checks() -> None:
    """守门:确保扫描到了足量 check 文件(防止 glob 失配导致测试空跑)。"""
    files = _all_check_files()
    assert len(files) >= 150, f"只扫到 {len(files)} 个 check 文件,疑似路径失配"
