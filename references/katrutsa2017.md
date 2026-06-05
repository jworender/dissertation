# Comprehensive Study of Feature Selection Methods to Solve Multicollinearity (Katrutsa and Strijov, 2017)

## Dissertation Alignment Context
The dissertation proposal uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into {-1,+1} indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Paper
1. **Problem framing and motivation (Section 1):** The paper studies multicollinearity in regression/feature-selection settings, emphasizing instability, redundancy, and over-complex models when predictors are strongly correlated.
2. **Formal problem setup (Section 2):** It separates data fitting from feature selection by defining a subset-selection objective over feature indices (and equivalent binary indicator vectors) rather than only coefficient estimation.
3. **Multicollinearity definitions (Section 2.1):** The authors provide explicit definitions for multicollinearity and related special cases (feature-feature and feature-target relationships) to ground later evaluation criteria.
4. **Quadratic-programming feature selection (Section 3):** The core method minimizes a quadratic objective \(a^TQa - b^Ta\), where \(Q\) encodes pairwise feature similarity and \(b\) encodes feature relevance to the target.
5. **Choice of similarity/relevance functions (Sections 3.1-3.3):** The paper instantiates the framework with Pearson-correlation and mutual-information measures, and also introduces normalized feature significance from t-test p-values as a relevance term.
6. **Convex relaxation and thresholding (Section 3.4):** Because the binary optimization is NP-hard, the method relaxes to a convex domain \(z \in [0,1]^n\) (with \(\ell_1\) constraint), then recovers a selected subset via a tunable significance threshold \(\tau\).
7. **Synthetic benchmark design (Section 4):** Four controlled test configurations are defined (inadequate-correlated, adequate-random, adequate-redundant, adequate-correlated) to probe distinct multicollinearity patterns.
8. **Evaluation framework (Section 5):** Model/subset quality is assessed with VIF, stability (condition-number-based), complexity (subset size), Mallows \(C_p\), and BIC to capture tradeoffs among redundancy, fit, and robustness.
9. **Comparative experiments (Section 6.1-6.2):** The approach is compared with LARS, LASSO, Ridge, Stepwise, Genetic algorithm, and Elastic Net on synthetic and real diesel NIR data; results report strong synthetic performance and competitive real-data behavior.
10. **Threshold tuning and conclusions (Sections 6.3 and 7):** The paper proposes visual tuning of \(\tau\) using criterion/error curves and concludes that the QP method provides a practical way to obtain less redundant, more stable feature subsets under multicollinearity.

## Relevance to the Dissertation
Comprehensive Study of Feature Selection Methods to Solve Multicollinearity (Katrutsa and Strijov, 2017) is relevant background that helps position the proposal among existing longitudinal, sparse, and interpretable modeling approaches.

## Elements from This Paper to Use in the Dissertation
1. Use this reference to strengthen the related-work bridge to the dissertation pipeline.
2. Extract terminology and assumptions that clarify modeling constraints in longitudinal settings.
3. Reuse details around comprehensive, solve, multicollinearity to sharpen experiment design and discussion.
4. Tie this reference to ablations comparing raw, rectified, and compressed models.

## Competitive Method Assessment
This paper does not present the main competing algorithmic pipeline. It is most useful for problem framing, benchmark selection, and identifying contexts where interpretable lag-aware rules are preferable to opaque alternatives.

## Dissertation Citation Traceability

- Chapter: `Introduction`; Section: `Chapter opening`; Line: `Chapters/01_introduction.tex:20`; Relevance: Cited to support the statement that Correlation-aware variants in domain-specific contexts further reinforce this point: dependence can be mitigated, but stable, interpretable attribution remains difficult when predictors are densely coupled.
- Chapter: `Related Work`; Section: `Group, Block, and Ordered Sparsity`; Line: `Chapters/03_relatedwork.tex:39`; Relevance: Cited to support the statement that Katrutsa and Strijov proposed a quadratic-programming feature-selection framework where pairwise similarity and target relevance are balanced in a convex relaxation.
- Chapter: `Rectification Improves Sparse Longitudinal Selection (RQ1)`; Section: `Comparison to competing feature-selection baselines`; Line: `Chapters/05_rq1.tex:270`; Relevance: Cited to support the statement that A focused comparator is the quadratic-programming selector of Katrutsa and Strijov, which optimizes a relevance-redundancy objective using pairwise similarity structure.
