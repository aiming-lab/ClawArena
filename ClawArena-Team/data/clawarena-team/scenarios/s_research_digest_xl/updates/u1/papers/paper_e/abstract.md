# Privacy-Preserving Language Model Fine-Tuning via Differential Federated Alignment

**Authors:** Leila Mansouri¹, Tobias Grün², Cheng Wei³, Amara Diallo¹

¹ Privacy and AI Lab, EPFL, ² TU Munich, ³ Peking University

**Venue:** Proceedings of NeurIPS 2026

## Abstract

Fine-tuning large language models on sensitive user data presents a fundamental privacy dilemma: improved personalisation requires data centralisation, which conflicts with privacy regulation and user trust. Federated learning distributes training across devices without centralising data, but standard federated optimisers suffer from significant accuracy degradation due to client data heterogeneity. We introduce **FedAlign**, a federated fine-tuning framework that combines differential privacy noise injection with a novel alignment regulariser that reduces client drift without requiring data sharing. Our central finding is that **federated learning preserves privacy with only 8% accuracy drop** relative to centralised training, measured under a rigorous (ε=2, δ=10⁻⁵) differential privacy guarantee. This represents a 19-percentage-point improvement over vanilla FedAvg under the same privacy budget. FedAlign is validated across three domain adaptation benchmarks and three federated data distributions.

**Keywords:** federated learning, differential privacy, language model fine-tuning, client drift
