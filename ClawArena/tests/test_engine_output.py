"""Tests for CLI engine stdout normalization."""

from clawarena.core.provider import ModelConfig
from clawarena.engines.output_sanitizer import detect_provider_error, normalize_agent_output


def test_normalize_openclaw_rate_limit_as_error():
    answer, error = normalize_agent_output("⚠️ API rate limit reached. Please try again later.")
    assert answer == ""
    assert error is not None
    assert "rate limit" in error.lower()


def test_normalize_nanobot_strips_prelude():
    raw = """
Using config:
/tmp/nanobot/config.json
  Created HEARTBEAT.md

🐈 nanobot
\\bbox{A,B}
"""
    answer, error = normalize_agent_output(raw, framework="nanobot")
    assert error is None
    assert answer == "\\bbox{A,B}"


def test_normalize_nanobot_error_body_as_failed():
    raw = """
Using config:
/tmp/nanobot/config.json

🐈 nanobot
Error: {
  "error": {
    "message": "Too Many Requests"
  }
}
"""
    answer, error = normalize_agent_output(raw, framework="nanobot")
    assert answer == ""
    assert error is not None
    assert "too many requests" in error.lower()


def test_normalize_picoclaw_strips_banner():
    raw = (
        "\x1b[1;38;2;62;93;185m██████╗ ██╗ ██████╗\n"
        "\x1b[1;38;2;62;93;185m██╔══██╗██║██╔════╝\n"
        "\x1b[0m\n\n"
        "🦞 \\bbox{B,D,E}\n"
    )
    answer, error = normalize_agent_output(raw, framework="picoclaw")
    assert error is None
    assert answer == "\\bbox{B,D,E}"


def test_detect_provider_invalid_model_error():
    error = detect_provider_error(
        "400 {'error': '/chat/completions: Invalid model name passed in model=claude-opus-4.6'}"
    )
    assert error is not None


def test_model_config_normalizes_legacy_claude_alias():
    model = ModelConfig(model_id="claude-opus-4-6", provider="anthropic")
    assert model.model_id == "claude-opus-4.6"
