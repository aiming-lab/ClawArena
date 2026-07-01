"""clawarena-team clean -t/--targets 行为覆盖。"""
from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from clawarena_team.cli import main


def _make_results_tree(root: Path) -> None:
    """构造典型 results/run_*/<sid>/{work,sessions,logs}/ 结构。"""
    for run in ("run_aaa", "run_bbb"):
        for sid in ("s1", "s2"):
            base = root / run / sid
            (base / "work").mkdir(parents=True)
            (base / "work" / "f.txt").write_text("w", encoding="utf-8")
            (base / "sessions").mkdir()
            (base / "sessions" / "main.jsonl").write_text("{}", encoding="utf-8")
            (base / "logs").mkdir()
            (base / "logs" / "x.log").write_text("log", encoding="utf-8")
            (base / "metadata.json").write_text("{}", encoding="utf-8")


def _count(root: Path, name: str) -> int:
    return sum(1 for p in root.rglob(name) if p.is_dir())


def test_clean_default_only_work(tmp_path: Path):
    out = tmp_path / "results"
    _make_results_tree(out)
    runner = CliRunner()
    res = runner.invoke(main, ["clean", "-o", str(out)])
    assert res.exit_code == 0, res.output
    assert _count(out, "work") == 0
    assert _count(out, "sessions") == 4
    assert _count(out, "logs") == 4


def test_clean_logs_only(tmp_path: Path):
    out = tmp_path / "results"
    _make_results_tree(out)
    runner = CliRunner()
    res = runner.invoke(main, ["clean", "-o", str(out), "-t", "logs"])
    assert res.exit_code == 0, res.output
    assert _count(out, "work") == 4
    assert _count(out, "logs") == 0


def test_clean_all_removes_everything(tmp_path: Path):
    out = tmp_path / "results"
    _make_results_tree(out)
    runner = CliRunner()
    res = runner.invoke(main, ["clean", "-o", str(out), "-t", "all"])
    assert res.exit_code == 0, res.output
    assert _count(out, "work") == 0
    assert _count(out, "logs") == 0
    assert _count(out, "sessions") == 0
    # metadata.json 不应被清掉（2 run × 2 sid = 4 份）
    assert sum(1 for _ in out.rglob("metadata.json")) == 4


def test_clean_unknown_target_errors(tmp_path: Path):
    out = tmp_path / "results"
    out.mkdir()
    runner = CliRunner()
    res = runner.invoke(main, ["clean", "-o", str(out), "-t", "nope"])
    assert res.exit_code != 0
    assert "unknown clean targets" in (res.output + str(res.exception))


def test_clean_nonexistent_dir_is_noop(tmp_path: Path):
    runner = CliRunner()
    res = runner.invoke(main, ["clean", "-o", str(tmp_path / "nope")])
    assert res.exit_code == 0
    assert "nothing to clean" in res.output
