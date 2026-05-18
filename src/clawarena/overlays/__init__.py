"""Overlay modules — transparent LLM proxy/middleware layers.

Each overlay sits between the benchmark agent and the upstream LLM,
intercepting requests and augmenting them with capabilities such as
memory, skills, and reinforcement learning without replacing the
underlying API surface.

Available overlays:
  metaclaw    — original MetaClaw proxy (memory / skills / RL)
  mm_metaclaw — refactored gateway-modules MetaClaw (memory / skill / multimodal)
"""
