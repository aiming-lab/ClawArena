"""mm-metaclaw overlay — gateway-modules integration for ClawArena.

Provides memory, skill, and multimodal augmentation via the refactored
mm-metaclaw gateway (gateway-modules branch).  Acts as a transparent
overlay: the benchmark agent connects to the gateway, which intercepts
LLM calls and injects context from enabled modules.

Two hook modes are supported (configured via ``hook_mode`` in tests.json):

* **proxy** — modules are exercised transparently through the proxy
  pipeline; hooks issue explicit ``/collect`` calls at trigger points
  to verify collection behaviour.
* **http** — hooks drive every inject/collect step via direct HTTP
  requests to individual module endpoints, bypassing the proxy
  pipeline.  Useful for testing module endpoints in isolation.

Mutually exclusive with the original ``metaclaw`` overlay.
"""

from clawarena.overlays.mm_metaclaw.manager import MmMetaClawManager

__all__ = ["MmMetaClawManager"]
