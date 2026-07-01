# 3. Method

FedAlign is a federated fine-tuning algorithm that operates over `K` clients connected to a central aggregator. Each round of training consists of (a) the aggregator broadcasting the current global model and a small set of public *anchor inputs*; (b) each client performing some number of local optimisation steps on its private data, regularised by an alignment term computed against the anchors; (c) each client clipping and noising its weight update under a differential privacy mechanism; and (d) the aggregator averaging the noised updates. The procedure is closely related to FedAvg and DP-FedAvg, but the alignment regulariser is the new ingredient that controls client drift.

## 3.1 Anchor inputs and the alignment regulariser

The alignment regulariser is computed against a fixed set of `A` public anchor inputs. The anchors are drawn from publicly available, non-sensitive text — for example, news articles, Wikipedia, or open-source code repositories — and are agreed upon by all clients and the aggregator at the start of training. Roughly 4096 anchors are typically sufficient.

At the start of each round, the aggregator computes the global model's *intermediate representations* on the anchors — specifically, the activations at a chosen subset of the model's layers — and broadcasts these representations along with the model itself. The representations occupy roughly 1% of the bandwidth of the model parameters themselves and add a negligible communication overhead.

During local training, each client computes the same intermediate representations on the anchors under its current local model and adds a regularisation term to its loss:

```
L_align = (1 / A) Σ_a || h_local(a) - h_global(a) ||^2
```

This term penalises any drift of the client's intermediate representations on the anchors away from the global model's. Because the anchors are public and shared across clients, the regulariser does not require any private data and does not create a side channel through which one client could learn about another's data.

The regulariser's effect on convergence under heterogeneous data can be characterised: under standard convexity assumptions, the alignment term provides a Lyapunov function that bounds the divergence between clients' local trajectories, which in turn bounds the cost of the heterogeneity. The formal statement is given as Theorem 1 in the paper.

## 3.2 Differential privacy mechanism

FedAlign uses a per-client DP-SGD mechanism. Each client computes its weight update, clips it to a norm bound `C`, and adds Gaussian noise with variance proportional to `(C / N) · σ²`, where `N` is a normalising factor and `σ` is the noise multiplier. The aggregator then averages the noised updates with a Federated Averaging step.

A subtle point is the interaction between the alignment regulariser and the privacy mechanism. The regulariser is computed on public anchor inputs, so the regularisation gradient itself carries no privacy cost — it is data-independent in the DP sense. We exploit this by clipping only the data-dependent portion of the gradient (the standard SGD term on the client's private examples), while leaving the regularisation gradient unclipped. This keeps the privacy budget identical to DP-FedAvg while allowing the regulariser to contribute its full magnitude to the update. We refer to this as **selective clipping**, and it is a key part of how FedAlign achieves accuracy gains without spending additional privacy budget.

## 3.3 Aggregator-side update

The aggregator averages the noised updates using standard FedAvg weighting (proportional to each client's number of local examples, subject to a cap that prevents large clients from dominating). The aggregator does not see any private data; it sees only the noised weight updates, which are protected by the DP guarantee.

After updating the global model, the aggregator recomputes the intermediate representations on the anchors and broadcasts them along with the new global model for the next round.

## 3.4 Communication and computational cost

FedAlign's communication overhead relative to DP-FedAvg consists of the broadcast of the anchor representations — roughly 1% of the cost of the model parameter broadcast, which is itself the dominant per-round cost. The computational overhead is the per-client forward pass on the anchors, which costs roughly 0.5% of a typical local-training round. Both overheads are negligible in practice, and the algorithm is amenable to the same communication-efficiency optimisations (compression, partial participation) as standard FedAvg.

## 3.5 Implementation details

We provide a reference implementation in PyTorch that integrates with the Flower and FedML federated learning frameworks. The implementation supports both full-parameter fine-tuning and LoRA-style low-rank adaptation; the latter is more practical for very large models, and we report results for both configurations in the next section.
