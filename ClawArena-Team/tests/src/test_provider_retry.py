"""OpenAICompatProvider 瞬时错误重试回归测试。

并发跑长场景时偶发连接抖动(ReadError/RemoteProtocolError/超时),曾让整个场景以
空消息 ProviderError 失败、丢一份结果。chat() 现对传输层错误与 5xx 有限重试,4xx 不重试。
"""
from __future__ import annotations

import asyncio

import httpx
import pytest

from clawarena_team.provider.base import ProviderError
from clawarena_team.provider.openai_compat import OpenAICompatProvider
from clawarena_team.types import ModelConfig


def _cfg() -> ModelConfig:
    return ModelConfig(
        provider="openai_compat", model_id="m",
        api_base="http://x/v1", api_key="k", modalities=["text"], extra={},
    )


class _Resp:
    def __init__(self, status: int, payload: dict, headers: dict | None = None):
        self.status_code = status
        self._p = payload
        self._headers = headers or {}

    def raise_for_status(self):
        if self.status_code >= 400:
            req = httpx.Request("POST", "http://x/v1/chat/completions")
            raise httpx.HTTPStatusError(
                "err", request=req,
                response=httpx.Response(self.status_code, request=req, headers=self._headers),
            )

    def json(self):
        return self._p


@pytest.fixture(autouse=True)
def _fast_sleep(monkeypatch):
    async def _nosleep(*_a, **_k):
        return None
    monkeypatch.setattr("clawarena_team.provider.openai_compat.asyncio.sleep", _nosleep)


async def test_retry_on_transient_then_success(monkeypatch):
    calls = {"n": 0}

    async def fake_post(self, url, json=None, headers=None):
        calls["n"] += 1
        if calls["n"] == 1:
            raise httpx.ReadError("transient connection drop")
        return _Resp(200, {"choices": [{"message": {"content": "ok"}}]})

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)
    r = await OpenAICompatProvider(_cfg()).chat(messages=[{"role": "user", "content": "hi"}])
    assert r["content"] == "ok"
    assert calls["n"] == 2  # 首次瞬时错误后重试一次成功


async def test_no_retry_on_4xx(monkeypatch):
    calls = {"n": 0}

    async def fake_post(self, url, json=None, headers=None):
        calls["n"] += 1
        return _Resp(400, {})

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)
    with pytest.raises(ProviderError):
        await OpenAICompatProvider(_cfg()).chat(messages=[{"role": "user", "content": "hi"}])
    assert calls["n"] == 1  # 4xx 确定性错误,不重试


async def test_gives_up_after_max_attempts(monkeypatch):
    calls = {"n": 0}

    async def fake_post(self, url, json=None, headers=None):
        calls["n"] += 1
        raise httpx.ConnectError("down")

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)
    monkeypatch.setenv("CATEAM_PROVIDER_MAX_RETRIES", "3")
    with pytest.raises(ProviderError):
        await OpenAICompatProvider(_cfg()).chat(messages=[{"role": "user", "content": "hi"}])
    assert calls["n"] == 3  # 重试到上限后放弃


async def test_retry_on_429_then_success(monkeypatch):
    """429 限流可重试(区别于其他 4xx),退避后成功。"""
    calls = {"n": 0}

    async def fake_post(self, url, json=None, headers=None):
        calls["n"] += 1
        if calls["n"] <= 2:
            return _Resp(429, {})
        return _Resp(200, {"choices": [{"message": {"content": "ok"}}]})

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)
    r = await OpenAICompatProvider(_cfg()).chat(messages=[{"role": "user", "content": "hi"}])
    assert r["content"] == "ok"
    assert calls["n"] == 3  # 两次 429 各重试,第三次成功


