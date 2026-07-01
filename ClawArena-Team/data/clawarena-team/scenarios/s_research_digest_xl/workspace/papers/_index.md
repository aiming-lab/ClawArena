# Papers Index

This index lists every chapter file for each paper in this workspace. Sub-agents reading individual chapters should consult this index first to locate the chapter most likely to contain the information they need.

| path | tokens (approx) | claim summary |
|---|---|---|
| papers/paper_a/abstract.md | 0.4k | sparse attention → 40% VRAM savings |
| papers/paper_a/introduction.md | 1.4k | quadratic attention memory wall and SparseFormer motivation |
| papers/paper_a/method.md | 1.4k | adaptive locality prior, bucketed top-k selection, straight-through gradient |
| papers/paper_a/results.md | 1.4k | 40% VRAM saving, 1.43–1.92× throughput, 97.3% accuracy retention |
| papers/paper_a/discussion.md | 1.1k | comparison to Routing Transformer, Longformer, Linformer; limitations |
| papers/paper_a/conclusion.md | 0.3k | SparseFormer summary and release notes |
| papers/paper_b/abstract.md | 0.4k | mixture-of-experts → 35% inference latency reduction |
| papers/paper_b/introduction.md | 1.4k | MoE load imbalance and communication overhead; ClusterMoE motivation |
| papers/paper_b/method.md | 1.4k | spectral expert clustering, pipeline-parallel scheduler, per-device capacity |
| papers/paper_b/results.md | 1.2k | 35% median latency reduction, network sensitivity, throughput |
| papers/paper_b/discussion.md | 1.1k | comparison to DeepSpeed-MoE, tutel, FasterMoE; operational lessons |
| papers/paper_b/conclusion.md | 0.3k | ClusterMoE summary and release notes |
| papers/paper_c/abstract.md | 0.4k | retrieval augmentation → 28% factual accuracy boost |
| papers/paper_c/introduction.md | 1.2k | context drift in standard RAG; FaithRAG motivation |
| papers/paper_c/method.md | 1.3k | attribution scorer, constrained decoding objective, λ annealing |
| papers/paper_c/results.md | 1.3k | 28% factuality gain, 41% hallucination reduction, fluency Pareto |
| papers/paper_c/discussion.md | 1.1k | comparison to FUDGE, FactCC, RankZephyr; deployment considerations |
| papers/paper_c/conclusion.md | 0.3k | FaithRAG summary and release notes |
| papers/paper_d/abstract.md | 0.4k | constitutional AI alignment → 52% toxicity reduction |
| papers/paper_d/introduction.md | 1.3k | RLHF labelling cost and Constitutional AI critique overhead |
| papers/paper_d/method.md | 1.5k | tutor critique, principle-conditioned reward model, PPO student |
| papers/paper_d/results.md | 1.4k | 52% toxicity reduction, 3× training cost saving, robustness |
| papers/paper_d/discussion.md | 1.3k | comparison to InstructGPT, HH-RLHF, PRMs; safety considerations |
| papers/paper_d/conclusion.md | 0.3k | DistillAlign summary and release notes |

<!-- paper_e/f are added via update u1 -->

## Withdrawn Versions

The `_archive/` sub-directory contains **withdrawn pre-submission drafts**.
These are kept for audit purposes only. Do **not** cite figures from `_archive/`.

| path | note |
|------|------|
| `papers/_archive/paper_a_v0/` | Early SparseFormer draft — headline VRAM figure (23%) is **wrong**; use `papers/paper_a/` instead. |

See `papers/_archive/_index.md` for the full withdrawal notice.
