"""Multi-choice question type implementation."""

from __future__ import annotations

import re
from typing import Any

from clawarena.core.types import TestContext
from clawarena.prompts import (
    CONTINUE_REMINDER, FORMAT_ERROR, MULTI_CHOICE_INSTRUCTION, UPDATE_NOTES,
    missed_option, wrong_option,
)

from .base import QuestionType
from .command_check import (
    append_pref_feedback,
    run_command_check,
    validate_pref_config,
)


def _get_eval(rr: dict) -> dict:
    return rr.get("eval", {})


def _get_options(rr: dict) -> dict:
    opts = _get_eval(rr).get("options")
    return opts if opts is not None else rr.get("options", {})


def _get_answer_raw(rr: dict) -> Any:
    ans = _get_eval(rr).get("answer")
    return ans if ans is not None else rr.get("answer", "")


def _get_pref(rr: dict) -> dict | None:
    pref = rr.get("pref")
    return pref if isinstance(pref, dict) else None


def _normalize_answer(answer: Any) -> set[str]:
    if isinstance(answer, list):
        result: set[str] = set()
        for item in answer:
            result.update(re.findall(r"[A-Za-z]", str(item)))
        return {l.upper() for l in result}
    if isinstance(answer, str):
        return {l.upper() for l in re.findall(r"[A-Za-z]", answer)}
    return set()


def _extract_bbox(text: str) -> set[str] | None:
    # Strip LaTeX math-mode wrappers \[...\] and \(...\) that some models emit
    cleaned = re.sub(r'\\\[|\\\]|\\\(|\\\)', '', text)
    # Normalize Unicode-corrupted \bbox: some models emit non-ASCII chars before "box{"
    # e.g. \్బbox{A,B} or \्बbox{A,B} — strip non-ASCII between \ and box{
    cleaned = re.sub(r'\\[^\x00-\x7F]*box\{', r'\\bbox{', cleaned)
    match = re.search(r"\\(?:bbox|boxed)\{([^}]*)\}", cleaned)
    if match:
        letters = re.findall(r"[A-Za-z]", match.group(1))
        if letters:
            return {l.upper() for l in letters}
    return None


def _calculate_metrics(
    answer: set[str] | None, ground: set[str], q_num: int,
) -> tuple[float, dict]:
    if answer is None or not ground:
        return 0, {}
    tp = len(answer & ground)
    fp = len(answer - ground)
    fn = len(ground - answer)
    exact_match = 1.0 if answer == ground else 0.0
    union = len(answer | ground)
    iou = tp / union if union else 0.0
    prec_d = tp + fp
    precision = tp / prec_d if prec_d else (1.0 if not ground else 0.0)
    rec_d = tp + fn
    recall = tp / rec_d if rec_d else 1.0
    f1_d = precision + recall
    f1 = 2 * precision * recall / f1_d if f1_d else 0.0
    score = 1.0 if exact_match else 0.0
    return score, {
        "iou": iou, "precision": precision, "recall": recall,
        "f1": f1, "exact_match": exact_match,
    }


