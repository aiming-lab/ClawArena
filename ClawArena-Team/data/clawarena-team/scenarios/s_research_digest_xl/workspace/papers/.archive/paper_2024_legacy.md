# Efficient Text Classification via Distilled LSTM Ensembles

> **ARCHIVED — Previous Project**
> This paper was relevant to the Fall 2024 sequence classification project.
> The advisor brief for the April 2026 research digest explicitly states:
> "ignore archived papers from previous projects" — do NOT include this paper
> in the current assignment.

**Authors:** Reinhardt, Søren; Nakamura, Yuki; Patel, Divya
**Venue:** ACL Findings 2024
**Archive date:** 2025-01-10

---

**Abstract**

We revisit LSTM-based text classifiers in the context of knowledge distillation from
large pre-trained transformers. Despite the dominance of transformer architectures,
LSTM ensembles remain competitive on resource-constrained deployment targets with
strict latency requirements. We train a teacher-student pipeline where a BERT-Large
teacher is used to generate soft labels for a 3-layer bidirectional LSTM student.
The distilled ensemble achieves 94.1% accuracy on SST-2 and 88.6% on AG News while
running at 12× the throughput of the teacher on CPU inference.

**Main claim:** Knowledge-distilled LSTM ensembles achieve near-BERT accuracy at
transformer-incompatible inference budgets, making them viable for edge deployment.

**Key evidence:** Evaluation on SST-2, AG News, IMDb, and Yelp Polarity. Ablations
over teacher model size (BERT-Base vs. Large), distillation temperature (1–10),
and ensemble size (1–8 members). Deployment on Raspberry Pi 4 with real latency
measurements.

**Limitations:** Results are limited to English classification tasks. The gap versus
transformers widens substantially on tasks requiring long-range dependencies (>128
tokens). The approach does not transfer to generation tasks.

---

## 1. Introduction

The transformer revolution has reshaped natural language processing, but the practical
question of which architecture to deploy under strict resource constraints has received
less systematic attention. A Raspberry Pi 4 running inference for a mobile keyboard
application cannot afford the memory or compute of even a quantised BERT-Base model
for every keystroke. Lightweight recurrent models, though displaced on the research
frontier, may still serve important engineering needs.

This paper investigates whether knowledge distillation from large transformers can
close the accuracy gap for LSTM-based classifiers sufficiently to make them viable
on constrained hardware. We answer in the affirmative for a practical range of
classification tasks, while characterising the conditions under which the gap remains
too large to bridge with distillation alone.

*[Section 2–6 omitted from archive — see full paper on ACL Anthology]*

---

*Archived by: Research Assistant, 2025-01-10. Do not reference in current digest.*
