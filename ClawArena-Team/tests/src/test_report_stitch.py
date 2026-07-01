"""``collect_scenario_metadata`` 拼接逻辑单测。

场景相互独立,允许从不同 run 的「已完成」场景(根目录有 metadata.json)拼出一趟完整
测试再经 build_run_report 重生成 report。本测试覆盖:跨目录收集、scenario_id 去重
(保留 finished_at 最新)、缺 scenario_id / 损坏文件跳过。
"""
from __future__ import annotations

import json
from pathlib import Path

from clawarena_team.scoring.report import build_run_report, collect_scenario_metadata


def _write_meta(root: Path, run: str, sid: str, finished_at: str,
                task_success: float = 1.0) -> None:
    """在 ``root/<run>/<sid>/metadata.json`` 写一份最小 metadata。"""
    d = root / run / sid
    d.mkdir(parents=True, exist_ok=True)
    (d / "metadata.json").write_text(json.dumps({
        "scenario_id": sid,
        "finished_at": finished_at,
        "rounds": [],
        "metrics": {
            "scenario_id": sid,
            "task_success_rate": task_success,
            "rounds_passed": 6, "rounds_total": 6,
        },
        "models": {},
    }), encoding="utf-8")


def test_collect_across_runs(tmp_path: Path):
    _write_meta(tmp_path, "run_a", "s_alpha", "2026-06-06T01:00:00")
    _write_meta(tmp_path, "run_a", "s_beta", "2026-06-06T01:10:00")
    _write_meta(tmp_path, "run_b", "s_gamma", "2026-06-06T02:00:00")
    meta, info = collect_scenario_metadata([tmp_path])
    assert info["scanned"] == 3
    assert info["unique"] == 3
    # 按 scenario_id 排序
    assert [m["scenario_id"] for m in meta] == ["s_alpha", "s_beta", "s_gamma"]
    assert info["duplicates"] == {}


def test_dedupe_keeps_latest_finished(tmp_path: Path):
    # 同一场景出现在两个 run:旧的 task_success=0.2,新的 1.0 —— 应保留新的
    _write_meta(tmp_path, "run_old", "s_dup", "2026-06-06T01:00:00", task_success=0.2)
    _write_meta(tmp_path, "run_new", "s_dup", "2026-06-06T05:00:00", task_success=1.0)
    meta, info = collect_scenario_metadata([tmp_path])
    assert info["unique"] == 1
    assert info["duplicates"] == {"s_dup": 2}
    assert meta[0]["metrics"]["task_success_rate"] == 1.0  # finished_at 更新的一份
    assert "run_new" in info["sources"]["s_dup"]


def test_multiple_input_dirs(tmp_path: Path):
    a = tmp_path / "exp_a"
    b = tmp_path / "exp_b"
    _write_meta(a, "run_1", "s_x", "2026-06-06T01:00:00")
    _write_meta(b, "run_1", "s_y", "2026-06-06T01:00:00")
    meta, info = collect_scenario_metadata([a, b])
    assert info["unique"] == 2
    assert {m["scenario_id"] for m in meta} == {"s_x", "s_y"}


def test_skips_malformed_and_missing_id(tmp_path: Path):
    _write_meta(tmp_path, "run_a", "s_ok", "2026-06-06T01:00:00")
    # 缺 scenario_id
    bad1 = tmp_path / "run_a" / "s_noid"
    bad1.mkdir(parents=True, exist_ok=True)
    (bad1 / "metadata.json").write_text(json.dumps({"finished_at": "x"}), encoding="utf-8")
    # 损坏 JSON
    bad2 = tmp_path / "run_a" / "s_broken"
    bad2.mkdir(parents=True, exist_ok=True)
    (bad2 / "metadata.json").write_text("{not json", encoding="utf-8")
    meta, info = collect_scenario_metadata([tmp_path])
    assert info["unique"] == 1
    assert meta[0]["scenario_id"] == "s_ok"


def test_stitched_metadata_feeds_build_run_report(tmp_path: Path):
    """拼接结果可直接喂 build_run_report 重生成 report。"""
    _write_meta(tmp_path, "run_a", "s_alpha", "2026-06-06T01:00:00")
    _write_meta(tmp_path, "run_b", "s_beta", "2026-06-06T02:00:00")
    meta, _ = collect_scenario_metadata([tmp_path])
    report_json, report_md = build_run_report("stitched", meta)
    assert report_json["run_id"] == "stitched"
    assert report_json["scenarios_count"] == 2
    assert isinstance(report_md, str) and report_md
