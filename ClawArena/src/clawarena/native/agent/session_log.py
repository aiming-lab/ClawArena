"""Session JSONL append-only 持久化 + 重建 transcript。

每次 ``AgentHarness`` 要拼装发给 provider 的 messages 时，都通过 ``SessionLog.load()``
从 jsonl 反序列化得到 ``Message`` 列表，再 :func:`messages_after_last_compact` 切片
得到可见消息——保证"压缩之前的内容被物理隔离在 boundary 之前"，且不囤内存。

可选优化（v1 暂不做）：维护一个 (uuid -> file_offset) 索引，增量读 jsonl 末尾。
"""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Iterator

from .messages import Message, message_from_dict


class SessionLog:
    """单一 session 的 jsonl 文件读写器。"""

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.touch()

    def append(self, msg: Message) -> None:
        # 若已有内容且末尾无换行（如 convert 用 "\n".join 写出的 session 末行无 \n），
        # 先补一个换行，否则新行会拼到上一行尾部，导致 iter_raw 解析时 "Extra data"。
        if self.path.exists() and self.path.stat().st_size > 0:
            with self.path.open("rb") as f:
                f.seek(-1, 2)
                needs_nl = f.read(1) != b"\n"
            if needs_nl:
                with self.path.open("a", encoding="utf-8") as f:
                    f.write("\n")
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(msg), ensure_ascii=False, default=str) + "\n")

    def iter_raw(self) -> Iterator[dict]:
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                yield json.loads(line)

    def load(self) -> list[Message]:
        return [message_from_dict(d) for d in self.iter_raw()]

    def truncate_to_uuid(self, last_kept_uuid: str) -> None:
        """resume 时使用：把日志截到指定 uuid 后停止。

        实现：读全部 → 找到 uuid 行 → 重写文件。jsonl 量级在 v1 可接受。
        """
        kept: list[str] = []
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                kept.append(line)
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if d.get("uuid") == last_kept_uuid:
                    break
        with self.path.open("w", encoding="utf-8") as f:
            f.writelines(kept)
