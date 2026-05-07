# Feature Selection, L1 vs. L2 Regularization, and Rotational Invariance (Ng, 2004)

## Dissertation Alignment Context
The dissertation proposal uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into {-1,+1} indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Paper
1. **Problem setup and motivation (Introduction):** The paper studies supervised learning with many irrelevant features and asks how regularization choice affects sample complexity and overfitting.
2. **Modeling framework (Preliminaries):** It formulates logistic regression with regularization, contrasting L1 and L2 penalties, and presents the constrained form with a norm budget selected by hold-out validation.
3. **Main positive result for L1:** The central theorem shows that, when only a small number of features are truly relevant, L1-regularized logistic regression can achieve sample complexity that grows only logarithmically with the number of irrelevant features.
4. **Rotational invariance analysis:** The paper defines rotationally invariant learners and proves a lower-bound result that such methods (including typical L2-style formulations) can require sample complexity that grows at least linearly with irrelevant dimensions in worst-case settings.
5. **Algorithm class implications:** It discusses why this lower-bound applies broadly to several common model families and highlights L1 methods as non-rotationally invariant alternatives better suited to sparse-relevance regimes.
6. **Empirical study:** Synthetic experiments compare L1 vs L2 logistic regression across increasing dimensionality, different relevance patterns (single relevant feature, few relevant features, exponentially decaying relevance), and two training-set sizes; L1 remains substantially more robust as irrelevant dimensions increase.
7. **Technical appendix:** Proof details are provided using covering-number and uniform-convergence arguments to support the theoretical sample-complexity claims.

## Relevance to the Dissertation
Feature Selection, L1 vs. L2 Regularization, and Rotational Invariance (Ng, 2004) is directly relevant because it offers a sparse-selection strategy that competes with the proposal's rectification-first approach under multicollinearity.

## Elements from This Paper to Use in the Dissertation
1. Include this method as an explicit baseline on both raw lag-expanded and rectified features.
2. Track support stability, false positives, and lag attribution quality, not only AUC/F1.
3. Reuse discussion around latest, updates, article to motivate when penalty-only methods are sufficient.
4. Compare runtime and memory against the rectification + L1 + anytime-rule pipeline.

## Competitive Method Assessment
This paper describes a genuine competing method family. Relative to the dissertation pipeline, it can fall short when raw lag-expanded correlation is so high that support selection remains unstable or when explicit threshold/rule semantics are required. It can excel when linear signal is strong, penalty tuning is mature, and compact logical rules are not the primary requirement.

## Dissertation Citation Traceability

- Chapter: `Introduction`; Section: `Chapter opening`; Line: `Chapters/01_introduction.tex:18`; Relevance: Cited to support the statement that This strategy is attractive because sparse models can retain predictive performance while reducing dimensionality.
- Chapter: `Background`; Section: `Chapter opening`; Line: `Chapters/02_background.tex:5`; Relevance: Cited to support the statement that Sparse modeling with L1 penalties is a standard tool for feature selection in high-dimensional settings because it often yields compact models with useful predictive performance.
- Chapter: `Related Work`; Section: `Sparse Regularization Foundations`; Line: `Chapters/03_relatedwork.tex:11`; Relevance: Cited to support the statement that In sparse-relevance regimes, L1 methods can scale better with growing nuisance dimensionality than rotationally invariant alternatives.
