"""Tests for question types — multi_choice and exec_check."""

import json
import pytest
from pathlib import Path

from clawarena.core.types import TestContext, WorkCopy
from clawarena.qtypes.multi_choice import (
    MultiChoice, _extract_bbox, _normalize_answer, _calculate_metrics,
)
from clawarena.qtypes.command_check import expand_placeholders
from clawarena.qtypes.exec_check import ExecCheck
from clawarena.qtypes.registry import get_qtype, registered_types


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

def test_registry_types():
    types = registered_types()
    assert "multi_choice" in types
    assert "exec_check" in types


def test_get_qtype_unknown():
    with pytest.raises(ValueError, match="Unknown"):
        get_qtype("nonexistent_type")


# ---------------------------------------------------------------------------
# MultiChoice helpers
# ---------------------------------------------------------------------------

def test_extract_bbox_single():
    assert _extract_bbox(r"The answer is \bbox{A}") == {"A"}


def test_extract_bbox_multiple():
    assert _extract_bbox(r"\bbox{A,C,D}") == {"A", "C", "D"}


def test_extract_bbox_boxed():
    assert _extract_bbox(r"\boxed{B}") == {"B"}


def test_extract_bbox_none():
    assert _extract_bbox("No answer here") is None


def test_normalize_answer_list():
    assert _normalize_answer(["A", "C"]) == {"A", "C"}


def test_normalize_answer_string():
    assert _normalize_answer("A,B") == {"A", "B"}


def test_calculate_metrics_exact():
    score, m = _calculate_metrics({"A", "C"}, {"A", "C"}, 5)
    assert m["exact_match"] == 1.0
    assert m["precision"] == 1.0
    assert m["recall"] == 1.0
    assert score == 1.0


def test_calculate_metrics_partial():
    score, m = _calculate_metrics({"A"}, {"A", "C"}, 5)
    assert m["exact_match"] == 0.0
    assert m["recall"] == 0.5
    assert score == 0.0


def test_calculate_metrics_none():
    score, m = _calculate_metrics(None, {"A"}, 5)
    assert score == 0
    assert m == {}


# ---------------------------------------------------------------------------
# MultiChoice pipeline
# ---------------------------------------------------------------------------

