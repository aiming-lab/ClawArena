# Neurosymbolic Reasoning for Language Understanding via Structured Semantic Parsing

**Authors:** Konstantin Voronov¹, Sara Espinoza², Hideaki Yamamoto³, Preethi Krishnamurthy¹

¹ Carnegie Mellon University LTI, ² Universidad de Chile, ³ RIKEN AIP

**Venue:** Proceedings of ICML 2026

## Abstract

Large language models excel at pattern matching but struggle with systematic compositional generalisation — the ability to combine known primitives in novel ways. Neurosymbolic approaches address this by pairing a neural encoder with an explicit symbolic reasoner, but prior work has either required extensive domain-specific engineering or suffered from error propagation between the neural and symbolic components. We introduce **NSR** (Neurosymbolic Reasoner), which uses a pretrained language model to parse utterances into a typed lambda calculus form, then executes the resulting programs against a structured knowledge base. Our key finding is that **neurosymbolic reasoning achieves 91% accuracy on compositional tasks** across the SCAN, COGS, and CFQ benchmarks — an 18-percentage-point improvement over the best neural-only baseline. NSR generalises to unseen operator combinations without additional training, a property neural models fundamentally lack.

**Keywords:** neurosymbolic, compositional generalisation, semantic parsing, lambda calculus
