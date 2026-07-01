"""Exec-check question type implementation."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

from clawarena.core.types import TestContext
from clawarena.prompts import FILE_CHECK_INCORRECT_SUFFIX

from .base import QuestionType
from .command_check import (
    append_pref_feedback,
    check_eval_dir_files,
    check_workspace_files,
    run_command_check,
    validate_pref_config,
    workspace_check_enabled,
)


class ExecCheck(QuestionType):

    @property
    def name(self) -> str:
        return "exec_check"

    def format_query(self, round_record: dict, ctx: TestContext) -> str:
        return round_record["question"]

    def compute_inline_score(
        self, round_record: dict, answer_text: str, ctx: TestContext,
    ) -> dict:
        eval_cfg = round_record.get("eval", {})
        result = run_command_check(eval_cfg, ctx)
        pref = round_record.get("pref")
        if pref:
            pref_result = run_command_check(pref, ctx)
            result["pref_passed"] = pref_result["passed"]
        return result

    def build_feedback(
        self, round_record: dict, inline_score: dict, ctx: TestContext,
    ) -> str:
        feedback_rec = round_record.get("feedback", {})
        passed = inline_score.get("passed", False)
        text = feedback_rec.get("correct" if passed else "incorrect", "")
        if not passed and text:
            text = f"{text}\n{FILE_CHECK_INCORRECT_SUFFIX}"
        return append_pref_feedback(text, round_record.get("pref"), inline_score.get("pref_passed", True))

    def validate_round(
        self, round_data: dict, scenario: str,
        eval_dir: Path | None = None,
        workspace: Path | None = None,
    ) -> tuple[list[str], list[str]]:
        errors: list[str] = []
        warnings: list[str] = []
        rid = round_data.get("id", "unknown")
        prefix = f"{scenario}: round '{rid}'"

        _REQUIRED = {"id", "type", "question", "update_ids", "eval", "feedback"}
        _OPTIONAL = {"pref"}
        _ALLOWED = _REQUIRED | _OPTIONAL

        extra = set(round_data.keys()) - _ALLOWED
        if extra:
            errors.append(f"{prefix}: unexpected top-level fields: {sorted(extra)}")
        for f in _REQUIRED:
            if f not in round_data:
                errors.append(f"{prefix}: missing required field '{f}'")

        _EVAL_REQUIRED = {"command"}
        _EVAL_OPTIONAL = {"expect_exit", "timeout", "expect_stdout", "expect_stdout_regex"}
        _EVAL_ALLOWED = _EVAL_REQUIRED | _EVAL_OPTIONAL

        eval_cfg = round_data.get("eval")
        command = ""
        if eval_cfg is not None:
            if not isinstance(eval_cfg, dict):
                errors.append(f"{prefix}: 'eval' must be a dict")
            else:
                extra_eval = set(eval_cfg.keys()) - _EVAL_ALLOWED
                if extra_eval:
                    errors.append(f"{prefix}: unexpected eval fields: {sorted(extra_eval)}")
                command = eval_cfg.get("command", "")
                if not isinstance(command, str) or not command:
                    errors.append(f"{prefix}: eval.command must be a non-empty string")
                expect_exit = eval_cfg.get("expect_exit")
                if expect_exit is not None and not isinstance(expect_exit, int):
                    errors.append(f"{prefix}: eval.expect_exit must be an integer")
                timeout = eval_cfg.get("timeout")
                if timeout is not None and not isinstance(timeout, (int, float)):
                    errors.append(f"{prefix}: eval.timeout must be a number")
                expect_stdout = eval_cfg.get("expect_stdout")
                if expect_stdout is not None and not isinstance(expect_stdout, str):
                    errors.append(f"{prefix}: eval.expect_stdout must be a string or null")
                expect_stdout_regex = eval_cfg.get("expect_stdout_regex")
                if expect_stdout_regex is not None and not isinstance(expect_stdout_regex, bool):
                    errors.append(f"{prefix}: eval.expect_stdout_regex must be a boolean")

        feedback = round_data.get("feedback")
        if feedback is not None:
            if not isinstance(feedback, dict):
                errors.append(f"{prefix}: 'feedback' must be a dict")
            else:
                extra_fb = set(feedback.keys()) - {"correct", "incorrect"}
                if extra_fb:
                    errors.append(f"{prefix}: unexpected feedback fields: {sorted(extra_fb)}")
                for key in ("correct", "incorrect"):
                    if key not in feedback:
                        errors.append(f"{prefix}: feedback.{key} is required")
                    elif not isinstance(feedback[key], str):
                        errors.append(f"{prefix}: feedback.{key} must be a string")

        pref = round_data.get("pref")
        pref_errors, pref_warnings = validate_pref_config(
            pref, scenario, rid, "exec_check", eval_dir, workspace
        )
        errors.extend(pref_errors)
        warnings.extend(pref_warnings)

        commands = [command] if isinstance(command, str) and command else []
        if isinstance(pref, dict):
            pc = pref.get("command", "")
            if isinstance(pc, str) and pc:
                commands.append(pc)

        if eval_dir is not None:
            for cmd in commands:
                errors.extend(check_eval_dir_files(cmd, eval_dir, scenario, prefix))

        if workspace is not None and workspace_check_enabled():
            for cmd in commands:
                warnings.extend(check_workspace_files(cmd, workspace, prefix))

        return errors, warnings

    def score(
        self, answer_text: str, round_record: dict, ctx: TestContext,
        infer_result: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        inline = (infer_result or {}).get("inline_score", {})
        passed = inline.get("passed", False)
        round_id = round_record.get("id", "?")
        logger.debug("exec_check %s: using cached inline_score (passed=%s)", round_id, passed)
        return {
            "extracted_answer": None,
            "correct_answer": None,
            "score": 1.0 if passed else 0.0,
            "metrics": {"passed": passed},
        }

    _run_command = staticmethod(run_command_check)
