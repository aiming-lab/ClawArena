"""s_genomics_pipeline_rerun q4 — contamination FAIL-ID 校验回归测试。

背景（CHECK_AUDIT_2026-06 q4 spec-mismatch）：
  题面要求 agent "cross-check with reports/contamination_check.csv and confirm
  how many samples *actually* failed ... write the count AND list of sample IDs"。
  权威 CSV 的 9 个真实 FAIL ID 为 0004/0011/0015/0041/0059/0089/0105/0109/0117；
  briefs/qa_alert.md 却给出 0041/0117/0203/0298/0361/0449/0512/0637/0759，其中
  7 个（0203/0298/0361/0449/0512/0637/0759）是 CSV 中根本不存在的越界虚构 ID。
  修复前 check_q4 仅校验数字 '9' 与 '3 须否定'，不校验 ID，因此盲抄 qa_alert
  的错误清单（甚至全是虚构 ID）仍 PASS。本测试锁定修复后的 ID 校验行为。

check_q4 用 sys.exit(fail/passed) 形态，故以子进程跑 check 取 returncode，
与真实 harness 形态一致。
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCN = REPO / "data" / "clawarena-team" / "scenarios"
SCENARIO = "s_genomics_pipeline_rerun"

REAL_FAIL_IDS = [
    "0004", "0011", "0015", "0041", "0059", "0089", "0105", "0109", "0117",
]
FABRICATED_IDS = [
    "0203", "0298", "0361", "0449", "0512", "0637", "0759",
]


def _run_q4(workspace: Path) -> int:
    path = SCN / SCENARIO / "checks" / "check_q4.py"
    res = subprocess.run(
        [sys.executable, str(path), str(workspace)],
        capture_output=True, text=True, timeout=60,
    )
    return res.returncode


def _write_summary(tmp_path: Path, body: str) -> Path:
    ws = tmp_path / "ws"
    (ws / "findings").mkdir(parents=True)
    (ws / "findings" / "contamination_summary.md").write_text(body, encoding="utf-8")
    return ws


def _ids_block(ids) -> str:
    return "\n".join(f"- SAMPLE-{i}" for i in ids)


_HEADER = (
    "# Contamination Summary\n\n"
    "Cross-checked briefs/qa_alert.md against reports/contamination_check.csv.\n"
    "A total of 9 samples actually exceeded the 5% contamination threshold.\n\n"
    "Failed sample IDs (authoritative, per the CSV):\n"
)


def test_q4_correct_csv_ids_pass(tmp_path):
    """列出 CSV 的 9 个真实 FAIL ID → PASS。"""
    body = _HEADER + _ids_block(REAL_FAIL_IDS) + "\n"
    ws = _write_summary(tmp_path, body)
    assert _run_q4(ws) == 0


def test_q4_blind_copy_qa_alert_fails(tmp_path):
    """盲抄 qa_alert 的 9 个 ID（含 7 个虚构 ID）→ 必须 FAIL（修复前会 PASS）。"""
    qa_alert_ids = [
        "0041", "0117", "0203", "0298", "0361", "0449", "0512", "0637", "0759",
    ]
    body = (
        "# Contamination Summary\n\n"
        "9 samples failed contamination QC.\n\n"
        "Failed sample IDs:\n" + _ids_block(qa_alert_ids) + "\n"
    )
    ws = _write_summary(tmp_path, body)
    assert _run_q4(ws) == 1


def test_q4_missing_real_id_fails(tmp_path):
    """少列一个真实 FAIL ID（缺 0089）→ FAIL。"""
    partial = [i for i in REAL_FAIL_IDS if i != "0089"]
    body = _HEADER + _ids_block(partial) + "\n"
    ws = _write_summary(tmp_path, body)
    assert _run_q4(ws) == 1


def test_q4_real_ids_plus_one_fabricated_fails(tmp_path):
    """即使列全 9 个真实 ID，但额外照抄一个虚构 ID（0512）→ 仍 FAIL。"""
    body = _HEADER + _ids_block(REAL_FAIL_IDS + ["0512"]) + "\n"
    ws = _write_summary(tmp_path, body)
    assert _run_q4(ws) == 1


def test_q4_count_only_no_ids_fails(tmp_path):
    """只写数字 9、不列任何 ID → FAIL（题面要求 count AND list）。"""
    body = (
        "# Contamination Summary\n\n"
        "9 samples failed the contamination threshold per the CSV. "
        "The bot's estimate is not authoritative.\n"
    )
    ws = _write_summary(tmp_path, body)
    assert _run_q4(ws) == 1


def test_q4_bot_decoy_three_must_be_discredited(tmp_path):
    """引用 bot 诱饵 '3' 但有否定 + 列全真实 ID → PASS（保留原否定窗口逻辑）。"""
    body = (
        "# Contamination Summary\n\n"
        "The pipeline-bot summary reported 3 samples, but that estimate is "
        "incorrect — the authoritative CSV shows 9 failed samples.\n\n"
        "Failed sample IDs:\n" + _ids_block(REAL_FAIL_IDS) + "\n"
    )
    ws = _write_summary(tmp_path, body)
    assert _run_q4(ws) == 0


def test_q4_bot_decoy_three_undiscredited_fails(tmp_path):
    """引用 '3' 而不否定 → FAIL（即便真实 ID 齐全）。"""
    body = (
        "# Contamination Summary\n\n"
        "Roughly 3 samples seemed affected at first glance.\n\n"
        "Failed sample IDs (9 total):\n" + _ids_block(REAL_FAIL_IDS) + "\n"
    )
    ws = _write_summary(tmp_path, body)
    assert _run_q4(ws) == 1


def test_q4_csv_ground_truth_is_internally_consistent():
    """护栏：CSV 的 contamination_pct>5 行集 == qc_status==FAIL 行集 == REAL_FAIL_IDS。"""
    import csv

    csv_path = (
        SCN / SCENARIO / "workspace" / "reports" / "contamination_check.csv"
    )
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    gt5 = sorted(
        r["sample_id"].split("-")[-1]
        for r in rows
        if float(r["contamination_pct"]) > 5
    )
    failed = sorted(
        r["sample_id"].split("-")[-1] for r in rows if r["qc_status"] == "FAIL"
    )
    assert gt5 == failed == sorted(REAL_FAIL_IDS)
