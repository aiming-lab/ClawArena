# Faithful Retrieval-Augmented Generation with Constrained Decoding

**Authors:** Clara Hoffman¹, Ravi Shankar², David Park¹, Fatima Al-Rashid³

¹ MIT CSAIL, ² IIT Bombay, ³ Oxford Internet Institute

**Venue:** Proceedings of ACL 2026

## Abstract

Retrieval-augmented generation (RAG) has emerged as a leading strategy for grounding language model outputs in verifiable sources. Yet standard RAG pipelines suffer from "context drift": the model frequently ignores retrieved passages and falls back on parametric knowledge, producing confident but factually incorrect outputs. We introduce **FaithRAG**, a framework combining dense retrieval with a constrained decoding objective that penalises tokens not attributable to retrieved passages. Our main result is that **retrieval augmentation boosts factual accuracy by 28%** on the TruthfulQA and FActScore benchmarks relative to non-augmented baselines of equal parameter count. FaithRAG further reduces hallucination rate by 41% as measured by a separate automatic factuality checker, while maintaining competitive fluency scores.

**Keywords:** retrieval augmented generation, factual accuracy, constrained decoding, hallucination
