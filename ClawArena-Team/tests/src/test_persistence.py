from __future__ import annotations

from pathlib import Path

from clawarena_team.agent.harness import HarnessTurn
from clawarena_team.persistence import read_session_jsonl, write_session_jsonl


def test_roundtrip(tmp_path: Path):
    turns = [
        HarnessTurn(role="system", content="sys"),
        HarnessTurn(role="user", content="hi", is_real_user_question=True),
        HarnessTurn(role="assistant", content="hello"),
    ]
    p = tmp_path / "main.jsonl"
    write_session_jsonl(p, turns, owner="main")
    rows = read_session_jsonl(p)
    assert rows[0]["type"] == "system_meta"
    assert rows[1]["role"] == "system"
    assert any(r.get("is_real_user_question") for r in rows)


def test_assistant_persists_provider_model_id_and_extra(tmp_path: Path):
    """assistant turn 的 provider_model_id / provider_extra 必须落 jsonl。

    fable refusal→opus-4-8 回退的审计依赖此条:每个 turn 实际服务模型 + extra
    字典(``fable_refusal_fallback`` 等)是仅有的事后溯源信号。
    """
    turns = [
        HarnessTurn(role="system", content="sys"),
        HarnessTurn(role="user", content="ping", is_real_user_question=True),
        HarnessTurn(
            role="assistant",
            content="pong",
            provider_model_id="claude-opus-4-8",
            provider_extra={
                "fable_refusal_fallback": True,
                "fallback_from_model": "claude-fable-5",
                "fallback_model": "claude-opus-4-8",
            },
        ),
        # 第二个 assistant turn 无 fallback,只透传 model_id
        HarnessTurn(role="user", content="next"),
        HarnessTurn(
            role="assistant",
            content="reply",
            provider_model_id="claude-fable-5",
        ),
    ]
    p = tmp_path / "main.jsonl"
    write_session_jsonl(p, turns, owner="main")
    rows = read_session_jsonl(p)
    asst = [r for r in rows if r.get("role") == "assistant"]
    assert len(asst) == 2
    assert asst[0]["provider_model_id"] == "claude-opus-4-8"
    assert asst[0]["provider_extra"]["fable_refusal_fallback"] is True
    assert asst[0]["provider_extra"]["fallback_from_model"] == "claude-fable-5"
    assert asst[1]["provider_model_id"] == "claude-fable-5"
    # 第二条无 extra 不应写空字典字段(节省 jsonl 体积)
    assert "provider_extra" not in asst[1]


def test_assistant_no_extra_no_field(tmp_path: Path):
    """没设 provider_model_id/provider_extra(老路径)不应注入空键,保持向后兼容。"""
    turns = [
        HarnessTurn(role="user", content="hi"),
        HarnessTurn(role="assistant", content="ok"),
    ]
    p = tmp_path / "main.jsonl"
    write_session_jsonl(p, turns, owner="main")
    rows = read_session_jsonl(p)
    asst = [r for r in rows if r.get("role") == "assistant"][0]
    assert "provider_model_id" not in asst
    assert "provider_extra" not in asst
