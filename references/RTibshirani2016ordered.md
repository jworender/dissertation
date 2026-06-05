# An Ordered Lasso and Sparse Time-Lagged Regression (Tibshirani et al., 2016)

## Dissertation Alignment Context
The dissertation proposal uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into {-1,+1} indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Paper
1. **Motivation and core idea (Section 1):** The paper introduces an order-constrained variant of LASSO for settings where coefficient magnitudes should decay along a known feature order.
2. **Ordered LASSO formulation (Section 2.1):** It augments the standard \(\ell_1\)-penalized regression with monotonicity constraints on positive/negative coefficient components to enforce ordered shrinkage.
3. **Convex optimization strategy (Section 2.2):** The method is solved efficiently with proximal gradient updates whose proximal operator is isotonic regression (PAVA), making large problems practical.
4. **Empirical contrast with standard LASSO (Section 2.3):** Simulations show improved recovery when the true coefficients follow monotone decay, with reduced tail fluctuations relative to unconstrained LASSO.
5. **Strongly ordered variant (Section 2.4):** A two-stage extension is proposed to enforce monotonicity in absolute value, yielding a stationary point for the non-convex absolute-order target.
6. **Alternative relaxations (Sections 2.5-2.6):** The paper discusses looser convex and near-isotonic formulations that soften strict monotonicity while retaining efficient computation.
7. **Static time-lagged regression (Section 3.1):** Ordered constraints are applied blockwise over lags per predictor, allowing automatic truncation of effective lag length via sparsity plus monotone decay.
8. **Rolling prediction and AR settings (Sections 3.2 and 3.6):** The framework is adapted to sequential forecasting and autoregressive models, where it gives interpretable lag profiles and competitive order recovery.
9. **Real/simulated time-series evidence (Sections 3.4-3.5):** Experiments (including Los Angeles ozone data) show lower validation error than cross-sectional baselines and more interpretable lag structures than unconstrained LASSO.
10. **Generalizations and diagnostics (Sections 4-6):** The paper discusses degrees-of-freedom estimates, extends the method to logistic regression (and GLM-style IRLS updates), and outlines broader dynamic prediction applications.

## Relevance to the Dissertation
An Ordered Lasso and Sparse Time-Lagged Regression (Tibshirani et al., 2016) is directly relevant because it offers a sparse-selection strategy that competes with the proposal's rectification-first approach under multicollinearity.

## Elements from This Paper to Use in the Dissertation
1. Include this method as an explicit baseline on both raw lag-expanded and rectified features.
2. Track support stability, false positives, and lag attribution quality, not only AUC/F1.
3. Reuse discussion around ordered, sparse, time-lagged to motivate when penalty-only methods are sufficient.
4. Compare runtime and memory against the rectification + L1 + anytime-rule pipeline.

## Competitive Method Assessment
This paper describes a genuine competing method family. Relative to the dissertation pipeline, it can fall short when raw lag-expanded correlation is so high that support selection remains unstable or when explicit threshold/rule semantics are required. It can excel when linear signal is strong, penalty tuning is mature, and compact logical rules are not the primary requirement.

## Dissertation Citation Traceability

- Chapter: `Introduction`; Section: `Chapter opening`; Line: `Chapters/01_introduction.tex:20`; Relevance: Cited to support the statement that A substantial body of work addresses these issues through penalty design and optimization advances, including elastic net, adaptive lasso, group-based penalties, and ordered lag constraints.
- Chapter: `Background`; Section: `Longitudinal lag expansion and structured sparsity`; Line: `Chapters/02_background.tex:22`; Relevance: Cited to support the statement that One general response is to impose temporal or group structure directly in coefficient space, for example through monotone lag assumptions or shared-support assumptions.
- Chapter: `Related Work`; Section: `Group, Block, and Ordered Sparsity`; Line: `Chapters/03_relatedwork.tex:33`; Relevance: Cited to support the statement that Ordered lasso introduces monotonicity constraints across lag coefficients, reflecting assumptions such as decaying lag influence and yielding interpretable lag profiles when those assumptions hold.
- Chapter: `Related Work`; Section: `Summary of Gaps in Prior Work`; Line: `Chapters/03_relatedwork.tex:105`; Relevance: Cited to support the statement that Structured and dependence-aware penalties improve behavior in specific regimes, yet usually remain tied to raw correlated representations and do not produce threshold-native logic outputs.
- Chapter: `Rectification Improves Sparse Longitudinal Selection (RQ1)`; Section: `Comparison to competing feature-selection baselines`; Line: `Chapters/05_rq1.tex:268`; Relevance: Cited to support the statement that Group and block-structured sparse families remain important comparators because they are explicitly designed for correlated predictor settings.
- Chapter: `Theoretical Analysis (RQ2)`; Section: `How this differs from penalty-only fixes`; Line: `Chapters/06_rq2.tex:229`; Relevance: Cited to support the statement that Existing work already proposes many penalty-level fixes for dependence, including elastic net, adaptive penalties, and grouped or ordered structures.
- Chapter: `Conclusion`; Section: `Positioning Relative to Prior Work`; Line: `Chapters/89_conclusion.tex:56`; Relevance: Cited to support the statement that Relative to grouped and ordered penalties, this work emphasizes threshold logic and lag-attribution clarity in a longitudinal context.
