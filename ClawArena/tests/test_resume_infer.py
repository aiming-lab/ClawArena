"""Tests for resume-infer logic."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from clawarena.core.infer import _find_completed_rounds, _resolve_infer_out_dir


class TestFindCompletedRounds:
    def test_empty_dir(self, tmp_path):
        """No results at all → everything incomplete."""
        completed, preloaded = _find_completed_rounds(tmp_path, "t1", ["r1", "r2"])
        assert completed == frozenset()
        assert preloaded == {}

    def test_partial_completion(self, tmp_path):
        """Only r1 written → r2 remains pending."""
        result = {"inline_score": {"passed": True}, "answer": {"text": "A"}}
        p = tmp_path / "t1" / "r1" / "infer_result.json"
        p.parent.mkdir(parents=True)
        p.write_text(json.dumps(result))

        completed, preloaded = _find_completed_rounds(tmp_path, "t1", ["r1", "r2"])
        assert completed == frozenset({"r1"})
        assert preloaded["r1"] == result
        assert "r2" not in preloaded

    def test_all_completed(self, tmp_path):
        """All rounds written → completed set equals all round ids."""
        for rid in ["r1", "r2", "r3"]:
            p = tmp_path / "t1" / rid / "infer_result.json"
            p.parent.mkdir(parents=True)
            p.write_text(json.dumps({"inline_score": {"passed": False}}))

        completed, preloaded = _find_completed_rounds(tmp_path, "t1", ["r1", "r2", "r3"])
        assert completed == frozenset({"r1", "r2", "r3"})
        assert len(preloaded) == 3

    def test_malformed_json_treated_as_incomplete(self, tmp_path):
        """Corrupt infer_result.json is treated as incomplete, not raised."""
        p = tmp_path / "t1" / "r1" / "infer_result.json"
        p.parent.mkdir(parents=True)
        p.write_text("not valid json{{{")

        completed, preloaded = _find_completed_rounds(tmp_path, "t1", ["r1"])
        assert completed == frozenset()
        assert preloaded == {}

    def test_only_requested_rounds_are_checked(self, tmp_path):
        """Files outside the round_ids list don't affect the result."""
        # r3 exists on disk but is not in the round list
        p = tmp_path / "t1" / "r3" / "infer_result.json"
        p.parent.mkdir(parents=True)
        p.write_text(json.dumps({"inline_score": {}}))

        completed, preloaded = _find_completed_rounds(tmp_path, "t1", ["r1", "r2"])
        assert completed == frozenset()
        assert preloaded == {}

    def test_returns_frozenset(self, tmp_path):
        """Return type is frozenset (hashable, immutable)."""
        completed, _ = _find_completed_rounds(tmp_path, "t1", [])
        assert isinstance(completed, frozenset)


class TestResolveInferOutDir:
    def test_flat_dir_unchanged(self, tmp_path):
        """No infer/ subdir → return as-is."""
        (tmp_path / "t1" / "r1").mkdir(parents=True)
        assert _resolve_infer_out_dir(tmp_path) == tmp_path

    def test_empty_infer_subdir_unchanged(self, tmp_path):
        """infer/ exists but is empty → return as-is."""
        (tmp_path / "infer").mkdir()
        assert _resolve_infer_out_dir(tmp_path) == tmp_path

    def test_hbench_run_layout_detected(self, tmp_path):
        """infer/ subdir with content → return infer/ path."""
        infer = tmp_path / "infer" / "t1" / "r1"
        infer.mkdir(parents=True)
        (infer / "infer_result.json").write_text("{}")
        assert _resolve_infer_out_dir(tmp_path) == tmp_path / "infer"

    def test_infer_subdir_with_scoring_sibling(self, tmp_path):
        """Typical clawarena-run layout has infer/, scoring/, report/ siblings."""
        (tmp_path / "infer" / "t1").mkdir(parents=True)
        (tmp_path / "infer" / "t1" / "dummy").touch()
        (tmp_path / "scoring").mkdir()
        (tmp_path / "report").mkdir()
        assert _resolve_infer_out_dir(tmp_path) == tmp_path / "infer"
