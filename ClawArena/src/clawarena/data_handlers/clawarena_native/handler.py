"""clawarena-native data handler。

数据布局（仿 openclaw 的多 session 设计，但结构精简）::

    manifest.json
    state/
      {agent_id}/
        sessions.json                 # 索引（key=session_id，去掉 openclaw 的 agent: 前缀）
        {active_session}.jsonl        # 主 session（native Message 紧凑格式，运行时写入）
        {history_session}.jsonl       # 预置历史 session（数据集作者提供，只读）
    workspaces/
      {agent_id}/                     # agent 工作目录初始文件

manifest.json::

    {
      "agents": {
        "{test_id}": {
          "agent_id": "{agent_id}",
          "session": "{active_session_id}",
          "history_sessions": ["{sid1}", "{sid2}"],
          "workspace": "workspaces/{agent_id}"
        }
      },
      "state_dir": "state",
      "workspaces_dir": "workspaces"
    }

会话记录用 native 的紧凑 jsonl（role/content/tool_calls/... 见 ``clawarena.native.agent.messages``），
不再像 picoclaw/nanobot 那样摊平为 md，从而保留"分 session + 跨 session 读取"的 benchmark 语义。
"""
from __future__ import annotations

import json
import os
import shutil
from datetime import datetime
from pathlib import Path

from clawarena.core.types import WorkCopy
from clawarena.data_handlers.base import DataHandler


def _guess_channel(filename: str) -> str:
    """从文件名猜通信渠道（与 openclaw 同款，用于 sessions.json 的 channel 标签）。"""
    lower = filename.lower()
    for ch in ("feishu", "slack", "discord", "telegram", "wechat", "email", "im", "ticket", "kefu"):
        if ch in lower:
            return ch
    return "unknown"


