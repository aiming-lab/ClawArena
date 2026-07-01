#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ClawArena 真实数据集造数公共工具库。

提供：
  - SessionBuilder : 构造 OpenClaw 原生 session JSONL（header + 控制行 + user/assistant 消息链），
                     自动维护 id / parentId / timestamp 链，符合 data_handlers/openclaw/validate.py
                     的消息顺序约束（连续 assistant 非法；user/assistant 交替）。
  - est_tokens     : cl100k_base token 估算（与 clawarena stats 默认 tokenizer 对齐）。
  - init_dataset   : 初始化一个空的 clawarena 数据集骨架（tests.json + openclaw 骨架）。
  - register_scenario : 幂等地把一个场景注册进数据集（tests.json / manifest.json /
                     openclaw.json agents.list / sessions.json）。

所有路径相对 dataset_root（如 data/clawarena-real）。设计为可被 build_<scene>.py 复用。
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

# --------------------------------------------------------------------------- #
# Token 估算
# --------------------------------------------------------------------------- #
try:
    import tiktoken

    _ENC = tiktoken.get_encoding("cl100k_base")

    def est_tokens(text: str) -> int:
        return len(_ENC.encode(text, disallowed_special=()))
except Exception:  # pragma: no cover - tiktoken 缺失时退化
    def est_tokens(text: str) -> int:
        return max(1, len(text) // 4)


def est_path_tokens(path: Path) -> int:
    try:
        return est_tokens(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return 0


# --------------------------------------------------------------------------- #
# OpenClaw session JSONL 构造
# --------------------------------------------------------------------------- #
_DEF_MODEL = "claude-sonnet-4-6"


class SessionBuilder:
    """构造一个 OpenClaw 原生 session JSONL 文件。

    用法：
        sb = SessionBuilder("main_<uuid>", "/workspace/eng2", "2026-03-09T01:00:00",
                            is_main=True)
        sb.add_user("...")            # user 消息
        sb.add_assistant("...")       # assistant 回复（必须与 user 交替）
        sb.write(path)

    约束（来自 validate.py）：
        - 连续 assistant 非法；连续 user 允许但本 builder 默认强制交替。
        - 主 session header 含 cwd；history session header 同样可含 cwd（与现网 hil_* 一致）。
    """

    def __init__(
        self,
        session_id: str,
        cwd: str,
        start_iso: str,
        *,
        is_main: bool = False,
        model: str = _DEF_MODEL,
        thinking: str = "low",
        step_seconds: int = 60,
    ) -> None:
        self.session_id = session_id
        self.cwd = cwd
        self.model = model
        self.thinking = thinking
        self.step = timedelta(seconds=step_seconds)
        self.is_main = is_main
        self._seq = 0
        self._t = _parse_iso(start_iso)
        self._last_id: str | None = None
        self._last_role: str | None = None
        self._lines: list[dict] = []
        self._build_header()

    # -- 内部 -------------------------------------------------------------- #
    def _nid(self) -> str:
        self._seq += 1
        return hashlib.md5(f"{self.session_id}:{self._seq}".encode()).hexdigest()[:8]

    def _iso(self, t: datetime) -> str:
        return t.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") + f"{t.microsecond // 1000:03d}Z"

    def _ms(self, t: datetime) -> int:
        return int(t.timestamp() * 1000)

    def _build_header(self) -> None:
        t0 = self._t
        header = {
            "type": "session",
            "version": 3,
            "id": self.session_id,
            "timestamp": self._iso(t0),
            "cwd": self.cwd,
        }
        mc_id = self._nid()
        mc = {
            "type": "model_change",
            "id": mc_id,
            "parentId": None,
            "timestamp": self._iso(t0 + timedelta(milliseconds=10)),
            "provider": "anthropic",
            "modelId": self.model,
        }
        tl_id = self._nid()
        tl = {
            "type": "thinking_level_change",
            "id": tl_id,
            "parentId": mc_id,
            "timestamp": self._iso(t0 + timedelta(milliseconds=20)),
            "thinkingLevel": self.thinking,
        }
        snap_id = self._nid()
        snap = {
            "type": "custom",
            "customType": "model-snapshot",
            "data": {
                "timestamp": self._ms(t0) + 30,
                "provider": "anthropic",
                "modelApi": "openai-completions",
                "modelId": self.model,
            },
            "id": snap_id,
            "parentId": tl_id,
            "timestamp": self._iso(t0 + timedelta(milliseconds=30)),
        }
        self._lines.extend([header, mc, tl, snap])
        self._last_id = snap_id

    def _add_message(self, role: str, text: str, at: datetime | None) -> None:
        if at is not None:
            self._t = _parse_iso(at) if isinstance(at, str) else at
        else:
            self._t = self._t + self.step
        mid = self._nid()
        line = {
            "type": "message",
            "id": mid,
            "parentId": self._last_id,
            "timestamp": self._iso(self._t),
            "message": {
                "role": role,
                "content": [{"type": "text", "text": text}],
                "timestamp": self._ms(self._t),
            },
        }
        self._lines.append(line)
        self._last_id = mid
        self._last_role = role

    # -- 公共 API ---------------------------------------------------------- #
    def add_user(self, text: str, at: datetime | str | None = None) -> "SessionBuilder":
        if self._last_role == "user":
            raise ValueError(f"{self.session_id}: consecutive user (builder enforces alternation)")
        self._add_message("user", text, at)
        return self

    def add_assistant(self, text: str, at: datetime | str | None = None) -> "SessionBuilder":
        if self._last_role in (None, "assistant"):
            raise ValueError(
                f"{self.session_id}: assistant must follow a user message (no leading/consecutive assistant)"
            )
        self._add_message("assistant", text, at)
        return self

    def add_turns(self, pairs: Iterable[tuple[str, str]]) -> "SessionBuilder":
        """批量添加 (user, assistant) 对。"""
        for u, a in pairs:
            self.add_user(u)
            self.add_assistant(a)
        return self

    @property
    def lines(self) -> list[dict]:
        return self._lines

    @property
    def last_message_ms(self) -> int:
        return self._ms(self._t)

    def write(self, path: Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as fh:
            for ln in self._lines:
                fh.write(json.dumps(ln, ensure_ascii=False) + "\n")
        return path


def append_history(path: Path, session_id: str, cwd: str, start_iso: str,
                   turns: list[tuple[str, str]], **kw) -> SessionBuilder:
    """便捷：构造一个 history session（user/assistant 交替）并写盘。"""
    sb = SessionBuilder(session_id, cwd, start_iso, is_main=False, **kw)
    sb.add_turns(turns)
    sb.write(path)
    return sb


# --------------------------------------------------------------------------- #
# 数据集骨架与注册
# --------------------------------------------------------------------------- #
def _benchmark_path(dataset_root: Path) -> str:
    """openclaw.json 中 ${BENCHMARK_ROOT} 之后的数据集相对前缀，如 data/clawarena-real。"""
    # dataset_root 形如 <repo>/data/clawarena-real
    parts = dataset_root.resolve().parts
    idx = parts.index("data")
    return "/".join(parts[idx:])


def _openclaw_config_skeleton() -> dict:
    return {
        "meta": {"lastTouchedVersion": "2026.2.15"},
        "auth": {
            "profiles": {
                "anthropic:manual": {"provider": "anthropic", "mode": "token"},
                "openai-codex:manual": {"provider": "openai-codex", "mode": "oauth"},
            }
        },
        "agents": {
            "defaults": {
                "model": {"primary": "anthropic/claude-opus-4-6"},
                "compaction": {"mode": "safeguard"},
                "sandbox": {"sessionToolsVisibility": "all"},
            },
            "list": [],
        },
        "plugins": {
            "load": {"paths": ["${BENCHMARK_ROOT}/helpers/openclaw_customize"]},
            "entries": {
                "llm-prompt-logger": {
                    "enabled": True,
                    "config": {
                        "logDir": "${BENCHMARK_ROOT}/logs/llm_prompts/openclaw",
                        "enableLlmInput": False,
                        "enableLlmOutput": False,
                        "enableAgentEnd": True,
                    },
                }
            },
            "allow": ["llm-prompt-logger"],
        },
        "tools": {"sessions": {"visibility": "agent"}},
    }


def init_dataset(dataset_root: Path, name: str, description: str) -> None:
    """初始化空数据集骨架（幂等：已存在则不覆盖已注册内容）。"""
    dataset_root = Path(dataset_root)
    (dataset_root / "eval").mkdir(parents=True, exist_ok=True)
    oc = dataset_root / "openclaw"
    (oc / "config").mkdir(parents=True, exist_ok=True)
    (oc / "state" / "agents").mkdir(parents=True, exist_ok=True)
    (oc / "workspaces").mkdir(parents=True, exist_ok=True)
    (oc / "updates").mkdir(parents=True, exist_ok=True)

    tests = dataset_root / "tests.json"
    if not tests.exists():
        _dump(tests, {
            "name": name,
            "description": description,
            "eval_dir": "eval",
            "frameworks": {"openclaw": {"manifest": "openclaw/manifest.json"}},
            "tests": [],
        })
    man = oc / "manifest.json"
    if not man.exists():
        _dump(man, {
            "framework": "openclaw",
            "config_file": "config/openclaw.json",
            "state_dir": "state",
            "workspaces_dir": "workspaces",
            "updates_dir": "updates",
            "agents": {},
            "updates": {},
        })
    cfg = oc / "config" / "openclaw.json"
    if not cfg.exists():
        _dump(cfg, _openclaw_config_skeleton())


def register_scenario(
    dataset_root: Path,
    *,
    test_id: str,
    desc: str,
    main_session: str,
    history_sessions: list[tuple[str, str]],   # [(session_id, channel), ...]
    updates: dict | None = None,                # {update_id: {"type","dir","files":[...]}}
    last_ms: int | None = None,
) -> None:
    """幂等注册一个场景到 tests.json / manifest.json / openclaw.json / sessions.json。

    history_sessions: (session_id, channel) 列表，channel 如 im/feishu/email/slack/discord。
    updates: manifest.updates[test_id] 的内容（dir 为相对 updates_dir 的路径）。
    """
    dataset_root = Path(dataset_root)
    bench_prefix = _benchmark_path(dataset_root)

    # 1) tests.json
    tests_path = dataset_root / "tests.json"
    tests = _load(tests_path)
    tests["tests"] = [t for t in tests["tests"] if t.get("id") != test_id]
    tests["tests"].append({"id": test_id, "desc": desc, "eval": test_id})
    tests["tests"].sort(key=lambda t: t["id"])
    _dump(tests_path, tests)

    # 2) manifest.json
    man_path = dataset_root / "openclaw" / "manifest.json"
    man = _load(man_path)
    man["agents"][test_id] = {
        "agent_id": test_id,
        "agent_dir": f"state/agents/{test_id}",
        "session": main_session,
        "history_sessions": [sid for sid, _ in history_sessions],
        "workspace": f"workspaces/{test_id}",
    }
    if updates:
        man["updates"][test_id] = updates
    elif test_id in man.get("updates", {}):
        del man["updates"][test_id]
    _dump(man_path, man)

    # 3) openclaw.json agents.list
    cfg_path = dataset_root / "openclaw" / "config" / "openclaw.json"
    cfg = _load(cfg_path)
    lst = [a for a in cfg["agents"]["list"] if a.get("id") != test_id]
    lst.append({
        "id": test_id,
        "name": test_id,
        "skills": [],
        "workspace": f"${{BENCHMARK_ROOT}}/{bench_prefix}/openclaw/workspaces/{test_id}",
        "agentDir": f"${{BENCHMARK_ROOT}}/{bench_prefix}/openclaw/state/agents/{test_id}/agent",
    })
    lst.sort(key=lambda a: a["id"])
    cfg["agents"]["list"] = lst
    _dump(cfg_path, cfg)

    # 4) sessions.json
    sess_dir = dataset_root / "openclaw" / "state" / "agents" / test_id / "sessions"
    sess_dir.mkdir(parents=True, exist_ok=True)
    reg: dict = {}
    base_ms = last_ms or 1_772_960_400_000
    reg[f"agent:{test_id}:{main_session}"] = {
        "sessionId": main_session,
        "sessionFile": f"{main_session}.jsonl",
        "channel": "main",
        "lastChannel": "main",
        "updatedAt": base_ms,
    }
    for sid, ch in history_sessions:
        reg[f"agent:{test_id}:{sid}"] = {
            "sessionId": sid,
            "sessionFile": f"{sid}.jsonl",
            "channel": ch,
            "lastChannel": ch,
            "updatedAt": base_ms,
        }
    _dump(sess_dir / "sessions.json", reg)


# --------------------------------------------------------------------------- #
# 小工具
# --------------------------------------------------------------------------- #
def _parse_iso(s) -> datetime:
    if isinstance(s, datetime):
        return s
    s = s.replace("Z", "+00:00")
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _load(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _dump(path: Path, obj) -> None:
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def dump_register_meta(
    dataset_root: Path,
    *,
    test_id: str,
    desc: str,
    main_session: str,
    history_sessions: list[tuple[str, str]],
    updates: dict | None = None,
) -> Path:
    """并行造数用：把注册元数据落 _register.json（不碰共享 manifest/tests/config），
    由主控在 workflow 后用 register_all 串行注册，避免并发写冲突。"""
    meta = {
        "test_id": test_id,
        "desc": desc,
        "main_session": main_session,
        "history_sessions": history_sessions,
        "updates": updates or {},
    }
    p = Path(dataset_root) / "openclaw" / "state" / "agents" / test_id / "_register.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    _dump(p, meta)
    return p


def register_all_from_meta(dataset_root: Path) -> list[str]:
    """主控串行注册：读所有 _register.json，逐个 register_scenario。返回已注册 id 列表。"""
    dataset_root = Path(dataset_root)
    agents_dir = dataset_root / "openclaw" / "state" / "agents"
    registered = []
    for meta_path in sorted(agents_dir.glob("*/_register.json")):
        m = _load(meta_path)
        # 跳过未完成场景（无 questions.json）——避免半成品污染全量 check
        if not (dataset_root / "eval" / m["test_id"] / "questions.json").exists():
            continue
        register_scenario(
            dataset_root,
            test_id=m["test_id"], desc=m["desc"],
            main_session=m["main_session"],
            history_sessions=[tuple(h) for h in m["history_sessions"]],
            updates=m.get("updates") or None,
        )
        registered.append(m["test_id"])
    return registered


def gen_session_id(role_name_channel: str, seed: str) -> str:
    """生成形如 <role_name_channel>_<uuid> 的稳定 session id（uuid 由 seed 决定，可复现）。"""
    h = hashlib.md5(f"{role_name_channel}:{seed}".encode()).hexdigest()
    uuid = f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"
    return f"{role_name_channel}_{uuid}"
