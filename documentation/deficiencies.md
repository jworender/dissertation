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

- Status: Addressed on 2026-04-19.
- Added notebooks:
  - `notebooks/cross_domain.ipynb`
  - `notebooks/goose_bay_robustness.ipynb`
- Added notebook regeneration helpers:
  - `scripts/_generate_cross_domain_notebook.py`
  - `scripts/_generate_goose_bay_robustness_notebook.py`
- Added cached result files:
  - `notebooks/runs_new/cross_domain/synthetic_baseline_summary.csv`
  - `notebooks/runs_new/cross_domain/synthetic_baseline_summary_formatted.csv`
  - `notebooks/runs_new/cross_domain/cross_domain_transfer_summary.csv`
  - `notebooks/runs_new/cross_domain/cross_domain_transfer_summary_formatted.csv`
  - `notebooks/runs_new/cross_domain/ionosphere_protocol_comparison.csv`
  - `notebooks/runs_new/cross_domain/ionosphere_protocol_comparison_formatted.csv`
  - `notebooks/runs_new/cross_domain/cross_domain_takeaways.txt`
  - `notebooks/runs_new/goose_bay_robustness/goose_bay_protocol_summary.csv`
  - `notebooks/runs_new/goose_bay_robustness/goose_bay_protocol_summary_formatted.csv`
  - `notebooks/runs_new/goose_bay_robustness/goose_bay_quantile_sweep_summary.csv`
  - `notebooks/runs_new/goose_bay_robustness/goose_bay_quantile_sweep_summary_formatted.csv`
  - `notebooks/runs_new/goose_bay_robustness/goose_bay_c_sweep_summary.csv`
  - `notebooks/runs_new/goose_bay_robustness/goose_bay_c_sweep_cv_summary.csv`
  - `notebooks/runs_new/goose_bay_robustness/goose_bay_seed2345_decomposition.csv`
  - `notebooks/runs_new/goose_bay_robustness/goose_bay_seed2345_decomposition_formatted.csv`
  - `notebooks/runs_new/goose_bay_robustness/goose_bay_takeaways.txt`
- Moved notebook-generated figures into the manuscript `Figures/` directory:
  - `Figures/cross_domain_transfer_deltas.png`
  - `Figures/cross_domain_ionosphere_protocol_comparison.png`
  - `Figures/goose_bay_delta_j_protocols.png`
  - `Figures/goose_bay_quantile_sweep.png`
  - `Figures/goose_bay_c_sweep_scatter.png`
- Updated manuscript discussion in `Chapters/05_rq1.tex`:
  - replaced both `<<< deficiency D002 >>>` placeholders,
  - added Table `tab:d002_baselines` covering elastic net, adaptive lasso, group lasso, ordered-prefix, and QP-based comparators,
  - added Figures `fig:d002_transfer_deltas`, `fig:d002_ionosphere_protocols`, `fig:d002_goose_bay_protocols`, `fig:d002_goose_bay_quantiles`, and `fig:d002_goose_bay_c_sweep`,
  - added narrative on mixed cross-domain transferability under a standardized protocol,
  - added a protocol audit explaining why the Goose Bay generic probe differs from the published 2022 result,
  - added sensitivity discussion for split choice, rectifier quantiles, and penalty strength `C`, including the implication that the default `C=0.1` and default `25/75` cutlass quantiles understate Goose Bay performance.
- Main dissertation LaTeX edits taken:
  - `main.tex` required no direct change because `Chapters/05_rq1.tex` was already included in the build.
  - `Chapters/05_rq1.tex` now contains the full D002 backfill used by the main dissertation document.
- Net effect on the dissertation: D002 is now backed by a concrete expanded-baseline package, a broader cross-domain transfer panel, and an explicit explanation of why the Goose Bay ionosphere result changes under different protocol settings.

## D003 - RQ2 empirical boundary-condition package

