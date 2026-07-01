"""ClawArena —— 多框架 AI Agent benchmark 评测平台。

公开的 Python SDK 入口::

    from clawarena import ClawArena, download_data, data_root

    ca = ClawArena(data="clawarena-real", out="results")
    ca.run(["clawarena-native"], test_id="eng1")
"""

from __future__ import annotations

from clawarena._paths import data_root
from clawarena.datafetch import download_data
from clawarena.sdk import ClawArena

__version__ = "1.0.0"

__all__ = ["ClawArena", "download_data", "data_root", "__version__"]
