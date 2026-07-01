"""ArcBench 工具集：Read / Write / Edit / Bash / Grep / Glob / LS / Agent。

模块布局：

- :mod:`base` —— :class:`BaseTool` / :class:`ToolContext` / :class:`ToolExecResult`
- :mod:`_helpers` —— 扩展名分类、modality 检测、office 解析、路径校验等内部 helper
- :mod:`read` / :mod:`write` / :mod:`edit` / :mod:`bash` / :mod:`grep` / :mod:`glob`
  —— 6 件基础工具，每件一个文件
- :mod:`ls` —— LS 工具（与 :data:`BASIC_TOOLS` 平级，由调用方按需装配）
- :mod:`agent_tool` —— Agent 工具（spawn subagent 入口，仅 main 可用）

:data:`BASIC_TOOLS` 只收 6 件基础工具；LS 与 Agent 按 ``ToolContext`` 是否具备
``subagent_manager`` 等条件被外部装配器单独注入，不进 dict 防止误启。
"""
from .base import BaseTool, ToolContext, ToolExecResult
from ._helpers import detect_modality, schema_format_kwargs
from .bash import BashTool
from .edit import EditTool
from .glob import GlobTool
from .grep import GrepTool
from .read import ReadTool
from .write import WriteTool

BASIC_TOOLS: dict[str, type[BaseTool]] = {
    "Read": ReadTool,
    "Write": WriteTool,
    "Edit": EditTool,
    "Bash": BashTool,
    "Grep": GrepTool,
    "Glob": GlobTool,
}

__all__ = [
    "BaseTool",
    "ToolContext",
    "ToolExecResult",
    "ReadTool",
    "WriteTool",
    "EditTool",
    "BashTool",
    "GrepTool",
    "GlobTool",
    "BASIC_TOOLS",
    "detect_modality",
    "schema_format_kwargs",
]
