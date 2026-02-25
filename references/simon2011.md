# Regularization Paths for Cox's Proportional Hazards Model via Coordinate Descent (Simon et al., 2011)

## Dissertation Alignment Context
The dissertation proposal uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into {-1,+1} indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Paper
1. **Problem and motivation (Section 1):** The paper addresses high-dimensional survival modeling where standard Cox fitting is unstable or undefined, and proposes elastic-net regularization for sparse, robust estimation.
2. **Penalized Cox formulation (Sections 1-2):** It optimizes the Cox partial log-likelihood with an elastic-net penalty, covering lasso-like sparsity and ridge-like stabilization in one framework.
3. **Core optimization strategy (Section 2.1):** A pathwise procedure is developed using warm starts over a sequence of \(\lambda\) values, improving numerical efficiency and stability.
4. **Coordinate-descent engine (Section 2.2):** Each path point is solved by cyclical coordinate descent on penalized weighted least-squares approximations derived from local quadratic updates.
5. **Path construction details (Section 2.3):** The algorithm specifies \(\lambda_{max}\), a decreasing \(\lambda\)-grid, and practical lower-cutoff logic to avoid expensive/unstable near-unregularized regions.
6. **Risk-set computational acceleration (Section 2.4):** Efficient cumulative updates exploit the ordered risk-set structure to avoid naive \(O(n^2)\)-style repeated summations.
7. **Practical data-handling extensions (Section 2.5):** The method incorporates observation weights and tied event times (Breslow approximation) without changing the overall algorithmic template.
8. **Convergence/runtime safeguards (Section 2.6):** Deviance-based and step-size checks are used to terminate paths early when additional computation yields negligible modeling gain.
9. **Empirical validation (Section 3):** Simulated and real-data benchmarks show substantial speed improvements and competitive predictive performance relative to contemporaneous Cox-penalization methods.
10. **Model-family extension and implications (Sections 4-6):** The paper discusses effective degrees-of-freedom estimation, extends the approach to logistic models, and positions coordinate-descent regularization paths as a scalable template for generalized models.

## Relevance to the Dissertation
Regularization Paths for Cox's Proportional Hazards Model via Coordinate Descent (Simon et al., 2011) is directly relevant because it offers a sparse-selection strategy that competes with the proposal's rectification-first approach under multicollinearity.

## Elements from This Paper to Use in the Dissertation
1. Include this method as an explicit baseline on both raw lag-expanded and rectified features.
2. Track support stability, false positives, and lag attribution quality, not only AUC/F1.
3. Reuse discussion around journal, statistical, software to motivate when penalty-only methods are sufficient.
4. Compare runtime and memory against the rectification + L1 + anytime-rule pipeline.

## Competitive Method Assessment
This paper describes a genuine competing method family. Relative to the dissertation pipeline, it can fall short when raw lag-expanded correlation is so high that support selection remains unstable or when explicit threshold/rule semantics are required. It can excel when linear signal is strong, penalty tuning is mature, and compact logical rules are not the primary requirement.


## Dissertation Citation Traceability

- No direct citation occurrences were found in the current dissertation chapter files.