- Status: Corrected on 2026-04-20. The boundary-condition notebook package was integrated into the main dissertation text, and the Chapter 06 D003 placeholders were replaced with a full empirical boundary-condition subsection.
- Added notebook: `notebooks/boundary_conditions.ipynb`
- Added notebook regeneration helper: `scripts/_generate_boundary_conditions_notebook.py`
- Added cached result files:
  - `notebooks/runs_new/boundary_conditions/ic_boundary_runs.csv`
  - `notebooks/runs_new/boundary_conditions/ic_boundary_summary.csv`
  - `notebooks/runs_new/boundary_conditions/ic_stress_runs.csv`
  - `notebooks/runs_new/boundary_conditions/ic_stress_summary.csv`
  - `notebooks/runs_new/boundary_conditions/ic_stress_crossing_summary.csv`
  - `notebooks/runs_new/boundary_conditions/inactive_count_runs.csv`
  - `notebooks/runs_new/boundary_conditions/inactive_count_summary.csv`
  - `notebooks/runs_new/boundary_conditions/threshold_bridge_sweep.csv`
  - `notebooks/runs_new/boundary_conditions/interval_bridge_summary.csv`
  - `notebooks/runs_new/boundary_conditions/negative_complement_summary.csv`
  - `notebooks/runs_new/boundary_conditions/boundary_conditions_summary.csv`
  - `notebooks/runs_new/boundary_conditions/boundary_takeaways.txt`
- Notebook-generated figures currently retained under `notebooks/Figures/`:
  - `notebooks/Figures/boundary_ic_stress_profiles.png`
- Boundary figures moved into the dissertation-wide `Figures/` directory for manuscript inclusion:
  - `Figures/boundary_ic_sweep.png`
  - `Figures/boundary_ic_stress_heatmaps.png`
  - `Figures/boundary_inactive_count_sweep.png`
  - `Figures/boundary_threshold_bridge.png`
- Notebook scope delivered:
  - positive and negative correlation sweeps using an empirical IC proxy,
  - a harder cross-scale stress sweep showing where raw and rectified `\Theta` cross the IC boundary,
  - a fixed-`s=4` inactive-count sweep showing how a larger off-support pool worsens the max-based IC proxy,
  - a threshold bridge from exact zero-threshold sign binarization to shifted one-sided and interval critical ranges,
  - a negative-correlation complement-feature check,
  - a final strong/weak/fail summary table suitable for Chapter 06 backfill.
- Main dissertation LaTeX edits taken:
  - `Chapters/06_rq2.tex` now includes the full D003 backfill: synthetic dataset construction, IC proxy definition, baseline IC sweep interpretation, harder cross-scale boundary maps, fixed-`s=4` inactive-count scaling, threshold-bridge analysis, complement-feature repair, and a manuscript summary table.
  - `Chapters/89_conclusion.tex` now summarizes the strong/weak/fail boundary interpretation in the RQ2 conclusion.
- Net effect on the dissertation: D003 is now backed by a concrete empirical boundary-condition package inside the main document, with figures and a summary table that identify where the theorem is strongest, where it weakens, and where complement features or out-of-scope language are required.

## D004 - RQ3 real-data compression validation package

- Status: Corrected on 2026-04-20. The real-data compression validation package was integrated into the main dissertation text, and the Chapter 07 D004 placeholders were replaced with a full real-data policy, frontier, and non-inferiority summary.
- Added notebook: `notebooks/compression_validation.ipynb`
- Added notebook regeneration helper: `scripts/_generate_compression_validation_notebook.py`
- Added cached result files:
  - `notebooks/runs_new/compression_validation/real_data_frontiers.csv`
  - `notebooks/runs_new/compression_validation/compression_policy_summary.csv`
  - `notebooks/runs_new/compression_validation/strict_policy_noninferiority_summary.csv`
  - `notebooks/runs_new/compression_validation/compression_validation_takeaways.txt`
  - `notebooks/runs_new/compression_validation/compression_validation_metadata.json`
- Compression figure moved into the dissertation-wide `Figures/` directory for manuscript inclusion:
  - `Figures/rq3_real_data_frontiers.png`
- Main dissertation LaTeX edits taken:
  - `Chapters/07_rq3.tex` now includes the prespecified strict deployment policy, Figure `fig:rq3_real_frontiers`, Table `tab:rq3_strict_policy`, a policy-sweep interpretation over `\epsilon \in \{0.01, 0.02, 0.05\}`, and a revised RQ3 answer tied to the held-out validation results.
  - `Chapters/89_conclusion.tex` now summarizes the strict real-data RQ3 outcome in the dissertation conclusion.
- Figure-location note:
  - No additional D004 manuscript figure remained under `notebooks/Figures/`; the notebook already generated the retained RQ3 frontier plot directly into `Figures/`.
- Net effect on the dissertation: D004 is now backed by a concrete real-data anytime-frontier package, an explicit non-inferiority table, and a deployment-policy summary inside the main document rather than a placeholder reference.
