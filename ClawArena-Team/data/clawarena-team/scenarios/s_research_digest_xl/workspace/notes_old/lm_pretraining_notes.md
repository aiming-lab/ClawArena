# Pre-training Reading Notes — Fall 2025 (OUTDATED)

> **Warning:** These notes are from last semester and relate to a different project.
> They are NOT relevant to the April 2026 research digest assignment.

## BERT (Devlin et al., 2018)

Bidirectional Encoder Representations from Transformers. Pre-trained on masked language
modelling and next sentence prediction. Fine-tuned on 11 NLP tasks, achieving SOTA at the time.

Key takeaway: bidirectionality matters more than directionality for understanding tasks.

## GPT-2 (Radford et al., 2019)

Autoregressive language model trained on WebText corpus (~40GB). Demonstrated zero-shot
transfer across many tasks without fine-tuning. Generated controversy for potential misuse.

Key claim: language models are multitask learners.

## T5 (Raffel et al., 2020)

Text-to-text transfer transformer. Unified all NLP tasks as seq2seq. Used C4 corpus.
Explored scaling laws systematically.

Key claim: "text-to-text" framework simplifies multi-task learning.

## GPT-3 (Brown et al., 2020)

175B parameter autoregressive model. In-context few-shot learning without gradient updates.
Used Common Crawl + Books + Wikipedia.

Key observation: scaling alone yields emergent few-shot capabilities.

---

*Notes compiled by: Graduate Research Assistant, Fall 2025*
