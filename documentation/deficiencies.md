# Dissertation Deficiencies

This file tracks places where prospectus-era language was rewritten into dissertation-final language, but the supporting material is not yet present in the manuscript. Each identifier corresponds to a placeholder of the form `<<< deficiency D00X >>>` in the LaTeX sources. When a deficiency is addressed, this file also records what was added so the manuscript and supporting artifacts stay synchronized.

## D001 - RQ1 stability and ablation package

- Status: Addressed on 2026-04-19.
- Added notebook: `notebooks/stability_ablation.ipynb`
- Added notebook regeneration helper: `scripts/_generate_stability_ablation_notebook.py`
- Added cached result files:
  - `notebooks/runs_new/stability_ablation/stability_ablation_runs.csv`
  - `notebooks/runs_new/stability_ablation/stability_ablation_summary_numeric.csv`
  - `notebooks/runs_new/stability_ablation/stability_ablation_summary_formatted.csv`
  - `notebooks/runs_new/stability_ablation/stability_ablation_deltas.csv`
  - `notebooks/runs_new/stability_ablation/stability_pairwise_jaccard.csv`
  - `notebooks/runs_new/stability_ablation/stability_pairwise_summary.csv`
  - `notebooks/runs_new/stability_ablation/lag_scaling_runs.csv`
  - `notebooks/runs_new/stability_ablation/selection_frequency_raw.csv`
  - `notebooks/runs_new/stability_ablation/selection_frequency_rectified.csv`
  - `notebooks/runs_new/stability_ablation/selection_frequency_rule.csv`
- Added generated figures to the manuscript `Figures/` directory:
  - `Figures/stability_ablation_summary.png`
  - `Figures/stability_pairwise_jaccard.png`
  - `Figures/stability_selection_frequency.png`
  - `Figures/lag_runtime_scaling.png`
- Updated manuscript discussion in `Chapters/05_rq1.tex`:
  - replaced both `<<< deficiency D001 >>>` placeholders,
  - added a repeated-resample stability and stage-wise ablation subsection,
  - added Table `tab:d001_stability`,
  - added Figures `fig:d001_ablation`, `fig:d001_pairwise_jaccard`, `fig:d001_selection_frequency`, and `fig:d001_runtime_scaling`,
  - added narrative interpreting the ablation deltas, support-stability results, lag-fidelity gains, and runtime-scaling behavior.
- Net effect on the dissertation: D001 is now backed by a concrete synthetic resampling package rather than a placeholder reference.

## D002 - RQ1 expanded baseline and cross-domain comparison package

- Needed: consolidated comparisons against additional correlated-feature baselines and at least one broader cross-domain validation summary beyond the currently shown core case studies.
- Affected files: `main.tex`, `Chapters/05_rq1.tex`
- Suggested backfill: one benchmark table covering elastic net/adaptive/group/ordered/QP comparators plus a concise transferability discussion.

## D003 - RQ2 empirical boundary-condition package

- Needed: empirical stress tests or summarized results for correlation sweeps, threshold perturbations, negative-correlation cases, and/or a bridge from the zero-threshold theorem to practical critical-range settings.
- Affected files: `Chapters/06_rq2.tex`
- Suggested backfill: one subsection with a figure or table showing where the theorem's mechanism holds strongly, weakly, or fails.

## D004 - RQ3 real-data compression validation package

- Needed: full real-data `J`-versus-`k` curves, equivalence or non-inferiority comparisons, and a prespecified adoption-policy summary for compressed rule models.
- Affected files: `Chapters/07_rq3.tex`
- Suggested backfill: one real-data anytime frontier figure, one equivalence table, and a short paragraph defining the deployment policy used to accept a compressed rule.
