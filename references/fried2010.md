# Regularization Paths for Generalized Linear Models via Coordinate Descent (Friedman et al., 2010)

## Dissertation Alignment Context
The dissertation proposal uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into {-1,+1} indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Paper
1. **Motivation and scope (Introduction):** The paper develops fast pathwise algorithms for fitting generalized linear models with convex penalties, focusing on lasso, ridge, and elastic-net regularization.
2. **Core optimization setup:** It formulates penalized objectives for linear and generalized linear models and emphasizes regularization paths (many \(\lambda\) values) rather than one-off optimization.
3. **Coordinate-descent foundation (Section 2):** The central method is cyclical coordinate descent with warm starts, including the soft-thresholding update for \(\ell_1\)-penalized coefficients.
4. **Computational accelerations:** The paper presents covariance updates, sparse-matrix handling, weighted updates, and active-set style implementation details that dramatically reduce runtime in high dimensions.
5. **Pathwise strategy and tuning grid:** It explains how to start from \(\lambda_{\max}\) (all-zero coefficients) and descend on a log-scaled grid, leveraging previous solutions for stability and speed.
6. **Binomial logistic regression extension (Section 3):** The same coordinate-descent framework is embedded inside IRLS/Newton-style updates to handle two-class logistic models with regularization.
7. **Multinomial regression extension (Section 4):** The algorithm is generalized to multi-class logistic models, including treatment of parameter non-identifiability and penalty-aware re-centering.
8. **Grouped/matrix response handling:** The implementation supports grouped outcomes and observation weights, broadening applicability to practical data formats.
9. **Empirical timing comparisons (later sections):** Extensive benchmarks show the proposed implementation (glmnet) is substantially faster than competing methods across dense/sparse settings and varying \(n,p\), while tracing full regularization paths.
10. **Practical tools and model selection:** The paper includes cross-validation usage and software details, positioning the method as a production-ready framework for scalable sparse GLM fitting.

## Relevance to the Dissertation
Regularization Paths for Generalized Linear Models via Coordinate Descent (Friedman et al., 2010) is directly relevant because it offers a sparse-selection strategy that competes with the proposal's rectification-first approach under multicollinearity.

## Elements from This Paper to Use in the Dissertation
1. Include this method as an explicit baseline on both raw lag-expanded and rectified features.
2. Track support stability, false positives, and lag attribution quality, not only AUC/F1.
3. Reuse discussion around journal, statistical, software to motivate when penalty-only methods are sufficient.
4. Compare runtime and memory against the rectification + L1 + anytime-rule pipeline.

## Competitive Method Assessment
This paper describes a genuine competing method family. Relative to the dissertation pipeline, it can fall short when raw lag-expanded correlation is so high that support selection remains unstable or when explicit threshold/rule semantics are required. It can excel when linear signal is strong, penalty tuning is mature, and compact logical rules are not the primary requirement.


## Dissertation Citation Traceability

- Chapter: `Introduction`; Section: `Thesis Organization`; Line: `Chapters/01_introduction.tex:45`; Relevance: Cited to support the statement that Following this introduction, the dissertation is organized as follows. The background chapter formalizes longitudinal feature-learning assumptions, sparse regularization foundations, and interpretability criteria, and then positions related methods in grouped, ordered, and dependence-aware selection . The methodology chapter presents the rectification algorithm, sparse fitting procedure, and anytime rule-compression mechanism in unified notation, including implementation details needed for reproducibility.
- Chapter: `Background`; Section: `L1-regularized models and feature selection`; Line: `Chapters/02_background.tex:12`; Relevance: Cited to support the statement that Modern implementations make these methods computationally practical at scale: coordinate-descent path algorithms with warm starts support efficient generalized linear modeling across many tuning values . Beyond plain L1 penalties, elastic net, adaptive lasso, and group-aware variants address correlated and block-structured predictors, which is directly relevant for lagged longitudinal features.
- Chapter: `Related Work`; Section: `Sparse Regularization Foundations`; Line: `Chapters/03_relatedwork.tex:13`; Relevance: Cited to support the statement that A second reason this family became dominant is computational maturity. Coordinate-descent path algorithms provide efficient fitting across full regularization paths for generalized linear models and related objectives . These advances made sparse modeling feasible at operational scales and enabled cross-validated tuning in realistic workflows rather than one-off, expensive optimization.
- Chapter: `Anytime Rule Compression (RQ3)`; Section: `From Rectified Sparse Models to Rule Space`; Line: `Chapters/07_rq3.tex:19`; Relevance: Cited to support the statement that where is the binarized/rectified feature and is sparse due to the L1 penalty . Let the active set be . RQ3 starts from this fitted model and asks whether we can replace the full weighted sum with a smaller rule that preserves operating performance.
- Chapter: `Anytime Rule Compression (RQ3)`; Section: `Algorithmic Pipeline > 1. Train Baseline Sparse Rectified Model`; Line: `Chapters/07_rq3.tex:39`; Relevance: Cited to support the statement that Fit L1-regularized logistic regression on the rectified matrix and compute baseline operating metrics (AUC, , sensitivity, specificity) at the chosen operating threshold. This baseline defines the reference quality floor for compression.
- Chapter: `Future Work`; Section: `Workstream A: RQ1 Empirical Strengthening > A2. Baseline expansion under multicollinearity`; Line: `Chapters/88_futurework.tex:35`; Relevance: Cited to support the statement that item L1 and elastic-net path baselines.
- Chapter: `Conclusion`; Section: `Positioning Relative to Prior Work`; Line: `Chapters/89_conclusion.tex:51`; Relevance: Cited to support the statement that This work extends, rather than replaces, prior sparse and interpretable modeling literature. Relative to classical L1 and elastic-net families , the main difference is intervention point: representation is modified before sparse optimization. Relative to grouped and ordered penalties , this work emphasizes threshold logic and lag-attribution clarity in a longitudinal context. Relative to direct rule-learning approaches , it uses sparse convex fitting as a scalable front end and performs structured rule simplification afterward.
