# The Group Lasso for Logistic Regression (Meier, van de Geer, and Buhlmann, 2008)

## Dissertation Alignment Context
The dissertation proposal uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into {-1,+1} indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Paper
1. **Motivation and setting (Section 1):** The paper extends group lasso from linear regression to logistic regression, targeting grouped variable selection that is invariant to within-group orthogonal reparameterizations.
2. **Model formulation (Section 2.1):** Logistic group lasso is defined as penalized negative log-likelihood with an \(\ell_2\)-norm per predefined group (and no penalty on the intercept), typically scaled by \(\sqrt{df_g}\).
3. **Interpretive effect of the penalty (Section 2.1):** The mixed penalty encourages sparsity at the group level, i.e., predictors tend to enter or leave the model by groups rather than by isolated coefficients.
4. **Primary optimization strategy (Section 2.2.1):** A block coordinate descent procedure is developed for direct optimization of the convex penalized objective, including groupwise zero-check conditions and iterative block updates.
5. **Fast alternative strategy (Section 2.2.2):** A block coordinate gradient-descent variant is proposed, with convergence guarantees and applicability beyond logistic regression to generalized linear models.
6. **Algorithmic comparison (Section 2.3):** The authors compare their methods against contemporaneous approaches (including blockwise sparse regression and path-following variants), emphasizing practical convergence reliability and high-dimensional scalability.
7. **High-dimensional theory (Section 2.4):** Under sparsity and regularity assumptions, the paper provides global consistency results when the number of groups can exceed sample size, with rates depending on \(\log(G)\), sample size, and sparsity.
8. **Two-stage refinement (Section 3.1):** A group lasso-ridge hybrid is introduced: first perform group selection by group lasso, then refit/shrink within the selected model using a ridge-type second stage.
9. **Hierarchical modeling extension (Section 3.2):** The two-stage framework is adapted to enforce hierarchical structures (e.g., interaction/main-effect hierarchy), using ridge in stage two to avoid unintended additional selection.
10. **Empirical evidence and application (Sections 4-6):** Simulations and splice-site DNA experiments show competitive or improved prediction with smaller, more interpretable models for the hybrid approach, while confirming practical effectiveness of the proposed optimization framework.

## Relevance to the Dissertation
The Group Lasso for Logistic Regression (Meier, van de Geer, and Buhlmann, 2008) is directly relevant because it offers a sparse-selection strategy that competes with the proposal's rectification-first approach under multicollinearity.

## Elements from This Paper to Use in the Dissertation
1. Include this method as an explicit baseline on both raw lag-expanded and rectified features.
2. Track support stability, false positives, and lag attribution quality, not only AUC/F1.
3. Reuse discussion around royal, statistical, society to motivate when penalty-only methods are sufficient.
4. Compare runtime and memory against the rectification + L1 + anytime-rule pipeline.

## Competitive Method Assessment
This paper describes a genuine competing method family. Relative to the dissertation pipeline, it can fall short when raw lag-expanded correlation is so high that support selection remains unstable or when explicit threshold/rule semantics are required. It can excel when linear signal is strong, penalty tuning is mature, and compact logical rules are not the primary requirement.

## Dissertation Citation Traceability

- Chapter: `Introduction`; Section: `Chapter opening`; Line: `Chapters/01_introduction.tex:20`; Relevance: Cited to support the statement that A substantial body of work addresses these issues through penalty design and optimization advances, including elastic net, adaptive lasso, group-based penalties, and ordered lag constraints.
- Chapter: `Related Work`; Section: `Group, Block, and Ordered Sparsity`; Line: `Chapters/03_relatedwork.tex:31`; Relevance: Cited to support the statement that Group lasso for logistic regression and blockwise sparse regression improved feasibility in high-dimensional designs, while unified majorization-descent solvers strengthened practical convergence.
- Chapter: `Rectification Improves Sparse Longitudinal Selection (RQ1)`; Section: `Comparison to competing feature-selection baselines`; Line: `Chapters/05_rq1.tex:243`; Relevance: Cited to support the statement that Group and block-structured sparse families remain important comparators because they are explicitly designed for correlated predictor settings.
- Chapter: `Conclusion`; Section: `Positioning Relative to Prior Work`; Line: `Chapters/89_conclusion.tex:56`; Relevance: Cited to support the statement that Relative to grouped and ordered penalties, this work emphasizes threshold logic and lag-attribution clarity in a longitudinal context.
