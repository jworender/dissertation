# Definitions, Methods, and Applications in Interpretable Machine Learning (Murdoch et al., 2019)

## Dissertation Alignment Context
The dissertation proposal uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into {-1,+1} indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Paper
1. **Problem framing and objective (Section 1):** The paper formalizes interpretable machine learning as extracting model/data relationships that provide useful insight for a specific  audience.
2. **Literature positioning (Section 2):** It distinguishes interpretable ML from adjacent topics (especially causal inference and stability) and surveys prior explainability work that lacked a unifying framework.
3. **Data-science life-cycle placement (Section 3):** Interpretability is organized within a problem-data-model-post hoc loop, clarifying where different interpretation methods are applied.
4. **PDR framework (Section 4):** The authors introduce three evaluation desiderata: predictive accuracy, descriptive accuracy, and relevancy to the target audience.
5. **Core tradeoff articulation (Section 4):** A central tension is identified between predictive and descriptive accuracy, motivating careful method choice rather than one-size-fits-all interpretability claims.
6. **Model-based interpretability taxonomy (Section 5):** The paper categorizes model-based approaches into sparsity, simulatability, modularity, and feature-engineering strategies (domain-based and model-based).
7. **Model-based examples and cautions (Section 5):** Real applications (for example healthcare and genomics) illustrate benefits of transparent models while emphasizing stability checks before drawing conclusions.
8. **Post hoc interpretability taxonomy (Section 6):** Post hoc methods are split into dataset-level and prediction-level analyses, including feature/interaction importances, visualizations, and trend/outlier diagnostics.
9. **Evaluation limitations and methodology (Section 7):** The paper highlights weak evaluation practices (e.g., cherry-picked explanations) and recommends stronger validation via simulations, domain tasks, and human studies.
10. **Main conclusion and agenda (Section 7):** It calls for a shared vocabulary and rigorous measurement standards so interpretability methods can be selected and trusted according to concrete problem and audience needs.

## Relevance to the Dissertation
Definitions, Methods, and Applications in Interpretable Machine Learning (Murdoch et al., 2019) is directly relevant to the proposal's interpretable-model objective and the final anytime rule-compression stage.

## Elements from This Paper to Use in the Dissertation
1. Use this paper's interpretability framing to justify rule-first design decisions.
2. Borrow complexity metrics (rule count, rule length, transparency) for evaluation.
3. Reuse details around statistics, nitions, applications to improve model reporting and human-auditable outputs.
4. Benchmark rule quality against the proposal's anytime compression stage.

## Competitive Method Assessment
This paper is a direct competitor for interpretable-model construction. Competing rule methods may outperform the dissertation approach when their search objective matches the data regime (e.g., small categorical spaces), but can fall short under large lag-expanded continuous settings where anytime compression is computationally safer.

## Dissertation Citation Traceability

- Chapter: `Introduction`; Section: `Chapter opening`; Line: `Chapters/01_introduction.tex:22`; Relevance: Cited to support the statement that Post hoc explanations of complex models can be useful, but interpretable-model-first approaches are often preferable when transparency, auditability, and operational trust are mandatory.
- Chapter: `Introduction`; Section: `Research Questions`; Line: `Chapters/01_introduction.tex:129`; Relevance: Cited to support the statement that Accordingly, RQ1 tests whether representation-level rectification improves sparse longitudinal selection in practice; RQ2 explains why those improvements should occur and where the theoretical boundary lies; and RQ3 asks whether the recovered sparse structure can be converted into models that are usable in real decision workflows.
- Chapter: `Introduction`; Section: `Evaluation Priorities`; Line: `Chapters/01_introduction.tex:137`; Relevance: Cited to support the statement that Interpretability complexity: active-feature count, rule count, and rule length as direct proxies for human audit burden.
- Chapter: `Background`; Section: `Interpretability as a design requirement`; Line: `Chapters/02_background.tex:27`; Relevance: Cited to support the statement that Interpretable-model-first arguments emphasize that transparent model classes are often preferable to post hoc explanations layered on top of black boxes.
- Chapter: `Related Work`; Section: `Interpretable Modeling and Rule-Learning Literature`; Line: `Chapters/03_relatedwork.tex:49`; Relevance: Cited to support the statement that Interpretability-focused literature increasingly argues that high-stakes deployments should prefer inherently interpretable models over post hoc explanations of black boxes whenever performance is competitive.
- Chapter: `Anytime Rule Compression (RQ3)`; Section: `Why RQ3 Matters After RQ1 and RQ2`; Line: `Chapters/07_rq3.tex:11`; Relevance: Cited to support the statement that In interpretability terms, this chapter focuses on the transition from post hoc explanations to inherently interpretable rule structure.
- Chapter: `Anytime Rule Compression (RQ3)`; Section: `Motivation and Application Context`; Line: `Chapters/07_rq3.tex:22`; Relevance: Cited to support the statement that The anytime mechanism then provides a tunable point on the complexity-performance frontier for each deployment constraint.
- Chapter: `Future Work`; Section: `Prospective Deployment and Human Evaluation`; Line: `Chapters/88_futurework.tex:21`; Relevance: Cited to support the statement that Human-centered validation is especially important in high-stakes environments where explanation quality matters alongside discrimination.
- Chapter: `Conclusion`; Section: `Research Program Summary`; Line: `Chapters/89_conclusion.tex:16`; Relevance: Cited to support the statement that This sequencing is intentional: interpretability claims are weak if support recovery is unstable, and practical rule compression is less meaningful without a credible upstream selection mechanism.
- Chapter: `Conclusion`; Section: `Conclusions by Research Question > RQ3 conclusion: Anytime compression makes interpretability operational`; Line: `Chapters/89_conclusion.tex:35`; Relevance: Cited to support the statement that In real-world data, however, threshold-triggered effects can coexist with smoother additive relationships and with measurement uncertainty, so the more important contribution is the explicit acceptance policy that determines when simplification should be adopted and when the upstream sparse model should be retained.
- Chapter: `Conclusion`; Section: `Scope Boundaries and Limitations`; Line: `Chapters/89_conclusion.tex:72`; Relevance: Cited to support the statement that These boundaries are consistent with broader evidence that no sparse-selection or interpretable-modeling method is uniformly optimal across all dependence structures and objectives.
