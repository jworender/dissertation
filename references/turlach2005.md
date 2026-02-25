# Simultaneous Variable Selection (Turlach, Venables, and Wright, 2005)

## Dissertation Alignment Context
The dissertation proposal uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into {-1,+1} indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Paper
1. **Motivation and objective (Section 1):** The paper targets settings with multiple related responses and seeks one common predictor subset that is jointly useful across responses.
2. **Why separate lasso fits are insufficient (Section 1):** It shows that running single-response lasso models independently can produce unstable, response-specific supports in highly correlated predictor spaces.
3. **Proposed simultaneous-selection model (Section 1.1):** The authors extend lasso by minimizing joint residual sum of squares under a shared sparsity constraint built from per-predictor maxima across responses.
4. **Conceptual framing and related work (Section 2):** The method is interpreted as grouped parameter selection and compared to alternative multivariate/ Bayesian selection approaches and related regularization ideas.
5. **Convex-program reformulation (Section 3):** The estimator is expressed in matrix form as a convex constrained optimization problem over all response coefficients simultaneously.
6. **Solution characterization (Section 3.1):** Subgradient/KKT conditions are derived to describe optimal solutions and the role of the tuning parameter through the Lagrangian system.
7. **Orthonormal-design analysis (Section 3.2):** For orthonormal predictors, the paper develops a homotopy view and shows piecewise-linear solution behavior as the constraint level varies.
8. **General-design algorithm (Section 3.3):** For realistic correlated designs, it gives a primal-dual infeasible interior-point method via a quadratic-program representation with auxiliary variables.
9. **Empirical study (Section 4):** On infrared spectrometry data (24 samples, 14 responses, 770 wavelengths), the method identifies compact shared wavelength sets and shows similar selections with/without an outlying observation.
10. **Extensions and conclusions (Sections 5-6):** The paper discusses handling missing-response entries, reports computational scaling considerations, and concludes that simultaneous subset selection is practical and useful for multiresponse modeling.

## Relevance to the Dissertation
Simultaneous Variable Selection (Turlach, Venables, and Wright, 2005) is directly relevant because it offers a sparse-selection strategy that competes with the proposal's rectification-first approach under multicollinearity.

## Elements from This Paper to Use in the Dissertation
1. Include this method as an explicit baseline on both raw lag-expanded and rectified features.
2. Track support stability, false positives, and lag attribution quality, not only AUC/F1.
3. Reuse discussion around simultaneous, variable, berwin to motivate when penalty-only methods are sufficient.
4. Compare runtime and memory against the rectification + L1 + anytime-rule pipeline.

## Competitive Method Assessment
This paper describes a genuine competing method family. Relative to the dissertation pipeline, it can fall short when raw lag-expanded correlation is so high that support selection remains unstable or when explicit threshold/rule semantics are required. It can excel when linear signal is strong, penalty tuning is mature, and compact logical rules are not the primary requirement.


## Dissertation Citation Traceability

- Chapter: `Background`; Section: `Longitudinal lag expansion and structured sparsity`; Line: `Chapters/02_background.tex:22`; Relevance: Cited to support the statement that Lag expansion is the dominant way to represent temporal effects in classical supervised learning, but it can quickly create high-dimensional, redundant design matrices. Ordered and structured penalties attempt to encode temporal assumptions directly in the coefficient space, for example monotone lag decay or shared supports across tasks.
- Chapter: `Related Work`; Section: `Group, Block, and Ordered Sparsity`; Line: `Chapters/03_relatedwork.tex:29`; Relevance: Cited to support the statement that Structured penalties were developed to stabilize selection when predictors have known organization. Early simultaneous-selection formulations for multiresponse models and later grouped penalties introduced mechanisms that select predictors at the block level rather than coefficient-by-coefficient . This is relevant in longitudinal settings where features can be grouped by channel, basis expansion, or lag family.
- Chapter: `Future Work`; Section: `Workstream A: RQ1 Empirical Strengthening > A2. Baseline expansion under multicollinearity`; Line: `Chapters/88_futurework.tex:37`; Relevance: Cited to support the statement that item Grouped-penalty baselines.
- Chapter: `Conclusion`; Section: `Positioning Relative to Prior Work`; Line: `Chapters/89_conclusion.tex:51`; Relevance: Cited to support the statement that This work extends, rather than replaces, prior sparse and interpretable modeling literature. Relative to classical L1 and elastic-net families , the main difference is intervention point: representation is modified before sparse optimization. Relative to grouped and ordered penalties , this work emphasizes threshold logic and lag-attribution clarity in a longitudinal context. Relative to direct rule-learning approaches , it uses sparse convex fitting as a scalable front end and performs structured rule simplification afterward.