async def test_429_independent_of_max_attempts(monkeypatch):
    """429 重试预算独立于 CATEAM_PROVIDER_MAX_RETRIES——限流不应吃光普通重试预算。"""
    calls = {"n": 0}

    async def fake_post(self, url, json=None, headers=None):
        calls["n"] += 1
        return _Resp(429, {})

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)
    monkeypatch.setenv("CATEAM_PROVIDER_MAX_RETRIES", "3")
    monkeypatch.setenv("CATEAM_PROVIDER_RATELIMIT_RETRIES", "5")
    with pytest.raises(ProviderError):
        await OpenAICompatProvider(_cfg()).chat(messages=[{"role": "user", "content": "hi"}])
    assert calls["n"] == 5  # 用限流预算(5)而非 max_attempts(3)


async def test_total_timeout_stall_then_retry_succeeds(monkeypatch):
    """启用 CATEAM_PROVIDER_TOTAL_TIMEOUT_SEC 时,单次请求永久停滞(httpx 逐次 read
    超时无法兜底的 trickle-stall)被总时限取消、按瞬时错误重试,下一次成功。"""
    calls = {"n": 0}

    async def fake_post(self, url, json=None, headers=None):
        calls["n"] += 1
        if calls["n"] == 1:
            await asyncio.Event().wait()  # 永久挂起,模拟流停滞
        return _Resp(200, {"choices": [{"message": {"content": "ok"}}]})

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)
    monkeypatch.setenv("CATEAM_PROVIDER_TOTAL_TIMEOUT_SEC", "0.05")
    r = await OpenAICompatProvider(_cfg()).chat(messages=[{"role": "user", "content": "hi"}])
    assert r["content"] == "ok"
    assert calls["n"] == 2  # 首次停滞被总时限掐断后重试一次成功


async def test_total_timeout_disabled_by_default_no_wrap(monkeypatch):
    """默认(未设/0)不套总时限:正常响应直接返回,不会因总时限误触发超时。"""
    calls = {"n": 0}

    async def fake_post(self, url, json=None, headers=None):
        calls["n"] += 1
        return _Resp(200, {"choices": [{"message": {"content": "ok"}}]})

    monkeypatch.delenv("CATEAM_PROVIDER_TOTAL_TIMEOUT_SEC", raising=False)
    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)
    r = await OpenAICompatProvider(_cfg()).chat(messages=[{"role": "user", "content": "hi"}])
    assert r["content"] == "ok"
    assert calls["n"] == 1


async def test_total_timeout_persistent_stall_gives_up(monkeypatch):
    """请求始终停滞:总时限每次掐断、重试到上限后以 ProviderError 干净失败(不无限挂)。"""
    calls = {"n": 0}

    async def fake_post(self, url, json=None, headers=None):
        calls["n"] += 1
        await asyncio.Event().wait()  # 始终挂起

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)
    monkeypatch.setenv("CATEAM_PROVIDER_TOTAL_TIMEOUT_SEC", "0.05")
    monkeypatch.setenv("CATEAM_PROVIDER_MAX_RETRIES", "3")
    with pytest.raises(ProviderError):
        await OpenAICompatProvider(_cfg()).chat(messages=[{"role": "user", "content": "hi"}])
    assert calls["n"] == 3  # 每次总时限掐断,重试到上限放弃


async def test_retry_after_header_honored(monkeypatch):
    """429 带 Retry-After 时按其秒数退避(而非指数兜底)。"""
    slept: list[float] = []

    async def _capture_sleep(d):
        slept.append(d)

    monkeypatch.setattr("clawarena_team.provider.openai_compat.asyncio.sleep", _capture_sleep)
    calls = {"n": 0}

    async def fake_post(self, url, json=None, headers=None):
        calls["n"] += 1
        if calls["n"] == 1:
            return _Resp(429, {}, headers={"Retry-After": "7"})
        return _Resp(200, {"choices": [{"message": {"content": "ok"}}]})

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)
    r = await OpenAICompatProvider(_cfg()).chat(messages=[{"role": "user", "content": "hi"}])
    assert r["content"] == "ok"
    assert slept == [7.0]  # 遵守 Retry-After
