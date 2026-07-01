# Scalable Constitutional AI Alignment via Principle Distillation

**Authors:** Yuka Takahashi¹, Marcus Weber², Shreya Patel¹, Jean-Pierre Dumont³

¹ DeepAlignment Institute, ² Humboldt University Berlin, ³ INRIA Paris

**Venue:** Proceedings of ICLR 2026

## Abstract

Constitutional AI alignment trains language models to evaluate and revise their own outputs according to a set of ethical principles, reducing harmful content without requiring human labels for every example. Existing approaches, however, scale poorly: the self-critique loop is expensive at inference time, and the constitutional principles require careful manual engineering. We introduce **DistillAlign**, which distills the constitutional self-critique capability into a lightweight reward model that provides alignment guidance during standard RLHF training, eliminating the per-generation critique overhead. Our primary finding is that **constitutional AI alignment reduces toxicity by 52%** on the ToxicBench suite compared to RLHF-only baselines, while achieving competitive performance on helpfulness benchmarks. DistillAlign requires 3× fewer GPU-hours to train than vanilla constitutional AI at the 13B parameter scale.

**Keywords:** constitutional AI, RLHF, toxicity reduction, alignment, principle distillation
