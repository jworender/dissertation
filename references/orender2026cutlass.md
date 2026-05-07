# cutlass: Rectified L1 Logistic Regression with Critical-Range Encoding (Orender, 2026)

## Dissertation Alignment Context
The dissertation uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into {-1,+1} indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Artifact
1. **Artifact identity:** `cutlass` is the reusable Python package that exposes the dissertation's modeling core outside the manuscript repository.
2. **Package purpose:** The package implements critical-range rectified L1 logistic regression for interpretable sparse modeling with optional logic-style compression.
3. **Current public package state:** The PyPI page currently lists `cutlass` version `0.4.0`, released April 2, 2026, with the description "Rectified L1 logistic regression with CUTLASS critical range encoding."
4. **Core estimator design:** The project description presents a scikit-learn-inspired estimator that rectifies input features into {-1,+1} indicators, fits an L1-penalized logistic model, and can compress the fitted model into a logical rule.
5. **Rectification component:** `cutlass.Rectifier` infers critical ranges from positive-class observations and binarizes features into event-aligned indicators.
6. **Sparse-learning component:** `cutlass.CutlassLogisticCV` provides the lower-level cross-validated L1 logistic path solver, including warm-started coordinate descent and an optional FISTA solver.
7. **Workflow component:** `cutlass.CutlassClassifier` composes rectification, optional scaling, sparse logistic fitting, and logic polishing into the high-level interface used by migrated experiment drivers.
8. **Logic-polishing component:** The package includes a top-k voting compression step with fixed magnitude `K` and multiple intercept policies, mirroring the dissertation's research code.
9. **Packaging and dependencies:** PyPI lists MIT licensing, Python >=3.9 support, NumPy and pandas as core lightweight dependencies, and an optional `plots` extra for plotting diagnostics.
10. **Reproducibility role:** The package separates reusable modeling machinery from the dissertation repository's study layer, so the manuscript can cite a stable public implementation while preserving notebooks and cached outputs separately.

## Relevance to the Dissertation
The `cutlass` package is directly relevant as the public implementation of the dissertation's reusable modeling core. It supports the artifact-backed claim that the pipeline is not only manuscript prose: rectification, sparse logistic fitting, serialization, and optional logic polishing are packaged for reuse.

## Source and Artifact Notes

- Public PyPI page: <https://pypi.org/project/cutlass/>
- Install command: `pip install cutlass`
- Optional plotting extra: `pip install cutlass[plots]`
- Current PyPI version observed during this summary: `0.4.0` (released April 2, 2026)
- Local bibliography note: `ref.bib` currently describes the package as version `0.1.0`; the PyPI page now lists newer releases through `0.4.0`.
- PyPI metadata: author Jason Orender; MIT License; Python >=3.9; tags include logistic regression, lasso, interpretability, and machine learning.
- Principal APIs named on PyPI: `cutlass.Rectifier`, `cutlass.CutlassLogisticCV`, `cutlass.CutlassClassifier`, and `cutlass.serialization`.

## Elements from This Artifact to Use in the Dissertation
1. Cite it when describing the reusable modeling core that implements the dissertation pipeline.
2. Use it to distinguish reusable package logic from dissertation-specific notebooks and cached experiments.
3. Use the API structure to support claims of modularity: rectifier, sparse estimator, classifier workflow, and serialization.
4. Use the public package metadata as part of the reproducibility and external-utility argument.

## Competitive Method Assessment
This is not a competing method; it is the dissertation's packaged implementation artifact. Its value is practical reuse and reproducibility. It does not replace the dissertation repository because it does not preserve every study notebook, cached output, figure, or manuscript-specific audit trail.

## Dissertation Citation Traceability

- Chapter: `Introduction`; Section: `Approach`; Line: `Chapters/01_introduction.tex:79`; Relevance: Cited to support the statement that The reusable modeling core is exposed through the public cutlass package, while the dissertation repository preserves the study layer: notebooks, paired scripts/_generate_*.py generators, cached run summaries under notebooks/runs_new/, and manuscript-ready figures under Figures/.