class MultiChoice(QuestionType):

    @property
    def name(self) -> str:
        return "multi_choice"

    def format_query(self, round_record: dict, ctx: TestContext) -> str:
        question = round_record["question"]
        options = _get_options(round_record)
        if not options:
            return question
        lines: list[str] = []
        if round_record.get("update_ids"):
            lines.append(UPDATE_NOTES)
        lines.append(question)
        for letter in sorted(options.keys()):
            lines.append(f"{letter}. {options[letter]}")
        lines.append("")
        lines.append(MULTI_CHOICE_INSTRUCTION)
        return "\n".join(lines)

    def compute_inline_score(
        self, round_record: dict, answer_text: str, ctx: TestContext,
    ) -> dict:
        extracted = _extract_bbox(answer_text or "")
        correct_set = _normalize_answer(_get_answer_raw(round_record))
        passed = extracted is not None and bool(correct_set) and extracted == correct_set
        result = {
            "passed": passed,
            "type": "multi_choice",
            "format_valid": extracted is not None,
            "selected": sorted(extracted) if extracted is not None else [],
        }
        pref = _get_pref(round_record)
        if pref:
            pref_result = run_command_check(pref, ctx)
            result["pref_passed"] = pref_result["passed"]
        return result

    def build_feedback(
        self, round_record: dict, inline_score: dict, ctx: TestContext,
    ) -> str:
        if not inline_score.get("format_valid", True):
            text = FORMAT_ERROR
        else:
            correct = _normalize_answer(_get_answer_raw(round_record))
            selected = set(inline_score.get("selected", []))
            feedback_rec = round_record.get("feedback", {})
            if selected == correct:
                text = feedback_rec.get("correct", "")
            else:
                options_fb = feedback_rec.get("options", {})
                lines: list[str] = []
                for opt in sorted(correct - selected):
                    lines.append(missed_option(opt, options_fb.get(opt, "")))
                for opt in sorted(selected - correct):
                    lines.append(wrong_option(opt, options_fb.get(opt, "")))
                lines.append(CONTINUE_REMINDER)
                text = "\n".join(lines)

        return append_pref_feedback(text, _get_pref(round_record), inline_score.get("pref_passed", True))

    def validate_round(
        self, round_data: dict, scenario: str, eval_dir=None, workspace=None,
    ) -> tuple[list[str], list[str]]:
        errors: list[str] = []
        warnings: list[str] = []
        rid = round_data.get("id", "unknown")
        prefix = f"{scenario}: round '{rid}'"

        _REQUIRED = {"id", "type", "question", "update_ids", "eval", "feedback"}
        _OPTIONAL = {"pref"}
        _ALLOWED = _REQUIRED | _OPTIONAL
        _LEGACY = {"options", "answer"}

        extra = set(round_data.keys()) - _ALLOWED
        if extra:
            errors.append(f"{prefix}: unexpected top-level fields: {sorted(extra)}")
        for f in _REQUIRED:
            if f not in round_data:
                errors.append(f"{prefix}: missing required field '{f}'")
        for f in _LEGACY & set(round_data.keys()):
            errors.append(f"{prefix}: '{f}' must be inside 'eval', not at top level")

        eval_cfg = round_data.get("eval")
        option_keys: set[str] = set()
        if eval_cfg is not None:
            if not isinstance(eval_cfg, dict):
                errors.append(f"{prefix}: 'eval' must be a dict")
            else:
                extra_eval = set(eval_cfg.keys()) - {"options", "answer"}
                if extra_eval:
                    errors.append(f"{prefix}: unexpected eval fields: {sorted(extra_eval)}")
                options = eval_cfg.get("options")
                if not isinstance(options, dict):
                    errors.append(f"{prefix}: eval.options must be a dict")
                else:
                    option_keys = set(options.keys())
                    for k, v in options.items():
                        if not (isinstance(k, str) and len(k) == 1 and k.isupper()):
                            errors.append(f"{prefix}: eval.options key '{k}' must be a single uppercase letter")
                        if not isinstance(v, str):
                            errors.append(f"{prefix}: eval.options['{k}'] must be a string")
                answer = eval_cfg.get("answer")
                if answer is None:
                    errors.append(f"{prefix}: eval.answer is required")
                elif not isinstance(answer, list):
                    errors.append(f"{prefix}: eval.answer must be a list")

        feedback = round_data.get("feedback")
        if feedback is not None:
            if not isinstance(feedback, dict):
                errors.append(f"{prefix}: 'feedback' must be a dict")
            else:
                extra_fb = set(feedback.keys()) - {"correct", "options"}
                if extra_fb:
                    errors.append(f"{prefix}: unexpected feedback fields: {sorted(extra_fb)}")
                if "correct" not in feedback:
                    errors.append(f"{prefix}: feedback.correct is required")
                elif not isinstance(feedback["correct"], str):
                    errors.append(f"{prefix}: feedback.correct must be a string")
                fb_opts = feedback.get("options")
                if not isinstance(fb_opts, dict):
                    errors.append(f"{prefix}: feedback.options must be a dict")
                elif option_keys:
                    missing = option_keys - set(fb_opts.keys())
                    if missing:
                        errors.append(f"{prefix}: feedback.options missing keys for: {sorted(missing)}")
                    extra_fb_opt = set(fb_opts.keys()) - option_keys
                    if extra_fb_opt:
                        errors.append(f"{prefix}: feedback.options has keys not in eval.options: {sorted(extra_fb_opt)}")

        pref_errors, pref_warnings = validate_pref_config(
            round_data.get("pref"), scenario, rid, "multi_choice", eval_dir, workspace
        )
        errors.extend(pref_errors)
        warnings.extend(pref_warnings)
        return errors, warnings

    def score(
        self, answer_text: str, round_record: dict, ctx: TestContext,
        infer_result: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        extracted = _extract_bbox(answer_text) if answer_text else None
        correct_raw = _get_answer_raw(round_record)
        correct_set = _normalize_answer(correct_raw) if correct_raw else None
        q_num = len(_get_options(round_record))
        sc, metrics = _calculate_metrics(extracted, correct_set, q_num)
        return {
            "extracted_answer": sorted(extracted) if extracted else None,
            "correct_answer": sorted(correct_set) if correct_set else None,
            "score": sc,
            "metrics": metrics,
        }
