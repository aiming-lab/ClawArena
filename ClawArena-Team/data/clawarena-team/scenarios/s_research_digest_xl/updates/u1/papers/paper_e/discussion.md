# 5. Discussion

FedAlign closes a substantial portion of the long-standing gap between federated and centralised fine-tuning of large language models, doing so while providing a rigorous differential privacy guarantee. In this section we situate the work, discuss its limitations, and consider practical deployment implications.

## 5.1 Related work

FedAlign builds on a substantial federated learning literature. **FedAvg** is the canonical baseline; **FedProx** adds a proximal term that penalises drift from the global model in parameter space; **SCAFFOLD** uses control variates to correct the bias induced by heterogeneous data. FedAlign's alignment regulariser is conceptually closest to FedProx but differs in two ways: it operates in *representation space* rather than parameter space (which we find is a better proxy for the model's functional behaviour), and it is computed on public anchor inputs rather than on the client's private data (which makes it compatible with selective clipping). Both differences are essential to the empirical gains we report.

Within the differential privacy literature, our work uses the standard DP-SGD mechanism and the moments accountant for composition. The novel ingredient is selective clipping, which exploits the fact that the regularisation gradient is data-independent. The general technique of decomposing a gradient into data-dependent and data-independent parts to reduce privacy cost has appeared in prior work on auxiliary losses, but to our knowledge it has not been applied to federated alignment in this form.

The broader question of how to combine federated learning with privacy guarantees has been studied for many years. We are not the first to argue for the combination, but the empirical gains we report — particularly the 19-point improvement over DP-FedAvg — are large enough to make the combination practical for the first time at the language-model scale.

## 5.2 Limitations

Three limitations are worth noting. First, FedAlign assumes that the clients agree on a set of public anchor inputs at the start of training. In some deployments, finding suitable anchors is non-trivial — for example, when the clients all operate in a closed domain (medical or legal) where most relevant text is non-public. In such cases the alignment regulariser may be computed on out-of-domain anchors, which degrades its effectiveness. We have begun exploring techniques for generating synthetic in-domain anchors that themselves satisfy a DP guarantee; the early results are encouraging and will be reported in follow-up work.

Second, our experiments assume reliable client participation and stable network conditions. In real deployments, clients may join and leave the federation unpredictably, and stale updates from disconnected clients can degrade the global model. FedAlign inherits the standard federated learning mitigations for these issues (asynchronous aggregation, client sampling) but does not address them directly.

Third, the privacy guarantee we provide is at the level of the model update, not at the level of individual training examples. Stronger guarantees (such as personalised DP that allows each client to choose its own privacy budget) are a natural extension and are the subject of ongoing work.

## 5.3 Deployment considerations

We have prototyped FedAlign on three production-like scenarios. Two recurring lessons are worth recording. First, the choice of anchor inputs has a measurable effect on the alignment regulariser's quality, and practitioners should plan to invest in curating anchors that are representative of the deployed model's input distribution. Second, the privacy budget is a fixed resource that should be allocated thoughtfully across training rounds; a uniform allocation is rarely optimal, and adaptive budgeting based on the validation-loss trajectory consistently outperforms it.

We have also engaged with privacy reviewers about the empirical validation of our DP guarantee. The membership inference AUC we report is a useful confidence check but is not a substitute for the formal accountant; deployments should rely on the accountant for the privacy claim and use empirical attacks only as a defence-in-depth signal.