class ClawArenaNativeDataHandler(DataHandler):
    name = "clawarena-native"

    # ── Manifest ──────────────────────────────────────
    def load_manifest(self, manifest_path: Path) -> dict:
        return json.loads(Path(manifest_path).read_text(encoding="utf-8"))

    # ── Validation ────────────────────────────────────
    def validate(
        self,
        manifest: dict,
        manifest_dir: Path,
        eval_dir: Path,
        test_entries: list[dict],
    ) -> list[str]:
        errors: list[str] = []
        agents = manifest.get("agents", {})
        state_rel = manifest.get("state_dir", "state")
        ws_rel = manifest.get("workspaces_dir", "workspaces")
        for entry in test_entries:
            test_id = entry.get("test_id") or entry.get("id")
            info = agents.get(test_id)
            if info is None:
                errors.append(f"[clawarena-native] manifest.agents missing test '{test_id}'")
                continue
            agent_id = info.get("agent_id", test_id)
            if not info.get("session"):
                errors.append(f"[clawarena-native] agent '{test_id}' has no 'session'")
            ws = manifest_dir / ws_rel / agent_id
            if not ws.exists():
                errors.append(f"[clawarena-native] workspace not found: {ws}")
            sess_dir = manifest_dir / state_rel / agent_id
            for hsid in info.get("history_sessions", []) or []:
                hf = sess_dir / f"{hsid}.jsonl"
                if not hf.exists():
                    errors.append(
                        f"[clawarena-native] history session file missing: {hf}"
                    )
        return errors

    # ── Work Copy ─────────────────────────────────────
    def prepare_work_copy(
        self,
        manifest: dict,
        manifest_dir: Path,
        project_root: Path,
    ) -> WorkCopy:
        # sandbox scope 要求 accessible path 为绝对路径；manifest_dir/project_root
        # 可能以相对路径传入（如 data/clawarena-real/clawarena-native），故先 resolve，
        # 使派生的 work_dir/state_dst/ws_dst/project_root 全为绝对路径。
        manifest_dir = Path(manifest_dir).resolve()
        project_root = Path(project_root).resolve()
        run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + f"_{os.getpid()}"
        work_dir = manifest_dir / "work"
        work_dir.mkdir(exist_ok=True)

        state_src = manifest_dir / manifest.get("state_dir", "state")
        ws_src = manifest_dir / manifest.get("workspaces_dir", "workspaces")

        state_dst = work_dir / f"state_{run_id}"
        if state_src.exists():
            shutil.copytree(state_src, state_dst)
        else:
            state_dst.mkdir(parents=True, exist_ok=True)

        ws_dst = None
        if ws_src.exists():
            ws_dst = work_dir / f"workspaces_{run_id}"
            shutil.copytree(ws_src, ws_dst)

        return WorkCopy(
            state_dir=state_dst,
            config_path=None,
            project_root=project_root,
            workspace_root=ws_dst,
            extra={"manifest": manifest, "manifest_dir": manifest_dir},
        )

    # ── Session ───────────────────────────────────────
    def _agent_id(self, work_copy: WorkCopy, test_id: str) -> str:
        agents = work_copy.extra.get("manifest", {}).get("agents", {})
        return agents.get(test_id, {}).get("agent_id", test_id)

    def _sessions_dir(self, work_copy: WorkCopy, test_id: str) -> Path:
        return work_copy.state_dir / self._agent_id(work_copy, test_id)

    def init_session(self, work_copy: WorkCopy, test_id: str) -> str:
        """确定该 test 的 active session id，并在 sessions.json 登记为 active。

        active session 直接用 manifest 声明的 ``session``（多 round 共用同一条）；history
        session 由数据集预置，此处只确保 active 登记存在、且历史条目都在索引里。
        """
        from clawarena.native.agent.session_history import SessionHistoryStore

        agents = work_copy.extra.get("manifest", {}).get("agents", {})
        info = agents.get(test_id, {})
        session_id = info.get("session") or "main"
        sessions_dir = self._sessions_dir(work_copy, test_id)
        sessions_dir.mkdir(parents=True, exist_ok=True)

        store = SessionHistoryStore(sessions_dir, session_id)
        # 登记 active
        store.upsert(session_id, channel="main", is_active=True)
        # 确保历史 session 条目都在索引内（若数据集已写 sessions.json 则保留其 channel）
        index = store.load_index()
        for hsid in info.get("history_sessions", []) or []:
            if hsid not in index:
                store.upsert(hsid, channel="history", is_active=False)
        return session_id

    # ── Update ────────────────────────────────────────
    def execute_update(
        self,
        update_id: str,
        work_copy: WorkCopy,
        test_id: str,
        session_id: str,
    ) -> None:
        """应用一个 update（对齐 openclaw 语义，但用精简的 native 布局）。

        update 规格从 ``manifest['updates'][test_id]`` 读取，结构与 openclaw 一致::

            {
              "{upd_id}": {"type": "session"|"workspace"|"group",
                            "dir": "updates/{agent_id}/{upd_id}",
                            "files": [{"name":..,"action":new|append|..}, ...]},
              "{group_id}": {"type": "group", "children": ["{upd_id}", ...]}
            }

        与 openclaw 的差异：session 文件落在 ``state/{agent_id}/`` 下（无 agents/sessions
        嵌套），且 update 源文件已是 native 紧凑 jsonl（转换脚本已转好）。
        """
        manifest = work_copy.extra.get("manifest", {})
        manifest_dir: Path | None = work_copy.extra.get("manifest_dir")
        if manifest_dir is None:
            return
        updates_map = (manifest.get("updates", {}) or {}).get(test_id, {})
        resolved = self._resolve_update_entries(updates_map, update_id)
        if not resolved:
            return
        agent_id = self._agent_id(work_copy, test_id)
        for _uid, meta in resolved:
            utype = meta.get("type", "")
            src_dir = Path(manifest_dir) / meta.get("dir", "")
            files = meta.get("files", []) or []
            if utype == "session":
                self._apply_session_update(files, src_dir, work_copy, agent_id)
            elif utype == "workspace":
                self._apply_workspace_update(files, src_dir, work_copy, test_id)

    @staticmethod
    def _resolve_update_entries(updates_map: dict, update_id: str) -> list[tuple[str, dict]]:
        """展开 update_id：group → 其 children；否则即自身。"""
        meta = updates_map.get(update_id)
        if meta is None:
            return []
        if meta.get("type") == "group":
            out: list[tuple[str, dict]] = []
            for child in meta.get("children", []) or []:
                cm = updates_map.get(child)
                if cm:
                    out.append((child, cm))
            return out
        return [(update_id, meta)]

    @staticmethod
    def _norm_file_item(item) -> tuple[str, str, str]:
        """归一化 files 项 → (name, action, target)。支持裸字符串与 dict。"""
        if isinstance(item, str):
            return item, "new", item
        name = item.get("name", "")
        return name, item.get("action", "new"), item.get("target", name)

    def _apply_session_update(self, files, src_dir: Path, work_copy: WorkCopy, agent_id: str) -> None:
        from clawarena.native.agent.session_history import SessionHistoryStore

        sessions_dir = work_copy.state_dir / agent_id
        sessions_dir.mkdir(parents=True, exist_ok=True)
        store = SessionHistoryStore(sessions_dir, "")
        for item in files:
            name, action, target = self._norm_file_item(item)
            if not name:
                continue
            src = src_dir / name
            dst = sessions_dir / target
            sid = target[:-6] if target.endswith(".jsonl") else target
            channel = item.get("channel") if isinstance(item, dict) else None
            channel = channel or _guess_channel(name)
            if action == "new":
                if not src.exists():
                    continue
                shutil.copy2(src, dst)
                store.upsert(sid, channel=channel, is_active=False)
            elif action == "append":
                if not src.exists():
                    continue
                with open(dst, "a", encoding="utf-8") as f:
                    f.write(src.read_text(encoding="utf-8"))
                if sid not in store.load_index():
                    store.upsert(sid, channel=channel, is_active=False)

    def _apply_workspace_update(self, files, src_dir: Path, work_copy: WorkCopy, test_id: str) -> None:
        ws = self.resolve_workspace(work_copy, test_id)
        if ws is None:
            return
        ws.mkdir(parents=True, exist_ok=True)
        for item in files:
            name, action, target = self._norm_file_item(item)
            if not name:
                continue
            src = src_dir / name
            dst = (ws / target)
            try:
                dst.resolve().relative_to(ws.resolve())
            except ValueError:
                continue  # 越界保护
            if action in ("new", "modify", "add"):
                if not src.exists():
                    continue
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
            elif action == "append":
                if not src.exists():
                    continue
                dst.parent.mkdir(parents=True, exist_ok=True)
                with open(dst, "a", encoding="utf-8") as f:
                    f.write(src.read_text(encoding="utf-8"))
            elif action == "delete":
                if dst.exists():
                    dst.unlink()

    # ── Path ──────────────────────────────────────────
    def resolve_workspace(self, work_copy: WorkCopy, test_id: str) -> Path | None:
        if work_copy.workspace_root is None:
            return None
        ws = work_copy.workspace_root / self._agent_id(work_copy, test_id)
        return ws if ws.exists() else work_copy.workspace_root

    # ── Model config ──────────────────────────────────
    def apply_model_config(self, work_copy: WorkCopy, model) -> None:  # noqa: ANN001
        """把 ClawArena ModelConfig 存进 work_copy.extra，供 engine 构造 native provider。

        native harness 自己直连 LLM，不改任何外部框架配置文件——这里只是把模型信息
        透传给进程内 engine。
        """
        from clawarena.engines.clawarena_native.engine import native_model_json_from_claw

        work_copy.extra["native_model"] = native_model_json_from_claw(model)

    # ── LLM log / token ───────────────────────────────
    def read_llm_log(self, work_copy: WorkCopy, session_id: str, after_ts: float) -> dict | None:
        return None

    def count_session_tokens(self, state_dir: Path, test_id: str) -> int:
        return 0
