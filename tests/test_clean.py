"""Tests for clean command."""

from pathlib import Path

from clawarena.core.clean import run_clean


def test_clean_work(tmp_path):
    work = tmp_path / "results" / "work"
    work.mkdir(parents=True)
    (work / "state_abc").mkdir()

    run_clean(tmp_path / "results", ["work"])
    assert not work.exists()


def test_clean_logs(tmp_path):
    logs = tmp_path / "results" / "llm_logs"
    logs.mkdir(parents=True)
    (logs / "session1").mkdir()

    run_clean(tmp_path / "results", ["logs"])
    assert not logs.exists()


def test_clean_all(tmp_path):
    work = tmp_path / "out" / "work"
    work.mkdir(parents=True)
    logs = tmp_path / "out" / "llm_logs"
    logs.mkdir(parents=True)

    run_clean(tmp_path / "out")
    assert not work.exists()
    assert not logs.exists()