class TestMultiChoice:

    def setup_method(self):
        self.mc = MultiChoice()
        self.ctx = TestContext(framework="openclaw", test_id="t1")
        self.round_record = {
            "id": "r1",
            "type": "multi_choice",
            "question": "Which are correct?",
            "update_ids": [],
            "eval": {
                "options": {"A": "Opt A", "B": "Opt B", "C": "Opt C"},
                "answer": ["A", "C"],
            },
            "feedback": {
                "correct": "Well done!",
                "options": {
                    "A": "A is correct.",
                    "B": "B is wrong because...",
                    "C": "C is correct.",
                },
            },
        }

    def test_format_query(self):
        q = self.mc.format_query(self.round_record, self.ctx)
        assert "Which are correct?" in q
        assert "A. Opt A" in q
        assert r"\bbox{X,Y,...}" in q

    def test_format_query_with_update(self):
        rr = {**self.round_record, "update_ids": ["u1"]}
        q = self.mc.format_query(rr, self.ctx)
        assert "updated" in q.lower()

    def test_compute_inline_score_correct(self):
        score = self.mc.compute_inline_score(
            self.round_record, r"I think \bbox{A,C}", self.ctx,
        )
        assert score["passed"] is True
        assert score["format_valid"] is True
        assert sorted(score["selected"]) == ["A", "C"]

    def test_compute_inline_score_wrong(self):
        score = self.mc.compute_inline_score(
            self.round_record, r"\bbox{B}", self.ctx,
        )
        assert score["passed"] is False

    def test_compute_inline_score_no_bbox(self):
        score = self.mc.compute_inline_score(
            self.round_record, "I think A and C", self.ctx,
        )
        assert score["passed"] is False
        assert score["format_valid"] is False

    def test_compute_inline_score_pref_passed(self, tmp_path):
        rr = {
            **self.round_record,
            "pref": {
                "command": "echo pref_ok",
                "expect_exit": 0,
                "feedback": {"correct": "", "incorrect": "P1 violated."},
            },
        }
        ctx = TestContext(framework="openclaw", test_id="t1", workspace=tmp_path)
        score = self.mc.compute_inline_score(rr, r"\bbox{A,C}", ctx)
        assert score["passed"] is True
        assert score["pref_passed"] is True

    def test_compute_inline_score_ignores_legacy_exec_check(self, tmp_path):
        rr = {
            **self.round_record,
            "exec_check": {
                "command": "exit 1",
                "expect_exit": 0,
                "feedback": {"correct": "", "incorrect": "legacy"},
            },
        }
        ctx = TestContext(framework="openclaw", test_id="t1", workspace=tmp_path)
        score = self.mc.compute_inline_score(rr, r"\bbox{A,C}", ctx)
        assert score["passed"] is True
        assert "pref_passed" not in score

    def test_build_feedback_correct(self):
        inline = {"passed": True, "format_valid": True, "selected": ["A", "C"]}
        fb = self.mc.build_feedback(self.round_record, inline, self.ctx)
        assert fb == "Well done!"

    def test_build_feedback_wrong(self):
        inline = {"passed": False, "format_valid": True, "selected": ["B"]}
        fb = self.mc.build_feedback(self.round_record, inline, self.ctx)
        assert "missed option a" in fb.lower() or "missed option c" in fb.lower()

    def test_build_feedback_format_error(self):
        inline = {"passed": False, "format_valid": False, "selected": []}
        fb = self.mc.build_feedback(self.round_record, inline, self.ctx)
        assert "bbox" in fb.lower()

    def test_build_feedback_pref_appended_on_failure(self, tmp_path):
        rr = {
            **self.round_record,
            "pref": {
                "command": "exit 1",
                "expect_exit": 0,
                "feedback": {"correct": "", "incorrect": "P1 violated."},
            },
        }
        ctx = TestContext(framework="openclaw", test_id="t1", workspace=tmp_path)
        inline = {
            "passed": True,
            "format_valid": True,
            "selected": ["A", "C"],
            "pref_passed": False,
        }
        fb = self.mc.build_feedback(rr, inline, ctx)
        assert "Well done!" in fb
        assert "P1 violated." in fb

    def test_build_feedback_pref_correct_empty_not_appended(self, tmp_path):
        rr = {
            **self.round_record,
            "pref": {
                "command": "echo pref_ok",
                "expect_exit": 0,
                "feedback": {"correct": "", "incorrect": "P1 violated."},
            },
        }
        ctx = TestContext(framework="openclaw", test_id="t1", workspace=tmp_path)
        inline = {
            "passed": True,
            "format_valid": True,
            "selected": ["A", "C"],
            "pref_passed": True,
        }
        fb = self.mc.build_feedback(rr, inline, ctx)
        assert fb == "Well done!"

    def test_score(self):
        result = self.mc.score(r"\bbox{A,C}", self.round_record, self.ctx)
        assert result["score"] == 1.0
        assert result["extracted_answer"] == ["A", "C"]
        assert result["correct_answer"] == ["A", "C"]

    def test_score_partial(self):
        result = self.mc.score(r"\bbox{A}", self.round_record, self.ctx)
        assert result["score"] == 0.0

    def test_score_empty(self):
        result = self.mc.score("", self.round_record, self.ctx)
        assert result["score"] == 0

    def test_validate_round_ok(self):
        errs, warns = self.mc.validate_round(self.round_record, "test_s1")
        assert errs == []

    def test_validate_round_missing_answer(self):
        rr = {"id": "r1", "type": "multi_choice", "question": "?"}
        errs, warns = self.mc.validate_round(rr, "test_s1")
        # Strict schema: missing required fields surface as errors, not warnings.
        assert len(errs) > 0

    def test_validate_round_pref_ok(self):
        rr = {
            **self.round_record,
            "pref": {
                "command": "echo pref",
                "feedback": {"correct": "", "incorrect": "violated."},
            },
        }
        errs, warns = self.mc.validate_round(rr, "test_s1")
        assert errs == []
        assert warns == []

    def test_validate_round_pref_missing_command(self):
        rr = {
            **self.round_record,
            "pref": {
                "feedback": {"correct": "", "incorrect": "violated."},
            },
        }
        errs, _ = self.mc.validate_round(rr, "test_s1")
        assert any("pref.command" in e for e in errs)

    def test_validate_round_pref_feedback_not_dict(self):
        rr = {
            **self.round_record,
            "pref": {
                "command": "echo pref",
                "feedback": "violated",
            },
        }
        errs, _ = self.mc.validate_round(rr, "test_s1")
        assert any("pref.feedback" in e for e in errs)

    def test_validate_round_pref_feedback_incorrect_must_be_string(self):
        rr = {
            **self.round_record,
            "pref": {
                "command": "echo pref",
                "feedback": {"correct": "", "incorrect": 1},
            },
        }
        errs, _ = self.mc.validate_round(rr, "test_s1")
        assert any("pref.feedback.incorrect" in e for e in errs)


