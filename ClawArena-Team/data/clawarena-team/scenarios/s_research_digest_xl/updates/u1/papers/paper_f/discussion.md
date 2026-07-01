# 5. Discussion

NSR demonstrates that combining a pretrained neural parser with a symbolic executor and a learned verifier can substantially close the compositional generalisation gap. In this section we situate the work and discuss its limitations.

## 5.1 Related work

NSR draws on several lines of work. **Semantic parsing** has a long history of mapping natural language to structured logical forms, with early systems based on synchronous context-free grammars and later systems on seq2seq neural models. Our parser inherits the seq2seq tradition but uses a pretrained model and in-context prompting rather than supervised training from scratch.

**Neurosymbolic systems** as a category include a wide range of architectures: neural module networks, the Neural Symbolic Concept Learner (NS-CL), differentiable theorem provers, and many others. NSR is most similar to NS-CL in spirit (a neural parser feeding a symbolic executor) but differs in its use of multiple candidate parses, its training-free transfer to new domains, and its learned verifier component. The multiple-parse strategy is what allows NSR to recover from individual parsing errors, and it is in our experiments the single most impactful design choice.

**Compositional generalisation benchmarks** have been an active area of research since the introduction of SCAN by Lake and Baroni. COGS and CFQ followed, each adding complexity to the compositional generalisation challenge. Neural-only systems have made steady progress on these benchmarks via training-data augmentation, specialised architectures (Transformer variants with relative position encoding, structured attention), and meta-learning. The gains from these techniques are real but typically smaller than the gains from neurosymbolic approaches at the same compute scale.

## 5.2 Limitations

NSR has several limitations. First, it requires a symbolic vocabulary appropriate to the domain, which a developer must specify. For tasks with a small, well-defined vocabulary (such as the benchmarks we evaluate on), this is easy. For tasks with an open-ended or fluid vocabulary (such as free-form conversation about the real world), specifying the vocabulary is itself a substantial engineering task and may not be feasible.

Second, NSR's accuracy depends on the parser's ability to produce at least one correct parse among its candidates. When all 8 candidates are incorrect, no amount of downstream processing can recover. Our error analysis shows that this failure mode accounts for roughly half of NSR's errors and is the most direct lever for further improvement. Increasing the number of candidate parses helps slightly but with diminishing returns; we are exploring complementary strategies based on parser fine-tuning on the verifier's reward.

Third, the verifier is trained on synthetic data, which is sufficient for the benchmarks we study but may not transfer to settings with more subtle semantic distinctions. The cross-domain transfer numbers we report give a partial picture, but more extensive evaluation across heterogeneous domains is needed.

Finally, our experiments use English-language benchmarks. Adapting NSR to other languages requires a parser with comparable capability in the target language and a symbolic vocabulary that aligns with the language's semantic distinctions; we have not yet evaluated this and consider it an important direction for follow-up.

## 5.3 Implications for the neural-symbolic debate

NSR provides a data point in the long-running debate over whether neural and symbolic approaches are complementary or competitive. Our results suggest that, at least for compositional generalisation, the combination is meaningfully better than either alone. The key insight is that the neural and symbolic components serve complementary purposes: the neural parser handles the surface ambiguity of natural language, where pure symbolic methods are brittle, while the symbolic executor handles compositional structure, where neural methods are unreliable. Neither component on its own would deliver NSR's accuracy.

This does not, of course, settle the broader debate. There are reasoning tasks for which neither a typed lambda calculus nor any other compact formal system is appropriate, and there are deployment contexts where the engineering overhead of maintaining a symbolic vocabulary is prohibitive. NSR is one point on the design spectrum, not a universal solution.
