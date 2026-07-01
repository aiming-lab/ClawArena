"""决策项回归测试（2026-06-05 §7 拍板后）。

覆盖：
  - 簇D feedback 文本修正不影响评分（check 逻辑本就正确）。
  - incident_postmortem q2 时间锚点由 14:21 改为 14:23（数据复核：14:21 无 ERROR）。
  - 簇C 各数据矛盾项修复后的 check 行为。

复用 load_check 动态加载范式，隔离各场景同名 _common。
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCN = REPO / "data" / "clawarena-team" / "scenarios"


def load_check(scenario: str, qid: str):
    checks_dir = SCN / scenario / "checks"
    path = checks_dir / f"check_{qid}.py"
    sys.modules.pop("_common", None)
    sys.path.insert(0, str(checks_dir))
    try:
        spec = importlib.util.spec_from_file_location(f"chk_{scenario}_{qid}", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    finally:
        if str(checks_dir) in sys.path:
            sys.path.remove(str(checks_dir))
        sys.modules.pop("_common", None)


# ---------------------------------------------------------------------------
# incident_postmortem q2 — 时间锚点 14:21 -> 14:23
# ---------------------------------------------------------------------------

_Q2_NOTE = (
    "# First-error analysis\n\n"
    "The first incident-relevant ERROR was emitted by **payments-api** at "
    "{ts}. The memory_pressure_high warning preceded the oom_kill_imminent "
    "ERROR. The on-call's redis cache-eviction theory does not hold up: the "
    "redis evictions are a downstream symptom of the payments-api memory "
    "pressure, not the root cause.\n"
)


def _run_q2(tmp_path: Path, ts: str) -> int:
    mod = load_check("s_incident_postmortem", "q2")
    note = tmp_path / "output" / "notes" / "q2_first_error.md"
    note.parent.mkdir(parents=True)
    note.write_text(_Q2_NOTE.format(ts=ts), encoding="utf-8")
    argv = sys.argv
    sys.argv = ["check_q2.py", str(tmp_path)]
    try:
        return mod.main()
    finally:
        sys.argv = argv


def test_incident_q2_accepts_1423(tmp_path: Path):
    """14:23（数据支持的真实首错分钟）现在 PASS。"""
    assert _run_q2(tmp_path, "14:23:29") == 0


def test_incident_q2_rejects_1421_only(tmp_path: Path):
    """仅 14:21（无 ERROR 的旧错误锚点）现在 FAIL。"""
    assert _run_q2(tmp_path, "14:21:08") == 1


def test_incident_q2_timestamp_regex_targets_1423():
    mod = load_check("s_incident_postmortem", "q2")
    assert mod.TIMESTAMP_FIRST_ERROR_RE.search("error at 14:23:42")
    assert not mod.TIMESTAMP_FIRST_ERROR_RE.search("only 14:21:05 here")
