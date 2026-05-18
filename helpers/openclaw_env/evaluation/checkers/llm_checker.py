"""LLM-based fuzzy checker — semantic evaluation via Claude."""

from __future__ import annotations

import json
import os
import re
from typing import Any

from openclaw_env.core.observation import CheckResult
from openclaw_env.evaluation.evaluator import Evaluator


class LLMChecker(Evaluator):
    """Uses Claude to semantically judge whether a task criterion was satisfied.

    Unlike rule-based checkers (EffectChecker, OutputChecker …), LLMChecker
    handles open-ended criteria such as:
    - "The agent's reply was polite and on-topic"
    - "The agent found the correct email and extracted the right date"
    - "The follow-up task title is meaningfully related to the email subject"

    The checker calls the Anthropic API (``anthropic`` package) and returns a
    structured result. If the package is missing, the API call fails, or the
    ANTHROPIC_API_KEY is unset, the check fails gracefully without raising.

    Task spec example::

        {
            "type": "llm",
            "criterion": "The agent found an email about 'proposal' and created a
                          follow-up task whose title relates to the email subject.",
            "name": "email→task semantic check",
            "weight": 1.0,
            "model": "claude-haiku-4-5-20251001"
        }
    """

    DEFAULT_MODEL = "claude-haiku-4-5-20251001"

    def __init__(
        self,
        criterion: str,
        name: str = "",
        weight: float = 1.0,
        model: str = DEFAULT_MODEL,
        temperature: float = 0.0,
        max_tokens: int = 256,
    ) -> None:
        self.criterion = criterion
        self.name = name or f"llm:{criterion[:50]}"
        self.weight = weight
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    # ------------------------------------------------------------------ #
    # Evaluator interface                                                   #
    # ------------------------------------------------------------------ #

    def evaluate(
        self, env_state: dict[str, Any], task_data: dict[str, Any]
    ) -> CheckResult:
        try:
            return self._call_llm(env_state, task_data)
        except Exception as exc:
            return CheckResult(
                name=self.name,
                passed=False,
                score=0.0,
                weight=self.weight,
                message=f"LLM evaluation error: {exc}",
            )

    @classmethod
    def from_spec(cls, spec: dict[str, Any]) -> LLMChecker:
        return cls(
            criterion=spec["criterion"],
            name=spec.get("name", ""),
            weight=spec.get("weight", 1.0),
            model=spec.get("model", cls.DEFAULT_MODEL),
            temperature=spec.get("temperature", 0.0),
            max_tokens=spec.get("max_tokens", 256),
        )

    # ------------------------------------------------------------------ #
    # Internal                                                              #
    # ------------------------------------------------------------------ #

    def _call_llm(
        self, env_state: dict[str, Any], task_data: dict[str, Any]
    ) -> CheckResult:
        try:
            import anthropic
        except ImportError:
            return CheckResult(
                name=self.name,
                passed=False,
                score=0.0,
                weight=self.weight,
                message=(
                    "anthropic package not installed. "
                    "Run: pip install anthropic"
                ),
            )

        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            return CheckResult(
                name=self.name,
                passed=False,
                score=0.0,
                weight=self.weight,
                message="ANTHROPIC_API_KEY environment variable is not set.",
            )

        client = anthropic.Anthropic(api_key=api_key)
        prompt = _build_prompt(self.criterion, env_state, task_data)

        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}],
        )

        raw_text = response.content[0].text.strip()
        parsed = _parse_response(raw_text)

        return CheckResult(
            name=self.name,
            passed=parsed["passed"],
            score=float(parsed["score"]),
            weight=self.weight,
            message=parsed.get("reason", raw_text[:200]),
        )


# ------------------------------------------------------------------ #
# Prompt construction                                                   #
# ------------------------------------------------------------------ #

def _build_prompt(
    criterion: str,
    env_state: dict[str, Any],
    task_data: dict[str, Any],
) -> str:
    task_instruction = (
        env_state.get("task_instruction")
        or task_data.get("public", {}).get("instruction", "")
        or "(not provided)"
    )

    # Command history: last 8 steps
    history = env_state.get("command_history", [])[-8:]
    if history:
        history_lines = []
        for i, h in enumerate(history, 1):
            stdout_preview = (h.get("stdout") or "").strip()[:300]
            history_lines.append(
                f"  [{i}] $ {h.get('action', '')}\n"
                f"      exit={h.get('exit_code', '?')}  "
                f"stdout: {stdout_preview or '(empty)'}"
            )
        history_block = "\n".join(history_lines)
    else:
        history_block = "  (no commands recorded)"

    # Effects summary
    effects = env_state.get("effects", {})
    effect_lines = [
        f"  {k}: {len(v)} event(s)"
        for k, v in effects.items()
        if v
    ]
    effects_block = "\n".join(effect_lines) or "  (none)"

    last_stdout = (env_state.get("last_stdout") or "").strip()[:600]
    last_exit = env_state.get("last_exit_code", "?")

    return f"""You are an automated evaluator for an AI agent task.

## Task instruction given to the agent
{task_instruction}

## Agent command history
{history_block}

## Side effects produced during the episode
{effects_block}

## Final command output
Exit code: {last_exit}
{last_stdout or "(empty)"}

## Criterion to evaluate
{criterion}

## Your job
Decide whether the criterion above was satisfied based solely on the evidence
provided. Do not invent information not present in the evidence.

Respond with ONLY a JSON object in this exact format (no other text):
{{"passed": true_or_false, "score": 0.0_to_1.0, "reason": "one concise sentence"}}

Scoring guide:
  1.0 — criterion fully satisfied
  0.5 — partially satisfied (e.g., correct intent but wrong details)
  0.0 — not satisfied"""


# ------------------------------------------------------------------ #
# Response parsing                                                      #
# ------------------------------------------------------------------ #

def _parse_response(text: str) -> dict[str, Any]:
    """Parse LLM JSON response, with fallback for malformed output."""
    # Try strict parse first
    try:
        data = json.loads(text)
        return _normalise(data)
    except (json.JSONDecodeError, ValueError):
        pass

    # Extract embedded JSON object
    match = re.search(r"\{[^{}]+\}", text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group())
            return _normalise(data)
        except (json.JSONDecodeError, ValueError):
            pass

    # Last resort: keyword scan
    lower = text.lower()
    passed = "true" in lower and "false" not in lower
    return {
        "passed": passed,
        "score": 1.0 if passed else 0.0,
        "reason": text[:200],
    }


def _normalise(data: dict[str, Any]) -> dict[str, Any]:
    """Ensure the parsed dict has the expected fields and types."""
    return {
        "passed": bool(data.get("passed", False)),
        "score": max(0.0, min(1.0, float(data.get("score", 0.0)))),
        "reason": str(data.get("reason", "")),
    }