# ---------------------------------------------------------------------------
# expand_placeholders
# ---------------------------------------------------------------------------

class TestExpandPlaceholders:

    def test_known_vars(self, tmp_path):
        ctx = TestContext(
            framework="test", test_id="t1",
            workspace=tmp_path, eval_dir=tmp_path / "eval",
        )
        result = expand_placeholders("cd ${workspace} && ls ${eval_dir}", ctx)
        assert str(tmp_path) in result
        assert str(tmp_path / "eval") in result

    def test_unknown_var_preserved(self):
        ctx = TestContext(framework="test", test_id="t1")
        result = expand_placeholders("echo ${API_KEY}", ctx)
        assert result == "echo ${API_KEY}"

    def test_dollar_var_untouched(self, tmp_path):
        ctx = TestContext(framework="test", test_id="t1", workspace=tmp_path)
        result = expand_placeholders("echo $HOME ${workspace}", ctx)
        assert "$HOME" in result
        assert str(tmp_path) in result

    def test_subshell_untouched(self, tmp_path):
        ctx = TestContext(framework="test", test_id="t1", workspace=tmp_path)
        result = expand_placeholders("echo $(date) ${workspace}", ctx)
        assert "$(date)" in result

    def test_none_value_preserved(self):
        ctx = TestContext(framework="test", test_id="t1")
        # workspace not set → None → preserve literal
        result = expand_placeholders("cd ${workspace}", ctx)
        assert result == "cd ${workspace}"

    def test_state_dir(self, tmp_path):
        wc = WorkCopy(
            state_dir=tmp_path / "state",
            config_path=None,
            project_root=tmp_path,
        )
        ctx = TestContext(framework="test", test_id="t1", work_copy=wc)
        result = expand_placeholders("ls ${state_dir}", ctx)
        assert str(tmp_path / "state") in result

    def test_shlex_quoting(self, tmp_path):
        # Create a path with spaces to verify quoting
        space_path = tmp_path / "path with spaces"
        space_path.mkdir()
        ctx = TestContext(framework="test", test_id="t1", workspace=space_path)
        result = expand_placeholders("cd ${workspace}", ctx)
        # shlex.quote wraps in single quotes for paths with spaces
        assert "'" in result or "\\" in result


# ---------------------------------------------------------------------------
# ExecCheck
# ---------------------------------------------------------------------------

