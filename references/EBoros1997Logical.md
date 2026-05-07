# Logical Analysis of Numerical Data (Boros et al., 1997)

## Dissertation Alignment Context
The dissertation proposal uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into {-1,+1} indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Paper
1. **Motivation and scope (Introduction):** The paper extends Logical Analysis of Data (LAD) from binary datasets to numerical datasets by formalizing binarization via cut points and indicator variables.
2. **LAD framing and examples:** It introduces the idea of deriving logical explanations (Boolean extensions) that separate positive and negative observations, and uses concrete examples to show how different cut-point choices change model simplicity and interpretability.
3. **Core definitions and preliminaries:** The paper defines partially defined Boolean functions and extension classes (all, monotone/positive, Horn, threshold, linear, quadratic), then recalls feasibility conditions for extensions in these classes.
4. **Master binarization construction:** It develops the concept of a master partially defined Boolean function induced by all potentially useful cut points, establishing a common representation for optimization over binarizations.
5. **Existence and complexity results:** It studies when a numerical dataset admits a binarization compatible with a target logical class, proving polynomial solvability in some settings and NP-hardness in others (notably constrained one-cut-per-attribute variants).
6. **Minimum-cut-point optimization problem:** The main combinatorial problem is to minimize the number of cut points while preserving existence of an extension in a chosen function class.
7. **Integer programming formulations:** It formulates the minimization problem as compact integer programs (including set-cover style formulations for certain classes), enabling practical solution via optimization methods.
8. **Class-specific analysis:** The paper provides separate treatment and formulations for monotone, Horn, threshold, linear, and quadratic function classes, highlighting where structure can be exploited computationally.
9. **Polynomially solvable special cases:** It gives polynomial-time algorithms for selected restricted settings (including bounded dimension and certain low-dimensional monotone cases), showing that tractability depends strongly on structural assumptions.
10. **Overall conclusion:** The work establishes binarization as a rigorous optimization problem within LAD, with a clear theory-computation bridge: some cases are tractable, others are NP-hard, and integer programming offers a practical framework for real data analysis.

## Relevance to the Dissertation
Logical Analysis of Numerical Data (Boros et al., 1997) is directly relevant to the proposal's interpretable-model objective and the final anytime rule-compression stage.

## Elements from This Paper to Use in the Dissertation
1. Use this paper's interpretability framing to justify rule-first design decisions.
2. Borrow complexity metrics (rule count, rule length, transparency) for evaluation.
3. Reuse details around mathematical, programming, logical to improve model reporting and human-auditable outputs.
4. Benchmark rule quality against the proposal's anytime compression stage.

## Competitive Method Assessment
This paper is a direct competitor for interpretable-model construction. Competing rule methods may outperform the dissertation approach when their search objective matches the data regime (e.g., small categorical spaces), but can fall short under large lag-expanded continuous settings where anytime compression is computationally safer.

## Dissertation Citation Traceability

- Chapter: `Introduction`; Section: `Chapter opening`; Line: `Chapters/01_introduction.tex:22`; Relevance: Cited to support the statement that Rule-structured models are especially relevant because they align with human review workflows and can be validated directly by domain experts.
- Chapter: `Related Work`; Section: `Interpretable Modeling and Rule-Learning Literature`; Line: `Chapters/03_relatedwork.tex:53`; Relevance: Cited to support the statement that Classical Logical Analysis of Data (LAD) frameworks formalize binarization and logic-pattern extraction, including optimization-based cut-point selection and pattern construction.
- Chapter: `Related Work`; Section: `Summary of Gaps in Prior Work`; Line: `Chapters/03_relatedwork.tex:106`; Relevance: Cited to support the statement that Rule-learning frameworks deliver transparency, but direct combinatorial optimization can be difficult to scale in high-dimensional longitudinal spaces.
- Chapter: `Anytime Rule Compression (RQ3)`; Section: `Relationship to Adjacent Interpretable Methods`; Line: `Chapters/07_rq3.tex:121`; Relevance: Cited to support the statement that The approach is also related to Logical Analysis of Data (LAD), particularly in its use of thresholded indicators and logical structure, but it targets a different optimization path and deployment interface.
- Chapter: `Future Work`; Section: `Richer Rule Families and Hybrid Models`; Line: `Chapters/88_futurework.tex:17`; Relevance: Cited to support the statement that Such extensions could preserve the current pipeline's transparency while reducing performance loss in settings where post-threshold magnitude still carries predictive information.
