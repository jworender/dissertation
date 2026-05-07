# Regression Shrinkage and Selection via the Lasso (Tibshirani, 1996)

## Dissertation Alignment Context
The dissertation proposal uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into {-1,+1} indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Paper
1. **Problem setup and motivation:** The paper targets linear regression settings where subset selection is unstable and seeks a method that combines coefficient shrinkage with automatic variable selection.
2. **Lasso formulation:** It introduces the lasso as least squares with an L1 constraint (or equivalent L1-penalized objective), producing sparse coefficient vectors.
3. **Geometric intuition:** The paper explains sparsity through the geometry of the L1 constraint region, where optimization frequently lands on corners corresponding to exact zeros.
4. **Links to prior methods:** It contrasts lasso with ridge regression and subset selection, positioning lasso as an intermediate that keeps shrinkage while performing selection.
5. **Optimization perspective:** It develops practical computation through constrained optimization/Lagrange multiplier viewpoints and path-style reasoning over tuning levels.
6. **Statistical behavior discussion:** The method is analyzed in terms of bias-variance tradeoff, showing how shrinkage can reduce prediction error relative to unpenalized fits.
7. **Model selection and tuning:** It discusses choosing the regularization level (for example with prediction-error criteria), emphasizing that performance depends on the penalty level.
8. **Empirical examples:** Simulations and data examples illustrate sparse recovery behavior and predictive competitiveness versus contemporaneous alternatives.
9. **Extensions beyond Gaussian regression:** The article outlines how the L1 idea can be adapted to broader likelihood settings, motivating later generalized-model lasso work.
10. **Main contribution and impact:** The paper establishes L1 regularization as a practical sparse modeling framework that became foundational for high-dimensional statistics and machine learning.

## Relevance to the Dissertation
Regression Shrinkage and Selection via the Lasso (Tibshirani, 1996) is directly relevant because it offers a sparse-selection strategy that competes with the proposal's rectification-first approach under multicollinearity.

## Elements from This Paper to Use in the Dissertation
1. Include this method as an explicit baseline on both raw lag-expanded and rectified features.
2. Track support stability, false positives, and lag attribution quality, not only AUC/F1.
3. Reuse discussion around its core concepts to motivate when penalty-only methods are sufficient.
4. Compare runtime and memory against the rectification + L1 + anytime-rule pipeline.

## Competitive Method Assessment
This paper describes a genuine competing method family. Relative to the dissertation pipeline, it can fall short when raw lag-expanded correlation is so high that support selection remains unstable or when explicit threshold/rule semantics are required. It can excel when linear signal is strong, penalty tuning is mature, and compact logical rules are not the primary requirement.

## Dissertation Citation Traceability

- Chapter: `Introduction`; Section: `Chapter opening`; Line: `Chapters/01_introduction.tex:18`; Relevance: Cited to support the statement that This strategy is attractive because sparse models can retain predictive performance while reducing dimensionality.
- Chapter: `Introduction`; Section: `Approach`; Line: `Chapters/01_introduction.tex:45`; Relevance: Cited to support the statement that Second, an L1-regularized logistic baseline is fitted on the rectified design, so nonzero coefficients identify candidate feature-lag triggers after the representation has already encoded threshold structure.
- Chapter: `Background`; Section: `Chapter opening`; Line: `Chapters/02_background.tex:5`; Relevance: Cited to support the statement that Sparse modeling with L1 penalties is a standard tool for feature selection in high-dimensional settings because it often yields compact models with useful predictive performance.
- Chapter: `Background`; Section: `L1-regularized models and feature selection`; Line: `Chapters/02_background.tex:10`; Relevance: Cited to support the statement that The LASSO and L1-regularized logistic regression induce sparsity by shrinking many coefficients to exactly zero, creating an embedded feature-selection mechanism inside model fitting.
- Chapter: `Related Work`; Section: `Sparse Regularization Foundations`; Line: `Chapters/03_relatedwork.tex:9`; Relevance: Cited to support the statement that The lasso formulation introduced by Tibshirani established a convex mechanism that performs shrinkage and variable selection simultaneously, making it practical for high-dimensional settings.
- Chapter: `Rectification Improves Sparse Longitudinal Selection (RQ1)`; Section: `Approach`; Line: `Chapters/05_rq1.tex:15`; Relevance: Cited to support the statement that The sparse learner is intentionally ordinary: an L1-regularized logistic model is fit on the rectified design and compared against a matched raw lag-expanded sparse baseline.
- Chapter: `Theoretical Analysis (RQ2)`; Section: `Why RQ2 matters after RQ1 evidence`; Line: `Chapters/06_rq2.tex:21`; Relevance: Cited to support the statement that Lasso is a strong predictive tool, but model-selection consistency depends on structural conditions that may fail under multicollinearity.
- Chapter: `Anytime Rule Compression (RQ3)`; Section: `Approach`; Line: `Chapters/07_rq3.tex:23`; Relevance: Cited to support the statement that where tilde x_ij is the binarized/rectified feature and beta_j is sparse due to the L1 penalty.
- Chapter: `Anytime Rule Compression (RQ3)`; Section: `Approach > Algorithmic Pipeline > 1. Train Baseline Sparse Rectified Model`; Line: `Chapters/07_rq3.tex:43`; Relevance: Cited to support the statement that This baseline defines the reference quality floor for compression.
- Chapter: `Conclusion`; Section: `Positioning Relative to Prior Work`; Line: `Chapters/89_conclusion.tex:56`; Relevance: Cited to support the statement that Relative to classical L1 and elastic-net families, the main difference is intervention point: representation is modified before sparse optimization.