class TestExecCheck:

    def setup_method(self):
        self.ec = ExecCheck()
        self.ctx = TestContext(framework="openclaw", test_id="t1")

    def test_format_query(self):
        rr = {"id": "r1", "question": "Fix the bug", "type": "exec_check"}
        q = self.ec.format_query(rr, self.ctx)
        assert q == "Fix the bug"

    def test_compute_inline_score_no_workspace(self):
        rr = {"id": "r1", "eval": {"command": "echo ok"}}
        # No workspace in ctx, but command doesn't use ${workspace}
        score = self.ec.compute_inline_score(rr, "", self.ctx)
        assert score["passed"] is True

    def test_compute_inline_score_with_workspace(self, tmp_path):
        rr = {"id": "r1", "eval": {"command": "echo hello", "expect_exit": 0}}
        ctx = TestContext(framework="openclaw", test_id="t1", workspace=tmp_path)
        score = self.ec.compute_inline_score(rr, "", ctx)
        assert score["passed"] is True
        assert "hello" in score["stdout"]

    def test_compute_inline_score_expect_stdout(self, tmp_path):
        rr = {"id": "r1", "eval": {
            "command": "echo hello world",
            "expect_exit": 0,
            "expect_stdout": "hello",
        }}
        ctx = TestContext(framework="openclaw", test_id="t1", workspace=tmp_path)
        score = self.ec.compute_inline_score(rr, "", ctx)
        assert score["passed"] is True

    def test_compute_inline_score_expect_stdout_regex(self, tmp_path):
        rr = {"id": "r1", "eval": {
            "command": "echo 'result: 42'",
            "expect_exit": 0,
            "expect_stdout": r"result:\s+\d+",
            "expect_stdout_regex": True,
        }}
        ctx = TestContext(framework="openclaw", test_id="t1", workspace=tmp_path)
        score = self.ec.compute_inline_score(rr, "", ctx)
        assert score["passed"] is True

    def test_placeholder_in_command(self, tmp_path):
        # Create a test file in workspace
        (tmp_path / "hello.txt").write_text("world")
        rr = {"id": "r1", "eval": {
            "command": "cat ${workspace}/hello.txt",
            "expect_exit": 0,
            "expect_stdout": "world",
        }}
        ctx = TestContext(framework="openclaw", test_id="t1", workspace=tmp_path)
        score = self.ec.compute_inline_score(rr, "", ctx)
        assert score["passed"] is True

    def test_eval_dir_placeholder(self, tmp_path):
        scripts_dir = tmp_path / "eval" / "scripts"
        scripts_dir.mkdir(parents=True)
        script = scripts_dir / "check.py"
        script.write_text("import sys; print('PASSED'); sys.exit(0)")
        rr = {"id": "r1", "eval": {
            "command": "python ${eval_dir}/scripts/check.py",
            "expect_exit": 0,
            "expect_stdout": "PASSED",
        }}
        ctx = TestContext(
            framework="openclaw", test_id="t1",
            workspace=tmp_path, eval_dir=tmp_path / "eval",
        )
        score = self.ec.compute_inline_score(rr, "", ctx)
        assert score["passed"] is True

    def test_score_from_inline(self):
        infer_result = {"inline_score": {"passed": True}}
        result = self.ec.score("", {}, self.ctx, infer_result=infer_result)
        assert result["score"] == 1.0

    def test_score_from_inline_failed(self):
        infer_result = {"inline_score": {"passed": False}}
        result = self.ec.score("", {}, self.ctx, infer_result=infer_result)
        assert result["score"] == 0.0

    def test_validate_round_ok(self):
        rr = {
            "id": "r1", "type": "exec_check",
            "question": "Run the check",
            "update_ids": [],
            "eval": {"command": "echo ok"},
            "feedback": {"correct": "good", "incorrect": "bad"},
        }
        errs, warns = self.ec.validate_round(rr, "test")
        assert errs == []

    def test_validate_round_missing_command(self):
        rr = {
            "id": "r1", "type": "exec_check",
            "eval": {},
            "feedback": {"correct": "ok", "incorrect": "bad"},
        }
        errs, _ = self.ec.validate_round(rr, "test")
        assert any("command" in e for e in errs)

    def test_validate_round_empty_feedback_errors(self):
        rr = {
            "id": "r1", "type": "exec_check",
            "question": "Run the check",
            "update_ids": [],
            "eval": {"command": "echo ok"},
            "feedback": {},
        }
        errs, _ = self.ec.validate_round(rr, "test")
        # Strict schema: feedback must carry both 'correct' and 'incorrect'.
        assert any("feedback.correct" in e for e in errs)
        assert any("feedback.incorrect" in e for e in errs)

    def test_build_feedback_correct(self):
        rr = {"feedback": {"correct": "Well done!", "incorrect": "Try again."}}
        inline = {"passed": True}
        fb = self.ec.build_feedback(rr, inline, self.ctx)
        assert fb == "Well done!"

    def test_build_feedback_incorrect(self):
        rr = {"feedback": {"correct": "Well done!", "incorrect": "Try again."}}
        inline = {"passed": False}
        fb = self.ec.build_feedback(rr, inline, self.ctx)
        assert "Try again." in fb

    def test_timeout(self, tmp_path):
        rr = {"id": "r1", "eval": {
            "command": "sleep 10",
            "timeout": 1,
        }}
        ctx = TestContext(framework="openclaw", test_id="t1", workspace=tmp_path)
        score = self.ec.compute_inline_score(rr, "", ctx)
        assert score["passed"] is False
        assert "Timeout" in score["stderr"]

    # ------------------------------------------------------------------
    # pref field
    # ------------------------------------------------------------------

    def test_pref_passed(self, tmp_path):
        rr = {
            "id": "r1",
            "eval": {"command": "echo ok"},
            "feedback": {"correct": "good", "incorrect": "bad"},
            "pref": {
                "command": "echo pref_ok",
                "expect_exit": 0,
                "feedback": {"correct": "", "incorrect": "P1 violated."},
            },
        }
        ctx = TestContext(framework="openclaw", test_id="t1", workspace=tmp_path)
        score = self.ec.compute_inline_score(rr, "", ctx)
        assert score["passed"] is True
        assert score["pref_passed"] is True

    def test_pref_failed_does_not_affect_score(self, tmp_path):
        rr = {
            "id": "r1",
            "eval": {"command": "echo ok"},
            "feedback": {"correct": "good", "incorrect": "bad"},
            "pref": {
                "command": "exit 1",
                "expect_exit": 0,
                "feedback": {"correct": "", "incorrect": "P1 violated."},
            },
        }
        ctx = TestContext(framework="openclaw", test_id="t1", workspace=tmp_path)
        inline = self.ec.compute_inline_score(rr, "", ctx)
        assert inline["passed"] is True
        assert inline["pref_passed"] is False
        # score only reads inline["passed"], so pref failure must not affect it
        infer_result = {"inline_score": inline}
        result = self.ec.score("", rr, ctx, infer_result=infer_result)
        assert result["score"] == 1.0

    def test_pref_feedback_appended(self, tmp_path):
        rr = {
            "id": "r1",
            "eval": {"command": "echo ok"},
            "feedback": {"correct": "good", "incorrect": "bad"},
            "pref": {
                "command": "exit 1",
                "expect_exit": 0,
                "feedback": {"correct": "", "incorrect": "P1 violated."},
            },
        }
        ctx = TestContext(framework="openclaw", test_id="t1", workspace=tmp_path)
        inline = {"passed": True, "pref_passed": False}
        fb = self.ec.build_feedback(rr, inline, ctx)
        assert "good" in fb
        assert "P1 violated." in fb

    def test_pref_feedback_correct_empty(self, tmp_path):
        rr = {
            "id": "r1",
            "eval": {"command": "echo ok"},
            "feedback": {"correct": "good", "incorrect": "bad"},
            "pref": {
                "command": "echo ok",
                "expect_exit": 0,
                "feedback": {"correct": "", "incorrect": "P1 violated."},
            },
        }
        ctx = TestContext(framework="openclaw", test_id="t1", workspace=tmp_path)
        inline = {"passed": True, "pref_passed": True}
        fb = self.ec.build_feedback(rr, inline, ctx)
        assert fb == "good"

    def test_validate_pref_ok(self):
        rr = {
            "id": "r1", "type": "exec_check",
            "question": "Run the check",
            "update_ids": [],
            "eval": {"command": "echo ok"},
            "feedback": {"correct": "good", "incorrect": "bad"},
            "pref": {
                "command": "echo pref",
                "feedback": {"correct": "", "incorrect": "violated."},
            },
        }
        errs, _ = self.ec.validate_round(rr, "test")
        assert errs == []

    def test_validate_pref_missing_command(self):
        rr = {
            "id": "r1", "type": "exec_check",
            "eval": {"command": "echo ok"},
            "feedback": {"correct": "good", "incorrect": "bad"},
            "pref": {
                "feedback": {"correct": "", "incorrect": "violated."},
            },
        }
        errs, _ = self.ec.validate_round(rr, "test")
        assert any("pref.command" in e for e in errs)

    def test_validate_pref_partial_feedback_ok(self):
        rr = {
            "id": "r1", "type": "exec_check",
            "question": "Run the check",
            "update_ids": [],
            "eval": {"command": "echo ok"},
            "feedback": {"correct": "good", "incorrect": "bad"},
            "pref": {
                "command": "echo pref",
                "feedback": {"correct": ""},
            },
        }
        errs, _ = self.ec.validate_round(rr, "test")
        assert errs == []
