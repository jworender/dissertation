# Stop Explaining Black Box Machine Learning Models for High Stakes Decisions and Use Interpretable Models Instead (Rudin, 2019)

## Dissertation Alignment Context
The dissertation proposal uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into {-1,+1} indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Paper
1. **Core thesis and scope (Abstract + Introduction):** The paper argues that for high-stakes decisions, we should prefer inherently interpretable models over post hoc explanations of black boxes because explanation layers can be misleading and unsafe.
2. **What counts as interpretability (Section 1):** It frames interpretability as domain-specific and emphasizes model-form constraints (for example sparsity, monotonicity, and structure) rather than one universal definition.
3. **Problems with explainable black boxes (Section 2):** The paper details major risks of post hoc explanation, including lack of faithfulness, potential for misleading users, and examples where explanation artifacts can misrepresent what the original model actually computes.
4. **Accuracy-versus-interpretability myth (Section 2/3 discussion):** It challenges the common claim that black boxes are always more accurate, arguing that in many structured-data tasks interpretable models can match predictive performance.
5. **Domain examples and evidence (Section 3):** It uses high-stakes applications (notably criminal justice and healthcare) and the COMPAS-vs-CORELS discussion to show that transparent models can be competitive while being auditable.
6. **Governance and policy recommendations (Section 4):** It proposes stronger accountability mechanisms, including requirements to report interpretable-model performance when deploying black-box systems in sensitive settings.
7. **Algorithmic challenges in interpretable ML (Section 5):** It identifies technical hurdles and organizes them into representative challenge families, including constructing optimal logical models, interpretable linear/additive modeling under constraints, and case-based reasoning approaches.
8. **Conclusion and supporting appendices (Section 6 + Appendices):** It closes by reinforcing the interpretability-first stance for high-stakes use and supplements the main argument with additional details on proprietary models and the accuracy-interpretability narrative.

## Relevance to the Dissertation
Stop Explaining Black Box Machine Learning Models for High Stakes Decisions and Use Interpretable Models Instead (Rudin, 2019) is directly relevant to the proposal's interpretable-model objective and the final anytime rule-compression stage.

## Elements from This Paper to Use in the Dissertation
1. Use this paper's interpretability framing to justify rule-first design decisions.
2. Borrow complexity metrics (rule count, rule length, transparency) for evaluation.
3. Reuse details around stop, explaining, black to improve model reporting and human-auditable outputs.
4. Benchmark rule quality against the proposal's anytime compression stage.

## Competitive Method Assessment
This paper is a direct competitor for interpretable-model construction. Competing rule methods may outperform the dissertation approach when their search objective matches the data regime (e.g., small categorical spaces), but can fall short under large lag-expanded continuous settings where anytime compression is computationally safer.

## Dissertation Citation Traceability

- Chapter: `Introduction`; Section: `Chapter opening`; Line: `Chapters/01_introduction.tex:22`; Relevance: Cited to support the statement that Post hoc explanations of complex models can be useful, but interpretable-model-first approaches are often preferable when transparency, auditability, and operational trust are mandatory.
- Chapter: `Introduction`; Section: `Research Questions`; Line: `Chapters/01_introduction.tex:129`; Relevance: Cited to support the statement that Accordingly, RQ1 tests whether representation-level rectification improves sparse longitudinal selection in practice; RQ2 explains why those improvements should occur and where the theoretical boundary lies; and RQ3 asks whether the recovered sparse structure can be converted into models that are usable in real decision workflows.
- Chapter: `Background`; Section: `Interpretability as a design requirement`; Line: `Chapters/02_background.tex:27`; Relevance: Cited to support the statement that Interpretable-model-first arguments emphasize that transparent model classes are often preferable to post hoc explanations layered on top of black boxes.
- Chapter: `Related Work`; Section: `Interpretable Modeling and Rule-Learning Literature`; Line: `Chapters/03_relatedwork.tex:49`; Relevance: Cited to support the statement that Interpretability-focused literature increasingly argues that high-stakes deployments should prefer inherently interpretable models over post hoc explanations of black boxes whenever performance is competitive.
- Chapter: `Anytime Rule Compression (RQ3)`; Section: `Why RQ3 Matters After RQ1 and RQ2`; Line: `Chapters/07_rq3.tex:11`; Relevance: Cited to support the statement that In interpretability terms, this chapter focuses on the transition from post hoc explanations to inherently interpretable rule structure.
- Chapter: `Anytime Rule Compression (RQ3)`; Section: `Relationship to Adjacent Interpretable Methods`; Line: `Chapters/07_rq3.tex:132`; Relevance: Cited to support the statement that Rule-list and scoring-system approaches provide strong interpretability baselines, but they often optimize directly in combinatorial rule space with different scalability profiles.
- Chapter: `Future Work`; Section: `Prospective Deployment and Human Evaluation`; Line: `Chapters/88_futurework.tex:21`; Relevance: Cited to support the statement that Human-centered validation is especially important in high-stakes environments where explanation quality matters alongside discrimination.
- Chapter: `Conclusion`; Section: `Research Program Summary`; Line: `Chapters/89_conclusion.tex:16`; Relevance: Cited to support the statement that This sequencing is intentional: interpretability claims are weak if support recovery is unstable, and practical rule compression is less meaningful without a credible upstream selection mechanism.
- Chapter: `Conclusion`; Section: `Conclusions by Research Question > RQ3 conclusion: Anytime compression makes interpretability operational`; Line: `Chapters/89_conclusion.tex:35`; Relevance: Cited to support the statement that In real-world data, however, threshold-triggered effects can coexist with smoother additive relationships and with measurement uncertainty, so the more important contribution is the explicit acceptance policy that determines when simplification should be adopted and when the upstream sparse model should be retained.
