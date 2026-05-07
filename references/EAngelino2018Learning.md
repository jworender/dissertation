# Learning Certifiably Optimal Rule Lists for Categorical Data (Angelino et al., 2018)

## Dissertation Alignment Context
The dissertation proposal uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into {-1,+1} indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Paper
1. **Problem framing and motivation (Introduction):** The paper targets interpretable classification on categorical data using rule lists, emphasizing that high-stakes settings need transparent models with provable optimality rather than heuristic approximations.
2. **Core objective:** It defines a regularized empirical-risk objective for rule lists (accuracy plus sparsity penalty), so optimization explicitly balances predictive performance and interpretability.
3. **Related-work positioning:** The paper contrasts CORELS with greedy decision-tree/rule-list methods and Bayesian or MIP-based alternatives, arguing that prior methods generally lack practical certificates of global optimality at useful scale.
4. **Optimization framework (Learning Optimal Rule Lists):** It presents branch-and-bound search over rule-list prefixes and introduces a hierarchy of bounds to prune large portions of the combinatorial search space.
5. **Key theoretical pruning results (Section 3 subsections):** The method derives bounds on prefix length, number of prefix evaluations, antecedent support, symmetry/permutation equivalence, and equivalent-point structure, each tightening search and preserving optimality guarantees.
6. **Incremental computation strategy (Section 4):** It shows how objective values and lower bounds are updated incrementally from parent prefixes to children, avoiding redundant computation during search.
7. **Systems implementation (Section 5):** The paper details the prefix-tree cache, queue/search policy design, symmetry-aware map, incremental execution mechanics, and memory-management/garbage-collection choices that make exact optimization practical.
8. **Experimental evaluation (Section 6):** It evaluates predictive performance, model size, runtime behavior, and pruning efficiency across multiple datasets, including recidivism and weapon-prediction tasks, and compares against black-box and heuristic baselines.
9. **Empirical takeaway:** CORELS can often find sparse transparent rule lists with competitive accuracy, sometimes matching black-box tools on benchmark tasks, while also producing certificates of optimality.
10. **Conclusion and future directions:** The paper highlights scalability limits in highly correlated feature spaces, discusses applicability boundaries (especially outside structured-feature settings), and suggests improved search scheduling and broader interpretable-model integrations as next steps.

## Relevance to the Dissertation
Learning Certifiably Optimal Rule Lists for Categorical Data (Angelino et al., 2018) is directly relevant to the proposal's interpretable-model objective and the final anytime rule-compression stage.

## Elements from This Paper to Use in the Dissertation
1. Use this paper's interpretability framing to justify rule-first design decisions.
2. Borrow complexity metrics (rule count, rule length, transparency) for evaluation.
3. Reuse details around journal, machine, learning to improve model reporting and human-auditable outputs.
4. Benchmark rule quality against the proposal's anytime compression stage.

## Competitive Method Assessment
This paper is a direct competitor for interpretable-model construction. Competing rule methods may outperform the dissertation approach when their search objective matches the data regime (e.g., small categorical spaces), but can fall short under large lag-expanded continuous settings where anytime compression is computationally safer.

## Dissertation Citation Traceability

- Chapter: `Introduction`; Section: `Chapter opening`; Line: `Chapters/01_introduction.tex:22`; Relevance: Cited to support the statement that Rule-structured models are especially relevant because they align with human review workflows and can be validated directly by domain experts.
- Chapter: `Introduction`; Section: `Contributions`; Line: `Chapters/01_introduction.tex:87`; Relevance: Cited to support the statement that An anytime rule-compression stage for interpretable deployment. Sparse coefficient models are converted into compact m-of-K rule forms that can be audited and deployed under explicit performance-tolerance policies.
- Chapter: `Introduction`; Section: `Evaluation Priorities`; Line: `Chapters/01_introduction.tex:135`; Relevance: Cited to support the statement that Interpretability complexity: active-feature count, rule count, and rule length as direct proxies for human audit burden.
- Chapter: `Related Work`; Section: `Interpretable Modeling and Rule-Learning Literature`; Line: `Chapters/03_relatedwork.tex:55`; Relevance: Cited to support the statement that Certifiably optimal rule-list learning shows that exact or bounded-search approaches can produce compact, auditable models with competitive predictive performance on structured tasks.
- Chapter: `Related Work`; Section: `Summary of Gaps in Prior Work`; Line: `Chapters/03_relatedwork.tex:106`; Relevance: Cited to support the statement that Rule-learning frameworks deliver transparency, but direct combinatorial optimization can be difficult to scale in high-dimensional longitudinal spaces.
- Chapter: `Anytime Rule Compression (RQ3)`; Section: `Relationship to Adjacent Interpretable Methods`; Line: `Chapters/07_rq3.tex:119`; Relevance: Cited to support the statement that Rule-list and scoring-system approaches provide strong interpretability baselines, but they often optimize directly in combinatorial rule space with different scalability profiles.
- Chapter: `Future Work`; Section: `Richer Rule Families and Hybrid Models`; Line: `Chapters/88_futurework.tex:17`; Relevance: Cited to support the statement that Such extensions could preserve the current pipeline's transparency while reducing performance loss in settings where post-threshold magnitude still carries predictive information.
- Chapter: `Conclusion`; Section: `Positioning Relative to Prior Work`; Line: `Chapters/89_conclusion.tex:56`; Relevance: Cited to support the statement that Relative to direct interpretable additive, rule-ensemble, and rule-list approaches, it uses sparse convex fitting as a scalable front end and performs structured rule simplification afterward.
