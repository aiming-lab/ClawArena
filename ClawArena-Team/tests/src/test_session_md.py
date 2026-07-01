"""session_md.render_session_md 渲染规则覆盖。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from clawarena_team.persistence.session_md import (
    MAX_INLINE_CHARS,
    _truncate,
    render_session_md,
)


@dataclass
class _Turn:
    role: str
    content: str = ""
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    tool_call_id: str | None = None
    system_reminders: list[str] = field(default_factory=list)


def test_truncate_above_limit():
    s = "x" * (MAX_INLINE_CHARS + 50)
    out = _truncate(s)
    assert out.startswith("x" * MAX_INLINE_CHARS)
    assert "[truncated 50 chars]" in out


def test_truncate_below_limit_unchanged():
    s = "hello"
    assert _truncate(s) == "hello"


def test_system_prompt_not_truncated():
    """system prompt 即使超长也不截断。"""
    long_prompt = "S" * (MAX_INLINE_CHARS * 3)
    md = render_session_md(
        owner="sub_x",
        turns=[_Turn(role="system", content=long_prompt)],
        system_prompt=long_prompt,
    )
    assert long_prompt in md
    assert "[truncated" not in md  # system 段不应被截断


def test_assistant_content_truncated():
    long_content = "A" * (MAX_INLINE_CHARS + 100)
    md = render_session_md(
        owner="main",
        turns=[_Turn(role="assistant", content=long_content)],
    )
    assert "A" * MAX_INLINE_CHARS in md
    assert "[truncated 100 chars]" in md


def test_tool_call_arguments_truncated():
    long_val = "B" * (MAX_INLINE_CHARS + 50)
    md = render_session_md(
        owner="main",
        turns=[
            _Turn(
                role="assistant",
                content="",
                tool_calls=[
                    {"id": "t1", "name": "Read", "arguments": {"file_path": long_val}}
                ],
            )
        ],
    )
    assert "Tool Call: `Read`" in md
    assert "file_path" in md
    assert "[truncated 50 chars]" in md


def test_tool_result_content_truncated():
    long_result = "R" * (MAX_INLINE_CHARS + 25)
    md = render_session_md(
        owner="main",
        turns=[_Turn(role="tool_result", content=long_result, tool_call_id="t1")],
    )
    assert "tool_call_id" in md
    assert "[truncated 25 chars]" in md


def test_system_role_not_in_timeline():
    md = render_session_md(
        owner="main",
        turns=[
            _Turn(role="system", content="ignored"),
            _Turn(role="user", content="hi"),
        ],
        system_prompt="sp",
    )
    # 主时间线只应有一个 Turn
    assert md.count("## Turn 1") == 1
    assert "## Turn 2" not in md


def test_header_meta_renders():
    md = render_session_md(
        owner="main",
        turns=[_Turn(role="user", content="hi")],
        header_meta={"model_id": "m1", "provider": "openai"},
    )
    assert "**model_id**" in md
    assert "**provider**" in md


def test_empty_turns_renders_placeholder():
    md = render_session_md(owner="main", turns=[])
    assert "(no turns recorded)" in md
