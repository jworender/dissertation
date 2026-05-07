# Dissertation Artifact Repository for Interpretable Sparse Modeling of Longitudinal Signals (Orender, 2026)

## Dissertation Alignment Context
The dissertation uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into {-1,+1} indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Artifact
1. **Artifact identity:** The GitHub repository is the public dissertation artifact repository for the manuscript, figures, notebooks, cached results, regeneration scripts, reference materials, and reproducibility documentation.
2. **Manuscript layer:** The repository contains `main.tex`, `main.pdf`, the `Chapters/` LaTeX sources, `Figures/`, `ref.bib`, the local `odusci.sty`, and generated build artifacts used for local manuscript audit.
3. **Study layer:** The `notebooks/` directory contains executable study notebooks, while `scripts/` contains notebook generators and supporting experiment scripts.
4. **Cached-output layer:** The `notebooks/runs_new/` directories preserve CSV, JSON, and text outputs so reported tables and figures can be audited without rerunning every long experiment.
5. **Reproducibility map:** The README and appendix map study packages to their notebooks, generator scripts, cached outputs, manuscript figures, tables, and consuming chapters.
6. **Environment capture:** The repository includes `environment.yml`, `requirements.txt`, and a smoke-check script to verify core imports, notebook kernel registration, representative cached outputs, and optional real-data readiness.
7. **Real-data setup:** The README documents external data requirements for HAI and UCI ionosphere inputs and the preprocessing path for deterministic HAI parquet artifacts.
8. **Workflow exemplar:** The repository includes a HAI `attack_p2 (a1)` walkthrough notebook that runs the raw baseline, rectified pilot, branch selection, compression frontier, and held-out deployment recommendation.
9. **Rule-card governance:** The repository and appendix provide a rule-card template for accepted compressed rules, recording selected conditions, vote threshold, metrics, validation deltas, risks, monitoring triggers, and artifact links.
10. **Dissertation role:** The repository is the manuscript-specific audit layer that complements the `cutlass` PyPI package: package for reusable modeling code, repository for study regeneration and evidence traceability.

## Relevance to the Dissertation
The dissertation artifact repository is directly relevant to the reproducibility and auditability claims in the manuscript. It preserves the empirical study layer behind the dissertation's figures, tables, and RQ chapters, while the separate `cutlass` package exposes the reusable modeling core.

## Source and Artifact Notes

- Public GitHub repository listed in `ref.bib`: <https://github.com/jworender/dissertation>
- Local repository title from README: `Dissertation Repository: Critical-Range Rectification and Anytime Rule Compression`
- Principal local entry points: `main.tex`, `main.pdf`, `Chapters/`, `Figures/`, `notebooks/`, `scripts/`, `notebooks/runs_new/`, `references/`, `documentation/`, `environment.yml`, `requirements.txt`, and `README.md`.
- Representative study stems documented in the README: `stability_ablation`, `cross_domain`, `goose_bay_robustness`, `interpretable_baselines`, `walkthrough`, `boundary_conditions`, and `compression_validation`.
- The repository is the authoritative local artifact for manuscript-to-output traceability; the PyPI package is the reusable implementation artifact.

## Elements from This Artifact to Use in the Dissertation
1. Cite it when describing where notebooks, generators, cached outputs, and manuscript figures are preserved.
2. Use it to substantiate artifact-backed reproducibility claims in the introduction and appendices.
3. Use the repository map and study-regeneration map to connect manuscript claims to executable or cached evidence.
4. Use the rule-card template and smoke-check documentation to support the dissertation's deployment-governance and external-reader utility story.

## Competitive Method Assessment
This is not a competing method. It is the evidence repository for the dissertation. Its main value is traceability from manuscript claims to scripts, notebooks, cached outputs, figures, environment capture, and operational rule-card documentation.

## Dissertation Citation Traceability

- Chapter: `Introduction`; Section: `Approach`; Line: `Chapters/01_introduction.tex:79`; Relevance: Cited to support the statement that The reusable modeling core is exposed through the public cutlass package, while the dissertation repository preserves the study layer: notebooks, paired scripts/_generate_*.py generators, cached run summaries under notebooks/runs_new/, and manuscript-ready figures under Figures/.
